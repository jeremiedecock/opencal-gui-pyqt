#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import Any, Optional, Union, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from opencal.card import Card

from opcgui.qt.widgets.editorwidget import EditorWidget

class AddCardsTab(QWidget):

    def __init__(
            self,
            card_list: List[Card],
            main_window,
            parent):
        super().__init__()

        self.card_list = card_list
        self.tabs = parent

        # Make widgets ####################################

        self.editor_widget = EditorWidget(self.card_list, stacked_default_widget="editor")

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

        if len(question_str.strip()) > 0 and len(tags_str.strip()) > 0:

            # Make the card and add it to the card list
            card = Card(
                creation_datetime=datetime.date.today(),
                question=question_str,
                answer=answer_str,
                is_hidden=False,
                tags=[tag.strip() for tag in tags_str.split("\n") if tag.strip() != ''],
                consolidation_reviews=[]
            )

            self.card_list.append(card)

            # Erase editors
            self.editor_widget.question_editor.text = ""
            self.editor_widget.answer_editor.text = ""
            #self.editor_widget.tags_editor.text = ""