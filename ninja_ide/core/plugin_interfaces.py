# -*- coding: utf-8 -*-

import abc

###############################################################################
# ABSTRACT CLASSES (This file contains useful interfaces for plugins)
###############################################################################


class IProjectTypeHandler:

    """
    Interface to create a Project type handler
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_pages(self):
        """
        Returns a collection of QWizardPage
        """

    @abc.abstractmethod
    def on_wizard_finish(self, wizard):
        """
        Called when the user finish the wizard
        @wizard: QWizard instance
        """

    def get_context_menus(self):
        """"
        Returns a iterable of QMenu
        """
        return ()


class ISymbolsHandler:
    """
    Interface to create a symbol handler
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def obtain_symbols(self, source):
        """
        Returns the dict needed by the tree
        @source: Source code in plain text
        """


class IPluginPreferences(object):
    """
    Interface for plugin preferences widget
    """
    def save(self):
        """
        Save the plugin data as NINJA-IDE settings
        """
        raise NotImplemented
