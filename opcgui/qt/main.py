#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import opencal.io.pkb
from opcgui.qt.widgets.mainwindow import MainWindow
from opcgui import APPLICATION_NAME

from PyQt5.QtWidgets import QApplication

PKB_PATH = "~/jeremie.pkb"                            # <<< TODO: REMOVE THIS...

def main():

    card_list = opencal.io.pkb.load_pkb(PKB_PATH)

    app = QApplication(sys.argv)
    app.setApplicationName(APPLICATION_NAME)

    # Make widgets
    window = MainWindow(card_list)

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
    exit_code = app.exec_()

    #opencal.io.pkb.save_pkb(card_list, PKB_PATH)     # <<< TODO: UNCOMMENT THIS LINE...

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
