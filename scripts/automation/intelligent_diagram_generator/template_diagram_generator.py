#!/usr/bin/env python3
"""
Template Diagram Generator
Specifically generates diagrams for the unified project analysis template placeholders
"""

import os
import json
import logging
from pathlib import Path
from intelligent_diagram_generator import IntelligentDiagramGenerator, ChartRequirement
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TemplateSpecificDiagramGenerator(IntelligentDiagramGenerator):
    """Specialized generator for template-specific diagram requirements"""
    
    def __init__(self, config_path='../../../config.yml'):
        super().__init__(config_path)
        
        # Define specific template diagram requirements
        self.template_requirements = {
            'PROJECT_OVERVIEW_IMAGE_PATH': {
                'title': 'Project Overview Dashboard',
                'context': 'Visual overview showing key project metrics, investment amount, expected ROI, timeline, and critical success factors in a comprehensive dashboard format',
                'chart_type': 'dashboard',
                'priority': 5
            },
            'FINANCIAL_PERFORMANCE_CHART_PATH': {
                'title': 'Financial Performance Comparison',
                'context': 'Bar chart comparing project financial metrics (ROI, DSCR, payback period) against industry benchmarks and averages',
                'chart_type': 'bar_chart',
                'priority': 5
            },
            'RISK_RETURN_MATRIX_PATH': {
                'title': 'Risk-Return Analysis Matrix',
                'context': 'Quadrant chart showing different project categories plotted by risk level (x-axis) versus expected return (y-axis)',
                'chart_type': 'quadrant_chart',
                'priority': 4
            },
            'PROCESS_FLOWCHART_PATH': {
                'title': 'Manufacturing Process Flow',
                'context': 'Step-by-step flowchart showing manufacturing process from raw materials to finished products with decision points and quality checks',
                'chart_type': 'flowchart',
                'priority': 4
            },
            'SUPPLY_CHAIN_DIAGRAM_PATH': {
                'title': 'Supply Chain Network',
                'context': 'Network diagram showing relationships between suppliers, manufacturers, distributors, and customers in the supply chain ecosystem',
                'chart_type': 'network_diagram',
                'priority': 3
            },
            'MARKET_TRENDS_CHART_PATH': {
                'title': 'Market Size Growth Trends',
                'context': 'Line chart showing market size evolution over the past 5 years and projected growth for the next 3 years with trend analysis',
                'chart_type': 'line_chart',
                'priority': 4
            },
            'COMPETITIVE_LANDSCAPE_PATH': {
                'title': 'Competitive Market Positioning',
                'context': 'Bubble chart showing competitive landscape with market share, competitive advantage, and threat levels for different competitor categories',
                'chart_type': 'bubble_chart',
                'priority': 3
            },
            'GEOGRAPHIC_DISTRIBUTION_MAP_PATH': {
                'title': 'Geographic Investment Distribution',
                'context': 'Heatmap showing geographic distribution of projects and investments across different states and regions with intensity indicators',
                'chart_type': 'heatmap',
                'priority': 4
            },
            'REGIONAL_PERFORMANCE_DASHBOARD_PATH': {
                'title': 'Regional Performance Analytics',
                'context': 'Dashboard comparing regional performance metrics including project count, investment, employment, and success rates across different regions',
                'chart_type': 'dashboard',
                'priority': 4
            },
            'INVESTMENT_HOTSPOTS_HEATMAP_PATH': {
                'title': 'Investment Hotspots Analysis',
                'context': 'Heatmap visualization showing investment hotspots and growth potential across different districts with color intensity representing opportunity levels',
                'chart_type': 'heatmap',
                'priority': 3
            },
            'RISK_MATRIX_VISUALIZATION_PATH': {
                'title': 'Comprehensive Risk Assessment Matrix',
                'context': 'Risk assessment matrix showing different risk categories (market, technical, financial, operational, geographic) plotted by probability and impact levels',
                'chart_type': 'quadrant_chart',
                'priority': 4
            },
            'SWOT_ANALYSIS_MATRIX_PATH': {
                'title': 'SWOT Strategic Analysis',
                'context': 'Quadrant diagram displaying Strengths, Weaknesses, Opportunities, and Threats in a structured matrix format for strategic planning',
                'chart_type': 'quadrant_chart',
                'priority': 3
            },
            'IMPLEMENTATION_GANTT_CHART_PATH': {
                'title': 'Project Implementation Timeline',
                'context': 'Gantt chart showing project implementation phases, milestones, dependencies, and timeline from planning to commercial operations',
                'chart_type': 'gantt',
                'priority': 5
            },
            'FINANCIAL_PROJECTIONS_CHART_PATH': {
                'title': '5-Year Financial Projections',
                'context': 'Line chart with multiple series showing revenue, cost, profit, ROI, and DSCR projections over a 5-year period with trend analysis',
                'chart_type': 'line_chart',
                'priority': 5
            },
            'MARKET_PROJECTIONS_CHART_PATH': {
                'title': 'Market Growth Projections',
                'context': 'Area chart showing market size growth projections over time with different market segments and growth trends stacked by category',
                'chart_type': 'area_chart',
                'priority': 4
            },
            'PROJECT_IMPLEMENTATION_ROADMAP_PATH': {
                'title': 'Implementation Roadmap',
                'context': 'Flowchart showing step-by-step project implementation roadmap with phases, decision points, milestones, and dependencies clearly mapped',
                'chart_type': 'flowchart',
                'priority': 4
            }
        }
    
    def generate_template_diagrams(self, project_name: str = "Sample Project") -> dict:
        """Generate all diagrams required by the template"""
        logger.info(f"Generating template diagrams for: {project_name}")
        
        generated_diagrams = {}
        
        # Create project-specific output directory
        project_dir = self.output_dir / project_name.replace(' ', '_').lower()
        project_dir.mkdir(parents=True, exist_ok=True)
        
        for placeholder_name, req_data in self.template_requirements.items():
            try:
                # Create chart requirement
                requirement = ChartRequirement(
                    title=req_data['title'],
                    context=req_data['context'],
                    data_type='mixed',  # Templates typically have mixed data
                    suggested_chart=req_data['chart_type'],
                    priority=req_data['priority'],
                    output_path=str(project_dir / f"{placeholder_name.lower().replace('_path', '.png')}")
                )
                
                # Generate the diagram
                diagram_path = self.chart_types[req_data['chart_type']](requirement)
                
                generated_diagrams[placeholder_name] = {
                    'path': diagram_path,
                    'title': req_data['title'],
                    'chart_type': req_data['chart_type'],
                    'status': 'success'
                }
                
                logger.info(f"✅ Generated: {req_data['title']}")
                
            except Exception as e:
                logger.error(f"❌ Failed to generate {req_data['title']}: {e}")
                generated_diagrams[placeholder_name] = {
                    'path': None,
                    'title': req_data['title'],
                    'chart_type': req_data['chart_type'],
                    'status': 'failed',
                    'error': str(e)
                }
        
        # Create template mapping file
        mapping_file = project_dir / 'template_mapping.json'
        with open(mapping_file, 'w') as f:
            json.dump(generated_diagrams, f, indent=2)
        
        logger.info(f"Template diagram generation complete. Mapping saved to: {mapping_file}")
        
        return generated_diagrams
    
    def generate_template_with_replacements(self, template_path: str, project_name: str, output_path: str = None):
        """Generate diagrams and create template with actual paths"""
        
        # Generate all required diagrams
        diagrams = self.generate_template_diagrams(project_name)
        
        # Read template file
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Replace placeholders with actual paths
        for placeholder_name, diagram_info in diagrams.items():
            if diagram_info['status'] == 'success' and diagram_info['path']:
                # Convert to relative path for the template
                relative_path = os.path.relpath(diagram_info['path'], start=os.path.dirname(template_path))
                template_content = template_content.replace(f"{{{placeholder_name}}}", relative_path)
            else:
                # Keep placeholder if generation failed
                logger.warning(f"Keeping placeholder {placeholder_name} - generation failed")
        
        # Save updated template
        if output_path is None:
            output_path = f"{project_name.replace(' ', '_').lower()}_analysis_report.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        logger.info(f"Generated complete analysis report: {output_path}")
        
        return {
            'template_path': output_path,
            'diagrams': diagrams,
            'success_count': sum(1 for d in diagrams.values() if d['status'] == 'success'),
            'total_count': len(diagrams)
        }
    
    def list_template_requirements(self):
        """List all template diagram requirements"""
        logger.info("Template Diagram Requirements:")
        logger.info("=" * 50)
        
        for i, (placeholder, req) in enumerate(self.template_requirements.items(), 1):
            logger.info(f"{i:2d}. {req['title']}")
            logger.info(f"    Placeholder: {placeholder}")
            logger.info(f"    Chart Type: {req['chart_type']}")
            logger.info(f"    Priority: {req['priority']}/5")
            logger.info(f"    Context: {req['context'][:100]}...")
            logger.info("")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Template-Specific Diagram Generator')
    parser.add_argument('--project-name', default='Sample PMEGP Project',
                       help='Name of the project for diagram generation')
    parser.add_argument('--template-path', 
                       default='../../../scripts/data/templates/unified_project_analysis_template.md',
                       help='Path to the analysis template')
    parser.add_argument('--output-path', 
                       help='Output path for the complete analysis report')
    parser.add_argument('--list-requirements', action='store_true',
                       help='List all template diagram requirements')
    parser.add_argument('--generate-only', 
                       choices=list(TemplateSpecificDiagramGenerator({}).template_requirements.keys()),
                       help='Generate only specific diagram')
    parser.add_argument('--config', default='../../../config.yml',
                       help='Configuration file path')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = TemplateSpecificDiagramGenerator(args.config)
    
    if args.list_requirements:
        generator.list_template_requirements()
        return
    
    if args.generate_only:
        # Generate single diagram
        req_data = generator.template_requirements[args.generate_only]
        requirement = ChartRequirement(
            title=req_data['title'],
            context=req_data['context'],
            data_type='mixed',
            suggested_chart=req_data['chart_type'],
            priority=req_data['priority'],
            output_path=''
        )
        
        diagram_path = generator.chart_types[req_data['chart_type']](requirement)
        logger.info(f"Generated single diagram: {diagram_path}")
        return
    
    # Generate complete template with diagrams
    if os.path.exists(args.template_path):
        results = generator.generate_template_with_replacements(
            args.template_path, 
            args.project_name, 
            args.output_path
        )
        
        logger.info("=" * 50)
        logger.info("GENERATION SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Project Name: {args.project_name}")
        logger.info(f"Template Path: {args.template_path}")
        logger.info(f"Output Report: {results['template_path']}")
        logger.info(f"Success Rate: {results['success_count']}/{results['total_count']} diagrams")
        logger.info("=" * 50)
        
    else:
        logger.error(f"Template file not found: {args.template_path}")
        
        # Just generate diagrams without template
        diagrams = generator.generate_template_diagrams(args.project_name)
        logger.info(f"Generated {len(diagrams)} template diagrams")

if __name__ == "__main__":
    main()
