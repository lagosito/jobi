from .common import *
from .secret import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# TODO: Set environment variables
if DEBUG:
    from .dev import *
else:
    from .prod import *
