#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLabel, QCompleter

class TagsEditor(QWidget):

    def __init__(self, card_list, parent=None, placeholder_text="Tags"):
        super().__init__(parent=parent)

        self.parent = parent

        self.card_list = card_list              # this will be useful for auto-completion
        self.placeholder_text = placeholder_text

        # Make widgets ####################################

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText(self.placeholder_text)

        self.title_label = QLabel(parent=self, text="Tags")
        font = self.title_label.font()
        font.setBold(True)
        self.title_label.setFont(font)

        # Set completer ##################################

        # Setup the auto-completion for self.editor
        # Remark: setCompleter() is not available for QPlainTextEdit; we have to implement it ourselves
        #         see https://doc.qt.io/qt-5/qtwidgets-tools-customcompleter-example.html

        #completer = QCompleter(["one", "two", "three"], parent=self)
        #completer.setCaseSensitivity(Qt.CaseInsensitive)
        #self.editor.setCompleter(completer)  # TODO: setCompleter() is not available for QPlainTextEdit

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