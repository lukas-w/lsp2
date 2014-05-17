"""
* default.py contains general settings that apply for all deployments
* dev.py contains settings for a development environment
"""

try:
	from .dev import *
except ImportError:
	from .default import *
