#!/usr/bin/env python3
"""
Intelligent Diagram Generator
Automatically analyzes business requirements and generates appropriate charts and diagrams
using AI to select the best visualization type for each context.
"""

import os
import json
import yaml
import logging
import openai
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
from wordcloud import WordCloud
import networkx as nx
from PIL import Image, ImageDraw, ImageFont
import textwrap
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/diagram_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ChartRequirement:
    """Data class for chart requirements"""
    title: str
    context: str
    data_type: str
    suggested_chart: str
    priority: int
    output_path: str

class IntelligentDiagramGenerator:
    """Main class for intelligent diagram generation"""
    
    def __init__(self, config_path='../../../config.yml'):
        """Initialize the diagram generator"""
        self.load_config(config_path)
        self.setup_openai()
        self.setup_directories()
        
        # Chart type mapping
        self.chart_types = {
            'flowchart': self.generate_flowchart,
            'gantt': self.generate_gantt_chart,
            'mind_map': self.generate_mind_map,
            'area_chart': self.generate_area_chart,
            'bar_chart': self.generate_bar_chart,
            'line_chart': self.generate_line_chart,
            'pie_chart': self.generate_pie_chart,
            'scatter_plot': self.generate_scatter_plot,
            'bubble_chart': self.generate_bubble_chart,
            'quadrant_chart': self.generate_quadrant_chart,
            'pyramid_chart': self.generate_pyramid_chart,
            'organization_chart': self.generate_org_chart,
            'network_diagram': self.generate_network_diagram,
            'heatmap': self.generate_heatmap,
            'dashboard': self.generate_dashboard
        }
        
        # Context to chart mapping prompts
        self.chart_selection_prompt = """
        Based on the business requirement context below, select the BEST chart type to visualize this information.
        
        Available chart types:
        - flowchart: Process flows, workflows, decision trees
        - gantt: Project timelines, implementation schedules
        - mind_map: Concept relationships, brainstorming, hierarchies  
        - area_chart: Trends over time, cumulative data
        - bar_chart: Comparisons between categories
        - line_chart: Trends, time series data
        - pie_chart: Parts of a whole, proportions
        - scatter_plot: Correlations, relationships between variables
        - bubble_chart: Three-dimensional data relationships
        - quadrant_chart: Matrix analysis, positioning
        - pyramid_chart: Hierarchical data, levels
        - organization_chart: Organizational structure
        - network_diagram: Connections, relationships
        - heatmap: Data density, geographic distribution
        - dashboard: Multiple metrics overview
        
        Context: {context}
        
        Respond with JSON:
        {{
            "chart_type": "selected_chart_type",
            "reasoning": "why this chart is best for this context",
            "data_structure": "what data structure this chart needs",
            "visual_elements": ["key visual elements to include"]
        }}
        """
    
    def load_config(self, config_path):
        """Load configuration"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            self.openai_api_key = config.get('openai', {}).get('api_key') or os.getenv('OPENAI_API_KEY')
            self.output_dir = Path(config.get('output', {}).get('diagrams_dir', 'outputs/diagrams'))
            self.research_file = config.get('input', {}).get('research_file', 'scripts/automation/intelligent_diagram_generator/deep_research.md')
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            # Use defaults
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
            self.output_dir = Path('outputs/diagrams')
            self.research_file = 'deep_research.md'
    
    def setup_openai(self):
        """Setup OpenAI client"""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or add to config.yml")
        
        openai.api_key = self.openai_api_key
        logger.info("OpenAI client initialized")
    
    def setup_directories(self):
        """Create necessary directories"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different chart types
        for chart_type in self.chart_types.keys():
            (self.output_dir / chart_type).mkdir(exist_ok=True)
    
    def analyze_research_file(self, file_path: str) -> List[ChartRequirement]:
        """Analyze research file and extract chart requirements"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use AI to analyze and extract visualization requirements
            analysis_prompt = f"""
            Analyze the following research document and identify sections that would benefit from visualization.
            
            For each section, provide:
            1. A descriptive title
            2. The context/content that needs visualization  
            3. The type of data (numerical, categorical, temporal, hierarchical, etc.)
            4. Priority level (1-5, where 5 is most important)
            
            Research Document:
            {content[:8000]}  # Limit to avoid token limits
            
            Respond with JSON array:
            [
                {{
                    "title": "Chart Title",
                    "context": "Content to visualize",
                    "data_type": "numerical/categorical/temporal/hierarchical",
                    "priority": 1-5
                }}
            ]
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3
            )
            
            requirements_data = json.loads(response.choices[0].message.content)
            
            # Convert to ChartRequirement objects
            requirements = []
            for i, req in enumerate(requirements_data):
                chart_req = ChartRequirement(
                    title=req['title'],
                    context=req['context'],
                    data_type=req['data_type'],
                    suggested_chart='',  # Will be filled by AI
                    priority=req['priority'],
                    output_path=''
                )
                requirements.append(chart_req)
            
            logger.info(f"Extracted {len(requirements)} visualization requirements")
            return requirements
            
        except Exception as e:
            logger.error(f"Error analyzing research file: {e}")
            return []
    
    def select_optimal_chart_type(self, requirement: ChartRequirement) -> str:
        """Use AI to select the optimal chart type for the requirement"""
        try:
            prompt = self.chart_selection_prompt.format(context=requirement.context)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            
            logger.info(f"Selected {result['chart_type']} for '{requirement.title}': {result['reasoning']}")
            return result['chart_type']
            
        except Exception as e:
            logger.error(f"Error selecting chart type: {e}")
            return 'bar_chart'  # Default fallback
    
    def generate_sample_data(self, chart_type: str, context: str) -> Dict:
        """Generate appropriate sample data for the chart type"""
        np.random.seed(42)  # For reproducible results
        
        data_generators = {
            'bar_chart': lambda: {
                'categories': ['Category A', 'Category B', 'Category C', 'Category D'],
                'values': np.random.randint(10, 100, 4)
            },
            'line_chart': lambda: {
                'x': pd.date_range('2020-01-01', periods=24, freq='M'),
                'y': np.cumsum(np.random.randn(24)) + 100
            },
            'pie_chart': lambda: {
                'labels': ['Segment 1', 'Segment 2', 'Segment 3', 'Segment 4'],
                'values': [30, 25, 25, 20]
            },
            'area_chart': lambda: {
                'x': pd.date_range('2020-01-01', periods=12, freq='M'),
                'y1': np.cumsum(np.random.randn(12)) + 50,
                'y2': np.cumsum(np.random.randn(12)) + 30,
                'y3': np.cumsum(np.random.randn(12)) + 20
            },
            'scatter_plot': lambda: {
                'x': np.random.normal(50, 15, 50),
                'y': np.random.normal(50, 15, 50),
                'categories': np.random.choice(['A', 'B', 'C'], 50)
            },
            'bubble_chart': lambda: {
                'x': np.random.normal(50, 15, 20),
                'y': np.random.normal(50, 15, 20),
                'size': np.random.randint(10, 100, 20),
                'categories': np.random.choice(['Type 1', 'Type 2', 'Type 3'], 20)
            },
            'heatmap': lambda: {
                'data': np.random.rand(10, 10),
                'x_labels': [f'Col {i}' for i in range(10)],
                'y_labels': [f'Row {i}' for i in range(10)]
            }
        }
        
        return data_generators.get(chart_type, data_generators['bar_chart'])()
    
    def generate_flowchart(self, requirement: ChartRequirement) -> str:
        """Generate a flowchart diagram"""
        output_path = self.output_dir / 'flowchart' / f"{requirement.title.replace(' ', '_').lower()}_flowchart.png"
        
        # Create flowchart using matplotlib and networkx
        G = nx.DiGraph()
        
        # Define nodes based on context
        nodes = [
            ("Start", {"pos": (0, 3)}),
            ("Process 1", {"pos": (1, 3)}),
            ("Decision", {"pos": (2, 3)}),
            ("Process 2A", {"pos": (3, 4)}),
            ("Process 2B", {"pos": (3, 2)}),
            ("End", {"pos": (4, 3)})
        ]
        
        edges = [
            ("Start", "Process 1"),
            ("Process 1", "Decision"),
            ("Decision", "Process 2A"),
            ("Decision", "Process 2B"),
            ("Process 2A", "End"),
            ("Process 2B", "End")
        ]
        
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        
        plt.figure(figsize=(12, 8))
        pos = nx.get_node_attributes(G, 'pos')
        
        # Draw flowchart
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=3000, alpha=0.7)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, arrowstyle='->')
        
        plt.title(requirement.title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated flowchart: {output_path}")
        return str(output_path)
    
    def generate_gantt_chart(self, requirement: ChartRequirement) -> str:
        """Generate a Gantt chart"""
        output_path = self.output_dir / 'gantt' / f"{requirement.title.replace(' ', '_').lower()}_gantt.png"
        
        # Sample project data
        tasks = [
            {'Task': 'Planning Phase', 'Start': '2024-01-01', 'End': '2024-01-31', 'Resource': 'Team A'},
            {'Task': 'Design Phase', 'Start': '2024-02-01', 'End': '2024-03-15', 'Resource': 'Team B'},
            {'Task': 'Development Phase', 'Start': '2024-03-01', 'End': '2024-05-31', 'Resource': 'Team C'},
            {'Task': 'Testing Phase', 'Start': '2024-05-15', 'End': '2024-06-30', 'Resource': 'Team D'},
            {'Task': 'Deployment Phase', 'Start': '2024-06-15', 'End': '2024-07-15', 'Resource': 'Team E'}
        ]
        
        df = pd.DataFrame(tasks)
        df['Start'] = pd.to_datetime(df['Start'])
        df['End'] = pd.to_datetime(df['End'])
        df['Duration'] = (df['End'] - df['Start']).dt.days
        
        # Create Gantt chart using plotly
        fig = px.timeline(df, x_start="Start", x_end="End", y="Task", color="Resource",
                         title=requirement.title, height=400)
        
        fig.update_layout(xaxis_title="Timeline", yaxis_title="Tasks")
        fig.write_image(output_path, width=1200, height=600)
        
        logger.info(f"Generated Gantt chart: {output_path}")
        return str(output_path)
    
    def generate_mind_map(self, requirement: ChartRequirement) -> str:
        """Generate a mind map"""
        output_path = self.output_dir / 'mind_map' / f"{requirement.title.replace(' ', '_').lower()}_mindmap.png"
        
        # Create mind map using networkx
        G = nx.Graph()
        
        # Central node
        central_topic = requirement.title
        G.add_node(central_topic, level=0)
        
        # Main branches
        main_branches = ['Concept 1', 'Concept 2', 'Concept 3', 'Concept 4']
        for branch in main_branches:
            G.add_node(branch, level=1)
            G.add_edge(central_topic, branch)
            
            # Sub-branches
            for i in range(2):
                sub_branch = f"{branch}.{i+1}"
                G.add_node(sub_branch, level=2)
                G.add_edge(branch, sub_branch)
        
        # Create layout
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        plt.figure(figsize=(14, 10))
        
        # Draw nodes by level
        levels = nx.get_node_attributes(G, 'level')
        colors = {0: 'red', 1: 'lightblue', 2: 'lightgreen'}
        sizes = {0: 4000, 1: 2000, 2: 1000}
        
        for level in [0, 1, 2]:
            nodes = [node for node, lev in levels.items() if lev == level]
            nx.draw_networkx_nodes(G, pos, nodelist=nodes, 
                                 node_color=colors[level], node_size=sizes[level], alpha=0.8)
        
        # Draw edges and labels
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.6)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        
        plt.title(f"Mind Map: {requirement.title}", fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated mind map: {output_path}")
        return str(output_path)
    
    def generate_area_chart(self, requirement: ChartRequirement) -> str:
        """Generate an area chart"""
        output_path = self.output_dir / 'area_chart' / f"{requirement.title.replace(' ', '_').lower()}_area.png"
        
        data = self.generate_sample_data('area_chart', requirement.context)
        
        plt.figure(figsize=(12, 8))
        plt.fill_between(data['x'], data['y1'], alpha=0.7, label='Series 1')
        plt.fill_between(data['x'], data['y2'], alpha=0.7, label='Series 2')
        plt.fill_between(data['x'], data['y3'], alpha=0.7, label='Series 3')
        
        plt.title(requirement.title, fontsize=16, fontweight='bold')
        plt.xlabel('Time Period')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated area chart: {output_path}")
        return str(output_path)
    
    def generate_bar_chart(self, requirement: ChartRequirement) -> str:
        """Generate a bar chart"""
        output_path = self.output_dir / 'bar_chart' / f"{requirement.title.replace(' ', '_').lower()}_bar.png"
        
        data = self.generate_sample_data('bar_chart', requirement.context)
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(data['categories'], data['values'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        
        plt.title(requirement.title, fontsize=16, fontweight='bold')
        plt.xlabel('Categories')
        plt.ylabel('Values')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated bar chart: {output_path}")
        return str(output_path)
    
    def generate_line_chart(self, requirement: ChartRequirement) -> str:
        """Generate a line chart"""
        output_path = self.output_dir / 'line_chart' / f"{requirement.title.replace(' ', '_').lower()}_line.png"
        
        data = self.generate_sample_data('line_chart', requirement.context)
        
        plt.figure(figsize=(12, 6))
        plt.plot(data['x'], data['y'], marker='o', linewidth=2, markersize=6, color='#FF6B6B')
        
        plt.title(requirement.title, fontsize=16, fontweight='bold')
        plt.xlabel('Time Period')
        plt.ylabel('Value')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated line chart: {output_path}")
        return str(output_path)
    
    def generate_pie_chart(self, requirement: ChartRequirement) -> str:
        """Generate a pie chart"""
        output_path = self.output_dir / 'pie_chart' / f"{requirement.title.replace(' ', '_').lower()}_pie.png"
        
        data = self.generate_sample_data('pie_chart', requirement.context)
        
        plt.figure(figsize=(10, 8))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        wedges, texts, autotexts = plt.pie(data['values'], labels=data['labels'], autopct='%1.1f%%',
                                          colors=colors, startangle=90, explode=(0.05, 0, 0, 0))
        
        plt.title(requirement.title, fontsize=16, fontweight='bold', pad=20)
        
        # Enhance text styling
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated pie chart: {output_path}")
        return str(output_path)
    
    def generate_scatter_plot(self, requirement: ChartRequirement) -> str:
        """Generate a scatter plot"""
        output_path = self.output_dir / 'scatter_plot' / f"{requirement.title.replace(' ', '_').lower()}_scatter.png"
        
        data = self.generate_sample_data('scatter_plot', requirement.context)
        
        plt.figure(figsize=(10, 8))
        
        # Create scatter plot with different colors for categories
        for category in np.unique(data['categories']):
            mask = data['categories'] == category
            plt.scatter(data['x'][mask], data['y'][mask], label=category, alpha=0.7, s=60)
        
        plt.title(requirement.title, fontsize=16, fontweight='bold')
        plt.xlabel('X Variable')
        plt.ylabel('Y Variable')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated scatter plot: {output_path}")
        return str(output_path)
    
    def generate_bubble_chart(self, requirement: ChartRequirement) -> str:
        """Generate a bubble chart"""
        output_path = self.output_dir / 'bubble_chart' / f"{requirement.title.replace(' ', '_').lower()}_bubble.png"
        
        data = self.generate_sample_data('bubble_chart', requirement.context)
        
        plt.figure(figsize=(12, 8))
        
        for category in np.unique(data['categories']):
            mask = data['categories'] == category
            plt.scatter(data['x'][mask], data['y'][mask], s=data['size'][mask]*3, 
                       label=category, alpha=0.6)
        
        plt.title(requirement.title, fontsize=16, fontweight='bold')
        plt.xlabel('X Variable')
        plt.ylabel('Y Variable')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated bubble chart: {output_path}")
        return str(output_path)
    
    def generate_quadrant_chart(self, requirement: ChartRequirement) -> str:
        """Generate a quadrant analysis chart"""
        output_path = self.output_dir / 'quadrant_chart' / f"{requirement.title.replace(' ', '_').lower()}_quadrant.png"
        
        # Sample data for quadrant analysis
        np.random.seed(42)
        n_points = 20
        x = np.random.uniform(-10, 10, n_points)
        y = np.random.uniform(-10, 10, n_points)
        
        plt.figure(figsize=(10, 10))
        
        # Create quadrants
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        
        # Color points based on quadrant
        colors = []
        for i in range(len(x)):
            if x[i] > 0 and y[i] > 0:
                colors.append('green')  # High-High
            elif x[i] < 0 and y[i] > 0:
                colors.append('blue')   # Low-High
            elif x[i] < 0 and y[i] < 0:
                colors.append('red')    # Low-Low
            else:
                colors.append('orange') # High-Low
        
        plt.scatter(x, y, c=colors, s=100, alpha=0.7)
        
        # Add quadrant labels
        plt.text(5, 5, 'High-High\n(Stars)', ha='center', va='center', fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.5))
        plt.text(-5, 5, 'Low-High\n(Question Marks)', ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.5))
        plt.text(-5, -5, 'Low-Low\n(Dogs)', ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.5))
        plt.text(5, -5, 'High-Low\n(Cash Cows)', ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='moccasin', alpha=0.5))
        
        plt.title(requirement.title, fontsize=16, fontweight='bold')
        plt.xlabel('X Dimension')
        plt.ylabel('Y Dimension')
        plt.grid(True, alpha=0.3)
        plt.xlim(-12, 12)
        plt.ylim(-12, 12)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated quadrant chart: {output_path}")
        return str(output_path)
    
    def generate_pyramid_chart(self, requirement: ChartRequirement) -> str:
        """Generate a pyramid chart"""
        output_path = self.output_dir / 'pyramid_chart' / f"{requirement.title.replace(' ', '_').lower()}_pyramid.png"
        
        # Sample pyramid data
        levels = ['Level 1 (Top)', 'Level 2', 'Level 3', 'Level 4 (Base)']
        values = [10, 25, 40, 100]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Calculate positions for pyramid effect
        max_width = max(values)
        y_positions = range(len(levels))
        
        for i, (level, value, color) in enumerate(zip(levels, values, colors)):
            width = value
            left = (max_width - width) / 2
            
            bar = ax.barh(i, width, left=left, height=0.8, color=color, alpha=0.8, 
                         edgecolor='white', linewidth=2)
            
            # Add value labels
            ax.text(max_width/2, i, f'{level}\n({value})', ha='center', va='center', 
                   fontweight='bold', color='white' if value > 30 else 'black')
        
        ax.set_yticks(y_positions)
        ax.set_yticklabels([])
        ax.set_xlim(0, max_width)
        ax.set_title(requirement.title, fontsize=16, fontweight='bold', pad=20)
        
        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([])
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated pyramid chart: {output_path}")
        return str(output_path)
    
    def generate_org_chart(self, requirement: ChartRequirement) -> str:
        """Generate an organizational chart"""
        output_path = self.output_dir / 'organization_chart' / f"{requirement.title.replace(' ', '_').lower()}_org.png"
        
        # Create hierarchical organization structure
        G = nx.DiGraph()
        
        # Define organizational hierarchy
        hierarchy = {
            'CEO': {'pos': (0, 4), 'level': 0},
            'VP Sales': {'pos': (-2, 3), 'level': 1},
            'VP Engineering': {'pos': (0, 3), 'level': 1},
            'VP Marketing': {'pos': (2, 3), 'level': 1},
            'Sales Manager': {'pos': (-2, 2), 'level': 2},
            'Dev Manager': {'pos': (-1, 2), 'level': 2},
            'QA Manager': {'pos': (1, 2), 'level': 2},
            'Marketing Manager': {'pos': (2, 2), 'level': 2},
            'Sales Rep 1': {'pos': (-2.5, 1), 'level': 3},
            'Sales Rep 2': {'pos': (-1.5, 1), 'level': 3},
            'Developer 1': {'pos': (-1.5, 1), 'level': 3},
            'Developer 2': {'pos': (-0.5, 1), 'level': 3},
            'QA Engineer': {'pos': (1, 1), 'level': 3},
            'Marketing Specialist': {'pos': (2, 1), 'level': 3}
        }
        
        # Add nodes
        for node, attrs in hierarchy.items():
            G.add_node(node, **attrs)
        
        # Add edges (reporting relationships)
        edges = [
            ('CEO', 'VP Sales'), ('CEO', 'VP Engineering'), ('CEO', 'VP Marketing'),
            ('VP Sales', 'Sales Manager'), ('VP Engineering', 'Dev Manager'), ('VP Engineering', 'QA Manager'),
            ('VP Marketing', 'Marketing Manager'), ('Sales Manager', 'Sales Rep 1'), ('Sales Manager', 'Sales Rep 2'),
            ('Dev Manager', 'Developer 1'), ('Dev Manager', 'Developer 2'), ('QA Manager', 'QA Engineer'),
            ('Marketing Manager', 'Marketing Specialist')
        ]
        G.add_edges_from(edges)
        
        plt.figure(figsize=(16, 12))
        pos = {node: attrs['pos'] for node, attrs in hierarchy.items()}
        
        # Draw nodes by level with different colors
        level_colors = {0: '#FF6B6B', 1: '#4ECDC4', 2: '#45B7D1', 3: '#96CEB4'}
        level_sizes = {0: 4000, 1: 3000, 2: 2000, 3: 1500}
        
        for level in range(4):
            level_nodes = [node for node, attrs in hierarchy.items() if attrs['level'] == level]
            nx.draw_networkx_nodes(G, pos, nodelist=level_nodes,
                                 node_color=level_colors[level], 
                                 node_size=level_sizes[level], alpha=0.8)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=15, alpha=0.6)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        
        plt.title(requirement.title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated organization chart: {output_path}")
        return str(output_path)
    
    def generate_network_diagram(self, requirement: ChartRequirement) -> str:
        """Generate a network diagram"""
        output_path = self.output_dir / 'network_diagram' / f"{requirement.title.replace(' ', '_').lower()}_network.png"
        
        # Create sample network
        G = nx.random_geometric_graph(20, 0.3, seed=42)
        
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Calculate node sizes based on degree
        degrees = dict(G.degree())
        node_sizes = [300 + degrees[node] * 100 for node in G.nodes()]
        
        # Draw network
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue',
                              alpha=0.8, edgecolors='navy', linewidths=1)
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.6)
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        plt.title(requirement.title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated network diagram: {output_path}")
        return str(output_path)
    
    def generate_heatmap(self, requirement: ChartRequirement) -> str:
        """Generate a heatmap"""
        output_path = self.output_dir / 'heatmap' / f"{requirement.title.replace(' ', '_').lower()}_heatmap.png"
        
        data = self.generate_sample_data('heatmap', requirement.context)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(data['data'], xticklabels=data['x_labels'], yticklabels=data['y_labels'],
                   annot=True, cmap='YlOrRd', fmt='.2f', cbar_kws={'label': 'Intensity'})
        
        plt.title(requirement.title, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('X Categories')
        plt.ylabel('Y Categories')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated heatmap: {output_path}")
        return str(output_path)
    
    def generate_dashboard(self, requirement: ChartRequirement) -> str:
        """Generate a comprehensive dashboard"""
        output_path = self.output_dir / 'dashboard' / f"{requirement.title.replace(' ', '_').lower()}_dashboard.png"
        
        fig = plt.figure(figsize=(16, 12))
        
        # Create subplots for dashboard
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Subplot 1: Line chart
        ax1 = fig.add_subplot(gs[0, :2])
        x = pd.date_range('2023-01-01', periods=12, freq='M')
        y = np.cumsum(np.random.randn(12)) + 100
        ax1.plot(x, y, marker='o')
        ax1.set_title('Trend Analysis')
        ax1.grid(True, alpha=0.3)
        
        # Subplot 2: Pie chart
        ax2 = fig.add_subplot(gs[0, 2])
        labels = ['A', 'B', 'C', 'D']
        sizes = [25, 30, 25, 20]
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax2.set_title('Distribution')
        
        # Subplot 3: Bar chart
        ax3 = fig.add_subplot(gs[1, :2])
        categories = ['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4']
        values = [20, 35, 30, 25]
        ax3.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        ax3.set_title('Performance Metrics')
        
        # Subplot 4: Heatmap
        ax4 = fig.add_subplot(gs[1, 2])
        heatmap_data = np.random.rand(5, 5)
        im = ax4.imshow(heatmap_data, cmap='YlOrRd')
        ax4.set_title('Correlation Matrix')
        plt.colorbar(im, ax=ax4, shrink=0.6)
        
        # Subplot 5: Scatter plot
        ax5 = fig.add_subplot(gs[2, :])
        x_scatter = np.random.normal(50, 15, 50)
        y_scatter = np.random.normal(50, 15, 50)
        ax5.scatter(x_scatter, y_scatter, alpha=0.6, s=60)
        ax5.set_title('Risk vs Return Analysis')
        ax5.grid(True, alpha=0.3)
        
        plt.suptitle(requirement.title, fontsize=20, fontweight='bold', y=0.98)
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Generated dashboard: {output_path}")
        return str(output_path)
    
    def generate_diagram(self, requirement: ChartRequirement) -> str:
        """Generate diagram based on requirement"""
        try:
            # Select optimal chart type using AI
            chart_type = self.select_optimal_chart_type(requirement)
            
            # Set output path
            requirement.output_path = str(self.output_dir / chart_type / f"{requirement.title.replace(' ', '_').lower()}.png")
            
            # Generate the chart
            if chart_type in self.chart_types:
                return self.chart_types[chart_type](requirement)
            else:
                logger.warning(f"Unknown chart type: {chart_type}, using bar_chart")
                return self.generate_bar_chart(requirement)
                
        except Exception as e:
            logger.error(f"Error generating diagram for '{requirement.title}': {e}")
            return ""
    
    def generate_all_diagrams(self, research_file_path: str = None) -> Dict:
        """Generate all diagrams from research file"""
        if research_file_path is None:
            research_file_path = self.research_file
        
        try:
            # Analyze research file
            requirements = self.analyze_research_file(research_file_path)
            
            if not requirements:
                logger.warning("No visualization requirements found")
                return {'status': 'no_requirements', 'diagrams': []}
            
            # Sort by priority
            requirements.sort(key=lambda x: x.priority, reverse=True)
            
            # Generate diagrams
            generated_diagrams = []
            for requirement in requirements:
                diagram_path = self.generate_diagram(requirement)
                if diagram_path:
                    generated_diagrams.append({
                        'title': requirement.title,
                        'chart_type': requirement.suggested_chart,
                        'path': diagram_path,
                        'priority': requirement.priority
                    })
            
            logger.info(f"Successfully generated {len(generated_diagrams)} diagrams")
            
            # Create summary report
            summary = {
                'status': 'success',
                'total_requirements': len(requirements),
                'generated_diagrams': len(generated_diagrams),
                'diagrams': generated_diagrams,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save summary
            summary_path = self.output_dir / 'generation_summary.json'
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating diagrams: {e}")
            return {'status': 'error', 'message': str(e)}

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Intelligent Diagram Generator')
    parser.add_argument('--research-file', default='deep_research.md',
                       help='Research file to analyze for visualization requirements')
    parser.add_argument('--config', default='../../../config.yml',
                       help='Configuration file path')
    parser.add_argument('--chart-type', choices=list(IntelligentDiagramGenerator({}).chart_types.keys()),
                       help='Generate specific chart type only')
    parser.add_argument('--list-types', action='store_true',
                       help='List available chart types')
    
    args = parser.parse_args()
    
    # Create generator
    generator = IntelligentDiagramGenerator(args.config)
    
    if args.list_types:
        logger.info("Available chart types:")
        for chart_type in generator.chart_types.keys():
            logger.info(f"  - {chart_type}")
        return
    
    if args.chart_type:
        # Generate single chart type
        requirement = ChartRequirement(
            title=f"Sample {args.chart_type.replace('_', ' ').title()}",
            context="Sample context for demonstration",
            data_type="numerical",
            suggested_chart=args.chart_type,
            priority=5,
            output_path=""
        )
        diagram_path = generator.generate_diagram(requirement)
        logger.info(f"Generated sample {args.chart_type}: {diagram_path}")
    else:
        # Generate all diagrams from research file
        results = generator.generate_all_diagrams(args.research_file)
        logger.info(f"Generation complete: {results}")

if __name__ == "__main__":
    main()
