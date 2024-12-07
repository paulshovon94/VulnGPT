"""
VulnGPT Load Testing Module

This module evaluates VulnGPT's performance under high-load conditions by
simulating multiple concurrent users and analyzing system response times.

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
import concurrent.futures
from dataclasses import dataclass
import numpy as np

@dataclass
class ConcurrentQueryResult:
    query: str
    total_time: float
    success: bool
    error: str = None

class LoadTester:
    def __init__(self, output_dir: str = "load_test_results"):
        """
        Initialize the load tester.
        
        Args:
            output_dir (str): Directory to store test results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def execute_single_query(self, query: str) -> ConcurrentQueryResult:
        """
        Execute a single query and measure its performance.
        
        Args:
            query (str): The query to execute
            
        Returns:
            ConcurrentQueryResult: Results and timing data
        """
        start_time = time.time()
        try:
            # Execute the complete query pipeline
            chatgpt_response = await get_shodan_query(query)
            shodan_results = await execute_shodan_query(chatgpt_response['shodan_query'], limit=5)
            await get_security_solutions(shodan_results)
            
            total_time = time.time() - start_time
            return ConcurrentQueryResult(
                query=query,
                total_time=total_time,
                success=True
            )
        except Exception as e:
            total_time = time.time() - start_time
            return ConcurrentQueryResult(
                query=query,
                total_time=total_time,
                success=False,
                error=str(e)
            )

    async def run_concurrent_queries(self, queries: List[str], concurrent_users: int = 10) -> List[ConcurrentQueryResult]:
        """
        Run multiple queries concurrently to simulate multiple users.
        
        Args:
            queries (List[str]): List of queries to execute
            concurrent_users (int): Number of concurrent users to simulate
            
        Returns:
            List[ConcurrentQueryResult]: Results for all queries
        """
        # Create tasks for concurrent execution
        tasks = []
        for _ in range(concurrent_users):
            # Cycle through queries if we have fewer queries than concurrent users
            for query in queries:
                tasks.append(self.execute_single_query(query))
                if len(tasks) >= concurrent_users:
                    break
            if len(tasks) >= concurrent_users:
                break

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if isinstance(r, ConcurrentQueryResult)]

    def analyze_results(self, results: List[ConcurrentQueryResult]) -> Dict:
        """
        Analyze the load test results.
        
        Args:
            results (List[ConcurrentQueryResult]): Results from concurrent queries
            
        Returns:
            Dict: Analysis of the results
        """
        successful_times = [r.total_time for r in results if r.success]
        failed_times = [r.total_time for r in results if not r.success]
        
        analysis = {
            "total_queries": len(results),
            "successful_queries": len(successful_times),
            "failed_queries": len(failed_times),
            "success_rate": len(successful_times) / len(results) * 100 if results else 0,
            "response_times": {
                "mean": statistics.mean(successful_times) if successful_times else 0,
                "median": statistics.median(successful_times) if successful_times else 0,
                "std_dev": statistics.stdev(successful_times) if len(successful_times) > 1 else 0,
                "min": min(successful_times) if successful_times else 0,
                "max": max(successful_times) if successful_times else 0,
                "95th_percentile": np.percentile(successful_times, 95) if successful_times else 0
            }
        }
        return analysis

    def save_results(self, results: List[ConcurrentQueryResult], analysis: Dict):
        """
        Save the load test results and analysis.
        
        Args:
            results (List[ConcurrentQueryResult]): Raw test results
            analysis (Dict): Analyzed results
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save raw results to CSV
        csv_path = self.output_dir / f"load_test_results_{timestamp}.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Query', 'Total Time', 'Success', 'Error'])
            for result in results:
                writer.writerow([result.query, result.total_time, result.success, result.error])

        # Save analysis to JSON
        json_path = self.output_dir / f"load_test_analysis_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(analysis, f, indent=4)

    def print_analysis(self, analysis: Dict):
        """
        Print a formatted analysis report.
        """
        print("\n=== Load Test Analysis ===")
        print(f"Total Queries: {analysis['total_queries']}")
        print(f"Successful Queries: {analysis['successful_queries']}")
        print(f"Failed Queries: {analysis['failed_queries']}")
        print(f"Success Rate: {analysis['success_rate']:.2f}%")
        print("\nResponse Times (seconds):")
        print(f"  Mean: {analysis['response_times']['mean']:.2f}")
        print(f"  Median: {analysis['response_times']['median']:.2f}")
        print(f"  95th Percentile: {analysis['response_times']['95th_percentile']:.2f}")
        print(f"  Standard Deviation: {analysis['response_times']['std_dev']:.2f}")
        print(f"  Min: {analysis['response_times']['min']:.2f}")
        print(f"  Max: {analysis['response_times']['max']:.2f}")

async def main():
    """
    Main function to run the load test.
    """
    # Test queries
    test_queries = [
        "Find vulnerable Apache servers in Germany",
        "Show me exposed MongoDB databases in the US",
        "Find IoT devices with default passwords",
        "Search for vulnerable WordPress sites in Canada",
        "Find exposed Jenkins servers"
    ]
    
    # Initialize load tester
    load_tester = LoadTester()
    
    print("Starting VulnGPT Load Test...")
    print(f"Simulating 10 concurrent users...")
    
    # Run load test
    results = await load_tester.run_concurrent_queries(test_queries, concurrent_users=10)
    
    # Analyze results
    analysis = load_tester.analyze_results(results)
    
    # Save results
    load_tester.save_results(results, analysis)
    
    # Print analysis
    load_tester.print_analysis(analysis)

if __name__ == "__main__":
    asyncio.run(main()) 