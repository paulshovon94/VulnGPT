"""
ChatGPT Service Module

This module handles all interactions with the OpenAI GPT API for generating
Shodan queries and explanations. It includes input validation, error handling,
and response formatting.

Author: Shovon Paul
Date: 2024-11-17
"""

from openai import AsyncOpenAI
from typing import Dict, Any
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize AsyncOpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not client.api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Define system prompt for consistent GPT responses
SYSTEM_PROMPT = """You are a Shodan search expert. Your role is to:
1. Convert user questions into effective Shodan search queries
2. Explain what the query does
3. Provide security considerations and warnings when relevant
4. Format your response as JSON with fields: 'shodan_query' and 'explanation'

Example response format:
{
    "shodan_query": "product:nginx country:US",
    "explanation": "This query searches for Nginx web servers located in the United States..."
}"""

async def get_shodan_query(user_question: str) -> Dict[str, Any]:
    """
    Generate a Shodan query based on the user's natural language question.

    Args:
        user_question (str): The user's natural language question about what to search for

    Returns:
        Dict[str, Any]: A dictionary containing the Shodan query and its explanation

    Raises:
        HTTPException: If there's an error in generating the query or communicating with OpenAI
    """
    try:
        # Validate input
        if not user_question.strip():
            raise ValueError("Empty question provided")

        # Create chat completion request using new API syntax
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,  # Balance between creativity and consistency
            max_tokens=500    # Limit response length
        )
        
        # Extract and validate response content
        content = response.choices[0].message.content
        
        # Handle non-JSON responses gracefully
        try:
            if isinstance(content, str):
                content = json.loads(content)
            return content
        except json.JSONDecodeError:
            return {
                "shodan_query": "Error: Could not generate query",
                "explanation": "The response format was invalid. Please try rephrasing your question."
            }

    except Exception as e:
        # Log the error (in a production environment, use proper logging)
        print(f"Error in get_shodan_query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating Shodan query: {str(e)}"
        ) 