#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QPushButton

class RichTextEditor(QWidget):

    def __init__(self, context_directory, parent=None, placeholder_text=""):
        super().__init__(parent=parent)

        self.context_directory = context_directory
        self.parent = parent

        self.placeholder_text = placeholder_text

        # Make widgets ####################################

        self.switch_display = QPushButton("Switch")
        self.editor = QPlainTextEdit()

        self.editor.setPlaceholderText(self.placeholder_text)

        # Make layouts ####################################

        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout(self)

        vbox.setContentsMargins(0, 0, 0, 0)
        hbox.setContentsMargins(0, 0, 0, 0)

        # HBox

        hbox.addWidget(self.switch_display)

        # VBox
        
        vbox.addLayout(hbox)
        vbox.addWidget(self.editor)

        # Set layouts #####################################

        self.setLayout(vbox)
