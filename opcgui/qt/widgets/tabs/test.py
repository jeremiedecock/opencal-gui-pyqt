#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from opcgui.qt.widgets.test import TestWidget

class TestTab(TestWidget):

    def __init__(self, professor, context_directory, main_window, parent=None):
        super().__init__(professor=professor, context_directory=context_directory, main_window=main_window, parent=parent)

