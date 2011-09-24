# -*- coding: utf-8 *-*

from __future__ import absolute_import

from ninja_ide.core import plugin_manager

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QVBoxLayout


class PluginPreferences(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.plugin_manager = plugin_manager.PluginManager()
        vbox = QVBoxLayout(self)

        self._tabs = QTabWidget()
        vbox.addWidget(self._tabs)
        #load widgets
        self._load_widgets()

    def _load_widgets(self):
        #Collect the preferences widget for each active plugin
        for plugin in self.plugin_manager.get_actives_plugins():
            preferences_widget = plugin.get_preferences_widget()
            if preferences_widget:
                plugin_name = plugin.metadata.get('name')
                try:
                    self._tabs.addTab(preferences_widget, plugin_name)
                except Exception:
                    print "Plugin preferences widget Error (%s)" % plugin_name
                    continue

    def save(self):
        for i in xrange(self._tabs.count()):
            self._tabs.widget(i).save()
