#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from opencal.core.professor.itm.ralph import ProfessorRalph
from opencal.core.professor.itm.randy import ProfessorRandy

from opcgui.qt.widgets.test import TestWidget

from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout

NEW_CARDS_STR = "New cards"
WRONG_CARDS_STR = "Tested cards (with wrong answer)"

class ReviewTab(QWidget):

    def __init__(self, card_list, context_directory, main_window, parent=None, date_mock=None):
        super().__init__(parent=parent)

        if date_mock is None:
            self.today = datetime.date.today()
        else:
            self.today = date_mock.today()

        self.orig_card_list = card_list
        self.current_card_list = []

        #self.professor = ProfessorRalph(self.current_card_list)
        self.professor = ProfessorRandy(self.current_card_list)

        # Make widgets ####################################

        self.combo_selection = QComboBox()
        self.combo_selection.addItems([NEW_CARDS_STR, WRONG_CARDS_STR])
        self.combo_selection.currentIndexChanged.connect(self.update_selection)

        self.test_widget = TestWidget(professor=self.professor, context_directory=context_directory, main_window=main_window, parent=parent)

        # Make layouts ####################################

        self.vbox = QVBoxLayout(self)

        # VBox

        self.vbox.addWidget(self.combo_selection)
        self.vbox.addWidget(self.test_widget)

        # Set layouts #####################################

        self.setLayout(self.vbox)

    def update_selection(self, index):
        selection_str = self.combo_selection.currentText()

        if selection_str == NEW_CARDS_STR:
            self.current_card_list = [card for card in self.orig_card_list if datetime_to_date(card["cdate"]) == self.today]
        elif selection_str == WRONG_CARDS_STR:
            self.current_card_list = [card for card in self.orig_card_list if has_been_reviewed_today(card, self.today)]
        else:
            raise ValueError("Unknown value " + selection_str)

        self.professor.update_card_list(self.current_card_list)

        self.test_widget.update_html()


def has_been_reviewed_today(card, today):
    ret = False

    if "reviews" in card.keys():
        for review in card["reviews"]:
            if datetime_to_date(review["rdate"]) == today:
                ret = True
    
    return ret


def datetime_to_date(d):
    '''If the object is an instance of datetime.datetime then convert it to a datetime.datetime.date object.

    If it's already a date object, do nothing.'''

    if isinstance(d, datetime.datetime):
        d = d.date()
    return d
