#!/usr/bin/python3
import sys
import site
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# site.addsitedir(os.path.join(PROJECT_ROOT, "ENV", "lib", "python3.5", "site-packages"))

# sys.path.insert(0, PROJECT_ROOT)
from server import app as application
