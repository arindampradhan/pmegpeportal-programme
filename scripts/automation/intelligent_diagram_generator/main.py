#!/usr/bin/env python3
"""
Main entry point for the Intelligent Diagram Generator
Can be run from project root directory
"""

import os
import sys
from pathlib import Path

# Add package to Python path
package_dir = Path(__file__).parent
sys.path.insert(0, str(package_dir))

# Change to project root directory for correct relative paths
project_root = package_dir / "../../../"
os.chdir(project_root)

def main():
    """Main entry point with corrected paths"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Intelligent Diagram Generator System')
    parser.add_argument('mode', choices=['generate', 'template', 'examples', 'list-types'],
                       help='Operation mode')
    parser.add_argument('--project-name', default='Sample Project',
                       help='Project name for diagram generation')
    parser.add_argument('--research-file', default='deep_research.md',
                       help='Research document to analyze')
    parser.add_argument('--config', default='config.yml',
                       help='Configuration file path')
    parser.add_argument('--chart-type', help='Specific chart type to generate')
    
    args = parser.parse_args()
    
    if args.mode == 'generate':
        from intelligent_diagram_generator import IntelligentDiagramGenerator
        generator = IntelligentDiagramGenerator(args.config)
        
        if args.chart_type:
            # Generate specific chart
            from intelligent_diagram_generator import ChartRequirement
            req = ChartRequirement(
                title=f"Sample {args.chart_type.replace('_', ' ').title()}",
                context="Sample context for demonstration",
                data_type="numerical",
                suggested_chart=args.chart_type,
                priority=5,
                output_path=""
            )
            result = generator.generate_diagram(req)
            print(f"Generated: {result}")
        else:
            # Generate from research file
            results = generator.generate_all_diagrams(args.research_file)
            print(f"Results: {results}")
    
    elif args.mode == 'template':
        from template_diagram_generator import TemplateSpecificDiagramGenerator
        generator = TemplateSpecificDiagramGenerator(args.config)
        
        template_path = "scripts/data/templates/unified_project_analysis_template.md"
        if Path(template_path).exists():
            results = generator.generate_template_with_replacements(
                template_path, args.project_name
            )
            print(f"Generated complete report: {results['template_path']}")
        else:
            # Just generate diagrams
            results = generator.generate_template_diagrams(args.project_name)
            print(f"Generated {len(results)} template diagrams")
    
    elif args.mode == 'examples':
        # Import and run examples
        sys.path.append(str(package_dir))
        from example_usage import main as run_examples
        run_examples()
    
    elif args.mode == 'list-types':
        from intelligent_diagram_generator import IntelligentDiagramGenerator
        generator = IntelligentDiagramGenerator(args.config)
        print("Available chart types:")
        for i, chart_type in enumerate(generator.chart_types.keys(), 1):
            print(f"{i:2d}. {chart_type.replace('_', ' ').title()}")

if __name__ == "__main__":
    main()
