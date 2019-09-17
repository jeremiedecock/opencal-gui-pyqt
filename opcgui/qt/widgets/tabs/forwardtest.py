#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opencal.core.professor.ltm.brutus import ProfessorBrutus
from opencal.core.tags import tag_list

from opcgui.qt.widgets.test import TestWidget

from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout

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

        self.current_card_list = [card for card in self.orig_card_list if selected_tag in card["tags"]]
        self.professor.update_card_list(self.current_card_list)

        self.test_widget.update_html()
