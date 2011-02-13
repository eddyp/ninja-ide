#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) - 2010 Juan B Cabral <jbc dot develop at gmail dot com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#===============================================================================
# DOCS
#===============================================================================

"""Setup for Ninja-ide (http://code.google.com/p/ninja-ide/)"""


#===============================================================================
# IMPORTS
#===============================================================================

import os
import sys

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import pkg_resources

import ninja_ide

#===============================================================================
# VALIDATE THE NEEDED MODULES
#===============================================================================

# This modules can't be easy installed
# Syntax: [(module, url of the tutorial)...]
NEEDED_MODULES = [("PyQt4", "http://www.riverbankcomputing.co.uk/software/pyqt/intro"), ]


for mn, urlm in NEEDED_MODULES:
    try:
        __import__(mn)
    except ImportError:
        print "Module '%s' not found. For more details see '%s'.\n" % (mn, urlm)
        sys.exit(1)


#===============================================================================
# PRE-SETUP
#===============================================================================

# Common
params = {
    "name":ninja_ide.__prj__,
    "version":ninja_ide.VERSION,
    "description":ninja_ide.__doc__,
    "author":ninja_ide.__author__,
    "author_email":ninja_ide.__mail__,
    "url":ninja_ide.__url__,
    "license":ninja_ide.__licence__,
    "keywords":"ide python ninja development",
    "classifiers":["Development Status :: 4 - Beta",
                   "Topic :: Utilities",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2"],
    
    # this line is required for install a plugin for mercurial to package all 
    # images and other resources
    "setup_requires":["setuptools_hg"],
      
    # Ninja need:
    "install_requires":["rope", "Pygments"],
      
    # include all resources
    "include_package_data": True,
    "package_data": {'': ['*.png', '*.json']},
      
    # include ninja pkg and setup the run script
    "packages":find_packages(),
    
    #auto create scripts
    "entry_points": {
        'console_scripts': [
            'ninjac = ninja_ide:setup_and_run',
        ],
        'gui_scripts': [
            'ninja = ninja_ide:setup_and_run',
        ]
    }
} 
      
      
#===============================================================================
# SETUP
#===============================================================================

setup(**params)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == '__main__':
    print(__doc__)
