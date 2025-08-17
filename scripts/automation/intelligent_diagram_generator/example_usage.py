#!/usr/bin/env python3
"""
Example Usage Script for Intelligent Diagram Generator
Demonstrates how to use the system with practical examples
"""

import os
import sys
from pathlib import Path

# Add the automation directory to Python path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def setup_environment():
    """Setup environment and check prerequisites"""
    print("🔧 Setting up environment...")
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   Please set it with: export OPENAI_API_KEY='your-api-key'")
        return False
    
    # Check if required directories exist
    directories = ['logs', 'outputs', 'outputs/diagrams']
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Environment setup complete")
    return True

def example_1_generate_all_template_diagrams():
    """Example 1: Generate all diagrams for the unified template"""
    print("\n📊 Example 1: Generating all template diagrams...")
    
    try:
        from template_diagram_generator import TemplateSpecificDiagramGenerator
        
        # Initialize generator
        generator = TemplateSpecificDiagramGenerator()
        
        # Generate all template diagrams
        project_name = "Aloe Vera Gel Manufacturing"
        diagrams = generator.generate_template_diagrams(project_name)
        
        print(f"✅ Generated {len(diagrams)} diagrams for {project_name}")
        
        # Print summary
        success_count = sum(1 for d in diagrams.values() if d['status'] == 'success')
        print(f"   Success rate: {success_count}/{len(diagrams)}")
        
        return diagrams
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure to install required packages: pip install -r requirements.txt")
        return {}
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return {}

def example_2_generate_from_research_document():
    """Example 2: Generate diagrams from research document analysis"""
    print("\n📄 Example 2: Generating diagrams from research document...")
    
    try:
        from intelligent_diagram_generator import IntelligentDiagramGenerator
        
        # Initialize generator
        generator = IntelligentDiagramGenerator()
        
        # Check if research file exists
        research_file = "deep_research.md"
        if not Path(research_file).exists():
            print(f"⚠️  Research file not found: {research_file}")
            print("   Using sample requirements instead...")
            return example_3_single_chart_generation()
        
        # Generate diagrams from research
        results = generator.generate_all_diagrams(research_file)
        
        print(f"✅ Analysis complete: {results['status']}")
        if results['status'] == 'success':
            print(f"   Generated {results['generated_diagrams']} diagrams")
        
        return results
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return {}

def example_3_single_chart_generation():
    """Example 3: Generate specific chart types"""
    print("\n📈 Example 3: Generating specific chart types...")
    
    try:
        from intelligent_diagram_generator import IntelligentDiagramGenerator, ChartRequirement
        
        # Initialize generator
        generator = IntelligentDiagramGenerator()
        
        # Define sample requirements for different chart types
        sample_requirements = [
            {
                'title': 'Investment Distribution Analysis',
                'context': 'Show distribution of investments across different project categories with percentages',
                'chart_type': 'pie_chart'
            },
            {
                'title': 'Revenue Growth Projection',
                'context': 'Display projected revenue growth over 5 years with trend analysis',
                'chart_type': 'line_chart'
            },
            {
                'title': 'Regional Performance Comparison',
                'context': 'Compare performance metrics across different regions using bars',
                'chart_type': 'bar_chart'
            },
            {
                'title': 'Risk-Return Portfolio Analysis',
                'context': 'Position different investment opportunities on risk vs return matrix',
                'chart_type': 'quadrant_chart'
            }
        ]
        
        generated_charts = []
        
        for req_data in sample_requirements:
            # Create chart requirement
            requirement = ChartRequirement(
                title=req_data['title'],
                context=req_data['context'],
                data_type='numerical',
                suggested_chart=req_data['chart_type'],
                priority=4,
                output_path=''
            )
            
            # Generate the chart
            chart_path = generator.chart_types[req_data['chart_type']](requirement)
            
            generated_charts.append({
                'title': req_data['title'],
                'type': req_data['chart_type'],
                'path': chart_path
            })
            
            print(f"   ✅ {req_data['title']} -> {req_data['chart_type']}")
        
        print(f"✅ Generated {len(generated_charts)} specific charts")
        return generated_charts
        
    except Exception as e:
        print(f"❌ Chart generation error: {e}")
        return []

def example_4_complete_analysis_report():
    """Example 4: Generate complete analysis report with diagrams"""
    print("\n📋 Example 4: Creating complete analysis report...")
    
    try:
        from template_diagram_generator import TemplateSpecificDiagramGenerator
        
        # Initialize generator
        generator = TemplateSpecificDiagramGenerator()
        
        # Define project details
        project_name = "Smart Manufacturing Unit"
        template_path = "../../../scripts/data/templates/unified_project_analysis_template.md"
        
        # Check if template exists
        if not Path(template_path).exists():
            print(f"⚠️  Template not found: {template_path}")
            print("   Generating diagrams only...")
            return generator.generate_template_diagrams(project_name)
        
        # Generate complete report
        results = generator.generate_template_with_replacements(
            template_path=template_path,
            project_name=project_name,
            output_path=f"{project_name.replace(' ', '_').lower()}_complete_report.md"
        )
        
        print(f"✅ Complete report generated: {results['template_path']}")
        print(f"   Diagrams: {results['success_count']}/{results['total_count']}")
        
        return results
        
    except Exception as e:
        print(f"❌ Report generation error: {e}")
        return {}

def list_available_chart_types():
    """List all available chart types"""
    print("\n📊 Available Chart Types:")
    print("=" * 40)
    
    try:
        from intelligent_diagram_generator import IntelligentDiagramGenerator
        
        generator = IntelligentDiagramGenerator()
        
        for i, chart_type in enumerate(generator.chart_types.keys(), 1):
            print(f"{i:2d}. {chart_type.replace('_', ' ').title()}")
        
        print(f"\nTotal: {len(generator.chart_types)} chart types available")
        
    except Exception as e:
        print(f"❌ Error listing chart types: {e}")

def main():
    """Main execution function with examples"""
    print("🚀 Intelligent Diagram Generator - Example Usage")
    print("=" * 50)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Environment setup failed. Please configure properly.")
        return
    
    # List available chart types
    list_available_chart_types()
    
    # Run examples
    print("\n🎯 Running Examples:")
    print("=" * 30)
    
    # Example 1: Template diagrams
    example_1_results = example_1_generate_all_template_diagrams()
    
    # Example 2: Research document analysis
    example_2_results = example_2_generate_from_research_document()
    
    # Example 3: Specific chart generation
    example_3_results = example_3_single_chart_generation()
    
    # Example 4: Complete report
    example_4_results = example_4_complete_analysis_report()
    
    # Summary
    print("\n📊 EXECUTION SUMMARY")
    print("=" * 30)
    print(f"Example 1 (Template): {len(example_1_results)} diagrams")
    print(f"Example 2 (Research): {len(example_2_results)} results")  
    print(f"Example 3 (Specific): {len(example_3_results)} charts")
    print(f"Example 4 (Complete): {'Success' if example_4_results else 'Failed'}")
    
    # Usage tips
    print("\n💡 Usage Tips:")
    print("- Set OPENAI_API_KEY environment variable")
    print("- Install requirements: pip install -r requirements.txt")
    print("- Check outputs/ directory for generated diagrams")
    print("- Modify config.yml for custom settings")
    
    print("\n🎉 Example execution complete!")

if __name__ == "__main__":
    main()
