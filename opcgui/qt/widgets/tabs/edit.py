#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QPushButton

from opcgui.qt.widgets.searchwiget import SearchWidget
from opcgui.qt.widgets.editorwidget import EditorWidget

class EditCardsTab(QWidget):

    def __init__(self, card_list, main_window, parent):
        super().__init__(parent=parent)

        self.card_list = card_list

        # Make widgets ####################################

        self.horizontal_splitter = QSplitter(orientation=Qt.Horizontal, parent=self)

        self.search_widget = SearchWidget(self.card_list, parent=self)
        self.editor_widget = EditorWidget(self.card_list, parent=self)

        self.horizontal_splitter.addWidget(self.search_widget)
        self.horizontal_splitter.addWidget(self.editor_widget)

        self.save_button = QPushButton('Save', self)
        self.cancel_button = QPushButton('Cancel', self)

        # Define the default relative size of widgets in the splitter
        # Warning: The setSizes() method is absolute not relative, it sets the sizes to actual pixel sizes;
        #          the setStretchFactor() method is relative, it sets the sizes relative to each other.
        # See https://stackoverflow.com/questions/29537762/pyqt-qsplitter-setsizes-usage
        # See https://stackoverflow.com/questions/43831474/how-to-equally-distribute-the-width-of-qsplitter
        self.horizontal_splitter.setStretchFactor(0, 20)
        self.horizontal_splitter.setStretchFactor(1, 80)

        # Set slots #######################################

        self.save_button.clicked.connect(self.save_btn_callback)
        self.cancel_button.clicked.connect(self.cancel_btn_callback)

        # Make layouts ####################################

        vbox = QVBoxLayout(self)

        vbox.addWidget(self.horizontal_splitter)
        vbox.addWidget(self.save_button)
        vbox.addWidget(self.cancel_button)

        # Set layouts #####################################

        self.setLayout(vbox)


    def save_btn_callback(self):
        question_str = self.editor_widget.question_editor.text
        answer_str = self.editor_widget.answer_editor.text
        tags_str = self.editor_widget.tags_editor.text

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
        self.editor_widget.question_editor.text = ""  # TODO
        self.editor_widget.answer_editor.text = ""    # TODO
        self.editor_widget.tags_editor.text = ""      # TODO