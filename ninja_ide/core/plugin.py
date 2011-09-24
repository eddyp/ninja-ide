# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from PyQt4.QtCore import QObject
import abc

#TODO:
    #plugin manager widget
    #install from web
    #list local plugins
    #uninstall plugins
    #services (project-type, project-tree, properties-widget, mainContainer)


class Plugin(QObject):
    '''
    Base class for ALL Plugin
    All plugins should inherit from this class
    '''

    def __init__(self, locator):
        QObject.__init__(self)
        self.locator = locator
        self.metadata = None

    def initialize(self):
        raise NotImplemented

    def finish(self):
        pass

    def get_preferences_widget(self):
        pass
