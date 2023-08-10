#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import qtme

import opencal.io.pkb
import opcgui

from opcgui.qt.widgets.mainwindow import MainWindow
from opcgui import APPLICATION_NAME

from PySide6.QtWidgets import QApplication


def main():

    # Load configuration file
    opcgui.load_config_file()

    qtme.cfg['qtme']['default_html_base_path'] = opcgui.config.default_html_base_path

    card_list = opencal.io.pkb.load_pkb(opcgui.config.pkb_path)

    app = QApplication(sys.argv)
    app.setApplicationName(APPLICATION_NAME)

    # Make widgets
    window = MainWindow(card_list=card_list)

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    opencal.io.pkb.save_pkb(card_list, opcgui.config.pkb_path)

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
