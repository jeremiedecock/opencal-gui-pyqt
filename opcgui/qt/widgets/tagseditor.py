#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Slot, QStringListModel
from PySide6.QtGui import QTextCursor, QKeyEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLabel, QCompleter

import opencal.core.tags


# See https://doc.qt.io/qtforpython-6/overviews/qtwidgets-tools-customcompleter-example.html
#     https://doc.qt.io/archives/qt-5.8/qtwidgets-tools-customcompleter-example.html
#     https://code.qt.io/cgit/qt/qtbase.git/tree/examples/widgets/tools/customcompleter?h=5.15
class PlainTextEditWithCompleter(QPlainTextEdit):

    def __init__(self):
        super().__init__()

        self.setPlaceholderText("Try to type name of planets in our Solar System.")
        self._completer = QCompleter(self)

        self.completer_model = QStringListModel()

        self._completer.setModel(self.completer_model)
        self._completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer.setWrapAround(False)
        self._completer.setWidget(self)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        self._completer.activated[str].connect(self.insertCompletion)


    @property
    def completer(self) -> QCompleter:
        return self._completer


    @Slot(str)
    def insertCompletion(self, completion: str):
        tc = self.textCursor()
        extra = len(completion) - len(self._completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfLine)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)


    def keyPressEvent(self, e: QKeyEvent):
        if self._completer.popup().isVisible():
            if e.key() in [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab]:
                e.ignore()
                return

        super(PlainTextEditWithCompleter, self).keyPressEvent(e)

        ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        if ctrlOrShift and not e.text():
            return

        hasModifier = e.modifiers() != Qt.NoModifier and not ctrlOrShift

        # Get the text under the cursor
        tc = self.textCursor()
        tc.select(QTextCursor.LineUnderCursor)
        completionPrefix = tc.selectedText()

        if hasModifier or not e.text() or len(completionPrefix) < 1:
            self._completer.popup().hide()
            return

        if completionPrefix != self._completer.completionPrefix():
            self._completer.setCompletionPrefix(completionPrefix)
            self._completer.popup().setCurrentIndex(self._completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self._completer.popup().sizeHintForColumn(0) + self._completer.popup().verticalScrollBar().sizeHint().width())
        self._completer.complete(cr)


class TagsEditor(QWidget):

    def __init__(self, card_list, placeholder_text="Tags"):
        super().__init__()

        self.card_list = card_list

        self.placeholder_text = placeholder_text

        # Make widgets ####################################

        self.editor = PlainTextEditWithCompleter()
        self.editor.setPlaceholderText(self.placeholder_text)

        tag_list = opencal.core.tags.tag_list(self.card_list, count_hidden_cards=True)
        tag_list = [tag.lower() for tag in tag_list]   # The list of words to be autocompleted have to be lower case otherwise some strange things happen (some tags randomly disappear from the suggestion list)!
        self.editor.completer_model.setStringList(sorted(tag_list))  # The list of words to be autocompleted have to be sorted otherwise it won't work!

        self.title_label = QLabel(text="Tags")
        font = self.title_label.font()
        font.setBold(True)
        self.title_label.setFont(font)

        # Make layouts ####################################

        vbox = QVBoxLayout(self)

        #vbox.setContentsMargins(0, 0, 0, 0)

        # VBox

        vbox.addWidget(self.title_label)
        vbox.addWidget(self.editor)

        # Set layouts #####################################

        self.setLayout(vbox)


    @property
    def text(self) -> str:
        """
        The text of the text edit as plain text.
        """
        return self.editor.toPlainText()

    @text.setter
    def text(self, new_text: str):
        self.editor.setPlainText(new_text)