#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit

import opencal.core.tags

class TagsTab(QWidget):

    def __init__(self, card_list, parent):
        super().__init__(parent=parent)

        self.tabs = parent

        self.edit = QPlainTextEdit()

        tag_list = opencal.core.tags.tag_list_count(card_list, count_hidden_cards=False)
        text = "\n".join(["{:6d}   {}".format(tag[1], tag[0]) for tag in tag_list])

        self.edit.setPlainText(text)
        self.edit.setReadOnly(True)

        # Set the layout ###############

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.edit)
        self.setLayout(vbox)
