#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opencal.core.professor.ltm.brutus import ProfessorBrutus
from opencal.core.tags import tag_list

from opcgui.qt.widgets.test import TestWidget
from opcgui.utils import datetime_to_date

from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QVBoxLayout, QLineEdit, QFormLayout, QCompleter, QSpinBox

import datetime

REMAINING_CARDS_LABEL = "Reviewed or skipped cards: {}     Remaining: {} / {}"

class ForwardTestTab(QWidget):

    def __init__(self, card_list, context_directory, main_window, parent=None):
        super().__init__(parent=parent)

        max_grade = max([card["grade"] for card in card_list if "grade" in card])

        self.ltm_card_list = card_list
        self.current_card_list = []
        self.num_total_cards = 0

        self.tags = [""] + tag_list(self.ltm_card_list, sort="asc")

        self.professor = ProfessorBrutus(self.current_card_list)
        self.professor.add_reply_observer(self)

        # Make widgets ####################################

        self.num_remaining_cards_label = QLabel(REMAINING_CARDS_LABEL.format(0, 0, 0))

        self.line_edit_contains_filter = QLineEdit()
        self.line_edit_contains_filter.setPlaceholderText("Filter pattern (on question and answer)")
        self.line_edit_contains_filter.textChanged.connect(self.filter_line_edit_callback)

        self.combo_tag_filter = QComboBox()
        self.combo_tag_filter.addItems(self.tags)
        self.combo_tag_filter.setEditable(True)
        self.combo_tag_filter.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.combo_tag_filter.currentIndexChanged.connect(self.filter_combo_callback)

        self.combo_card_level = QComboBox()
        self.combo_card_level.addItems([""] + [str(x) for x in range(max_grade)] + ["-1"])
        self.combo_card_level.setEditable(True)
        self.combo_card_level.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.combo_card_level.currentIndexChanged.connect(self.card_level_combo_callback)

        self.spinbox_null_period = QSpinBox()
        self.spinbox_null_period.setMinimum(0)
        #self.spinbox_null_period.setPlaceholderText("Minimum number of days since the last assessment")
        self.spinbox_null_period.valueChanged.connect(self.null_period_spinbox_callback)

        self.test_widget = TestWidget(professor=self.professor, context_directory=context_directory, main_window=main_window, parent=parent)

        # Make layouts ####################################

        self.vbox = QVBoxLayout(self)
        filter_layout = QFormLayout()

        # Filter form

        filter_layout.addRow("Contains:", self.line_edit_contains_filter)
        filter_layout.addRow("Tag:", self.combo_tag_filter)
        filter_layout.addRow("Card level:", self.combo_card_level)
        filter_layout.addRow("Min. num. of days since the last assessment:", self.spinbox_null_period)

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


    def card_level_combo_callback(self):
        self.update_selection_callback()
        self.combo_card_level.setFocus()            # Workaround: without this line, the lineedit widget loose focus after each HTML update...


    def null_period_spinbox_callback(self):
        self.update_selection_callback()


    def update_selection_callback(self):
        content_text = self.line_edit_contains_filter.text()
        selected_tag = self.combo_tag_filter.currentText()
        card_level = self.combo_card_level.currentText()
        card_level = None if card_level == "" else int(card_level)
        null_period = self.spinbox_null_period.value()

        self.current_card_list = [card for card in self.ltm_card_list if review_card(card, selected_tag, content_text, null_period, card_level)]
        self.professor.update_card_list(self.current_card_list)

        self.num_total_cards = len(self.current_card_list)

        self.num_remaining_cards_label.setText(REMAINING_CARDS_LABEL.format(0, self.num_total_cards, self.num_total_cards))

        self.test_widget.update_html()


    def answer_callback(self):
        num_remaining_cards = self.professor.remaining_cards
        num_total_cards = self.num_total_cards
        num_reviewed_cards = num_total_cards - num_remaining_cards

        self.num_remaining_cards_label.setText(REMAINING_CARDS_LABEL.format(num_reviewed_cards, num_remaining_cards, num_total_cards))


def review_card(card, selected_tag, content_text, null_period, card_level, date_mock=None):

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

    if (card_level is not None) and (card["grade"] != card_level):
        return False
    
    if (content_text != "") and (card["question"].lower().find(content_text.lower()) == -1) and (card["answer"].lower().find(content_text.lower()) == -1):
        return False

    if datetime_to_date(card["cdate"]) == today:
        return False

    if "reviews" not in card.keys():
        return True

    if len(card["reviews"]) == 0:
        return True

    card_not_reviewed_during_null_period = all([datetime_to_date(review["rdate"]) < today - datetime.timedelta(days=null_period) for review in card["reviews"]])   # Formerly "card_not_reviewed_today"
    if card_not_reviewed_during_null_period:
        return True
    else:
        return False
