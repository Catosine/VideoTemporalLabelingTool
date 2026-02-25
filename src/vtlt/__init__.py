"""Video Temporal Labeling Tool.

A GUI application for temporal video data labeling.
"""

__version__ = "2.0.0"
__author__ = "Pengnan Fan"
__license__ = "MIT"

from .app import App, Layout, main
from .service import Service

__all__ = ["App", "Layout", "Service", "main"]
