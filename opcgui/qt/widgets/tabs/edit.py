#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QPushButton

from opcgui.qt.widgets.searchwiget import SearchWidget
from opcgui.qt.widgets.editorwidget import EditorWidget

import opcgui.utils
from opcgui.utils import has_been_reviewed_today, has_been_created_today


class EditCardsTab(QWidget):

    def __init__(self, card_list, main_window, parent):
        super().__init__(parent=parent)

        self.card_list = card_list
        self.current_card_list = []

        # Make widgets ####################################

        self.horizontal_splitter = QSplitter(orientation=Qt.Horizontal, parent=self)

        self.search_widget = SearchWidget(self.card_list, parent=self)
        self.editor_widget = EditorWidget(self.card_list, stacked_default_widget="webview", parent=self)

        self.horizontal_splitter.addWidget(self.search_widget)
        self.horizontal_splitter.addWidget(self.editor_widget)

        self.save_button = QPushButton('Save', self)
        self.cancel_button = QPushButton('Cancel', self)

        # Define the default relative size of widgets in the splitter
        # Warning: The setSizes() method is absolute not relative, it sets the sizes to actual pixel sizes;
        #          the setStretchFactor() method is relative, it sets the sizes relative to each other.
        # See https://stackoverflow.com/questions/29537762/pyqt-qsplitter-setsizes-usage
        # See https://stackoverflow.com/questions/43831474/how-to-equally-distribute-the-width-of-qsplitter
        self.horizontal_splitter.setStretchFactor(0, 20)
        self.horizontal_splitter.setStretchFactor(1, 80)

        # Set slots #######################################

        self.search_widget.card_list_widget.currentRowChanged.connect(self.update_card_selection_callback)
        self.search_widget.search_mode_combo.currentTextChanged.connect(self.update_callback)
        self.search_widget.tags_combo.currentTextChanged.connect(self.update_callback)
        self.search_widget.pattern_search_edit.textChanged.connect(self.update_callback)
        self.search_widget.case_sensitive_checkbox.stateChanged.connect(self.update_callback)
        self.search_widget.show_hidden_cards_checkbox.stateChanged.connect(self.update_callback)

        self.save_button.clicked.connect(self.save_btn_callback)
        self.cancel_button.clicked.connect(self.cancel_btn_callback)

        # Make layouts ####################################

        vbox = QVBoxLayout(self)

        vbox.addWidget(self.horizontal_splitter)
        vbox.addWidget(self.save_button)
        vbox.addWidget(self.cancel_button)

        # Set layouts #####################################

        self.setLayout(vbox)

        # Update ##########################################

        self.update_callback()


    def update_callback(self, index=None):
        selected_mode = self.search_widget.search_mode_combo.currentText()
        selected_tag = self.search_widget.tags_combo.currentText()
        search_str = self.search_widget.pattern_search_edit.text()
        case_sensitive = self.search_widget.case_sensitive_checkbox.isChecked()
        show_hidden_cards = self.search_widget.show_hidden_cards_checkbox.isChecked()

        def search_str_filter(card: str) -> bool:
            if search_str.strip() == "":
                return True
            else:
                if case_sensitive:
                    return search_str in card["question"] or search_str in card["answer"]
                else:
                    return search_str.lower() in card["question"].lower() or search_str.lower() in card["answer"].lower()

        def tag_filter(card: str) -> bool:
            if selected_tag.strip() == "":
                return True
            else:
                return selected_tag in card["tags"]

        def hidden_filter(card: str) -> bool:
            return not card["hidden"] or show_hidden_cards


        if selected_mode == "All Cards":
            self.current_card_list = [card for card in self.card_list if search_str_filter(card) and hidden_filter(card) and tag_filter(card)]
        elif selected_mode == "Reviewed Cards":
            self.current_card_list = [card for card in self.card_list if has_been_reviewed_today(card) and search_str_filter(card) and hidden_filter(card) and tag_filter(card)]
        elif selected_mode == "New Cards":
            self.current_card_list = [card for card in self.card_list if has_been_created_today(card) and search_str_filter(card) and hidden_filter(card) and tag_filter(card)]
        elif selected_mode == "Hidden Cards":
            self.current_card_list = [card for card in self.card_list if search_str_filter(card) and tag_filter(card) and card["hidden"]]
        else:
            raise ValueError(f"Unknown search mode: {selected_mode}")
        
        def format_card(card) -> str:
            label = card["question"].split("\n")[0]

            if selected_mode == "Reviewed Cards":
                if has_been_reviewed_today(card, wrong_answers_only=True):
                    return "✖ " + label        # ✖🗷   ❌🗵☒✕
                else:
                    return "🗸 " + label        # ✔🗹   ✅☑✓🗸
            else:
                if card["hidden"]:
                    return "🕱 " + label
                else:
                    return label

        self.search_widget.card_list_widget.clear()
        self.search_widget.card_list_widget.addItems([format_card(card) for card in self.current_card_list])


    def update_card_selection_callback(self, index):
        card = self.current_card_list[index]
        self.editor_widget.question_editor.text = card["question"]
        self.editor_widget.answer_editor.text = card["answer"]
        self.editor_widget.tags_editor.text = "\n".join(card["tags"])


    def save_btn_callback(self):
        question_str = self.editor_widget.question_editor.text
        answer_str = self.editor_widget.answer_editor.text
        tags_str = self.editor_widget.tags_editor.text

        if len(question_str.strip()) > 0 and len(tags_str.strip()):

            pass  # TODO

        #     # Make the card and add it to the card list
        #     card = {
        #             "cdate": datetime.date.today(),
        #             "hidden": False,
        #             "question": question_str,
        #             "answer": answer_str,
        #             "reviews": [],
        #             "tags": [tag.strip() for tag in tags_str.split("\n") if tag.strip() != '']
        #         }

        #     self.card_list.append(card)


    def cancel_btn_callback(self):
        self.editor_widget.question_editor.text = ""  # TODO
        self.editor_widget.answer_editor.text = ""    # TODO
        self.editor_widget.tags_editor.text = ""      # TODO