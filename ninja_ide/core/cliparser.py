# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
import optparse

import ninja_ide


def _resolve_nargs(*opts):
    final_nargs = 1
    for opt in opts:
        nargs = 0
        try:
            start = sys.argv.index(opt) + 1
            for idx, arg in enumerate(sys.argv[start:]):
                if str(arg).startswith("-"):
                    break
                nargs += 1
            return nargs
        except ValueError:
            nargs = 1
        if final_nargs < nargs:
            final_nargs = nargs
    return final_nargs


def _get_parser():
    usage = "$python ninja-ide.py <option, [option3...option n]>"

    epilog = "This program comes with ABSOLUTELY NO WARRANTY." + \
             "This is free software, and you are welcome to redistribute " + \
             "it under certain conditions; for details see LICENSE.txt."

    parser = optparse.OptionParser(usage, version=ninja_ide.__version__,
        epilog=epilog)

    parser.add_option("-f", "--file",
        type="string",
        action="store",
        dest="filenames",
        default=(),
        help="A file/s to edit",
        nargs=_resolve_nargs("-f", "--file"))

    parser.add_option("-p", "--project",
        type="string",
        action="store",
        dest="projects_path",
        default=(),
        help="A project/s to edit",
        nargs=_resolve_nargs("-p", "--project"))

    parser.add_option("--plugin",
        type="string",
        action="store",
        dest="extra_plugins",
        default=(),
        help="A plugin to load",
        nargs=_resolve_nargs("--plugin"))

    return parser


def parse():
    filenames = None
    projects_path = None
    extra_plugins = None
    try:
        opts = _get_parser().parse_args()[0]

        filenames = opts.filenames \
            if isinstance(opts.filenames, tuple) \
            else (opts.filenames,)
        projects_path = opts.projects_path \
            if isinstance(opts.projects_path, tuple) \
            else  (opts.projects_path,)
        extra_plugins = opts.extra_plugins \
            if isinstance(opts.extra_plugins, tuple) \
            else  (opts.extra_plugins,)
    except Exception, reason:
        print "Args couldn't be parsed."
        print reason
    return filenames, projects_path, extra_plugins
