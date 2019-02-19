import os

from .pub_config import *

if os.path.exists("ksmod/config/priv_config.py"):
    from .priv_config import *
