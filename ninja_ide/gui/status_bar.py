# -*- coding: utf-8 -*-
from __future__ import absolute_import

from PyQt4.QtGui import QStatusBar
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from ninja_ide import resources
from ninja_ide.core import settings
from ninja_ide.tools import locator
from ninja_ide.gui.main_panel import main_container


__statusBarInstance = None


def StatusBar(*args, **kw):
    global __statusBarInstance
    if __statusBarInstance is None:
        __statusBarInstance = __StatusBar(*args, **kw)
    return __statusBarInstance


class __StatusBar(QStatusBar):

    def __init__(self, parent=None):
        QStatusBar.__init__(self, parent)

        self._widgetStatus = QWidget()
        vbox = QVBoxLayout(self._widgetStatus)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        #Search Layout
        self._searchWidget = SearchWidget(self)
        vbox.addWidget(self._searchWidget)
        #Replace Layout
        self._replaceWidget = ReplaceWidget(self)
        vbox.addWidget(self._replaceWidget)
        self._replaceWidget.setVisible(False)
        #Code Locator
        self._codeLocator = locator.CodeLocatorWidget(self)
        vbox.addWidget(self._codeLocator)
        self._codeLocator.setVisible(False)

        self.addWidget(self._widgetStatus)

        self._shortEsc = QShortcut(QKeySequence(Qt.Key_Escape), self)

        self.connect(self._searchWidget._btnClose, SIGNAL("clicked()"),
            self.hide_status)
        self.connect(self._searchWidget._btnFind, SIGNAL("clicked()"),
            self.find)
        self.connect(self._searchWidget.btnNext, SIGNAL("clicked()"),
            self.find_next)
        self.connect(self._searchWidget.btnPrevious, SIGNAL("clicked()"),
            self.find_previous)
        self.connect(self, SIGNAL("messageChanged(QString)"), self.message_end)
        self.connect(self._replaceWidget._btnCloseReplace, SIGNAL("clicked()"),
            lambda: self._replaceWidget.setVisible(False))
        self.connect(self._replaceWidget._btnReplace, SIGNAL("clicked()"),
            self.replace)
        self.connect(self._replaceWidget._btnReplaceAll, SIGNAL("clicked()"),
            self.replace_all)
        self.connect(self._shortEsc, SIGNAL("activated()"), self.hide_status)

    def explore_code(self):
        self._codeLocator.explore_code()

    def explore_file_code(self, path):
        self._codeLocator.explore_file_code(path)

    def show(self):
        self.clearMessage()
        QStatusBar.show(self)
        if self._widgetStatus.isVisible():
            self._searchWidget._line.setFocus()
            self._searchWidget._line.selectAll()

    def show_replace(self):
        self.clearMessage()
        self.show()
        editor = main_container.MainContainer().get_actual_editor()
        if editor:
            if editor.textCursor().hasSelection():
                word = editor.textCursor().selectedText()
                self._searchWidget._line.setText(word)
        self._replaceWidget.setVisible(True)

    def show_with_word(self):
        self.clearMessage()
        editor = main_container.MainContainer().get_actual_editor()
        if editor:
            word = editor._text_under_cursor()
            self._searchWidget._line.setText(word)
            self.show()

    def show_locator(self):
        self.clearMessage()
        self._searchWidget.setVisible(False)
        self.show()
        self._codeLocator.setVisible(True)
        self._codeLocator._completer.setFocus()
        self._codeLocator.show_suggestions()

    def hide_status(self):
        self._searchWidget._checkSensitive.setCheckState(Qt.Unchecked)
        self._searchWidget._checkWholeWord.setCheckState(Qt.Unchecked)
        self.hide()
        self._searchWidget.setVisible(True)
        self._replaceWidget.setVisible(False)
        self._codeLocator.setVisible(False)
        widget = main_container.MainContainer().get_actual_widget()
        if widget:
            widget.setFocus()

    def replace(self):
        s = 0 if not self._searchWidget._checkSensitive.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self._searchWidget._checkWholeWord.isChecked() \
            else QTextDocument.FindWholeWords
        flags = 0 + s + w
        editor = main_container.MainContainer().get_actual_editor()
        if editor:
            editor.replace_match(unicode(self._searchWidget._line.text()),
                unicode(self._replaceWidget._lineReplace.text()), flags)

    def replace_all(self):
        s = 0 if not self._searchWidget._checkSensitive.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self._searchWidget._checkWholeWord.isChecked() \
            else QTextDocument.FindWholeWords
        flags = 0 + s + w
        editor = main_container.MainContainer().get_actual_editor()
        if editor:
            editor.replace_match(unicode(self._searchWidget._line.text()),
                unicode(self._replaceWidget._lineReplace.text()), flags, True)

    def find(self):
        s = 0 if not self._searchWidget._checkSensitive.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self._searchWidget._checkWholeWord.isChecked() \
            else QTextDocument.FindWholeWords
        flags = s + w
        editor = main_container.MainContainer().get_actual_editor()
        if editor:
            editor.find_match(unicode(self._searchWidget._line.text()), flags)

    def find_next(self):
        s = 0 if not self._searchWidget._checkSensitive.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self._searchWidget._checkWholeWord.isChecked() \
            else QTextDocument.FindWholeWords
        flags = 0 + s + w
        editor = main_container.MainContainer().get_actual_editor()
        if editor:
            editor.find_match(unicode(self._searchWidget._line.text()),
                flags, True)

    def find_previous(self):
        s = 0 if not self._searchWidget._checkSensitive.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self._searchWidget._checkWholeWord.isChecked() \
            else QTextDocument.FindWholeWords
        flags = 1 + s + w
        editor = main_container.MainContainer().get_actual_editor()
        if editor:
            editor.find_match(unicode(self._searchWidget._line.text()), flags)

    def showMessage(self, message, timeout):
        self._widgetStatus.hide()
        self._replaceWidget.setVisible(False)
        self.show()
        QStatusBar.showMessage(self, message, timeout)

    def message_end(self, message):
        if message == '':
            self.hide()
            QStatusBar.clearMessage(self)
            self._widgetStatus.show()


class SearchWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        hSearch = QHBoxLayout(self)
        hSearch.setContentsMargins(0, 0, 0, 0)
        self._line = TextLine(parent)
        self._line.setMinimumWidth(250)
        self._checkSensitive = QCheckBox(self.tr("Respect Case Sensitive"))
        self._checkWholeWord = QCheckBox(self.tr("Find Whole Words"))
        self._btnClose = QPushButton(
            self.style().standardIcon(QStyle.SP_DialogCloseButton), '')
        self._btnFind = QPushButton(QIcon(resources.IMAGES['find']), '')
        self.btnPrevious = QPushButton(
            self.style().standardIcon(QStyle.SP_ArrowLeft), '')
        self.btnPrevious.setToolTip(self.tr("Press (%1 + Left Arrow)").arg(
            settings.OS_KEY))
        self.btnNext = QPushButton(
            self.style().standardIcon(QStyle.SP_ArrowRight), '')
        self.btnNext.setToolTip(self.tr("Press (%1 + Right Arrow)").arg(
            settings.OS_KEY))
        hSearch.addWidget(self._btnClose)
        hSearch.addWidget(self._line)
        hSearch.addWidget(self._btnFind)
        hSearch.addWidget(self.btnPrevious)
        hSearch.addWidget(self.btnNext)
        hSearch.addWidget(self._checkSensitive)
        hSearch.addWidget(self._checkWholeWord)


class ReplaceWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        hReplace = QHBoxLayout(self)
        hReplace.setContentsMargins(0, 0, 0, 0)
        self._lineReplace = QLineEdit()
        self._lineReplace.setMinimumWidth(250)
        self._btnCloseReplace = QPushButton(
            self.style().standardIcon(QStyle.SP_DialogCloseButton), '')
        self._btnReplace = QPushButton(self.tr("Replace"))
        self._btnReplaceAll = QPushButton(self.tr("Replace All"))
        hReplace.addWidget(self._btnCloseReplace)
        hReplace.addWidget(self._lineReplace)
        hReplace.addWidget(self._btnReplace)
        hReplace.addWidget(self._btnReplaceAll)


class TextLine(QLineEdit):

    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        self._parent = parent

    def keyPressEvent(self, event):
        editor = main_container.MainContainer().get_actual_editor()
        if editor and event.key() in \
        (Qt.Key_Enter, Qt.Key_Return):
            self._parent.find_next()
        elif event.modifiers() == Qt.ControlModifier and \
        event.key() == Qt.Key_Right:
            self._parent.find_next()
            return
        elif event.modifiers() == Qt.ControlModifier and \
        event.key() == Qt.Key_Left:
            self._parent.find_previous()
            return
        super(TextLine, self).keyPressEvent(event)
        if int(event.key()) in range(32, 162):
            self._parent.find()
