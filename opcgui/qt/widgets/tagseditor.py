#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit

class TagsEditor(QWidget):

    def __init__(self, card_list, parent=None, placeholder_text="Tags"):
        super().__init__(parent=parent)

        self.parent = parent

        self.card_list = card_list
        self.placeholder_text = placeholder_text

        # Make widgets ####################################

        self.editor = QPlainTextEdit()

        self.editor.setPlaceholderText(self.placeholder_text)

        # TODO: setup auto-completion https://doc.qt.io/qt-5/qtwidgets-tools-customcompleter-example.html

        # Make layouts ####################################

        vbox = QVBoxLayout(self)

        vbox.setContentsMargins(0, 0, 0, 0)

        # VBox

        vbox.addWidget(self.editor)

        # Set layouts #####################################

        self.setLayout(vbox)
