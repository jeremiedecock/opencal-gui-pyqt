#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, QRegularExpression
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTableView, QAbstractItemView

import opencal.core.tags

# TODO:
# - Implement dynamic updates of counts...
# - AJOUTER UNE CHECKBOX "Count hidden cards" -> BOF... pas très utile + attention ça va générer des bugs car les cartes cachées n'ont pas de "grade" par défaut !

class TagsTableModel(QAbstractTableModel):

    def __init__(self, parent):
        super().__init__(parent)
        self.tag_list = []

    def rowCount(self, parent):
        return len(self.tag_list)

    def columnCount(self, parent):
        if len(self.tag_list) == 0:
            return 0
        else:
            return len(self.tag_list[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if len(self.tag_list) > 0:
                row = index.row()
                column = index.column()
                return self.tag_list[row][column]
            else:
                return ""

    def headerData(self, index, orientation, role):
        num_columns = len(self.tag_list[0]) if len(self.tag_list) > 0 else 0

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if index == 0:
                    return "Tag"
                elif index == (num_columns - 1):
                    return "Total"
                elif index == (num_columns - 2):
                    return "Level -1"
                else:
                    return "Level {}".format(index - 1)
        return None


class TagsTab(QWidget):

    def __init__(self, card_list, parent):
        super().__init__(parent=parent)

        self.tabs = parent

        self.consolidation_card_list = card_list

        max_grade = max([card.grade for card in card_list if card.grade is not None])

        #self.edit = QPlainTextEdit()

        #text = "\n".join(["{:6d}   {}".format(tag[1], tag[0]) for tag in tag_list])

        #self.edit.setPlainText(text)
        #self.edit.setReadOnly(True)

        # Set widgets ##################

        # Line edit

        self.tag_filter_line_edit = QLineEdit()
        self.tag_filter_line_edit.setPlaceholderText("Tags filter")

        # Table view

        self.table_view = QTableView()
        self.tags_table_model = TagsTableModel(None)

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.tags_table_model)
        self.proxy_model.setFilterKeyColumn(0)

        self.table_view.setModel(self.proxy_model)

        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().hide()
        #self.table_view.setSortingEnabled(True)

        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)    # Select the full row when a cell is selected (See http://doc.qt.io/qt-5/qabstractitemview.html#selectionBehavior-prop )
        #self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)  # Set selection mode. See http://doc.qt.io/qt-5/qabstractitemview.html#selectionMode-prop

        self.table_view.setAlternatingRowColors(True)

        self.table_view.verticalHeader().setVisible(False)              # Hide the vertical header

        # Set data (tags) ##############

        #self.tags_table_model.tag_list = opencal.core.tags.tag_list_count(self.consolidation_card_list, count_hidden_cards=False)
        count_hidden_cards = False
        tag_dict = {}
        for card in card_list:
            if not card["hidden"] or count_hidden_cards:
                grade = card.grade if (card.grade is not None) else None   # Hidden cards don't have a grade by default (to speedup startup)
                for tag in card["tags"]:

                    if tag not in tag_dict:
                        tag_dict[tag] = [0] * (max_grade + 2)

                    if grade is not None:
                        if grade == -1:
                            tag_dict[tag][-2] += 1      # Grade -1 is on the penultimate column
                        else:
                            tag_dict[tag][grade] += 1

                    tag_dict[tag][-1] += 1
        
        self.tags_table_model.tag_list = [[k] + v for k, v in tag_dict.items()]

        # The following line are necessary e.g. to dynamically update the QSortFilterProxyModel
        #self.createIndex(0, 0)
        #self.createIndex(0, 1)
        self.tags_table_model.layoutChanged.emit()

        # Set the layout ###############

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.tag_filter_line_edit)
        vbox.addWidget(self.table_view)
        self.setLayout(vbox)

        self.table_view.show()

        # Misc ########################

        self.table_view.sortByColumn(0, Qt.AscendingOrder)
        #self.table_view.horizontalHeader().setStretchLastSection(True)
        #self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        #self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        #self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setColumnWidth(0, 300)

        # Set LineEdit slot #########################

        self.tag_filter_line_edit.textChanged.connect(self.tag_filter_callback)


    def tag_filter_callback(self):
        filter_str = self.tag_filter_line_edit.text()
        self.proxy_model.setFilterRegExp(QRegularExpression(filter_str, Qt.CaseInsensitive, QRegularExpression.FixedString))