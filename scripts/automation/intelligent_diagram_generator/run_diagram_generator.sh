#!/bin/bash

# Intelligent Diagram Generator Runner Script
# Provides easy access to diagram generation functionality

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    print_header "🔧 Checking Prerequisites"
    
    # Check Python version
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        return 1
    fi
    
    # Check OpenAI API key
    if [ -z "$OPENAI_API_KEY" ]; then
        print_warning "OPENAI_API_KEY environment variable not set"
        echo "Please set it with: export OPENAI_API_KEY='your-api-key'"
        echo "Or create a .env file with your API key"
    fi
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_warning "Virtual environment not found"
        echo "Consider creating one with: python3 -m venv venv"
    fi
    
    print_status "Prerequisites check complete"
    return 0
}

# Function to install dependencies
install_dependencies() {
    print_header "📦 Installing Dependencies"
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_status "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        return 1
    fi
}

# Function to run examples
run_examples() {
    print_header "🎯 Running Examples"
    python3 example_usage.py
}

# Function to generate template diagrams
generate_template_diagrams() {
    local project_name=${1:-"Sample Project"}
    print_header "📊 Generating Template Diagrams for: $project_name"
    
    python3 template_diagram_generator.py --project-name "$project_name"
}

# Function to generate from research file
generate_from_research() {
    local research_file=${1:-"deep_research.md"}
    print_header "📄 Generating Diagrams from Research File: $research_file"
    
    if [ ! -f "$research_file" ]; then
        print_warning "Research file not found: $research_file"
        print_status "Creating sample research file..."
        echo "# Sample Research Document" > "$research_file"
        echo "This is a sample research document for diagram generation." >> "$research_file"
    fi
    
    python3 intelligent_diagram_generator.py --research-file "$research_file"
}

# Function to list chart types
list_chart_types() {
    print_header "📈 Available Chart Types"
    python3 intelligent_diagram_generator.py --list-types
}

# Function to generate specific chart type
generate_specific_chart() {
    local chart_type=$1
    if [ -z "$chart_type" ]; then
        print_error "Chart type not specified"
        list_chart_types
        return 1
    fi
    
    print_header "🎨 Generating Specific Chart: $chart_type"
    python3 intelligent_diagram_generator.py --chart-type "$chart_type"
}

# Function to create complete report
create_complete_report() {
    local project_name=${1:-"Complete Analysis Project"}
    local template_path="../../../scripts/data/templates/unified_project_analysis_template.md"
    
    print_header "📋 Creating Complete Analysis Report"
    
    if [ ! -f "$template_path" ]; then
        print_error "Template not found: $template_path"
        return 1
    fi
    
    python3 template_diagram_generator.py \
        --project-name "$project_name" \
        --template-path "$template_path"
}

# Function to show usage
show_usage() {
    print_header "🚀 Intelligent Diagram Generator"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  check          Check prerequisites"
    echo "  install        Install dependencies"
    echo "  examples       Run example demonstrations"
    echo "  template       Generate all template diagrams"
    echo "  research       Generate from research document"
    echo "  list-types     List available chart types"
    echo "  chart TYPE     Generate specific chart type"
    echo "  report         Create complete analysis report"
    echo "  help           Show this help message"
    echo ""
    echo "Options:"
    echo "  --project-name NAME    Set project name (default: Sample Project)"
    echo "  --research-file FILE   Set research file (default: deep_research.md)"
    echo ""
    echo "Examples:"
    echo "  $0 template --project-name 'My Project'"
    echo "  $0 research --research-file my_research.md"
    echo "  $0 chart flowchart"
    echo "  $0 report --project-name 'Analysis Report'"
    echo ""
    echo "Environment Setup:"
    echo "  export OPENAI_API_KEY='your-openai-api-key'"
    echo "  python3 -m venv venv && source venv/bin/activate"
    echo "  $0 install"
}

# Main execution logic
main() {
    # Change to script directory
    cd "$(dirname "$0")" || exit 1
    
    # Parse command line arguments
    COMMAND=${1:-help}
    shift
    
    # Parse options
    PROJECT_NAME="Sample Project"
    RESEARCH_FILE="deep_research.md"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --project-name)
                PROJECT_NAME="$2"
                shift 2
                ;;
            --research-file)
                RESEARCH_FILE="$2"
                shift 2
                ;;
            *)
                break
                ;;
        esac
    done
    
    # Execute commands
    case $COMMAND in
        check)
            check_prerequisites
            ;;
        install)
            check_prerequisites
            install_dependencies
            ;;
        examples)
            run_examples
            ;;
        template)
            generate_template_diagrams "$PROJECT_NAME"
            ;;
        research)
            generate_from_research "$RESEARCH_FILE"
            ;;
        list-types)
            list_chart_types
            ;;
        chart)
            CHART_TYPE=$1
            generate_specific_chart "$CHART_TYPE"
            ;;
        report)
            create_complete_report "$PROJECT_NAME"
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            print_error "Unknown command: $COMMAND"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
