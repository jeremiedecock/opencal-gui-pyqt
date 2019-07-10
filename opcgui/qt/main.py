#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml

import opencal.io.pkb
from opencal.core.professor.ben import ProfessorBen

from opcgui.qt.widgets.mainwindow import MainWindow
from opcgui import APPLICATION_NAME

from PyQt5.QtWidgets import QApplication


CONFIG_PATH = "~/.opencal.yaml"


def load_config_file(file_path):

    file_path = os.path.expanduser(file_path)  # to handle "~/..." paths
    file_path = os.path.abspath(file_path)     # to handle relative paths

    with open(file_path) as stream:
        config = yaml.safe_load(stream)

    return config


def main():

    # Load configuration file
    config = load_config_file(CONFIG_PATH)

    card_list = opencal.io.pkb.load_pkb(config["pkb_path"])

    if config["professor"] == "ben":
        professor = ProfessorBen(card_list)
    else:
        raise ValueError('Unknown professor "{}"'.format(config["professor"]))

    app = QApplication(sys.argv)
    app.setApplicationName(APPLICATION_NAME)

    # Make widgets
    window = MainWindow(professor, card_list, app_config=config)

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    opencal.io.pkb.save_pkb(card_list, config["pkb_path"])

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
