"""
VulnGPT Visualization Module

This module creates visual representations of the VulnGPT performance evaluation results
using matplotlib and seaborn for better insight and presentation.

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

class PerformanceVisualizer:
    def __init__(self, results_dir: str = "evaluation_results"):
        """
        Initialize the visualizer with the results directory.
        
        Args:
            results_dir (str): Directory containing evaluation results
        """
        self.results_dir = Path(results_dir)
        # Set style for all plots - using a more basic style
        plt.style.use('default')  # Changed from 'seaborn' to 'default'
        # Configure seaborn settings separately
        sns.set_theme(style="whitegrid")  # Using whitegrid style instead
        sns.set_palette("husl")
        
    def load_latest_results(self) -> tuple[pd.DataFrame, Dict]:
        """
        Load the most recent evaluation results.
        
        Returns:
            tuple[pd.DataFrame, Dict]: Raw results DataFrame and analysis dictionary
        """
        # Find latest CSV and JSON files
        csv_files = list(self.results_dir.glob("timing_results_*.csv"))
        json_files = list(self.results_dir.glob("analysis_*.json"))
        
        if not csv_files or not json_files:
            raise FileNotFoundError("No results files found in the specified directory")
            
        latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
        latest_json = max(json_files, key=lambda x: x.stat().st_mtime)
        
        print(f"Loading data from:\n{latest_csv}\n{latest_json}")  # Debug print
        
        # Load data
        df = pd.read_csv(latest_csv)
        with open(latest_json, 'r') as f:
            analysis = json.load(f)
            
        return df, analysis

    def create_time_distribution_plot(self, df: pd.DataFrame) -> None:
        """
        Create a violin plot showing the distribution of response times.
        """
        # Clear any existing plots and set figure size
        plt.clf()
        plt.figure(figsize=(15, 8))
        
        try:
            # Set larger font sizes
            plt.rcParams.update({
                'font.size': 24,
                'axes.labelsize': 28,
                'xtick.labelsize': 24,
                'ytick.labelsize': 24
            })
            
            # Melt the DataFrame for seaborn
            df_melted = pd.melt(df, value_vars=['ChatGPT Time', 'Shodan Time', 'Solution Time'],
                               var_name='Component', value_name='Time (seconds)')
            
            # Create violin plot with larger scale
            ax = sns.violinplot(data=df_melted, x='Component', y='Time (seconds)', scale='width')
            
            # Customize the plot without title
            plt.xlabel('Component', labelpad=15, fontsize=28, fontweight='bold')
            plt.ylabel('Time (seconds)', labelpad=15, fontsize=28, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            
            # Increase tick label sizes
            ax.tick_params(axis='both', which='major', labelsize=24)
            
            # Adjust layout with more space
            plt.tight_layout()
            
            # Save plot with higher DPI
            output_path = self.results_dir / f'time_distribution_{datetime.now():%Y%m%d_%H%M%S}.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved time distribution plot to: {output_path}")
            plt.close()
        except Exception as e:
            print(f"Error creating time distribution plot: {str(e)}")
            plt.close()

    def create_component_breakdown_plot(self, df: pd.DataFrame) -> None:
        """
        Create a stacked bar plot showing the breakdown of component times.
        """
        # Clear any existing plots and set figure size
        plt.clf()
        plt.figure(figsize=(15, 10))
        
        try:
            # Set larger font sizes
            plt.rcParams.update({
                'font.size': 24,
                'axes.labelsize': 28,
                'xtick.labelsize': 24,
                'ytick.labelsize': 24,
                'legend.fontsize': 24
            })
            
            # Calculate means for each component
            means = df[['ChatGPT Time', 'Shodan Time', 'Solution Time']].mean()
            
            # Create stacked bar plot
            bottom = 0
            colors = ['#FF9999', '#66B2FF', '#99FF99']
            
            for component, color in zip(means.index, colors):
                plt.bar('Total Response Time', means[component], bottom=bottom, 
                       label=component, color=color)
                bottom += means[component]
            
            plt.ylabel('Time (seconds)', labelpad=15, fontsize=28, fontweight='bold')
            
            # Move legend to top center, horizontal orientation with larger text
            plt.legend(bbox_to_anchor=(0.5, 1.15), 
                      loc='upper center', 
                      ncol=3,
                      borderaxespad=0.,
                      fontsize=24)
            
            # Add total time label on top of the stack with larger font
            plt.text(0, bottom + 0.1, f'Total: {bottom:.2f}s', 
                    ha='center', va='bottom', fontsize=24, fontweight='bold')
            
            # Increase tick label sizes
            plt.xticks(fontsize=24)
            plt.yticks(fontsize=24)
            
            # Adjust layout
            plt.tight_layout()
            
            # Save plot with higher DPI
            output_path = self.results_dir / f'component_breakdown_{datetime.now():%Y%m%d_%H%M%S}.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved component breakdown plot to: {output_path}")
            plt.close()
        except Exception as e:
            print(f"Error creating component breakdown plot: {str(e)}")
            plt.close()

    def create_performance_summary(self, analysis: Dict) -> None:
        """
        Create a visual summary of performance metrics.
        """
        # Clear any existing plots and set figure size
        plt.clf()
        plt.figure(figsize=(15, 8))
        
        try:
            # Set larger font sizes
            plt.rcParams.update({
                'font.size': 24,
                'axes.labelsize': 28,
                'xtick.labelsize': 24,
                'ytick.labelsize': 24
            })
            
            # Extract metrics
            metrics = {
                'Mean': analysis['total']['mean'],
                'Median': analysis['total']['median'],
                'Std Dev': analysis['total']['std_dev'],
                'Min': analysis['total']['min'],
                'Max': analysis['total']['max']
            }
            
            # Create bar plot without title
            bars = plt.bar(metrics.keys(), metrics.values(), color='skyblue')
            plt.ylabel('Time (seconds)', labelpad=15, fontsize=28, fontweight='bold')
            
            # Add value labels on top of bars with larger font
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}s',
                        ha='center', va='bottom',
                        fontsize=24, fontweight='bold')
            
            # Increase tick label sizes
            plt.xticks(fontsize=24, rotation=0)
            plt.yticks(fontsize=24)
            
            # Adjust layout
            plt.tight_layout()
            
            # Save plot with higher DPI
            output_path = self.results_dir / f'performance_summary_{datetime.now():%Y%m%d_%H%M%S}.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved performance summary plot to: {output_path}")
            plt.close()
        except Exception as e:
            print(f"Error creating performance summary plot: {str(e)}")
            plt.close()

    def create_all_visualizations(self) -> None:
        """
        Generate all visualization plots.
        """
        try:
            print("Loading evaluation results...")
            df, analysis = self.load_latest_results()
            
            print("Generating visualizations...")
            self.create_time_distribution_plot(df)
            self.create_component_breakdown_plot(df)
            self.create_performance_summary(analysis)
            
            print(f"Visualizations saved in: {self.results_dir}")
            
        except Exception as e:
            print(f"Error generating visualizations: {str(e)}")

def main():
    """
    Main function to run the visualization.
    """
    visualizer = PerformanceVisualizer()
    visualizer.create_all_visualizations()

if __name__ == "__main__":
    main() 