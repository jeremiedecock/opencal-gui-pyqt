#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The next two lines are a workaround to fix an issue with QWebEngineView (see https://github.com/ContinuumIO/anaconda-issues/issues/9199#issuecomment-383842265)
import ctypes
ctypes.CDLL("libGL.so.1", mode=ctypes.RTLD_GLOBAL)

from PyQt5.QtCore import Qt, QModelIndex, QSortFilterProxyModel
from PyQt5.QtWidgets import QTableView, QWidget, QPushButton, QVBoxLayout, QAbstractItemView, \
    QAction, QPlainTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

class TestTab(QWidget):

    def __init__(self, data, parent=None):
        super().__init__(parent=parent)

        self.tabs = parent

        # Make widgets ####################################

        self.web_view = QWebEngineView(parent=self)

        self.btn_right_answer = QPushButton("Right", parent=self)
        self.btn_wrong_answer = QPushButton("Wrong", parent=self)
        self.btn_skip_card = QPushButton("Skip", parent=self)

        # Set layouts #####################################

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        # HBox

        self.hbox.addWidget(self.btn_right_answer)
        self.hbox.addWidget(self.btn_skip_card)
        self.hbox.addWidget(self.btn_wrong_answer)

        # VBox

        self.vbox.addWidget(self.web_view)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        # Set key shortcut ################################

        # see https://stackoverflow.com/a/17631703  and  http://doc.qt.io/qt-5/qaction.html#details

        # Right answer action

        right_answer_action = QAction(self.web_view)
        right_answer_action.setShortcut(Qt.Key_R)

        right_answer_action.triggered.connect(self.right_answer_btn_callback)
        self.web_view.addAction(right_answer_action)

        # Wrong answer action

        wrong_answer_action = QAction(self.web_view)
        wrong_answer_action.setShortcut(Qt.Key_W)

        wrong_answer_action.triggered.connect(self.wrong_answer_btn_callback)
        self.web_view.addAction(wrong_answer_action)

        # Skip card action

        skip_card_action = QAction(self.web_view)
        skip_card_action.setShortcut(Qt.CTRL | Qt.Key_Delete)

        skip_card_action.triggered.connect(self.skip_card_btn_callback)
        self.web_view.addAction(skip_card_action)

        # Hide card action

        hide_card_action = QAction(self.web_view)
        hide_card_action.setShortcut(Qt.Key_Delete)

        hide_card_action.triggered.connect(self.hide_card_btn_callback)
        self.web_view.addAction(hide_card_action)

        # Set slots #######################################

        self.btn_right_answer.clicked.connect(self.right_answer_btn_callback)
        self.btn_wrong_answer.clicked.connect(self.wrong_answer_btn_callback)
        self.btn_skip_card.clicked.connect(self.skip_card_btn_callback)

        # Set QWebEngineView ##############################

        self.web_view.setHtml("Hello")         # TODO
        self.web_view.show()


    def right_answer_btn_callback(self):
        print("Right")

    def wrong_answer_btn_callback(self):
        print("Wrong")

    def skip_card_btn_callback(self):
        print("Skip")

    def hide_card_btn_callback(self):
        print("Hide")