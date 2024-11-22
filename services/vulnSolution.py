"""
VulnSolution Service Module

This module handles the analysis of Shodan results and generates
step-by-step solutions for identified vulnerabilities using ChatGPT.

Author: Shovon Paul
Date: 2024-11-17
"""

from openai import AsyncOpenAI
from typing import Dict, List, Any
from fastapi import HTTPException
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize AsyncOpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

client = AsyncOpenAI(api_key=api_key)

SOLUTION_SYSTEM_PROMPT = """You are a cybersecurity expert. Analyze the provided system details 
and provide a detailed, step-by-step solution to address the identified vulnerabilities and security issues.
Focus on:
1. Critical security fixes
2. Configuration improvements
3. Best practices
4. Preventive measures

Keep your response concise but actionable, with clear steps."""

async def get_security_solution_for_result(result: Dict[str, Any]) -> str:
    """
    Generate security solution for a single Shodan result.

    Args:
        result (Dict[str, Any]): Single Shodan result

    Returns:
        str: Detailed security solution for the specific result
    """
    try:
        # Format the single result for analysis
        analysis_prompt = (
            f"Analyze this system and provide specific solutions:\n"
            f"Product: {result['product']} {result['version']}\n"
            f"Port: {result['port']}\n"
        )
        if result['vulns']:
            analysis_prompt += f"Vulnerabilities: {', '.join(result['vulns'])}\n"

        # Get solution from ChatGPT
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": SOLUTION_SYSTEM_PROMPT},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating solution for result: {str(e)}")
        return "Unable to generate solution for this result."

async def get_security_solutions(shodan_results: List[Dict[str, Any]]) -> List[str]:
    """
    Generate security solutions for each Shodan result.

    Args:
        shodan_results (List[Dict[str, Any]]): List of formatted Shodan results

    Returns:
        List[str]: List of security solutions corresponding to each result

    Raises:
        HTTPException: If there's an error generating solutions
    """
    try:
        solutions = []
        for result in shodan_results:
            solution = await get_security_solution_for_result(result)
            solutions.append(solution)
            
        return solutions

    except Exception as e:
        print(f"Error generating security solutions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating security solutions: {str(e)}"
        ) 