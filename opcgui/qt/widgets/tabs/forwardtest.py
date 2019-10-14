#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opencal.core.professor.ltm.brutus import ProfessorBrutus
from opencal.core.tags import tag_list

from opcgui.qt.widgets.test import TestWidget
from opcgui.utils import datetime_to_date

from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout

import datetime

class ForwardTestTab(QWidget):

    def __init__(self, card_list, context_directory, main_window, parent=None):
        super().__init__(parent=parent)

        self.orig_card_list = card_list
        self.current_card_list = []

        self.tags = tag_list(self.orig_card_list, sort="asc")

        self.professor = ProfessorBrutus(self.current_card_list)

        # Make widgets ####################################

        self.combo_tag_selection = QComboBox()
        self.combo_tag_selection.addItems(self.tags)
        self.combo_tag_selection.currentIndexChanged.connect(self.update_selection)

        self.test_widget = TestWidget(professor=self.professor, context_directory=context_directory, main_window=main_window, parent=parent)

        # Make layouts ####################################

        self.vbox = QVBoxLayout(self)

        # VBox

        self.vbox.addWidget(self.combo_tag_selection)
        self.vbox.addWidget(self.test_widget)

        # Set layouts #####################################

        self.setLayout(self.vbox)

    def update_selection(self, index):
        selected_tag = self.combo_tag_selection.currentText()

        self.current_card_list = [card for card in self.orig_card_list if review_card(card, selected_tag)]
        self.professor.update_card_list(self.current_card_list)

        self.test_widget.update_html()


def review_card(card, selected_tag, date_mock=None):

    if date_mock is None:
        today = datetime.date.today()
    else:
        today = date_mock.today()

    if card["hidden"]:
        return False

    if not selected_tag in card["tags"]:
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
