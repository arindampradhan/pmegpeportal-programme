# PMEGP Analysis Framework - Developer Guide

> Technical documentation and software tools for PMEGP project analysis

## 🚀 Getting Started

### Quick Start
1. **Clone Repository**: `git clone <repo-url>`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Configure Analysis**: Edit `config.yml` 
4. **Download Data**: `python scripts/automation/pdf_downloader.py`
5. **Generate Reports**: Choose analysis type and run corresponding script

### Analysis Workflow
```
Raw Data → Processing → Analysis → Report Generation → docs/ folder
```

## 🔧 Tech Stack

### Core Technologies
- **Python**: Data processing (pandas, numpy, scipy)
- **Visualization**: matplotlib, plotly, seaborn  
- **PDF Processing**: PyPDF2, pdfplumber
- **Automation**: requests, concurrent.futures
- **Configuration**: PyYAML

### Output Formats
- **Reports**: Markdown with embedded visualizations
- **Diagrams**: SVG format (Excalidraw/Tldraw compatible)
- **Data**: CSV, JSON exports
- **Charts**: PNG, SVG, HTML interactive

## 📁 Scripts Directory Structure

### `automation/` - Data Collection & Processing
| Script | Purpose | Usage |
|--------|---------|-------|
| [`pdf_downloader.py`](automation/pdf_downloader.py) | Download PMEGP project PDFs | `python automation/pdf_downloader.py` |
| `pdf_extractor.py` | Extract text and data from PDFs | `python automation/pdf_extractor.py` |
| `data_cleaner.py` | Clean and preprocess CSV data | `python automation/data_cleaner.py` |

### `analysis/` - Analysis Engines
| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `industry_analyzer.py` | Sector-wise analysis | CSV + PDFs | Industry insights |
| `investment_analyzer.py` | Financial pattern analysis | Investment data | Financial reports |
| `geographic_analyzer.py` | Regional distribution | Location data | Geographic insights |
| `trend_analyzer.py` | Market trend analysis | Time-series data | Trend reports |

### `visualization/` - Chart & Diagram Generation
| Script | Purpose | Output Format |
|--------|---------|---------------|
| `chart_generator.py` | Statistical charts | PNG, SVG |
| `map_generator.py` | Geographic visualizations | HTML, SVG |
| `diagram_builder.py` | Process flowcharts | SVG (Excalidraw compatible) |

## ⚙️ Configuration

### Main Configuration (`config.yml`)
```yaml
# Data Source
data_source:
  csv_file: "data/source/projects_output_clean.csv"
  pdf_base_url: "https://www.kviconline.gov.in/pmegp/pmegpweb/docs/commonprojectprofile/"
  pdf_download_dir: "data/source/pdfs/"

# Investment Brackets (in INR)
investment_brackets:
  micro: [0, 500000]        # Up to 5L
  small: [500001, 2500000]  # 5L to 25L  
  medium: [2500001, 10000000] # 25L to 1Cr
  large: [10000001, 50000000] # Above 1Cr

# Processing Settings
processing:
  max_concurrent_downloads: 5
  retry_attempts: 3
  timeout_seconds: 30
```

## 🛠️ Development Setup

### Prerequisites
```bash
# Python 3.8+
python --version

# Required packages
pip install pandas numpy matplotlib plotly seaborn
pip install requests PyPDF2 pdfplumber pyyaml
pip install jupyter folium openpyxl
```

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pandas, numpy, matplotlib; print('Setup complete!')"
```

## 📊 Creating New Analysis Scripts

### 1. Analysis Script Template
```python
#!/usr/bin/env python3
"""
PMEGP Analysis Script Template
"""
import pandas as pd
import yaml
from pathlib import Path

class PMEGPAnalyzer:
    def __init__(self, config_path='config.yml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def load_data(self):
        """Load and return project data"""
        return pd.read_csv(self.config['data_source']['csv_file'])
    
    def analyze(self):
        """Main analysis logic"""
        df = self.load_data()
        # Your analysis here
        return results
    
    def save_results(self, results, output_dir):
        """Save analysis results"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        # Save your results

if __name__ == "__main__":
    analyzer = PMEGPAnalyzer()
    results = analyzer.analyze()
    analyzer.save_results(results, "docs/my-analysis/")
```

### 2. Visualization Script Template
```python
import matplotlib.pyplot as plt
import seaborn as sns

def create_analysis_chart(data, output_path):
    """Create and save analysis chart"""
    plt.figure(figsize=(12, 8))
    # Your visualization code
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_svg_diagram(data, output_path):
    """Create SVG diagram compatible with Excalidraw"""
    # SVG generation code
    with open(output_path, 'w') as f:
        f.write(svg_content)
```

## 🔄 Automation Workflows

### PDF Download Pipeline
```bash
# Download all PDFs (production)
python automation/pdf_downloader.py

# Test with limited downloads
python automation/pdf_downloader.py --limit 10

# Check download status
python automation/pdf_downloader.py --status
```

### Analysis Pipeline
```bash
# Run complete industry analysis
python analysis/industry_analyzer.py

# Generate visualizations
python visualization/chart_generator.py --solution industry-analysis

# Create comprehensive report
python analysis/report_generator.py --template industry --solution industry-analysis
```

## 🧪 Testing & Quality

### Running Tests
```bash
# Data validation tests
python -m pytest tests/test_data_quality.py

# Analysis logic tests  
python -m pytest tests/test_analysis_engines.py

# Integration tests
python -m pytest tests/test_full_pipeline.py
```

### Code Quality
```bash
# Code formatting
black scripts/

# Linting
flake8 scripts/

# Type checking
mypy scripts/
```

## 📝 Adding New Analysis Types

### Step 1: Create Analysis Directory
```bash
mkdir -p docs/your-analysis-name
mkdir -p data/solutions/your-analysis-name/{processed-reports,insights,visualizations}
```

### Step 2: Develop Analysis Script
```bash
# Use template from data/templates/
cp data/templates/analyzer_template.py scripts/analysis/your_analyzer.py

# Implement your analysis logic
# Test with sample data
# Generate outputs in docs/your-analysis-name/
```

### Step 3: Create Visualization
```bash
# Generate charts
python scripts/visualization/chart_generator.py --solution your-analysis-name

# Create SVG diagram
python scripts/visualization/diagram_builder.py --solution your-analysis-name
```

### Step 4: Update Documentation
- Add entry to main README.md table
- Link to your analysis.md and diagrams.svg
- Update this developer README if needed

## 🐛 Troubleshooting

### Common Issues

**PDF Download Fails**
```bash
# Check internet connection and retry
python automation/pdf_downloader.py --retry 5
```

**Analysis Script Crashes**
```bash
# Validate data first
python automation/data_cleaner.py --validate

# Check logs
tail -f logs/analysis.log
```

**Visualization Not Generating**
```bash
# Check matplotlib backend
python -c "import matplotlib; print(matplotlib.get_backend())"

# Install GUI backend if needed (for development)
pip install tkinter
```

### Debug Mode
```bash
# Run with debug logging
export DEBUG=1
python scripts/analysis/your_analyzer.py
```

## 🤝 Contributing to Scripts

### Code Style Guidelines
- Follow PEP 8 for Python code
- Use type hints where possible
- Include docstrings for all functions
- Add logging for debugging

### Pull Request Process
1. Create feature branch: `git checkout -b feature/new-analysis`
2. Develop and test your script
3. Update documentation
4. Submit PR with clear description

### Script Naming Convention
- `*_analyzer.py` - Analysis engines
- `*_generator.py` - Output generators  
- `*_processor.py` - Data processors
- `*_downloader.py` - Data collectors

---

**For analysis report creation, see the main [README](../README.md)**  
**For project structure details, see [SIMPLIFIED_STRUCTURE.md](../SIMPLIFIED_STRUCTURE.md)**
