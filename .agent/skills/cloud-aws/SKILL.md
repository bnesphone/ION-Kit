---
name: cloud-aws
description: AWS cloud architecture, services, best practices, cost optimization. Covers EC2, S3, Lambda, RDS, CloudFormation, and serverless patterns.
allowed-tools: Read, Write, Bash
---

# AWS Cloud Architecture Skill

> Expert knowledge in AWS services, architecture patterns, and best practices

## Service Selection Matrix

| Need | Service | Alternative | When to Use |
|------|---------|-------------|-------------|
| **Compute** | EC2 | Fargate, Lambda | Long-running, full control |
| | Lambda | Fargate, EC2 | Event-driven, short tasks |
| | ECS/Fargate | EKS, EC2 | Containers, AWS-managed |
| | EKS | ECS, EC2 | Kubernetes needed |
| **Storage** | S3 | EFS, EBS | Object storage, static files |
| | EBS | EFS, S3 | Block storage for EC2 |
| | EFS | EBS, S3 | Shared file system |
| **Database** | RDS | Aurora, DynamoDB | Relational, managed |
| | DynamoDB | RDS, DocumentDB | NoSQL, serverless |
| | Aurora | RDS | High performance SQL |
| | ElastiCache | DynamoDB DAX | Caching layer |
| **Networking** | VPC | - | Isolated network |
| | CloudFront | S3, ELB | CDN, edge caching |
| | API Gateway | ALB, CloudFront | REST APIs, serverless |
| | Route 53 | - | DNS management |
| **Messaging** | SQS | SNS, EventBridge | Queue, decoupling |
| | SNS | SQS, EventBridge | Pub/sub, fanout |
| | EventBridge | SNS, SQS | Event routing |
| **Monitoring** | CloudWatch | Datadog, New Relic | Metrics, logs, alarms |

---

## Architecture Patterns

### Pattern 1: Serverless Web App

```
┌──────────────┐
│ Route 53     │ → DNS
└──────┬───────┘
       │
┌──────▼────────┐
│ CloudFront    │ → CDN
└──────┬────────┘
       │
┌──────▼────────┐
│ S3 (Static)   │ → Frontend (React/Vue)
└───────────────┘

┌──────────────┐
│ API Gateway  │ → REST API
└──────┬───────┘
       │
┌──────▼────────┐
│ Lambda        │ → Business Logic
└──────┬───────┘
       │
┌──────▼────────┐
│ DynamoDB      │ → Data Storage
└───────────────┘
```

**Pros:** No servers, auto-scaling, pay-per-use
**Cons:** Cold starts, vendor lock-in
**Cost:** $10-50/month for small apps

### Pattern 2: Traditional 3-Tier

```
┌──────────────┐
│ Route 53     │
└──────┬───────┘
       │
┌──────▼────────┐
│ ALB           │ → Load Balancer
└──────┬───────┘
       │
┌──────▼────────┐
│ EC2 (Web)     │ → Frontend Tier
│ Auto Scaling  │
└──────┬───────┘
       │
┌──────▼────────┐
│ EC2 (App)     │ → Application Tier
│ Auto Scaling  │
└──────┬───────┘
       │
┌──────▼────────┐
│ RDS (Multi-AZ)│ → Database Tier
└───────────────┘
```

**Pros:** Full control, mature tooling
**Cons:** More management, higher cost
**Cost:** $200-500/month minimum

### Pattern 3: Container-based

```
┌──────────────┐
│ Route 53     │
└──────┬───────┘
       │
┌──────▼────────┐
│ ALB           │
└──────┬───────┘
       │
┌──────▼────────┐
│ ECS/Fargate   │ → Containers
│ Auto Scaling  │
└──────┬───────┘
       │
┌──────▼────────┐
│ Aurora        │ → Database
│ Serverless    │
└───────────────┘
```

**Pros:** Containers, less management than EC2
**Cons:** Learning curve, debugging harder
**Cost:** $100-300/month

---

## Cost Optimization

### Compute Costs

| Instance | vCPU | RAM | Price/mo | Use Case |
|----------|------|-----|----------|----------|
| t3.micro | 2 | 1 GB | $7.50 | Dev/test |
| t3.small | 2 | 2 GB | $15 | Small apps |
| t3.medium | 2 | 4 GB | $30 | Medium apps |
| t3.large | 2 | 8 GB | $60 | Larger apps |
| m5.large | 2 | 8 GB | $70 | Production |

**Optimization strategies:**
1. **Right-size instances** - Start small, scale up
2. **Reserved Instances** - Save 30-70% for predictable workloads
3. **Spot Instances** - Save 70-90% for fault-tolerant workloads
4. **Auto Scaling** - Scale down during off-hours
5. **Lambda** - Pay only for execution time

### Storage Costs

| Service | Price/GB/mo | Use Case |
|---------|-------------|----------|
| S3 Standard | $0.023 | Frequent access |
| S3 IA | $0.0125 | Infrequent access |
| S3 Glacier | $0.004 | Archive |
| EBS gp3 | $0.08 | EC2 volumes |

**Optimization:**
- Use S3 lifecycle policies
- Delete old snapshots
- Use Glacier for archives

---

## Security Best Practices

### IAM Principles

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

**Rules:**
- ✅ Principle of least privilege
- ✅ Use IAM roles, not access keys
- ✅ Enable MFA for sensitive operations
- ✅ Rotate credentials regularly
- ❌ Never commit credentials to code
- ❌ Don't use root account

### Network Security

```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)
│   ├── Internet Gateway
│   └── NAT Gateway
└── Private Subnet (10.0.2.0/24)
    ├── Application servers
    └── Database servers
```

**Best practices:**
- Use private subnets for databases
- NAT Gateway for outbound internet
- Security groups: Allow only necessary ports
- Network ACLs: Additional layer
- VPC Flow Logs: Monitor traffic

---

## Infrastructure as Code

### CloudFormation Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Simple web application

Parameters:
  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues: [t3.micro, t3.small, t3.medium]

Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: ami-0c55b159cbfafe1f0  # Amazon Linux 2
      SecurityGroups:
        - !Ref WebServerSecurityGroup

  WebServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Allow HTTP
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

Outputs:
  PublicIP:
    Value: !GetAtt WebServer.PublicIp
    Description: Web server public IP
```

### Terraform Alternative

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "WebServer"
  }
}

resource "aws_security_group" "web" {
  name = "web-sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

## Common Use Cases

### Use Case 1: Static Website

**Stack:**
- S3: Host static files
- CloudFront: CDN
- Route 53: DNS
- ACM: SSL certificate

**Steps:**
1. Create S3 bucket
2. Enable static website hosting
3. Create CloudFront distribution
4. Point domain with Route 53
5. Add SSL with ACM

**Cost:** $1-5/month

### Use Case 2: API Backend

**Stack:**
- API Gateway: REST API
- Lambda: Functions
- DynamoDB: Database
- CloudWatch: Logs

**Code:**
```python
# Lambda function
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def lambda_handler(event, context):
    # Get user
    user_id = event['pathParameters']['id']
    
    response = table.get_item(
        Key={'userId': user_id}
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response.get('Item', {}))
    }
```

**Cost:** $0-20/month

### Use Case 3: Database Migration

**From:** On-premises MySQL
**To:** RDS MySQL

**Steps:**
1. Create RDS instance
2. Setup Database Migration Service (DMS)
3. Create replication instance
4. Create source/target endpoints
5. Create migration task
6. Start replication
7. Switch application connection
8. Monitor and validate

---

## Monitoring & Alerts

### CloudWatch Alarms

```python
# boto3 example
import boto3

cloudwatch = boto3.client('cloudwatch')

# Create alarm for high CPU
cloudwatch.put_metric_alarm(
    AlarmName='HighCPU',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=2,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=80.0,
    ActionsEnabled=True,
    AlarmActions=['arn:aws:sns:us-east-1:123456789012:alerts']
)
```

### Key Metrics to Monitor

| Metric | Threshold | Action |
|--------|-----------|--------|
| CPU Utilization | >80% | Scale up |
| Memory | >90% | Scale up |
| Disk Usage | >85% | Add storage |
| Network | Sustained high | Check for DDoS |
| HTTP 5xx | >1% | Investigate |
| Lambda Duration | Near timeout | Optimize code |

---

## Disaster Recovery

### Backup Strategies

| Strategy | RTO | RPO | Cost | Complexity |
|----------|-----|-----|------|------------|
| Backup & Restore | Hours-Days | Hours | $ | Low |
| Pilot Light | 10min-Hours | Minutes | $$ | Medium |
| Warm Standby | Minutes | Seconds | $$$ | Medium |
| Multi-Site Active | Seconds | None | $$$$ | High |

**RTO:** Recovery Time Objective
**RPO:** Recovery Point Objective

### Multi-Region Setup

```
Primary Region (us-east-1)
├── VPC
├── RDS (Multi-AZ)
└── S3 (Cross-region replication)
    │
    └──> Secondary Region (us-west-2)
         ├── VPC (standby)
         ├── RDS (Read Replica → Promote)
         └── S3 (replicated)
```

---

## Quick Reference

### AWS CLI Commands

```bash
# EC2
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# S3
aws s3 ls
aws s3 cp file.txt s3://bucket/
aws s3 sync ./local s3://bucket/

# Lambda
aws lambda list-functions
aws lambda invoke --function-name myFunction output.json

# RDS
aws rds describe-db-instances
aws rds create-db-snapshot --db-instance-identifier mydb --db-snapshot-identifier snap1

# CloudWatch
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization
```

### Cost Estimation Template

```
Monthly AWS Cost Estimate:

Compute:
- 2x t3.medium EC2 (24/7): $60
- Auto Scaling (avg 1 extra): $30
Subtotal: $90

Storage:
- 100 GB EBS gp3: $8
- 500 GB S3: $11.50
Subtotal: $19.50

Database:
- RDS t3.small (Multi-AZ): $60
Subtotal: $60

Network:
- Data transfer (1 TB): $90
- CloudFront (1 TB): $85
Subtotal: $175

Total: ~$345/month
```

---

## Decision Trees

### Choose Compute Service

```
Need to run code?
├─ Yes
│  ├─ Stateless, event-driven? → Lambda
│  ├─ Need full OS control? → EC2
│  ├─ Containers?
│  │  ├─ Need Kubernetes? → EKS
│  │  └─ Simple containers? → ECS/Fargate
│  └─ Batch processing? → Batch
└─ No → Use managed service
```

### Choose Database

```
Data structure?
├─ Relational (SQL)
│  ├─ Aurora compatible? → Aurora
│  ├─ Need specific engine? → RDS
│  └─ Serverless? → Aurora Serverless
├─ Document/Key-Value → DynamoDB
├─ In-memory cache → ElastiCache
├─ Graph → Neptune
└─ Time-series → Timestream
```

---

**Remember: Cloud architecture is about trade-offs between cost, performance, and complexity!**
