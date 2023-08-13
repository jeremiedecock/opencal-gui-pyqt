#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from opcgui.qt.widgets.editorwidget import EditorWidget

class AddCardsTab(QWidget):

    def __init__(self, card_list, main_window, parent):
        super().__init__(parent=parent)

        self.card_list = card_list
        self.tabs = parent

        # Make widgets ####################################

        self.editor_widget = EditorWidget(self.card_list, stacked_default_widget="editor", parent=self)

        self.add_button = QPushButton('Add', self)
        
        # Set slots #######################################

        self.add_button.clicked.connect(self.add_btn_callback)

        # Make layouts ####################################

        vbox = QVBoxLayout(self)

        vbox.addWidget(self.editor_widget)
        vbox.addWidget(self.add_button)

        # Set layouts #####################################

        self.setLayout(vbox)


    def add_btn_callback(self):
        question_str = self.editor_widget.question_editor.text
        answer_str = self.editor_widget.answer_editor.text
        tags_str = self.editor_widget.tags_editor.text

        if len(question_str.strip()) > 0 and len(tags_str.strip()):

            # Make the card and add it to the card list
            card = {
                    "cdate": datetime.date.today(),
                    "hidden": False,
                    "question": question_str,
                    "answer": answer_str,
                    "reviews": [],
                    "tags": [tag.strip() for tag in tags_str.split("\n") if tag.strip() != '']
                }

            self.card_list.append(card)

            # Erase editors
            self.editor_widget.question_editor.text = ""
            self.editor_widget.answer_editor.text = ""
            self.editor_widget.tags_editor.text = ""