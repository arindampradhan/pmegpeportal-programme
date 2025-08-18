#!/usr/bin/env python3
import csv
import os
from pathlib import Path

def load_csv_data():
    """Load project data from CSV file"""
    projects = {}
    csv_path = "scripts/data/source/projects_output_clean.csv"
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            project_name = row['Project Name']
            category = row['Category/Company']
            pdf_link = row['PDF Link']
            
            # Create a key that matches the folder naming pattern
            clean_name = project_name.replace("PROJECT PROFILE ON ", "").strip()
            
            # Create multiple possible keys for matching
            possible_keys = [
                project_name,
                clean_name,
                project_name.upper(),
                clean_name.upper(),
                project_name.replace(" ", ""),
                clean_name.replace(" ", "")
            ]
            
            for key in possible_keys:
                projects[key] = {
                    'name': project_name,
                    'category': category,
                    'pdf_link': pdf_link
                }
    
    return projects

def get_deep_research_projects():
    """Get list of projects that have Deep-Research.md files"""
    docs_dir = Path("docs")
    projects = []
    
    for folder in docs_dir.iterdir():
        if folder.is_dir() and (folder / "Deep-Research.md").exists():
            projects.append(folder.name)
    
    return sorted(projects)

def match_projects_with_csv():
    """Match folder names with CSV data"""
    csv_projects = load_csv_data()
    deep_research_projects = get_deep_research_projects()
    
    matched_projects = []
    
    for folder_name in deep_research_projects:
        # Try to match with CSV data
        matched = False
        
        # Try exact match first
        if folder_name in csv_projects:
            project_data = csv_projects[folder_name]
            matched_projects.append({
                'folder': folder_name,
                'name': project_data['name'],
                'category': project_data['category'],
                'pdf_link': project_data['pdf_link'],
                'deep_research_link': f"docs/{folder_name}/Deep-Research.md"
            })
            matched = True
            continue
        
        # Try matching by removing prefixes and cleaning up
        import re
        clean_folder = re.sub(r'^\d{4}_', '', folder_name)
        
        # Try matching with cleaned folder name
        if clean_folder in csv_projects:
            project_data = csv_projects[clean_folder]
            matched_projects.append({
                'folder': folder_name,
                'name': project_data['name'],
                'category': project_data['category'],
                'pdf_link': project_data['pdf_link'],
                'deep_research_link': f"docs/{folder_name}/Deep-Research.md"
            })
            matched = True
            continue
        
        # If no match found, create a basic entry
        if not matched:
            # Extract project name from folder name
            project_name = clean_folder.replace("_", " ").title()
            matched_projects.append({
                'folder': folder_name,
                'name': project_name,
                'category': 'Unknown',
                'pdf_link': 'N/A',
                'deep_research_link': f"docs/{folder_name}/Deep-Research.md"
            })
    
    return matched_projects

def generate_markdown_tables():
    """Generate markdown tables for each category"""
    projects = match_projects_with_csv()
    
    # Group by category
    categories = {}
    for project in projects:
        category = project['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(project)
    
    # Generate markdown
    markdown = ""
    
    for category, category_projects in categories.items():
        if not category_projects:
            continue
            
        # Clean category name
        clean_category = category.replace(" INDUSTRY", "").replace(" AND ", " & ").replace("BASED", "Based")
        
        markdown += f"#### {clean_category}\n\n"
        markdown += "| ☆ | Project Name | Sample Reports | Analysis | Status |\n"
        markdown += "|---|--------------|----------------|----------|--------|\n"
        
        for project in category_projects:
            star_rating = "★★★"
            project_name = project['name']
            pdf_link = project['pdf_link']
            deep_research_link = project['deep_research_link']
            
            # Create the sample reports column with both PDF and Deep-Research links
            if pdf_link != 'N/A':
                sample_reports = f"[PDF]({pdf_link}) | [Deep Research]({deep_research_link})"
            else:
                sample_reports = f"[Deep Research]({deep_research_link})"
            
            # Analysis features based on category
            analysis_features = "Financial modeling, Market analysis, Risk assessment, Strategic planning"
            
            status = "✅ Complete"
            
            markdown += f"| {star_rating} | **{project_name}** | {sample_reports} | {analysis_features} | {status} |\n"
        
        markdown += "\n"
    
    return markdown

if __name__ == "__main__":
    markdown_content = generate_markdown_tables()
    print(markdown_content)
