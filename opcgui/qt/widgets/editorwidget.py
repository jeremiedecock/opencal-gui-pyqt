#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel, QCompleter

import qtme

from opcgui.qt.widgets.tagseditor import TagsEditor


class EditorWidget(QWidget):

    def __init__(self, card_list, stacked_default_widget="webview"):
        super().__init__()

        self.card_list = card_list              # this will be useful for auto-completion

        # Make widgets ####################################

        self.vertical_splitter = QSplitter(orientation=Qt.Vertical)

        self.question_editor = qtme.widgets.QMultimediaEditor(layout="stacked",
                                                              html_scale=1.,
                                                              placeholder_text="Question",
                                                              stacked_default_widget=stacked_default_widget,
                                                              title="Question",
                                                              disable_markdown_by_default=True)
        self.answer_editor = qtme.widgets.QMultimediaEditor(layout="stacked",
                                                            html_scale=1.,
                                                            placeholder_text="Answer",
                                                            stacked_default_widget=stacked_default_widget,
                                                            title="Answer",
                                                            disable_markdown_by_default=True)
        self.tags_editor = TagsEditor(card_list=self.card_list)

        self.vertical_splitter.addWidget(self.question_editor)
        self.vertical_splitter.addWidget(self.answer_editor)
        self.vertical_splitter.addWidget(self.tags_editor)

        # Define the default relative size of widgets in the splitter
        # Warning: The setSizes() method is absolute not relative, it sets the sizes to actual pixel sizes;
        #          the setStretchFactor() method is relative, it sets the sizes relative to each other.
        # See https://stackoverflow.com/questions/29537762/pyqt-qsplitter-setsizes-usage
        # See https://stackoverflow.com/questions/43831474/how-to-equally-distribute-the-width-of-qsplitter
        self.vertical_splitter.setStretchFactor(0, 45)
        self.vertical_splitter.setStretchFactor(1, 45)
        self.vertical_splitter.setStretchFactor(2, 10)

        # Make layouts ####################################

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.vertical_splitter)

        # Set layouts #####################################

        self.setLayout(vbox)
