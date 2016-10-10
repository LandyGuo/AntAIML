import logging.config
import os
# The Kernel class is the only class most implementations should need.
from Kernel import Kernel

__all__ = ['Kernel']
_CONFIG_FILE = "logging.config"
_GLOBAL_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),_CONFIG_FILE)
logging.config.fileConfig(_GLOBAL_CONFIG_PATH)