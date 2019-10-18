#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opencal.core.professor.ltm.alice import ProfessorAlice
from opencal.core.professor.ltm.berenice import ProfessorBerenice

from opcgui.qt.widgets.tabs.test import TestTab
from opcgui.qt.widgets.tabs.add import AddCardsTab
from opcgui.qt.widgets.tabs.forwardtest import ForwardTestTab
from opcgui.qt.widgets.tabs.review import ReviewTab
from opcgui.qt.widgets.tabs.stats import StatsTab
from opcgui.qt.widgets.tabs.tags import TagsTab
from opcgui import APPLICATION_NAME

import os
import tempfile

from PyQt5.QtWidgets import QMainWindow, QTabWidget

class MainWindow(QMainWindow):

    def __init__(self, card_list, app_config):
        super().__init__()

        self.card_list = card_list
        self.app_config = app_config

        self.context_directory = tempfile.TemporaryDirectory()  # Make a temporary directory to store external files (JS, medias, ...)

        self.resize(1200, 900)
        self.setWindowTitle(APPLICATION_NAME)
        self.statusBar().showMessage("Ready", 2000)

        # Set Professor ###################################

        if self.app_config["ltm_professor"] == "alice":
            self.professor = ProfessorAlice(self.card_list)
        elif self.app_config["ltm_professor"] == "berenice":
            berenice_config = {key: value for key, value in self.app_config.items() if key in ("max_cards_per_grade", "tag_priority_dict", "tag_difficulty_dict")}
            self.professor = ProfessorBerenice(self.card_list, **berenice_config)
        else:
            raise ValueError('Unknown professor "{}"'.format(self.app_config["professor"]))

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
        mathjax_src_path = self.app_config['mathjax_path']
        mathjax_dst_path = os.path.join(self.context_directory.name, "mathjax")
        os.symlink(mathjax_src_path, mathjax_dst_path)

        # Cards media (images, audio and video files)

        medias_src_path = os.path.expanduser(self.app_config['pkb_medias_path'])
        medias_dst_path = os.path.join(self.context_directory.name, "materials")
        os.symlink(medias_src_path, medias_dst_path)

        # Show ############################################

        self.show()
