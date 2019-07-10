#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QTabWidget

from opcgui.qt.widgets.tabs.test import TestTab
from opcgui.qt.widgets.tabs.stats import StatsTab
from opcgui import APPLICATION_NAME

import os
import tempfile

class MainWindow(QMainWindow):

    def __init__(self, professor, card_list, app_config):
        super().__init__()

        self.app_config = app_config
        self.context_directory = tempfile.TemporaryDirectory()  # Make a temporary directory to store external files (JS, medias, ...)

        self.professor = professor
        self.card_list = card_list

        self.resize(1200, 900)
        self.setWindowTitle(APPLICATION_NAME)
        self.statusBar().showMessage("Ready", 2000)

        # Make widgets ####################################

        self.tabs = QTabWidget(parent=self)
        self.setCentralWidget(self.tabs)

        # Add tabs
        self.daily_test_tab = TestTab(self.professor, self.context_directory, main_window=self, parent=self.tabs)
        self.stats_tab = StatsTab(self.card_list, parent=self.tabs)

        self.tabs.addTab(self.daily_test_tab, "Daily test")
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
