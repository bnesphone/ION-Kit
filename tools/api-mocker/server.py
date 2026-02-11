#!/usr/bin/env python3
"""
API Mocker for AI Agent Toolkit
Dynamically serves a REST API based on a JSON schema.
"""
import sys
import json
import argparse
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import create_model
from typing import List, Dict, Any

app = FastAPI(title="AI Toolkit Mock API")
db = {} # In-memory DB

def create_endpoints(resource_name: str, fields: Dict[str, Any]):
    """Dynamically add CRUD endpoints for a resource"""
    # Simple model creation (for doc purpose mostly)
    # In a real tool we'd map types properly
    
    path = f"/{resource_name}"
    
    @app.get(path, tags=[resource_name])
    async def list_items():
        return db.get(resource_name, [])

    @app.post(path, tags=[resource_name])
    async def create_item(item: Dict[str, Any]):
        if resource_name not in db:
            db[resource_name] = []
        item['id'] = len(db[resource_name]) + 1
        db[resource_name].append(item)
        return item
        
    @app.delete(f"{path}/{{item_id}}", tags=[resource_name])
    async def delete_item(item_id: int):
        items = db.get(resource_name, [])
        for i, item in enumerate(items):
            if item.get('id') == item_id:
                return items.pop(i)
        raise HTTPException(status_code=404, detail="Item not found")

def load_schema(schema_path):
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        for resource, definition in schema.items():
            db[resource] = [] # Init DB
            create_endpoints(resource, definition)
            print(f"✅ Route created: /{resource}")
            
    except Exception as e:
        print(f"❌ Error loading schema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Mock API Server")
    parser.add_argument("schema", help="Path to schema.json")
    parser.add_argument("--port", type=int, default=8000)
    
    args = parser.parse_args()
    
    load_schema(args.schema)
    uvicorn.run(app, host="0.0.0.0", port=args.port)
