#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opencal.core.professor.ltm.brutus import ProfessorBrutus
from opencal.core.tags import tag_list

from opcgui.qt.widgets.test import TestWidget
from opcgui.utils import datetime_to_date

from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QVBoxLayout, QLineEdit, QFormLayout, QCompleter

import datetime

class ForwardTestTab(QWidget):

    def __init__(self, card_list, context_directory, main_window, parent=None):
        super().__init__(parent=parent)

        self.orig_card_list = card_list
        self.current_card_list = []

        self.tags = [""] + tag_list(self.orig_card_list, sort="asc")

        self.professor = ProfessorBrutus(self.current_card_list)

        # Make widgets ####################################

        self.num_remaining_cards_label = QLabel("Selected cards: 0")

        self.line_edit_contains_filter = QLineEdit()
        self.line_edit_contains_filter.setPlaceholderText("Filter pattern (on question and answer)")
        self.line_edit_contains_filter.textChanged.connect(self.filter_line_edit_callback)

        self.combo_tag_filter = QComboBox()
        self.combo_tag_filter.addItems(self.tags)
        self.combo_tag_filter.setEditable(True)
        self.combo_tag_filter.completer().setCompletionMode(QCompleter.PopupCompletion)

        self.combo_tag_filter.currentIndexChanged.connect(self.filter_combo_callback)

        self.test_widget = TestWidget(professor=self.professor, context_directory=context_directory, main_window=main_window, parent=parent)

        # Make layouts ####################################

        self.vbox = QVBoxLayout(self)
        filter_layout = QFormLayout()

        # Filter form

        filter_layout.addRow("Contains:", self.line_edit_contains_filter)
        filter_layout.addRow("Tag:", self.combo_tag_filter)

        # VBox

        self.vbox.addLayout(filter_layout)
        self.vbox.addWidget(self.num_remaining_cards_label)
        self.vbox.addWidget(self.test_widget)

        # Set layouts #####################################

        self.setLayout(self.vbox)


    def filter_line_edit_callback(self):
        self.update_selection_callback()
        self.line_edit_contains_filter.setFocus()   # Workaround: without this line, the lineedit widget loose focus after each HTML update...


    def filter_combo_callback(self, index):
        self.update_selection_callback()


    def update_selection_callback(self):
        content_text = self.line_edit_contains_filter.text()
        selected_tag = self.combo_tag_filter.currentText()

        self.current_card_list = [card for card in self.orig_card_list if review_card(card, selected_tag, content_text)]
        self.professor.update_card_list(self.current_card_list)

        self.num_remaining_cards_label.setText("Selected cards: {}".format(len(self.current_card_list)))

        self.test_widget.update_html()


def review_card(card, selected_tag, content_text, date_mock=None):

    if date_mock is None:
        today = datetime.date.today()
    else:
        today = date_mock.today()

    if card["hidden"]:
        return False

    # If nothing has been selected, the selection is empty
    if (selected_tag == "") and (content_text == ""):
        return False

    if (selected_tag != "") and (not selected_tag in card["tags"]):
        return False
    
    if (content_text != "") and (card["question"].lower().find(content_text.lower()) == -1) and (card["answer"].lower().find(content_text.lower()) == -1):
        return False

    if datetime_to_date(card["cdate"]) == today:
        return False

    if "reviews" not in card.keys():
        return True

    if len(card["reviews"]) == 0:
        return True

    card_not_reviewed_today = all([datetime_to_date(review["rdate"]) < today for review in card["reviews"]])
    if card_not_reviewed_today:
        return True
    else:
        return False
