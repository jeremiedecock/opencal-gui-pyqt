#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

import opencal
from opencal.core.professor.itm.ralph import ProfessorRalph
from opencal.core.professor.itm.randy import ProfessorRandy
from opencal.core.professor.itm.denis import ProfessorDenis
from opencal.core.professor.itm.ernest import ProfessorErnest
from opencal.core.professor.itm.arthur import ProfessorArthur
from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

import opcgui
import opcgui.utils

from opcgui.qt.widgets.test import TestWidget

from PySide6.QtWidgets import QWidget, QComboBox, QVBoxLayout

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

        stm_professor_name = opencal.cfg["opencal"]["stm_professor"].lower()

        if stm_professor_name == "ralf":
            self.professor = ProfessorRalph(self.current_card_list)
        elif stm_professor_name == "randy":
            self.professor = ProfessorRandy(self.current_card_list)
        elif stm_professor_name == "denis":
            self.professor = ProfessorDenis(self.current_card_list, opencal.cfg["opencal"]["professors"]["denis"]["cards_in_progress_increment_size"])
        elif stm_professor_name == "ernest":
            self.professor = ProfessorErnest(self.current_card_list, opencal.cfg["opencal"]["professors"]["ernest"]["cards_in_progress_increment_size"])
        elif stm_professor_name == "arthur":
            self.professor = ProfessorArthur(self.current_card_list,
                                             opencal.cfg["opencal"]["professors"]["arthur"]["cards_in_progress_increment_size"],
                                             opencal.cfg["opencal"]["professors"]["arthur"]["right_answers_rate_threshold"])
        else:
            raise ValueError("Unknown STM professor", stm_professor_name)

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
            self.current_card_list = [card for card in self.orig_card_list if opcgui.utils.has_been_created_today(card, today=self.today) and not card["hidden"]]
        elif selection_str == WRONG_CARDS_STR:
            self.current_card_list = [card for card in self.orig_card_list if opcgui.utils.has_been_reviewed_today(card, wrong_answers_only=True, today=self.today) and not card["hidden"]]
        else:
            raise ValueError("Unknown value " + selection_str)

        self.professor.update_card_list(self.current_card_list)

        self.test_widget.update_html()
