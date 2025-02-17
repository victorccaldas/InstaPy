# flake8: noqa

# __variables__ with double-quoted values will be available in setup.py
__version__ = "0.7"
print("Versão Instapy:", __version__)

from .instapy import InstaPy
from .util import smart_run
from .settings import Settings
from .file_manager import set_workspace
from .file_manager import get_workspace
from .exceptions import DeslogError