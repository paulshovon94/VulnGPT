"""
VulnGPT Evaluation Module

This module measures and analyzes the response times of VulnGPT components,
including Shodan queries and ChatGPT response generation.

Author: Shovon Paul
Date: 2024-11-17
"""

import asyncio
import time
from typing import List, Dict, Tuple
import statistics
from services.chatgpt import get_shodan_query
from services.shodan import execute_shodan_query
from services.vulnSolution import get_security_solutions
import json
from datetime import datetime
import csv
from pathlib import Path

class TimingResult:
    def __init__(self, total: float, chatgpt: float, shodan: float, solution: float):
        self.total = total
        self.chatgpt = chatgpt
        self.shodan = shodan
        self.solution = solution

async def measure_query_performance(query: str, limit: int = 5) -> TimingResult:
    """
    Measure the performance of a single query execution.
    
    Args:
        query (str): The query to test
        limit (int): Number of results to retrieve
        
    Returns:
        TimingResult: Timing measurements for different components
    """
    start_total = time.time()
    
    # Measure ChatGPT query generation
    start_chatgpt = time.time()
    chatgpt_response = await get_shodan_query(query)
    chatgpt_time = time.time() - start_chatgpt
    
    # Measure Shodan query execution
    start_shodan = time.time()
    shodan_results = await execute_shodan_query(chatgpt_response['shodan_query'], limit)
    shodan_time = time.time() - start_shodan
    
    # Measure solution generation
    start_solution = time.time()
    await get_security_solutions(shodan_results)
    solution_time = time.time() - start_solution
    
    total_time = time.time() - start_total
    
    return TimingResult(total_time, chatgpt_time, shodan_time, solution_time)

async def run_evaluation(test_queries: List[str], iterations: int = 10) -> List[TimingResult]:
    """
    Run performance evaluation on a set of test queries.
    
    Args:
        test_queries (List[str]): List of queries to test
        iterations (int): Number of times to run each query
        
    Returns:
        List[TimingResult]: List of timing results
    """
    results = []
    
    for query in test_queries:
        for _ in range(iterations):
            try:
                result = await measure_query_performance(query)
                results.append(result)
                # Add delay to avoid rate limiting
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error processing query '{query}': {str(e)}")
    
    return results

def analyze_results(results: List[TimingResult]) -> Dict:
    """
    Analyze timing results and generate statistics.
    
    Args:
        results (List[TimingResult]): List of timing measurements
        
    Returns:
        Dict: Statistical analysis of results
    """
    total_times = [r.total for r in results]
    chatgpt_times = [r.chatgpt for r in results]
    shodan_times = [r.shodan for r in results]
    solution_times = [r.solution for r in results]
    
    return {
        "total": {
            "mean": statistics.mean(total_times),
            "median": statistics.median(total_times),
            "std_dev": statistics.stdev(total_times) if len(total_times) > 1 else 0,
            "min": min(total_times),
            "max": max(total_times)
        },
        "components": {
            "chatgpt": statistics.mean(chatgpt_times),
            "shodan": statistics.mean(shodan_times),
            "solution": statistics.mean(solution_times)
        }
    }

def save_results(results: List[TimingResult], analysis: Dict, output_dir: str = "evaluation_results"):
    """
    Save evaluation results and analysis to files.
    
    Args:
        results (List[TimingResult]): Raw timing results
        analysis (Dict): Statistical analysis
        output_dir (str): Directory to save results
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save raw results to CSV
    csv_path = f"{output_dir}/timing_results_{timestamp}.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Total Time', 'ChatGPT Time', 'Shodan Time', 'Solution Time'])
        for r in results:
            writer.writerow([r.total, r.chatgpt, r.shodan, r.solution])
    
    # Save analysis to JSON
    json_path = f"{output_dir}/analysis_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(analysis, f, indent=4)

async def main():
    """
    Main function to run the evaluation.
    """
    # Sample test queries
    test_queries = [
        "Find vulnerable Apache servers in Germany",
        "Show me exposed MongoDB databases in the US",
        "Find IoT devices with default passwords",
        "Search for vulnerable WordPress sites in Canada",
        "Find exposed Jenkins servers"
    ]
    
    print("Starting VulnGPT Performance Evaluation...")
    print(f"Testing {len(test_queries)} queries with 10 iterations each...")
    
    # Run evaluation
    results = await run_evaluation(test_queries)
    
    # Analyze results
    analysis = analyze_results(results)
    
    # Save results
    save_results(results, analysis)
    
    # Print summary
    print("\nEvaluation Results:")
    print(f"Average Total Response Time: {analysis['total']['mean']:.2f} seconds")
    print(f"Median Response Time: {analysis['total']['median']:.2f} seconds")
    print(f"Standard Deviation: {analysis['total']['std_dev']:.2f} seconds")
    print("\nComponent Breakdown:")
    print(f"ChatGPT Generation: {analysis['components']['chatgpt']:.2f} seconds")
    print(f"Shodan Query: {analysis['components']['shodan']:.2f} seconds")
    print(f"Solution Generation: {analysis['components']['solution']:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main()) 