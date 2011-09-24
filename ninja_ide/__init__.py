#-*-coding:utf-8-*-

from __future__ import absolute_import

###############################################################################
# METADATA
###############################################################################

__prj__ = "ninja-ide"
__author__ = "The NINJA-IDE Team"
__mail__ = "ninja-ide at googlegroups dot com"
__url__ = "http://www.ninja-ide.org"
__source__ = "http://ninja-ide.googlecode.com"
__version__ = "2.0-beta"
__licence__ = "GPL3"

###############################################################################
# DOC
###############################################################################

"""NINJA-IDE is a cross-platform integrated development environment (IDE).
NINJA-IDE runs on Linux/X11, Mac OS X and Windows desktop operating systems,
and allows developers to create applications for several purposes using all the
tools and utilities of NINJA-IDE, making the task of writing software easier
and more enjoyable.
"""

###############################################################################
# START
###############################################################################


def setup_and_run():
    # import only on run
    # Dont import always this, setup.py will fail
    from ninja_ide import core, resources

    # Create NINJA-IDE user folder structure for plugins, themes, etc
    resources.create_home_dir_structure()

    # Run NINJA-IDE
    core.run_ninja()
