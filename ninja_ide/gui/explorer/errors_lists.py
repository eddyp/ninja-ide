# -*- coding: utf-8 -*-
from __future__ import absolute_import

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from ninja_ide.gui.main_panel import main_container


ERRORS_TEXT = "Static Errors: %1"
PEP8_TEXT = "PEP8 Errors: %1"


class ErrorsWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.pep8 = None
        self._outRefresh = True

        vbox = QVBoxLayout(self)
        self.listErrors = QListWidget()
        self.listPep8 = QListWidget()
        self.errorsLabel = QLabel(self.tr(ERRORS_TEXT).arg(0))
        vbox.addWidget(self.errorsLabel)
        vbox.addWidget(self.listErrors)
        self.pep8Label = QLabel(self.tr(PEP8_TEXT).arg(0))
        vbox.addWidget(self.pep8Label)
        vbox.addWidget(self.listPep8)

        self.connect(self.listErrors, SIGNAL("itemSelectionChanged()"),
            self.errors_selected)
        self.connect(self.listPep8, SIGNAL("itemSelectionChanged()"),
            self.pep8_selected)

    def errors_selected(self):
        editorWidget = main_container.MainContainer().get_actual_editor()
        if editorWidget and self._outRefresh:
            editorWidget.jump_to_line(
                self.listErrors.currentItem().data(Qt.UserRole).toInt()[0] - 1)

    def pep8_selected(self):
        editorWidget = main_container.MainContainer().get_actual_editor()
        if editorWidget and self._outRefresh:
            editorWidget.jump_to_line(
                self.pep8.pep8lines[self.listPep8.currentRow()] - 1)

    def refresh_lists(self, errors, pe):
        self.pep8 = pe
        self._outRefresh = False
        self.listErrors.clear()
        self.listPep8.clear()
        for data in errors.errorsLines:
            item = QListWidgetItem(errors.errorsSummary[data])
            item.setData(Qt.UserRole, data)
            self.listErrors.addItem(item)
        self.errorsLabel.setText(self.tr(ERRORS_TEXT).arg(
            len(errors.errorsLines)))
        for data in self.pep8.pep8checks:
            item = QListWidgetItem(data.split('\n')[0])
            self.listPep8.addItem(item)
        self.pep8Label.setText(self.tr(PEP8_TEXT).arg(
            len(self.pep8.pep8checks)))
        self._outRefresh = True
