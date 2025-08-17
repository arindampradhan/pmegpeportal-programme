"""
Intelligent Diagram Generator Package
AI-powered business visualization system for PMEGP analysis
"""

from .intelligent_diagram_generator import IntelligentDiagramGenerator, ChartRequirement
from .template_diagram_generator import TemplateSpecificDiagramGenerator

__version__ = "1.0.0"
__author__ = "PMEGP Analysis System"
__description__ = "AI-powered diagram generation for business analysis"

__all__ = [
    'IntelligentDiagramGenerator',
    'TemplateSpecificDiagramGenerator', 
    'ChartRequirement'
]
