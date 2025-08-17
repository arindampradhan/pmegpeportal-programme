# Intelligent Diagram Generator

An AI-powered tool that automatically analyzes business requirements and generates the most appropriate charts and diagrams using OpenAI APIs and advanced visualization libraries.

## 🚀 Features

### Smart Chart Selection
- Automatically analyzes context to select optimal visualization type
- Uses OpenAI GPT-4 for intelligent decision making
- Supports 15+ different chart and diagram types

### Comprehensive Chart Types
- **Process Visualizations**: Flowcharts, Network diagrams
- **Timeline Charts**: Gantt charts, Area charts, Line charts
- **Comparative Charts**: Bar charts, Bubble charts, Quadrant charts
- **Distribution Charts**: Pie charts, Heatmaps, Scatter plots
- **Hierarchical Charts**: Pyramid charts, Organization charts, Mind maps
- **Analytical Dashboards**: Multi-chart comprehensive views

### AI-Powered Analysis
- Intelligent context understanding
- Automatic data structure recommendation
- Best practice visualization suggestions
- Quality-focused chart generation

## 📋 Requirements

### System Requirements
- Python 3.8+
- OpenAI API key
- Minimum 4GB RAM
- 2GB free disk space

### Dependencies
Install required packages:
```bash
pip install -r ../requirements.txt
```

### Key Libraries
- `openai>=1.3.0` - AI-powered analysis
- `matplotlib>=3.5.0` - Core plotting
- `plotly>=5.0.0` - Interactive charts
- `networkx>=2.8` - Network diagrams
- `seaborn>=0.11.0` - Statistical plots
- `pandas>=1.3.0` - Data manipulation
- `Pillow>=9.0.0` - Image processing

## ⚙️ Configuration

### Environment Setup
1. Set OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. Configure in `config.yml`:
```yaml
openai:
  api_key: "${OPENAI_API_KEY}"
  model: "gpt-4"
  temperature: 0.3

output:
  diagrams_dir: "outputs/diagrams"
  
input:
  research_file: "deep_research.md"
```

### Directory Structure
```
automation/
├── intelligent_diagram_generator.py
├── README_diagram_generator.md
└── config.yml

outputs/
├── diagrams/
│   ├── flowchart/
│   ├── gantt/
│   ├── bar_chart/
│   ├── line_chart/
│   ├── pie_chart/
│   ├── heatmap/
│   └── dashboard/
└── generation_summary.json
```

## 🎯 Usage

### Basic Usage
Generate all diagrams from research document:
```bash
python intelligent_diagram_generator.py --research-file deep_research.md
```

### Advanced Options

#### Generate Specific Chart Type
```bash
python intelligent_diagram_generator.py --chart-type flowchart
python intelligent_diagram_generator.py --chart-type gantt
python intelligent_diagram_generator.py --chart-type dashboard
```

#### List Available Chart Types
```bash
python intelligent_diagram_generator.py --list-types
```

#### Custom Configuration
```bash
python intelligent_diagram_generator.py --config custom_config.yml --research-file custom_research.md
```

### Command Line Arguments
- `--research-file`: Input research document (default: deep_research.md)
- `--config`: Configuration file (default: config.yml)
- `--chart-type`: Generate specific chart type only
- `--list-types`: Show available chart types

## 🧠 How It Works

### 1. Document Analysis
```python
# AI analyzes research document
requirements = analyze_research_file("deep_research.md")
# Extracts visualization requirements with context
```

### 2. Chart Type Selection
```python
# AI selects optimal chart type
chart_type = select_optimal_chart_type(requirement)
# Returns best visualization method for context
```

### 3. Data Generation & Visualization
```python
# Generates appropriate sample data
data = generate_sample_data(chart_type, context)
# Creates professional visualization
chart_path = generate_diagram(requirement)
```

### 4. Output Generation
- High-quality PNG images (300 DPI)
- Organized in type-specific folders
- JSON summary with metadata
- Professional styling and branding

## 📊 Chart Type Mappings

### Context-Based Selection
The AI automatically maps business contexts to optimal chart types:

| Business Context | Recommended Charts |
|------------------|-------------------|
| Financial Trends | Line chart, Area chart, Bar chart |
| Process Flows | Flowchart, Network diagram |
| Project Timelines | Gantt chart, Timeline |
| Organizational Structure | Organization chart, Hierarchy |
| Market Analysis | Quadrant chart, Bubble chart |
| Geographic Data | Heatmap, Bubble map |
| Risk Assessment | Risk matrix, Quadrant analysis |
| Performance Metrics | Dashboard, KPI charts |

### Sample Outputs

#### Flowchart Example
- Process documentation
- Decision trees  
- Workflow visualization
- System architecture

#### Gantt Chart Example
- Project timelines
- Resource allocation
- Milestone tracking
- Dependencies mapping

#### Dashboard Example
- KPI monitoring
- Multi-metric overview
- Performance tracking
- Executive summaries

## 🎨 Customization

### Visual Styling
Modify appearance in `config.yml`:
```yaml
visualization:
  color_palette: ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
  figure_dpi: 300
  chart_sizes:
    small: [8, 6]
    medium: [12, 8]
    large: [16, 12]
```

### Chart Templates
Add custom chart types by extending the `chart_types` dictionary:
```python
def generate_custom_chart(self, requirement):
    # Custom chart implementation
    pass

self.chart_types['custom_chart'] = self.generate_custom_chart
```

### AI Prompt Customization
Modify the chart selection logic:
```python
self.chart_selection_prompt = """
Your custom prompt for AI chart selection...
"""
```

## 📝 Input Document Format

### Research Document Structure
The AI analyzes markdown documents with these sections:

```markdown
# Main Title

## Section 1: Financial Data
Numerical data, trends, comparisons...

## Section 2: Process Flow  
Step-by-step processes, workflows...

## Section 3: Timeline Information
Project phases, schedules, milestones...

## Section 4: Hierarchical Data
Organizational structures, categories...
```

### Required Elements
- **Clear section headers** for context identification
- **Data descriptions** for appropriate visualization
- **Business context** for chart type selection
- **Quantitative information** for data-driven charts

## 🔧 Troubleshooting

### Common Issues

#### OpenAI API Errors
```bash
Error: OpenAI API key not found
Solution: Set OPENAI_API_KEY environment variable
```

#### Import Errors  
```bash
Error: No module named 'networkx'
Solution: pip install -r requirements.txt
```

#### Permission Errors
```bash
Error: Permission denied writing to output directory
Solution: Check write permissions for output directory
```

### Debug Mode
Enable detailed logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Optimization

### Batch Processing
Process multiple documents efficiently:
```python
for research_file in research_files:
    generator.generate_all_diagrams(research_file)
```

### Parallel Generation
Use threading for multiple chart generation:
```python
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(generate_diagram, req) for req in requirements]
```

### Caching
Cache AI responses to reduce API calls:
```python
@lru_cache(maxsize=128)
def cached_chart_selection(context_hash):
    return select_optimal_chart_type(context)
```

## 🤝 Integration

### With Analysis Pipeline
```python
from intelligent_diagram_generator import IntelligentDiagramGenerator

generator = IntelligentDiagramGenerator()
results = generator.generate_all_diagrams("analysis_report.md")
```

### With Web Applications
```python
# Flask/Django integration
@app.route('/generate-charts', methods=['POST'])
def generate_charts():
    research_text = request.json['research']
    diagrams = generator.analyze_and_generate(research_text)
    return jsonify(diagrams)
```

### With Jupyter Notebooks
```python
# Display generated charts
from IPython.display import Image, display

for diagram in generated_diagrams:
    display(Image(diagram['path']))
```

## 🔮 Future Enhancements

### Planned Features
- Real-time data integration
- Interactive chart generation
- Web-based configuration interface
- Custom template management
- Batch processing optimization
- Advanced AI model integration

### API Expansion
- REST API for remote generation
- WebSocket for real-time updates
- GraphQL for flexible queries
- Webhook integrations

## 📚 Examples

### Complete Workflow
```bash
# 1. Setup environment
export OPENAI_API_KEY="your-key"

# 2. Install dependencies  
pip install -r requirements.txt

# 3. Configure settings
cp config.yml.example config.yml

# 4. Prepare research document
echo "# Research Data..." > my_research.md

# 5. Generate diagrams
python intelligent_diagram_generator.py --research-file my_research.md

# 6. View results
ls outputs/diagrams/
cat outputs/generation_summary.json
```

## 📞 Support

For issues and feature requests:
1. Check troubleshooting section
2. Review configuration settings
3. Validate input document format
4. Contact development team

## 📄 License

This project is part of the PMEGP Portal Programme analysis system.

---

*This intelligent diagram generator transforms business requirements into professional visualizations using cutting-edge AI technology.*
