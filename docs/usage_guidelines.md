# PMEGP Analysis Framework - Usage Guidelines

## 🚀 Quick Start Guide

### 1. Initial Setup
```bash
# Clone or download the project
git clone <repository-url>
cd pmegpeportal-programme

# Run setup script
python scripts/setup_project.py

# Install dependencies (if not done during setup)
pip install -r requirements.txt
```

### 2. Data Preparation
```bash
# Ensure your CSV file is in the correct location
# File should be at: data/source/projects_output_clean.csv

# Download project PDFs (start with a small batch)
python scripts/automation/pdf_downloader.py --limit 10

# Check download status
python scripts/automation/pdf_downloader.py --status
```

### 3. Choose Your Analysis Solution
Navigate to `data/solutions/` and select the analysis approach that matches your needs:

- **Industry Analysis**: Sector-wise trends and patterns
- **Investment Range**: Financial bracket analysis
- **Geographic Distribution**: Regional project mapping  
- **Feasibility Assessment**: Project viability evaluation
- **Market Trends**: Industry trend analysis

---

## 🎯 Solution-Specific Workflows

### Industry Analysis Workflow
```bash
# 1. Navigate to solution directory
cd data/solutions/industry-analysis/

# 2. Process raw data for industry analysis
python ../../../scripts/analysis/industry_analyzer.py

# 3. Generate visualizations
python ../../../scripts/visualization/chart_generator.py --solution industry-analysis

# 4. Create report
python ../../../scripts/analysis/report_generator.py --template industry --solution industry-analysis
```

### Investment Range Analysis Workflow
```bash
# 1. Navigate to solution directory
cd data/solutions/investment-range-analysis/

# 2. Analyze investment patterns
python ../../../scripts/analysis/investment_analyzer.py

# 3. Generate financial charts
python ../../../scripts/visualization/chart_generator.py --solution investment-range-analysis --type financial

# 4. Create investment report
python ../../../scripts/analysis/report_generator.py --template investment --solution investment-range-analysis
```

---

## 📊 Working with Data

### CSV Data Structure
The main dataset (`projects_output_clean.csv`) contains:
- **Serial Number**: Project identifier
- **Project Name**: Business/product name
- **Category/Company**: Industry classification
- **Amount/Value**: Investment amount (INR)
- **PDF Link**: Direct link to project profile
- **PDF Filename**: Document filename

### Adding New Solutions
1. Create solution directory:
```bash
mkdir -p data/solutions/your-solution-name/{processed-reports,insights,visualizations}
```

2. Create solution README:
```bash
cp templates/solution_readme_template.md data/solutions/your-solution-name/README.md
```

3. Develop analysis scripts:
```bash
# Create analysis script
touch scripts/analysis/your_solution_analyzer.py

# Create visualization script  
touch scripts/visualization/your_solution_visualizer.py
```

---

## 🛠️ Development Guidelines

### Code Organization
```
scripts/
├── automation/          # Data collection & processing
│   ├── pdf_downloader.py    # Download project PDFs
│   ├── pdf_extractor.py     # Extract text from PDFs
│   └── data_cleaner.py      # Clean and preprocess data
│
├── analysis/            # Core analysis engines
│   ├── industry_analyzer.py    # Industry analysis
│   ├── investment_analyzer.py  # Investment analysis
│   └── trend_analyzer.py       # Trend analysis
│
└── visualization/       # Chart and diagram generation
    ├── chart_generator.py      # Statistical charts
    ├── map_generator.py        # Geographic visualizations
    └── diagram_builder.py      # Flowcharts & diagrams
```

### Configuration Management
All configurations are stored in `config/analysis_config.yml`:
```yaml
# Example configuration
data_source:
  csv_file: "data/source/projects_output_clean.csv"
  pdf_download_dir: "data/source/pdfs/"

analysis_settings:
  investment_brackets:
    micro: [0, 500000]
    small: [500001, 2500000]
    medium: [2500001, 10000000]
```

### Template Usage
Templates are available in the `templates/` directory:
- `analysis_report_template.md`: Standard report format
- `visualization_templates/`: Chart and diagram templates
- `presentation_templates/`: Presentation formats

---

## 📈 Analysis Best Practices

### 1. Data Quality Checks
Always validate your data before analysis:
```python
import pandas as pd

# Load and inspect data
df = pd.read_csv('data/source/projects_output_clean.csv')
print(df.info())
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Validate investment amounts
print(f"Investment range: ₹{df['Amount/Value'].min():,} - ₹{df['Amount/Value'].max():,}")
```

### 2. Reproducible Analysis
- Use configuration files for parameters
- Document all analysis steps
- Save intermediate results
- Version control your scripts

### 3. Visualization Standards
- Use consistent color schemes
- Include proper legends and labels
- Export in multiple formats (PNG, SVG, HTML)
- Create both static and interactive versions

### 4. Report Generation
Follow the standard report template structure:
1. Executive Summary
2. Data Overview  
3. Methodology
4. Detailed Findings
5. Recommendations
6. Limitations & Future Work

---

## 🔧 Troubleshooting

### Common Issues

**Problem**: PDF download fails
```bash
# Solution: Check internet connection and retry with smaller batch
python scripts/automation/pdf_downloader.py --limit 5 --retry 3
```

**Problem**: Analysis script crashes
```bash
# Solution: Check data quality and configuration
python scripts/automation/data_cleaner.py --validate
```

**Problem**: Visualization not generating
```bash
# Solution: Check matplotlib backend and dependencies
python -c "import matplotlib; print(matplotlib.get_backend())"
```

### Log Files
Check log files for detailed error information:
```bash
# View recent logs
tail -f logs/analysis.log
tail -f logs/pdf_download.log
```

### Getting Help
1. Check documentation in `docs/` directory
2. Review solution-specific READMEs
3. Examine configuration files in `config/`
4. Run setup script again: `python scripts/setup_project.py`

---

## 📚 Advanced Usage

### Batch Processing
```bash
# Process multiple solutions in sequence
for solution in industry-analysis investment-range-analysis geographic-distribution; do
    python scripts/analysis/batch_processor.py --solution $solution
done
```

### Custom Analysis
```python
# Example custom analysis
import pandas as pd
import yaml

# Load configuration
with open('config/analysis_config.yml', 'r') as f:
    config = yaml.safe_load(f)

# Load data
df = pd.read_csv(config['data_source']['csv_file'])

# Your custom analysis here
result = df.groupby('Category/Company')['Amount/Value'].agg(['count', 'mean', 'sum'])

# Save results
result.to_csv('data/solutions/custom-analysis/processed-reports/custom_results.csv')
```

### Integration with Jupyter
```bash
# Start Jupyter for interactive analysis
jupyter notebook

# Navigate to data/solutions/your-solution/ 
# Create new notebook for exploratory analysis
```

---

*For additional support, refer to the project documentation or create an issue in the repository.*
