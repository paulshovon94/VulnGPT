"""
VulnGPT Load Test Visualization Module

This module creates visual representations of the load test results,
showing concurrent user performance and system scalability metrics.

Author: Shovon Paul
Date: 2024-11-17
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List
import numpy as np
from datetime import datetime

class LoadTestVisualizer:
    def __init__(self, results_dir: str = "load_test_results"):
        """
        Initialize the visualizer with the results directory.
        """
        self.results_dir = Path(results_dir)
        # Set style for plots
        plt.style.use('default')
        sns.set_theme(style="whitegrid")
        sns.set_palette("husl")

    def load_latest_results(self) -> tuple[pd.DataFrame, Dict]:
        """
        Load the most recent load test results.
        """
        csv_files = list(self.results_dir.glob("load_test_results_*.csv"))
        json_files = list(self.results_dir.glob("load_test_analysis_*.json"))
        
        if not csv_files or not json_files:
            raise FileNotFoundError("No load test results found")
            
        latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
        latest_json = max(json_files, key=lambda x: x.stat().st_mtime)
        
        print(f"Loading data from:\n{latest_csv}\n{latest_json}")
        
        df = pd.read_csv(latest_csv)
        with open(latest_json, 'r') as f:
            analysis = json.load(f)
            
        return df, analysis

    def create_response_time_distribution(self, df: pd.DataFrame) -> None:
        """
        Create a distribution plot of response times under load.
        """
        plt.clf()
        plt.figure(figsize=(15, 8))
        
        try:
            plt.rcParams.update({
                'font.size': 24,
                'axes.labelsize': 28,
                'xtick.labelsize': 24,
                'ytick.labelsize': 24
            })
            
            # Create distribution plot
            sns.histplot(data=df, x='Total Time', bins=20, kde=True)
            
            plt.xlabel('Response Time (seconds)', labelpad=15, fontsize=28, fontweight='bold')
            plt.ylabel('Frequency', labelpad=15, fontsize=28, fontweight='bold')
            
            plt.tight_layout()
            
            output_path = self.results_dir / f'load_distribution_{datetime.now():%Y%m%d_%H%M%S}.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved response time distribution plot to: {output_path}")
            plt.close()
        except Exception as e:
            print(f"Error creating response time distribution plot: {str(e)}")
            plt.close()

    def create_success_rate_plot(self, analysis: Dict) -> None:
        """
        Create a pie chart showing success vs failure rate.
        """
        plt.clf()
        plt.figure(figsize=(12, 8))
        
        try:
            plt.rcParams.update({
                'font.size': 24,
                'axes.labelsize': 28
            })
            
            # Prepare data
            sizes = [analysis['successful_queries'], analysis['failed_queries']]
            labels = [f'Successful\n({sizes[0]} queries)', f'Failed\n({sizes[1]} queries)']
            colors = ['#66b3ff', '#ff9999']
            
            # Create pie chart without title
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                   textprops={'fontsize': 24, 'fontweight': 'bold'})
            
            plt.tight_layout()
            
            output_path = self.results_dir / f'success_rate_{datetime.now():%Y%m%d_%H%M%S}.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved success rate plot to: {output_path}")
            plt.close()
        except Exception as e:
            print(f"Error creating success rate plot: {str(e)}")
            plt.close()

    def create_performance_metrics(self, analysis: Dict) -> None:
        """
        Create a bar plot of key performance metrics.
        """
        plt.clf()
        plt.figure(figsize=(15, 8))
        
        try:
            plt.rcParams.update({
                'font.size': 24,
                'axes.labelsize': 28,
                'xtick.labelsize': 24,
                'ytick.labelsize': 24
            })
            
            # Prepare data
            metrics = {
                'Mean': analysis['response_times']['mean'],
                'Median': analysis['response_times']['median'],
                '95th\nPercentile': analysis['response_times']['95th_percentile'],
                'Max': analysis['response_times']['max']
            }
            
            # Create bar plot without title
            bars = plt.bar(metrics.keys(), metrics.values(), color='skyblue')
            plt.ylabel('Response Time (seconds)', labelpad=15, fontsize=28, fontweight='bold')
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}s',
                        ha='center', va='bottom',
                        fontsize=24, fontweight='bold')
            
            plt.tight_layout()
            
            output_path = self.results_dir / f'load_metrics_{datetime.now():%Y%m%d_%H%M%S}.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved performance metrics plot to: {output_path}")
            plt.close()
        except Exception as e:
            print(f"Error creating performance metrics plot: {str(e)}")
            plt.close()

    def create_all_visualizations(self) -> None:
        """
        Generate all load test visualization plots.
        """
        try:
            print("Loading load test results...")
            df, analysis = self.load_latest_results()
            
            print("Generating visualizations...")
            self.create_response_time_distribution(df)
            self.create_success_rate_plot(analysis)
            self.create_performance_metrics(analysis)
            
            print(f"Visualizations saved in: {self.results_dir}")
            
        except Exception as e:
            print(f"Error generating visualizations: {str(e)}")

def main():
    """
    Main function to run the visualization.
    """
    visualizer = LoadTestVisualizer()
    visualizer.create_all_visualizations()

if __name__ == "__main__":
    main() 