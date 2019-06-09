#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The next two lines are a workaround to fix an issue with QWebEngineView (see https://github.com/ContinuumIO/anaconda-issues/issues/9199#issuecomment-383842265)
import ctypes
ctypes.CDLL("libGL.so.1", mode=ctypes.RTLD_GLOBAL)

import datetime

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

from PyQt5.QtCore import Qt, QModelIndex, QSortFilterProxyModel
from PyQt5.QtWidgets import QTableView, QWidget, QPushButton, QVBoxLayout, QAbstractItemView, \
    QAction, QPlainTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QStackedLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QSizePolicy

class TestTab(QWidget):

    def __init__(self, professor, parent=None):
        super().__init__(parent=parent)

        self.professor = professor

        self.tabs = parent

        # Make widgets ####################################

        self.web_view = QWebEngineView(parent=self)
        self.control_widget = QWidget(parent=self)

        self.navigation_widget = QWidget(parent=self.control_widget)
        self.answer_widget = QWidget(parent=self.control_widget)

        self.btn_answer = QPushButton("Answer", parent=self.navigation_widget)
        self.btn_skip_card = QPushButton("Skip", parent=self.navigation_widget)
        self.btn_hide_card = QPushButton("Hide", parent=self.navigation_widget)

        self.btn_wrong_answer = QPushButton("Wrong", parent=self.answer_widget)
        self.btn_right_answer = QPushButton("Right", parent=self.answer_widget)

        # Set SizePolicy ##################################

        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)         # horizontal, vertical
        self.control_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)       # horizontal, vertical
        self.navigation_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)    # horizontal, vertical
        self.answer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)        # horizontal, vertical

        # Make layouts ####################################

        self.vbox = QVBoxLayout(self)

        self.hbox_navigation = QHBoxLayout(self.navigation_widget)
        self.hbox_answer = QHBoxLayout(self.answer_widget)

        self.stack_layout = QStackedLayout()

        # HBox

        self.hbox_navigation.addWidget(self.btn_hide_card)
        self.hbox_navigation.addWidget(self.btn_answer)
        self.hbox_navigation.addWidget(self.btn_skip_card)

        self.hbox_answer.addWidget(self.btn_wrong_answer)
        self.hbox_answer.addWidget(self.btn_right_answer)

        # VBox

        self.vbox.addWidget(self.web_view)
        self.vbox.addWidget(self.control_widget)

        # StackedLayout

        self.stack_layout.addWidget(self.navigation_widget)
        self.stack_layout.addWidget(self.answer_widget)

        self.stack_layout.setCurrentWidget(self.navigation_widget)

        # Set layouts #####################################

        self.control_widget.setLayout(self.stack_layout)

        self.navigation_widget.setLayout(self.hbox_navigation)
        self.answer_widget.setLayout(self.hbox_answer)

        self.setLayout(self.vbox)

        # Set key shortcut ################################

        # see https://stackoverflow.com/a/17631703  and  http://doc.qt.io/qt-5/qaction.html#details

        # Answer action

        answer_action = QAction(self)
        answer_action.setShortcut(Qt.Key_Space)
        answer_action.setShortcutContext(Qt.WindowShortcut)

        answer_action.triggered.connect(self.answer_btn_callback)
        self.addAction(answer_action)

        # Skip card action

        skip_card_action = QAction(self)
        skip_card_action.setShortcut(Qt.CTRL | Qt.Key_Delete)
        skip_card_action.setShortcutContext(Qt.WindowShortcut)

        skip_card_action.triggered.connect(self.skip_card_btn_callback)
        self.addAction(skip_card_action)

        # Hide card action

        hide_card_action = QAction(self)
        hide_card_action.setShortcut(Qt.Key_Delete)
        hide_card_action.setShortcutContext(Qt.WindowShortcut)

        hide_card_action.triggered.connect(self.hide_card_btn_callback)
        self.addAction(hide_card_action)

        # Right answer action

        right_answer_action = QAction(self)
        right_answer_action.setShortcut(Qt.Key_R)

        right_answer_action.triggered.connect(self.right_answer_btn_callback)
        self.addAction(right_answer_action)

        # Wrong answer action

        wrong_answer_action = QAction(self)
        wrong_answer_action.setShortcut(Qt.Key_W)

        wrong_answer_action.triggered.connect(self.wrong_answer_btn_callback)
        self.addAction(wrong_answer_action)

        # Set slots #######################################

        self.btn_answer.clicked.connect(self.answer_btn_callback)
        self.btn_skip_card.clicked.connect(self.skip_card_btn_callback)
        self.btn_hide_card.clicked.connect(self.hide_card_btn_callback)

        self.btn_right_answer.clicked.connect(self.right_answer_btn_callback)
        self.btn_wrong_answer.clicked.connect(self.wrong_answer_btn_callback)

        # Set QWebEngineView ##############################

        self.update_html(show_answer=False)


    def update_html(self, show_answer=False):
        current_card = self.professor.current_card

        html = current_card["question"]
        if show_answer:
            html += "<br>"
            html += current_card["answer"]

        self.web_view.setHtml(html)

    def answer_btn_callback(self):
        self.stack_layout.setCurrentWidget(self.answer_widget)
        self.update_html(show_answer=True)

    def skip_card_btn_callback(self):
        self.professor.current_card_reply(answer="skip", duration=None, confidence=None)
        self.update_html(show_answer=False)

    def hide_card_btn_callback(self):
        self.professor.current_card_reply(answer="hide", duration=None, confidence=None)
        self.update_html(show_answer=False)

    def right_answer_btn_callback(self):
        self.professor.current_card_reply(answer=RIGHT_ANSWER_STR, duration=None, confidence=None)
        self.stack_layout.setCurrentWidget(self.navigation_widget)
        self.update_html(show_answer=False)

    def wrong_answer_btn_callback(self):
        self.professor.current_card_reply(answer=WRONG_ANSWER_STR, duration=None, confidence=None)
        self.stack_layout.setCurrentWidget(self.navigation_widget)
        self.update_html(show_answer=False)