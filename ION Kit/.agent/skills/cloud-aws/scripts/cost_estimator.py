#!/usr/bin/env python3
"""
AWS Cost Estimator
Estimates monthly AWS infrastructure costs

Usage: python cost_estimator.py [--config config.json]
"""
import json
import sys
import argparse

# AWS Pricing (us-east-1, on-demand, as of 2025)
PRICING = {
    "compute": {
        # EC2 instances (per hour)
        "t3.micro": 0.0104,
        "t3.small": 0.0208,
        "t3.medium": 0.0416,
        "t3.large": 0.0832,
        "t3.xlarge": 0.1664,
        "m5.large": 0.096,
        "m5.xlarge": 0.192,
        "c5.large": 0.085,
        "c5.xlarge": 0.17,
        # Lambda (per 1M requests + GB-second)
        "lambda_requests": 0.20,  # per 1M requests
        "lambda_duration": 0.0000166667,  # per GB-second
        # Fargate (per vCPU-hour + GB-hour)
        "fargate_vcpu": 0.04048,
        "fargate_memory": 0.004445,
    },
    "storage": {
        # EBS (per GB-month)
        "ebs_gp3": 0.08,
        "ebs_gp2": 0.10,
        "ebs_io1": 0.125,
        # S3 (per GB-month)
        "s3_standard": 0.023,
        "s3_ia": 0.0125,
        "s3_glacier": 0.004,
        # EFS (per GB-month)
        "efs_standard": 0.30,
        "efs_ia": 0.025,
    },
    "database": {
        # RDS (per hour)
        "rds_t3.micro": 0.017,
        "rds_t3.small": 0.034,
        "rds_t3.medium": 0.068,
        "rds_m5.large": 0.192,
        # DynamoDB (per million requests)
        "dynamodb_write": 1.25,
        "dynamodb_read": 0.25,
        # Aurora Serverless (per ACU-hour)
        "aurora_acu": 0.06,
    },
    "network": {
        # Data transfer (per GB)
        "data_out": 0.09,
        "cloudfront": 0.085,
    }
}

HOURS_PER_MONTH = 730

def estimate_ec2(instances):
    """Estimate EC2 costs"""
    total = 0
    breakdown = []
    
    for instance in instances:
        instance_type = instance.get("type", "t3.micro")
        count = instance.get("count", 1)
        hours = instance.get("hours", HOURS_PER_MONTH)
        
        hourly_cost = PRICING["compute"].get(instance_type, 0)
        monthly_cost = hourly_cost * hours * count
        
        total += monthly_cost
        breakdown.append({
            "service": "EC2",
            "details": f"{count}x {instance_type} ({hours}h)",
            "cost": monthly_cost
        })
    
    return total, breakdown

def estimate_lambda(config):
    """Estimate Lambda costs"""
    total = 0
    breakdown = []
    
    requests = config.get("requests", 0) / 1_000_000  # Convert to millions
    memory_gb = config.get("memory_mb", 128) / 1024
    duration_sec = config.get("duration_ms", 100) / 1000
    
    # Free tier: 1M requests + 400,000 GB-seconds/month
    request_cost = max(0, requests - 1) * PRICING["compute"]["lambda_requests"]
    
    gb_seconds = requests * 1_000_000 * memory_gb * duration_sec
    duration_cost = max(0, gb_seconds - 400_000) * PRICING["compute"]["lambda_duration"]
    
    total = request_cost + duration_cost
    
    if total > 0:
        breakdown.append({
            "service": "Lambda",
            "details": f"{int(requests * 1_000_000):,} requests, {memory_gb}GB, {duration_sec}s",
            "cost": total
        })
    
    return total, breakdown

def estimate_storage(storage):
    """Estimate storage costs"""
    total = 0
    breakdown = []
    
    for item in storage:
        storage_type = item.get("type", "s3_standard")
        size_gb = item.get("size_gb", 0)
        
        price_per_gb = PRICING["storage"].get(storage_type, 0)
        cost = size_gb * price_per_gb
        
        total += cost
        breakdown.append({
            "service": "Storage",
            "details": f"{size_gb}GB {storage_type}",
            "cost": cost
        })
    
    return total, breakdown

def estimate_database(databases):
    """Estimate database costs"""
    total = 0
    breakdown = []
    
    for db in databases:
        db_type = db.get("type", "rds")
        
        if db_type == "rds":
            instance_type = db.get("instance_type", "rds_t3.micro")
            multi_az = db.get("multi_az", False)
            
            hourly_cost = PRICING["database"].get(instance_type, 0)
            monthly_cost = hourly_cost * HOURS_PER_MONTH
            
            if multi_az:
                monthly_cost *= 2
            
            total += monthly_cost
            breakdown.append({
                "service": "RDS",
                "details": f"{instance_type} {'Multi-AZ' if multi_az else 'Single-AZ'}",
                "cost": monthly_cost
            })
        
        elif db_type == "dynamodb":
            writes = db.get("writes_millions", 0)
            reads = db.get("reads_millions", 0)
            
            # Free tier: 25 WCU, 25 RCU
            write_cost = max(0, writes - 25) * PRICING["database"]["dynamodb_write"]
            read_cost = max(0, reads - 25) * PRICING["database"]["dynamodb_read"]
            
            cost = write_cost + read_cost
            total += cost
            
            if cost > 0:
                breakdown.append({
                    "service": "DynamoDB",
                    "details": f"{writes}M writes, {reads}M reads",
                    "cost": cost
                })
    
    return total, breakdown

def estimate_network(config):
    """Estimate network costs"""
    total = 0
    breakdown = []
    
    data_out_gb = config.get("data_out_gb", 0)
    cloudfront_gb = config.get("cloudfront_gb", 0)
    
    # Free tier: 100 GB data out
    if data_out_gb > 100:
        cost = (data_out_gb - 100) * PRICING["network"]["data_out"]
        total += cost
        breakdown.append({
            "service": "Data Transfer",
            "details": f"{data_out_gb}GB out",
            "cost": cost
        })
    
    # CloudFront free tier: 1 TB
    if cloudfront_gb > 1024:
        cost = (cloudfront_gb - 1024) * PRICING["network"]["cloudfront"]
        total += cost
        breakdown.append({
            "service": "CloudFront",
            "details": f"{cloudfront_gb}GB",
            "cost": cost
        })
    
    return total, breakdown

def main():
    parser = argparse.ArgumentParser(description='Estimate AWS costs')
    parser.add_argument('--config', help='Path to config JSON file')
    args = parser.parse_args()
    
    # Default config if none provided
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    else:
        # Example configuration
        config = {
            "ec2": [
                {"type": "t3.small", "count": 2, "hours": 730}
            ],
            "lambda": {
                "requests": 5_000_000,
                "memory_mb": 512,
                "duration_ms": 200
            },
            "storage": [
                {"type": "ebs_gp3", "size_gb": 100},
                {"type": "s3_standard", "size_gb": 500}
            ],
            "database": [
                {"type": "rds", "instance_type": "rds_t3.small", "multi_az": True}
            ],
            "network": {
                "data_out_gb": 1000,
                "cloudfront_gb": 2000
            }
        }
    
    print("\n" + "="*60)
    print("AWS MONTHLY COST ESTIMATE")
    print("="*60 + "\n")
    
    grand_total = 0
    all_breakdown = []
    
    # Compute
    if "ec2" in config:
        total, breakdown = estimate_ec2(config["ec2"])
        grand_total += total
        all_breakdown.extend(breakdown)
    
    if "lambda" in config:
        total, breakdown = estimate_lambda(config["lambda"])
        grand_total += total
        all_breakdown.extend(breakdown)
    
    # Storage
    if "storage" in config:
        total, breakdown = estimate_storage(config["storage"])
        grand_total += total
        all_breakdown.extend(breakdown)
    
    # Database
    if "database" in config:
        total, breakdown = estimate_database(config["database"])
        grand_total += total
        all_breakdown.extend(breakdown)
    
    # Network
    if "network" in config:
        total, breakdown = estimate_network(config["network"])
        grand_total += total
        all_breakdown.extend(breakdown)
    
    # Print breakdown
    for item in all_breakdown:
        print(f"{item['service']:20} {item['details']:40} ${item['cost']:8.2f}")
    
    print("\n" + "="*60)
    print(f"{'TOTAL MONTHLY COST':60} ${grand_total:8.2f}")
    print(f"{'ANNUAL COST':60} ${grand_total * 12:8.2f}")
    print("="*60 + "\n")
    
    # Savings tips
    print("💡 Cost Optimization Tips:")
    if any(i.get("type", "").startswith("t3") for i in config.get("ec2", [])):
        print("  • Consider Reserved Instances for 30-70% savings on EC2")
    if config.get("database", []):
        print("  • Review database instance sizes - can you use smaller instances?")
    if config.get("storage", []):
        print("  • Use S3 lifecycle policies to move to cheaper storage tiers")
    print("  • Enable AWS Cost Explorer for detailed analysis")
    print("  • Set up billing alerts to avoid surprises\n")

if __name__ == "__main__":
    main()
