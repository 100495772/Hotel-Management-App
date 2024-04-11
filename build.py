#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init
import sys
import os

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "EG2"
default_task = "publish"


@init
def set_properties(project):
    src_parent_dir = os.path.abspath(os.path.join(project.basedir, 'src', '..'))
    sys.path.append(src_parent_dir)