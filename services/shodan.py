"""
Shodan Service Module

This module handles all interactions with the Shodan API, including
query execution and result formatting.

Author: Shovon Paul
Date: 2024-11-17
"""

import shodan
from typing import Dict, Any, List
from fastapi import HTTPException
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Shodan client
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
if not SHODAN_API_KEY:
    raise ValueError("SHODAN_API_KEY not found in environment variables")

api = shodan.Shodan(SHODAN_API_KEY)

async def execute_shodan_query(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Execute a Shodan query and return formatted results.

    Args:
        query (str): The Shodan query to execute
        limit (int): Number of results to return (default: 5)

    Returns:
        List[Dict[str, Any]]: List of formatted Shodan results

    Raises:
        HTTPException: If there's an error executing the query
    """
    try:
        # Execute Shodan search with user-specified limit
        results = api.search(query, limit=limit)
        
        # Format the results
        formatted_results = []
        for result in results['matches']:
            formatted_result = {
                'ip': result.get('ip_str', 'N/A'),
                'port': result.get('port', 'N/A'),
                'organization': result.get('org', 'N/A'),
                'location': f"{result.get('location', {}).get('country_name', 'N/A')}, "
                          f"{result.get('location', {}).get('city', 'N/A')}",
                'timestamp': result.get('timestamp', 'N/A'),
                'product': result.get('product', 'N/A'),
                'version': result.get('version', 'N/A'),
                'vulns': result.get('vulns', [])
            }
            formatted_results.append(formatted_result)
            
        return formatted_results

    except shodan.APIError as e:
        print(f"Shodan API Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Shodan API Error: {str(e)}"
        )
    except Exception as e:
        print(f"Error executing Shodan query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error executing Shodan query: {str(e)}"
        ) 