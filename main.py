"""
VulnGPT Main Application

This is the main FastAPI application that serves as the backend for VulnGPT.
It handles routing, request processing, and integrates various services.

Author: Shovon Paul
Date: 2024-11-17
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from services.chatgpt import get_shodan_query
from services.shodan import execute_shodan_query
import json
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="VulnGPT",
    description="Vulnerability Guided Protection Toolkit",
    version="1.0.0"
)

# Configure static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class QueryRequest(BaseModel):
    """
    Pydantic model for query requests.
    """
    query: str

    class Config:
        schema_extra = {
            "example": {
                "query": "Find vulnerable Apache servers in Germany"
            }
        }

@app.get("/")
async def root(request: Request):
    """
    Serve the main application interface.

    Args:
        request (Request): The incoming HTTP request

    Returns:
        TemplateResponse: The rendered HTML template
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query")
async def process_query(request: QueryRequest):
    """
    Process user queries and return both ChatGPT guidance and Shodan results.
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Get ChatGPT response
        chatgpt_response = await get_shodan_query(request.query)
        
        # Execute Shodan query
        shodan_results = await execute_shodan_query(chatgpt_response['shodan_query'])
        
        # Format the complete response
        formatted_response = (
            f"🔍 Suggested Shodan Query:\n"
            f"{chatgpt_response['shodan_query']}\n\n"
            f"📝 Explanation:\n"
            f"{chatgpt_response['explanation']}\n\n"
            f"🌐 Shodan Results:\n"
        )

        # Add Shodan results
        for idx, result in enumerate(shodan_results, 1):
            formatted_response += (
                f"\nResult {idx}:\n"
                f"IP: {result['ip']}\n"
                f"Port: {result['port']}\n"
                f"Organization: {result['organization']}\n"
                f"Location: {result['location']}\n"
                f"Product: {result['product']} {result['version']}\n"
            )
            if result['vulns']:
                formatted_response += f"Vulnerabilities: {', '.join(result['vulns'])}\n"
        
        return JSONResponse({
            "guidance": formatted_response
        })

    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

# Your existing routes go here... 