#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QCheckBox, QPushButton, QListWidget, QLabel, QCompleter

class SearchWidget(QWidget):

    def __init__(self, card_list, parent=None):
        super().__init__(parent=parent)

        self.card_list = card_list

        # Make widgets ####################################

        self.search_mode_combo = QComboBox(parent=self)
        self.search_mode_combo.addItems([
            "All Cards",
            "Reviewed Cards",
            "New Cards",
            "Hidden Cards"
        ])
        self.search_mode_combo.setCurrentIndex(1)
        self.search_mode_combo.currentIndexChanged.connect(self.update_search_mode)

        self.tags_combo = QComboBox(parent=self)
        self.tags_combo.addItems([""])
        self.tags_combo.setEditable(True)
        self.tags_combo.completer().setCompletionMode(QCompleter.PopupCompletion)

        self.pattern_search_edit = QLineEdit(parent=self)
        self.pattern_search_edit.setPlaceholderText("Search")

        self.case_sensitive_checkbox = QCheckBox("Case sensitive", parent=self)
        self.show_hidden_cards_checkbox = QCheckBox("Show hidden cards", parent=self)

        self.card_list_widget = QListWidget(parent=self)
        self.card_list_widget.setTextElideMode(Qt.ElideRight)                      # See https://stackoverflow.com/questions/69343830/not-eliding-correctly-on-qlistview-in-windows-os
        self.card_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # See https://stackoverflow.com/questions/69343830/not-eliding-correctly-on-qlistview-in-windows-os

        # Make layouts ####################################

        vbox = QVBoxLayout(parent=self)
        #vbox.setContentsMargins(0, 0, 0, 0)

        vbox.addWidget(self.search_mode_combo)
        vbox.addWidget(self.tags_combo)
        vbox.addWidget(self.pattern_search_edit)
        vbox.addWidget(self.case_sensitive_checkbox)
        vbox.addWidget(self.show_hidden_cards_checkbox)
        vbox.addWidget(self.card_list_widget)

        # Set layouts #####################################

        self.setLayout(vbox)

        # Update state ####################################

        self.update_search_mode()


    def update_search_mode(self, index=None):
        selected_mode = self.search_mode_combo.currentText()

        if selected_mode == "All Cards":
            self.show_hidden_cards_checkbox.show()
        elif selected_mode == "Reviewed Cards":
            self.show_hidden_cards_checkbox.hide()
        elif selected_mode == "New Cards":
            self.show_hidden_cards_checkbox.hide()
        elif selected_mode == "Hidden Cards":
            self.show_hidden_cards_checkbox.hide()
        else:
            raise ValueError(f"Unknown search mode: {selected_mode}")
