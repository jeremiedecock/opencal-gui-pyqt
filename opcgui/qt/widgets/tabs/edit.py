#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

import qtme

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QPushButton, QLabel

from opcgui.qt.widgets.tagseditor import TagsEditor

class EditCardsTab(QWidget):

    def __init__(self, card_list, context_directory, main_window, parent):
        super().__init__(parent=parent)

        self.card_list = card_list
        self.context_directory = context_directory
        self.tabs = parent

        # Make widgets ####################################

        self.splitter = QSplitter(orientation=Qt.Vertical, parent=self)

        self.question_editor = qtme.widgets.QMultimediaEditor(parent=self, layout="stacked", html_scale=0.8, placeholder_text="Question", stacked_default_widget="editor", title="Question")
        self.answer_editor = qtme.widgets.QMultimediaEditor(parent=self, layout="stacked", html_scale=0.8, placeholder_text="Answer", stacked_default_widget="editor", title="Answer")
        self.tags_editor = TagsEditor(self.card_list, parent=self)

        self.save_button = QPushButton('Save', self)
        self.cancel_button = QPushButton('Cancel', self)

        self.splitter.addWidget(self.question_editor)
        self.splitter.addWidget(self.answer_editor)
        self.splitter.addWidget(self.tags_editor)

        # Define the default relative size of widgets in the splitter
        # Warning: The setSizes() method is absolute not relative, it sets the sizes to actual pixel sizes;
        #          the setStretchFactor() method is relative, it sets the sizes relative to each other.
        # See https://stackoverflow.com/questions/29537762/pyqt-qsplitter-setsizes-usage
        # See https://stackoverflow.com/questions/43831474/how-to-equally-distribute-the-width-of-qsplitter
        self.splitter.setStretchFactor(0, 45)
        self.splitter.setStretchFactor(1, 45)
        self.splitter.setStretchFactor(2, 10)

        # Set slots #######################################

        self.save_button.clicked.connect(self.save_btn_callback)
        self.cancel_button.clicked.connect(self.cancel_btn_callback)

        # Make layouts ####################################

        vbox = QVBoxLayout(self)

        # VBox

        vbox.addWidget(self.splitter)
        vbox.addWidget(self.save_button)
        vbox.addWidget(self.cancel_button)

        # Set layouts #####################################

        self.setLayout(vbox)


    def save_btn_callback(self):
        question_str = self.question_editor.text
        answer_str = self.answer_editor.text
        tags_str = self.tags_editor.text

        if len(question_str.strip()) > 0 and len(tags_str.strip()):

            pass  # TODO

        #     # Make the card and add it to the card list
        #     card = {
        #             "cdate": datetime.date.today(),
        #             "hidden": False,
        #             "question": question_str,
        #             "answer": answer_str,
        #             "reviews": [],
        #             "tags": [tag.strip() for tag in tags_str.split("\n") if tag.strip() != '']
        #         }

        #     self.card_list.append(card)


    def cancel_btn_callback(self):
        self.question_editor.text = ""  # TODO
        self.answer_editor.text = ""    # TODO
        self.tags_editor.text = ""      # TODO