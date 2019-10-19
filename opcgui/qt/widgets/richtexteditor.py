#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit

class RichTextEditor(QWidget):

    def __init__(self, context_directory, parent=None, placeholder_text=""):
        super().__init__(parent=parent)

        self.context_directory = context_directory
        self.parent = parent

        self.placeholder_text = placeholder_text

        # Make widgets ####################################

        self.editor = QPlainTextEdit()

        self.editor.setPlaceholderText(self.placeholder_text)

        # Make layouts ####################################

        vbox = QVBoxLayout(self)

        vbox.setContentsMargins(0, 0, 0, 0)

        # VBox

        vbox.addWidget(self.editor)

        # Set layouts #####################################

        self.setLayout(vbox)
