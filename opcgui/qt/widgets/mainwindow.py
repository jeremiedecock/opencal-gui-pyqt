#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opencal
from opencal.core.professor.ltm.alice import ProfessorAlice
from opencal.core.professor.ltm.berenice import ProfessorBerenice
from opencal.core.professor.ltm.celia import ProfessorCelia
from opencal.core.professor.ltm.doreen import ProfessorDoreen

import opcgui
from opcgui.qt.widgets.tabs.test import TestTab
from opcgui.qt.widgets.tabs.add import AddCardsTab
from opcgui.qt.widgets.tabs.edit import EditCardsTab
from opcgui.qt.widgets.tabs.forwardtest import ForwardTestTab
from opcgui.qt.widgets.tabs.review import ReviewTab
from opcgui.qt.widgets.tabs.stats import StatsTab
from opcgui.qt.widgets.tabs.tags import TagsTab
from opcgui import APPLICATION_NAME

import os
import tempfile
import warnings

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QTabWidget

SMALL_SCALE = 0.6
MEDIUM_SCALE = 1.0
LARGE_SCALE = 2.5

class MainWindow(QMainWindow):

    def __init__(self, card_list):
        super().__init__()

        self.card_list = card_list

        self.context_directory = tempfile.TemporaryDirectory()  # Make a temporary directory to store external files (JS, medias, ...)

        self.resize(1200, 900)
        self.setWindowTitle(APPLICATION_NAME)
        self.statusBar().showMessage("Ready", 2000)

        # Set Professor ###################################

        ltm_professor_name = opencal.cfg["opencal"]["ltm_professor"]

        professor_config = {}
        professor_config.update(opencal.cfg["opencal"]["professors"]["common"])
        try:
            professor_config.update(opencal.cfg["opencal"]["professors"][ltm_professor_name])
        except KeyError:
            warnings.warn(f'No configuration found for professor "{ltm_professor_name}"')

        if ltm_professor_name == "alice":
            self.professor = ProfessorAlice(self.card_list)
        elif ltm_professor_name == "berenice":
            professor_config = {key: value for key, value in professor_config.items() if key in ("max_cards_per_grade", "tag_priorities", "tag_difficulties", "reverse_level_0")}
            self.professor = ProfessorBerenice(self.card_list, **professor_config)
        elif ltm_professor_name == "celia":
            professor_config = {key: value for key, value in professor_config.items() if key in ("max_cards_per_grade", "tag_priorities", "tag_difficulties")}
            self.professor = ProfessorCelia(self.card_list, **professor_config)
        elif ltm_professor_name == "doreen":
            professor_config = {key: value for key, value in professor_config.items() if key in ("max_cards_per_grade", "tag_priorities", "tag_difficulties", "priorities_per_level")}
            self.professor = ProfessorDoreen(self.card_list, **professor_config)
        else:
            raise ValueError(f'Unknown professor "{ltm_professor_name}"')

        # Make widgets ####################################

        self.tabs = QTabWidget(parent=self)
        self.tabs.currentChanged.connect(self.update_tab)
        self.setCentralWidget(self.tabs)

        # Add tabs
        self.daily_test_tab = TestTab(self.professor, self.context_directory, main_window=self, parent=self.tabs)
        self.add_cards_tab = AddCardsTab(self.card_list, main_window=self, parent=self.tabs)
        self.edit_cards_tab = EditCardsTab(self.card_list, main_window=self)
        self.forward_test_tab = ForwardTestTab(self.card_list, self.context_directory, main_window=self, parent=self.tabs)
        self.review_tab = ReviewTab(self.card_list, self.context_directory, main_window=self, parent=self.tabs)
        self.stats_tab = StatsTab(self.card_list, parent=self.tabs)
        self.tags_tab = TagsTab(self.card_list, parent=self.tabs)

        self.tabs.addTab(self.daily_test_tab, "Daily test")
        self.tabs.addTab(self.add_cards_tab, "Add Cards")
        self.tabs.addTab(self.edit_cards_tab, "Edit Cards")
        self.tabs.addTab(self.forward_test_tab, "Forward test")
        self.tabs.addTab(self.review_tab, "Review")
        self.tabs.addTab(self.tags_tab, "Tags")
        self.tabs.addTab(self.stats_tab, "Stats")

        # Make the context directory ######################

        print('Make the context directory:', self.context_directory)

        # Mathjax

        # Install MathJax on Debian: "aptitude install libjs-mathjax"
        mathjax_src_path = opencal.cfg["opencal_ui"]["mathjax_path"]
        mathjax_dst_path = os.path.join(self.context_directory.name, "mathjax")           # TODO!
        os.symlink(mathjax_src_path, mathjax_dst_path)

        # Cards media (images, audio and video files)

        medias_src_path = os.path.expanduser(opencal.cfg["opencal"]["db_assets_path"])
        medias_dst_path = os.path.join(self.context_directory.name, "materials")          # TODO!
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

        # Zoom in

        zoom_in_action = QAction(self)
        zoom_in_action.setShortcut(Qt.Key_Plus)
        zoom_in_action.setShortcutContext(Qt.WindowShortcut)

        zoom_in_action.triggered.connect(self.zoom_in_callback)
        self.addAction(zoom_in_action)

        # Zoom out

        zoom_out_action = QAction(self)
        zoom_out_action.setShortcut(Qt.Key_Minus)
        zoom_out_action.setShortcutContext(Qt.WindowShortcut)

        zoom_out_action.triggered.connect(self.zoom_out_callback)
        self.addAction(zoom_out_action)

        # Show ############################################

        self.show()


    def update_tab(self, index):
        if hasattr(self.tabs.currentWidget(), "update_callback"):
            self.tabs.currentWidget().update_callback()


    def get_webview_html_scale(self):
        try:
            html_scale = opencal.cfg["opencal_ui"]["html_scale"]
        except KeyError:
            html_scale = MEDIUM_SCALE

        return html_scale


    def set_webview_html_scale(self, html_scale):
        opencal.cfg["opencal_ui"]["html_scale"] = html_scale

        for test_widget in (self.daily_test_tab, self.forward_test_tab.test_widget, self.review_tab.test_widget):
            test_widget.web_view.setZoomFactor(html_scale)


    def zoom_in_callback(self):
        current_scale = self.get_webview_html_scale()

        if current_scale == SMALL_SCALE:
            self.set_webview_html_scale(html_scale=MEDIUM_SCALE)
        elif current_scale == MEDIUM_SCALE:
            self.set_webview_html_scale(html_scale=LARGE_SCALE)

    def zoom_out_callback(self):
        current_scale = self.get_webview_html_scale()

        if current_scale == MEDIUM_SCALE:
            self.set_webview_html_scale(html_scale=SMALL_SCALE)
        elif current_scale == LARGE_SCALE:
            self.set_webview_html_scale(html_scale=MEDIUM_SCALE)


    def font_small_calback(self):
        self.set_webview_html_scale(html_scale=SMALL_SCALE)

    def font_normal_calback(self):
        self.set_webview_html_scale(html_scale=MEDIUM_SCALE)

    def font_large_calback(self):
        self.set_webview_html_scale(html_scale=LARGE_SCALE)