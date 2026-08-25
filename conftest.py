import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "custom_components", "buspro"))

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()
