#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QTabWidget

from opcgui.qt.widgets.tabs.test import TestTab
from opcgui.qt.widgets.tabs.stats import StatsTab
from opcgui import APPLICATION_NAME

class MainWindow(QMainWindow):

    def __init__(self, professor, card_list):
        super().__init__()

        self.professor = professor
        self.card_list = card_list

        self.resize(1200, 900)
        self.setWindowTitle(APPLICATION_NAME)
        self.statusBar().showMessage("Ready", 2000)

        # Make widgets ####################################

        self.tabs = QTabWidget(parent=self)
        self.setCentralWidget(self.tabs)

        # Add tabs
        self.daily_test_tab = TestTab(self.professor, parent=self.tabs)
        self.stats_tab = StatsTab(self.card_list, parent=self.tabs)

        self.tabs.addTab(self.daily_test_tab, "Daily test")
        self.tabs.addTab(self.stats_tab, "Stats")

        # Show ############################################

        self.show()
