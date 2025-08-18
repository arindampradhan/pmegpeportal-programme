#!/usr/bin/env python3
"""
Enterprise-Grade Deep Research Generator with Mermaid Diagrams

- Scans PDFs in scripts/data/source/pdfs/
- Creates per-PDF folders under docs/<PDF_STEM>/
- Generates Deep-Research.md for each PDF using GPT-4o with enterprise-grade business analysis
- Uses scripts/data/templates/unified_project_analysis_template.md as the response structure
- Creates an assets/ directory with a placeholder diagrams.svg
- Automatically generates appropriate Mermaid diagrams for each visualization placeholder:
  * Flowcharts for manufacturing processes and project roadmaps
  * Gantt charts for implementation timelines
  * Pie charts for market share and cost breakdown
  * Bar charts for financial projections and regional performance
  * Line charts for market trends and growth projections
  * Quadrant charts for SWOT analysis and risk assessment
  * Mind maps for project overview and strategic planning

Advanced Business Analysis Features:
- Comprehensive financial modeling and projections
- Advanced market analysis with competitive intelligence
- Technical feasibility with industry benchmarking
- Risk assessment with mitigation strategies
- Geographic analysis with regional performance metrics
- Strategic recommendations for different stakeholders
- Sensitivity analysis and scenario planning
- Regulatory compliance assessment
- Technology adoption trends analysis
- Supply chain optimization opportunities

Usage:
  python scripts/automation/deep_research_generator.py \
    --pdf-dir scripts/data/source/pdfs \
    --output-root docs \
    --template scripts/data/templates/unified_project_analysis_template.md \
    --max-pages 30 \
    --model gpt-4o

Env:
  OPENAI_API_KEY must be set
  OPENAI_MODEL=gpt-4o (recommended for best results)
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

import pdfplumber

try:
    # New OpenAI SDK style (>=1.0)
    from openai import OpenAI
    HAS_OPENAI_NEW = True
except Exception:
    HAS_OPENAI_NEW = False

try:
    import openai  # Fallback older usage
    HAS_OPENAI_OLD = True
except Exception:
    HAS_OPENAI_OLD = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DEFAULT_PDF_DIR = "scripts/data/source/pdfs"
DEFAULT_OUTPUT_ROOT = "docs"
DEFAULT_TEMPLATE = "scripts/data/templates/unified_project_analysis_template.md"


def read_pdf_text(pdf_path: Path, max_pages: int = 30) -> str:
    """Extract readable text from the first max_pages of a PDF."""
    if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        return ""
    try:
        texts = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            total_pages = len(pdf.pages)
            pages_to_read = min(max_pages, total_pages)
            for i in range(pages_to_read):
                page = pdf.pages[i]
                content = page.extract_text() or ""
                if content:
                    texts.append(content)
        joined = "\n\n".join(texts)
        return joined
    except Exception as e:
        logger.warning(f"Failed to read PDF {pdf_path.name}: {e}")
        return ""


def load_template(template_path: Path) -> str:
    """Load unified template markdown content."""
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def ensure_output_structure(root: Path, pdf_stem: str) -> Path:
    """Create docs/<stem>/ and assets/; return folder path."""
    target_dir = root / pdf_stem
    assets_dir = target_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def write_placeholder_svg(target_dir: Path, title: str) -> Path:
    """Write a simple placeholder diagrams.svg in assets/."""
    assets_dir = target_dir / "assets"
    svg_path = assets_dir / "diagrams.svg"
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="240" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="240" fill="#f8f9fa"/>
  <text x="400" y="40" font-family="Arial, sans-serif" font-size="20" font-weight="bold" text-anchor="middle" fill="#2c3e50">Mermaid Diagrams Generated</text>
  <text x="400" y="80" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#34495e">{title}</text>
  <rect x="100" y="110" width="600" height="100" rx="8" fill="#e9ecef" stroke="#ced4da" stroke-width="2"/>
  <text x="400" y="165" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="#495057">Mermaid diagrams are embedded in Deep-Research.md</text>
</svg>
"""
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return svg_path


def build_prompt(pdf_text: str, template_md: str, pdf_name: str) -> str:
    """Create a comprehensive prompt for deep business research with advanced analysis and Mermaid diagrams."""
    return f"""
You are a senior business research analyst and data visualization expert with deep expertise in:
- Financial analysis and investment evaluation
- Market research and competitive intelligence
- Technical feasibility assessment
- Risk analysis and mitigation strategies
- Geographic market analysis
- Strategic planning and implementation

TASK: Create a comprehensive Deep-Research.md file that provides enterprise-grade business analysis with intelligent Mermaid diagrams for each visualization placeholder.

IMPORTANT: You MUST replace ALL image placeholders like ![Title](URL) with appropriate Mermaid diagrams. Do not leave any image placeholders in the final output.

PDF Name: {pdf_name}

PDF Extract (truncated if large):
{pdf_text}

Template to follow and fill (Markdown):
{template_md}

CRITICAL REQUIREMENTS:

1. **Deep Business Analysis**: Provide comprehensive, enterprise-level analysis including:
   - Detailed financial modeling and projections
   - Advanced market analysis with competitive intelligence
   - Technical feasibility with industry benchmarking
   - Comprehensive risk assessment with mitigation strategies
   - Geographic analysis with regional performance metrics
   - Strategic recommendations for different stakeholders

2. **Mermaid Diagrams**: For each image placeholder, create an appropriate Mermaid diagram based on the context:

   **Diagram Type Selection Guide:**
   - **Flowcharts** (graph TD): For manufacturing processes, implementation timelines, project roadmaps
   - **Gantt Charts** (gantt): For project timelines, implementation phases
   - **Pie Charts** (pie): For market share, cost breakdown, investment distribution
   - **Bar Charts** (bar): For financial projections, regional performance, competitive analysis
   - **Line Charts** (line): For market trends, growth projections, performance over time
   - **Quadrant Charts** (quadrant): For SWOT analysis, risk assessment, competitive positioning
   - **Mind Maps** (mindmap): For project overview, business model, strategic planning
   - **Journey Maps** (journey): For customer journey, supply chain, implementation process

   **Specific Diagram Assignments:**
   - Manufacturing Process Flowchart → Flowchart (graph TD)
   - Supply Chain Network → Flowchart with suppliers, manufacturers, distributors
   - Market Trends → Line chart showing growth over time
   - Competitive Landscape → Bar chart or quadrant chart
   - Geographic Distribution → Pie chart or bar chart by region
   - Regional Performance → Bar chart comparing regions
   - Investment Hotspots → Bar chart or heatmap representation
   - Risk Matrix → Quadrant chart (probability vs impact)
   - SWOT Analysis → Mind map or quadrant chart
   - Implementation Timeline → Gantt chart
   - Financial Projections → Line chart or bar chart
   - Market Projections → Line chart
   - Project Roadmap → Flowchart or Gantt chart

   **CRITICAL IMAGE PLACEHOLDER REPLACEMENT:**
   - Replace ![Project Overview Diagram](URL) → Mermaid mindmap or flowchart
   - Replace ![Financial Performance Chart](URL) → Mermaid bar/line chart
   - Replace ![Risk-Return Matrix](URL) → Mermaid quadrant chart
   - Replace ![Manufacturing Process Flowchart](URL) → Mermaid flowchart
   - Replace ![Supply Chain Network Diagram](URL) → Mermaid flowchart
   - Replace ![Market Size and Growth Trends](URL) → Mermaid line chart
   - Replace ![Competitive Landscape Map](URL) → Mermaid bar chart
   - Replace ![Geographic Distribution Map](URL) → Mermaid pie chart
   - Replace ![Regional Performance Dashboard](URL) → Mermaid bar chart
   - Replace ![Investment Hotspots Heatmap](URL) → Mermaid bar chart
   - Replace ![Risk Analysis Matrix Visualization](URL) → Mermaid quadrant chart
   - Replace ![SWOT Analysis Matrix](URL) → Mermaid mindmap
   - Replace ![Implementation Gantt Chart](URL) → Mermaid gantt chart
   - Replace ![5-Year Financial Projections Chart](URL) → Mermaid line chart
   - Replace ![Market Growth Projections Chart](URL) → Mermaid line chart
   - Replace ![Project Implementation Roadmap](URL) → Mermaid gantt chart

3. **Mermaid Syntax**: Use proper Mermaid syntax with clear titles, labels, and data
   - Use `xychart-beta` for bar and line charts (not `bar` or `line`)
   - Use `quadrantChart` for quadrant charts (not `quadrant`)
   - Use `pie` for pie charts
   - Use `graph TD` for flowcharts
   - Use `gantt` for timeline charts
   - Use `mindmap` for mind maps
4. **Data Accuracy**: Use actual numbers from the PDF for all diagrams
5. **Professional Quality**: Ensure diagrams are informative and visually appealing
6. **Indian Context**: Use ₹ currency and Indian market data where applicable
7. **CRITICAL**: Replace ALL image placeholders like ![Title](URL) with Mermaid diagrams
8. **Business Intelligence**: Include advanced analysis such as:
    - Sensitivity analysis for key variables
    - Scenario planning (best case, worst case, most likely)
    - Industry benchmarking and competitive positioning
    - Regulatory compliance assessment
    - Technology adoption trends
    - Supply chain optimization opportunities
    - Market entry strategies and timing
    - Exit strategy considerations

OUTPUT FORMAT:
- Return a complete Markdown document with ALL placeholders replaced
- Replace EVERY image placeholder (e.g., ![Project Overview Diagram](URL)) with appropriate Mermaid diagrams
- Include Mermaid diagrams using ```mermaid code blocks
- Each diagram should be relevant to the section content
- Maintain professional formatting and structure
- NO image placeholders should remain in the final output

EXAMPLE MERMAID DIAGRAM FORMATS:

**Flowchart:**
```mermaid
graph TD
    A[Raw Materials] --> B[Manufacturing]
    B --> C[Quality Control]
    C --> D[Packaging]
    D --> E[Distribution]
```

**Bar Chart:**
```mermaid
xychart-beta
    title "Financial Performance"
    x-axis [DSCR, ROI, Break-even, Payback]
    y-axis "Value" 0 --> 50
    bar [2.36, 25, 39, 5]
```

**Line Chart:**
```mermaid
xychart-beta
    title "Market Growth Trends"
    x-axis [2017, 2018, 2019, 2020, 2025]
    y-axis "Market Size (₹ Million)" 0 --> 7000
    line [4060, 4300, 4560, 4830, 6650]
```

**Pie Chart:**
```mermaid
pie title "Project Cost Breakdown"
    "Land & Building" : 22.15
    "Plant & Machinery" : 41.65
    "Working Capital" : 30.75
    "Other Assets" : 5.55
```

**Quadrant Chart:**
```mermaid
quadrantChart
    title Risk Analysis Matrix
    x-axis Probability --> Impact
    y-axis Low --> High
    quadrant-1 High Probability, High Impact
    quadrant-2 Low Probability, High Impact
    quadrant-3 Low Probability, Low Impact
    quadrant-4 High Probability, Low Impact
    "Market Risk": [0.8, 0.7]
    "Technical Risk": [0.6, 0.5]
    "Financial Risk": [0.5, 0.6]
```

**Gantt Chart:**
```mermaid
gantt
    title Project Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Planning
    Site Selection    :a1, 2023-10-01, 30d
    section Setup
    Equipment Procurement :a2, after a1, 60d
    section Operations
    Production Start  :a3, after a2, 30d
```

**Mind Map:**
```mermaid
mindmap
  root((Surgical 3 Ply Mask))
    Project Overview
      Key Metrics
        Cost: ₹18.05L
        Employment: 10
    Market Potential
      Growth: 6.1% CAGR
      Size: ₹4060M
```

Generate comprehensive, enterprise-grade business analysis with intelligent, data-driven Mermaid visualizations using proper syntax for each placeholder. Focus on providing actionable insights suitable for executive decision-making and investment evaluation.
"""


def call_openai_generate(markdown_prompt: str, model: Optional[str] = None) -> str:
    """Call OpenAI to generate the Deep Research markdown. Attempts modern client first, then legacy."""
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o")

    # Try newer client
    if HAS_OPENAI_NEW:
        try:
            client = OpenAI()
            # Use chat.completions as a broadly compatible path
            resp = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a senior business research analyst and data visualization expert with 15+ years of experience in enterprise-level project analysis. You specialize in PMEGP project reports and excel at creating comprehensive, investment-grade analysis with intelligent Mermaid diagrams. Your expertise includes financial modeling, market intelligence, risk assessment, and strategic planning. Provide detailed, actionable insights that would be suitable for executive decision-making and investment committees."},
                    {"role": "user", "content": markdown_prompt},
                ],
                temperature=0.1,
                max_tokens=16000,
            )
            content = resp.choices[0].message.content
            return content
        except Exception as e:
            logger.warning(f"OpenAI new client failed, falling back. Error: {e}")

    # Fallback to older API style
    if HAS_OPENAI_OLD:
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            resp = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a senior business research analyst and data visualization expert with 15+ years of experience in enterprise-level project analysis. You specialize in PMEGP project reports and excel at creating comprehensive, investment-grade analysis with intelligent Mermaid diagrams. Your expertise includes financial modeling, market intelligence, risk assessment, and strategic planning. Provide detailed, actionable insights that would be suitable for executive decision-making and investment committees."},
                    {"role": "user", "content": markdown_prompt},
                ],
                temperature=0.1,
                max_tokens=16000,
            )
            return resp.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI legacy client failed: {e}")
            return ""

    logger.error("OpenAI SDK not available. Please install and configure the openai package.")
    return ""


def write_deep_research_md(target_dir: Path, content_md: str):
    out_path = target_dir / "Deep-Research.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content_md)
    return out_path


def write_metadata(target_dir: Path, pdf_path: Path, success: bool, model: str):
    meta_path = target_dir / "metadata.txt"
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"Source PDF: {pdf_path}\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Status: {'success' if success else 'failed'}\n")
        f.write(f"Model: {model}\n")
    return meta_path


def process_single_pdf(pdf_path: Path, output_root: Path, template_md: str, max_pages: int, model: Optional[str]) -> None:
    pdf_stem = pdf_path.stem
    logger.info(f"Processing PDF: {pdf_stem}")

    # Check if Deep-Research.md already exists
    target_dir = output_root / pdf_stem
    existing_md = target_dir / "Deep-Research.md"
    if existing_md.exists():
        logger.info(f"⏭️  Skipping {pdf_stem} - Deep-Research.md already exists")
        return

    # Prepare output dirs
    target_dir = ensure_output_structure(output_root, pdf_stem)
    write_placeholder_svg(target_dir, pdf_stem)

    # Extract text
    text = read_pdf_text(pdf_path, max_pages=max_pages)
    if not text:
        logger.warning(f"No text extracted from {pdf_path.name}. Skipping AI generation.")
        write_metadata(target_dir, pdf_path, success=False, model=model or "auto")
        return

    # Build prompt & call OpenAI
    prompt = build_prompt(text, template_md, pdf_path.name)
    content_md = call_openai_generate(prompt, model=model)

    if not content_md:
        logger.error(f"AI generation failed for {pdf_path.name}")
        write_metadata(target_dir, pdf_path, success=False, model=model or "auto")
        return

    # Write output
    md_path = write_deep_research_md(target_dir, content_md)
    write_metadata(target_dir, pdf_path, success=True, model=model or "auto")
    logger.info(f"✅ Wrote {md_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate Deep-Research.md for each PDF using OpenAI and a unified template")
    parser.add_argument("--pdf-dir", default=DEFAULT_PDF_DIR, help="Directory containing PDFs")
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT, help="Docs output root directory")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE, help="Path to unified analysis template")
    parser.add_argument("--max-pages", type=int, default=30, help="Max pages to read per PDF")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o"), help="OpenAI model to use (gpt-4o recommended for deep research)")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of PDFs to process (0 = all)")
    parser.add_argument("--project-id", help="Process only the PDF with this specific project ID (e.g., '0001_3PlyMask')")

    args = parser.parse_args()

    # Prechecks
    pdf_dir = Path(args.pdf_dir)
    output_root = Path(args.output_root)
    template_path = Path(args.template)

    if not pdf_dir.exists():
        logger.error(f"PDF directory not found: {pdf_dir}")
        sys.exit(1)
    if not template_path.exists():
        logger.error(f"Template not found: {template_path}")
        sys.exit(1)

    output_root.mkdir(parents=True, exist_ok=True)

    template_md = load_template(template_path)

    pdf_files = sorted([p for p in pdf_dir.glob("*.pdf")])
    
    # Filter by project ID if specified
    if args.project_id:
        # Look for PDF that matches the project ID pattern
        target_pdf = None
        for pdf_path in pdf_files:
            # Check if the PDF name contains the project ID
            if args.project_id in pdf_path.stem:
                target_pdf = pdf_path
                break
        
        if target_pdf:
            pdf_files = [target_pdf]
            logger.info(f"Found PDF for project ID '{args.project_id}': {target_pdf.name}")
        else:
            logger.error(f"No PDF found matching project ID '{args.project_id}'")
            logger.info("Available PDFs:")
            for pdf_path in pdf_files[:10]:  # Show first 10 PDFs as examples
                logger.info(f"  - {pdf_path.stem}")
            if len(pdf_files) > 10:
                logger.info(f"  ... and {len(pdf_files) - 10} more")
            sys.exit(1)
    
    if args.limit > 0:
        pdf_files = pdf_files[:args.limit]

    if not pdf_files:
        logger.warning(f"No PDFs found in {pdf_dir}")
        return

    logger.info(f"Found {len(pdf_files)} PDF(s) to process")

    processed = 0
    for pdf_path in pdf_files:
        process_single_pdf(pdf_path, output_root, template_md, args.max_pages, args.model)
        processed += 1

    logger.info(f"Done. Processed {processed} PDF(s)")


if __name__ == "__main__":
    main()
