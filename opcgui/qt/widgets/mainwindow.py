#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opencal.core.professor.ltm.alice import ProfessorAlice
from opencal.core.professor.ltm.berenice import ProfessorBerenice
from opencal.core.professor.ltm.celia import ProfessorCelia

import opcgui
from opcgui.qt.widgets.tabs.test import TestTab
from opcgui.qt.widgets.tabs.add import AddCardsTab
from opcgui.qt.widgets.tabs.forwardtest import ForwardTestTab
from opcgui.qt.widgets.tabs.review import ReviewTab
from opcgui.qt.widgets.tabs.stats import StatsTab
from opcgui.qt.widgets.tabs.tags import TagsTab
from opcgui import APPLICATION_NAME

import os
import tempfile

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction

class MainWindow(QMainWindow):

    def __init__(self, card_list):
        super().__init__()

        self.card_list = card_list

        self.context_directory = tempfile.TemporaryDirectory()  # Make a temporary directory to store external files (JS, medias, ...)

        self.resize(1200, 900)
        self.setWindowTitle(APPLICATION_NAME)
        self.statusBar().showMessage("Ready", 2000)

        # Set Professor ###################################

        if opcgui.config.ltm_professor == "alice":
            self.professor = ProfessorAlice(self.card_list)
        elif opcgui.config.ltm_professor == "berenice":
            berenice_config = {key: value for key, value in opcgui.config.__dict__.items() if key in ("max_cards_per_grade", "tag_priority_dict", "tag_difficulty_dict", "reverse_level_0")}
            self.professor = ProfessorBerenice(self.card_list, **berenice_config)
        elif opcgui.config.ltm_professor == "celia":
            celia_config = {key: value for key, value in opcgui.config.__dict__.items() if key in ("max_cards_per_grade", "tag_priority_dict", "tag_difficulty_dict", "reverse_level_0")}
            self.professor = ProfessorCelia(self.card_list, **celia_config)
        else:
            raise ValueError('Unknown professor "{}"'.format(opcgui.config.professor))

        # Make widgets ####################################

        self.tabs = QTabWidget(parent=self)
        self.setCentralWidget(self.tabs)

        # Add tabs
        self.daily_test_tab = TestTab(self.professor, self.context_directory, main_window=self, parent=self.tabs)
        self.add_cards_tab = AddCardsTab(self.card_list, self.context_directory, main_window=self, parent=self.tabs)
        self.forward_test_tab = ForwardTestTab(self.card_list, self.context_directory, main_window=self, parent=self.tabs)
        self.review_tab = ReviewTab(self.card_list, self.context_directory, main_window=self, parent=self.tabs)
        self.stats_tab = StatsTab(self.card_list, parent=self.tabs)
        self.tags_tab = TagsTab(self.card_list, parent=self.tabs)

        self.tabs.addTab(self.daily_test_tab, "Daily test")
        self.tabs.addTab(self.add_cards_tab, "Add Cards")
        self.tabs.addTab(self.forward_test_tab, "Forward test")
        self.tabs.addTab(self.review_tab, "Review")
        self.tabs.addTab(self.tags_tab, "Tags")
        self.tabs.addTab(self.stats_tab, "Stats")

        # Make the context directory ######################

        print('Make the context directory:', self.context_directory)

        # Mathjax

        # Install MathJax on Debian: "aptitude install libjs-mathjax"
        mathjax_src_path = opcgui.config.mathjax_path
        mathjax_dst_path = os.path.join(self.context_directory.name, "mathjax")
        os.symlink(mathjax_src_path, mathjax_dst_path)

        # Cards media (images, audio and video files)

        medias_src_path = os.path.expanduser(opcgui.config.pkb_medias_path)
        medias_dst_path = os.path.join(self.context_directory.name, "materials")
        os.symlink(medias_src_path, medias_dst_path)

        # Set the menu bar ################################

        # Make the Action object
        font_small_action = QAction('Font &Small', self)
        #font_small_action.setShortcut('Ctrl+z+1')
        font_small_action.setStatusTip("Font small")
        font_small_action.triggered.connect(self.font_small_calback)

        font_normal_action = QAction('Font &Normal', self)
        #font_normal_action.setShortcut('Ctrl+z+2')
        font_normal_action.setStatusTip("Font normal")
        font_normal_action.triggered.connect(self.font_normal_calback)

        font_large_action = QAction('Font &Large', self)
        #font_large_action.setShortcut('Ctrl+z+3')
        font_large_action.setStatusTip("Font large")
        font_large_action.triggered.connect(self.font_large_calback)

        menu = self.menuBar()
        config_menu = menu.addMenu("&Configuration")
        config_menu.addAction(font_small_action)
        config_menu.addAction(font_normal_action)
        config_menu.addAction(font_large_action)

        # Show ############################################

        self.show()

    def set_webview_html_scale(self, html_scale):
        opcgui.config.html_scale = html_scale

        for test_widget in (self.daily_test_tab, self.forward_test_tab.test_widget, self.review_tab.test_widget):
            if test_widget.stack_layout.currentWidget() == test_widget.navigation_widget:
                test_widget.update_html(show_answer=False)
            if test_widget.stack_layout.currentWidget() == test_widget.answer_widget:
                test_widget.update_html(show_answer=True)

    def font_small_calback(self):
        self.set_webview_html_scale(html_scale=0.6)

    def font_normal_calback(self):
        self.set_webview_html_scale(html_scale=1.0)

    def font_large_calback(self):
        self.set_webview_html_scale(html_scale=2.5)