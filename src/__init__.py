```python
# src/__init__.py
"""
NeuroCortex - Self-Evolving AI Framework
"""

from .core import SRDFFramework
from .trawler import Trawler
from .generator import Generator
from .arbiter import Arbiter

__version__ = "0.1.0"
__author__ = "Mohammed Al-Athwary"
__email__ = "mohammedqaidalathwary@gmail.com"

__all__ = [
    "SRDFFramework",
    "Trawler",
    "Generator", 
    "Arbiter"
]
