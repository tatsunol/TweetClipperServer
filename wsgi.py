#!/usr/bin/python3
import sys
import site
import os
import toml

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, PROJECT_ROOT)
from server import app as application