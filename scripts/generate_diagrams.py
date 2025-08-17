#!/usr/bin/env python3
"""
Intelligent Diagram Generator - Project Wrapper
Easy access to the diagram generation system from scripts directory
"""

import sys
import os
from pathlib import Path

# Add the package to Python path
package_path = Path(__file__).parent / "automation/intelligent_diagram_generator"
sys.path.insert(0, str(package_path))

def main():
    """Main wrapper function"""
    print("🚀 Intelligent Diagram Generator System")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        show_usage()
        return
    
    command = sys.argv[1]
    
    try:
        if command == "template":
            # Generate all template diagrams
            project_name = sys.argv[2] if len(sys.argv) > 2 else "Sample Project"
            generate_template_diagrams(project_name)
            
        elif command == "research":
            # Generate from research file
            research_file = sys.argv[2] if len(sys.argv) > 2 else "automation/intelligent_diagram_generator/deep_research.md"
            generate_from_research(research_file)
            
        elif command == "chart":
            # Generate specific chart
            chart_type = sys.argv[2] if len(sys.argv) > 2 else "bar_chart"
            generate_specific_chart(chart_type)
            
        elif command == "list":
            # List available chart types
            list_chart_types()
            
        elif command == "examples":
            # Run examples
            run_examples()
            
        elif command == "help":
            show_usage()
            
        else:
            print(f"❌ Unknown command: {command}")
            show_usage()
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to install requirements: pip install -r requirements.txt")
        print("💡 Set OpenAI API key: export OPENAI_API_KEY='your-key'")
    except Exception as e:
        print(f"❌ Error: {e}")

def generate_template_diagrams(project_name):
    """Generate all template diagrams"""
    from template_diagram_generator import TemplateSpecificDiagramGenerator
    
    print(f"📊 Generating template diagrams for: {project_name}")
    
    generator = TemplateSpecificDiagramGenerator()
    diagrams = generator.generate_template_diagrams(project_name)
    
    success_count = sum(1 for d in diagrams.values() if d['status'] == 'success')
    print(f"✅ Generated {success_count}/{len(diagrams)} diagrams")
    
    # List generated diagrams
    print("\n📋 Generated Diagrams:")
    for placeholder, info in diagrams.items():
        status = "✅" if info['status'] == 'success' else "❌"
        print(f"  {status} {info['title']} ({info['chart_type']})")

def generate_from_research(research_file):
    """Generate diagrams from research document"""
    from intelligent_diagram_generator import IntelligentDiagramGenerator
    
    print(f"📄 Analyzing research file: {research_file}")
    
    if not Path(research_file).exists():
        print(f"⚠️  Research file not found: {research_file}")
        print("   Using default research file...")
        research_file = "automation/intelligent_diagram_generator/deep_research.md"
    
    generator = IntelligentDiagramGenerator()
    results = generator.generate_all_diagrams(research_file)
    
    print(f"✅ Analysis complete: {results.get('status', 'unknown')}")
    if results.get('status') == 'success':
        print(f"   Generated {results.get('generated_diagrams', 0)} diagrams")

def generate_specific_chart(chart_type):
    """Generate a specific chart type"""
    from intelligent_diagram_generator import IntelligentDiagramGenerator, ChartRequirement
    
    print(f"🎨 Generating specific chart: {chart_type}")
    
    generator = IntelligentDiagramGenerator()
    
    if chart_type not in generator.chart_types:
        print(f"❌ Unknown chart type: {chart_type}")
        print("Available types:", ", ".join(generator.chart_types.keys()))
        return
    
    # Create sample requirement
    requirement = ChartRequirement(
        title=f"Sample {chart_type.replace('_', ' ').title()}",
        context="Sample context for demonstration purposes",
        data_type="numerical",
        suggested_chart=chart_type,
        priority=5,
        output_path=""
    )
    
    result = generator.generate_diagram(requirement)
    print(f"✅ Generated: {result}")

def list_chart_types():
    """List all available chart types"""
    from intelligent_diagram_generator import IntelligentDiagramGenerator
    
    print("📈 Available Chart Types:")
    print("-" * 30)
    
    generator = IntelligentDiagramGenerator()
    for i, chart_type in enumerate(generator.chart_types.keys(), 1):
        print(f"{i:2d}. {chart_type.replace('_', ' ').title()}")
    
    print(f"\nTotal: {len(generator.chart_types)} chart types")

def run_examples():
    """Run example demonstrations"""
    print("🎯 Running examples...")
    
    # Change to the package directory to run examples
    original_cwd = os.getcwd()
    os.chdir(package_path)
    
    try:
        from example_usage import main as run_example_main
        run_example_main()
    finally:
        os.chdir(original_cwd)

def show_usage():
    """Show usage information"""
    print("""
Usage: python scripts/generate_diagrams.py [COMMAND] [OPTIONS]

Commands:
  template [PROJECT_NAME]     Generate all template diagrams
  research [FILE_PATH]        Generate diagrams from research document  
  chart [CHART_TYPE]          Generate specific chart type
  list                        List available chart types
  examples                    Run example demonstrations
  help                        Show this help message

Examples:
  python scripts/generate_diagrams.py template "My Project"
  python scripts/generate_diagrams.py research "my_research.md"
  python scripts/generate_diagrams.py chart flowchart
  python scripts/generate_diagrams.py list
  python scripts/generate_diagrams.py examples

Setup:
  1. Set OpenAI API key: export OPENAI_API_KEY='your-key'
  2. Install dependencies: pip install -r scripts/requirements.txt
  3. Run the system: python scripts/generate_diagrams.py [command]

Output Location:
  - Generated diagrams: outputs/diagrams/
  - Analysis reports: project root directory
    """)

if __name__ == "__main__":
    main()
