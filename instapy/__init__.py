# flake8: noqa

# __variables__ with double-quoted values will be available in setup.py
__version__ = "0.6.17"
# Commit 16/05/22 2:05
print("__version__:", __version__)
from .instapy import InstaPy
from .util import smart_run
from .settings import Settings
from .file_manager import set_workspace
from .file_manager import get_workspace
from .exceptions import DeslogError