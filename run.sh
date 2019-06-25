#!/bin/sh

source activate opencal-dev


# TODO: WORKAROUND https://forum.qt.io/topic/54802/linux-application-does-not-accept-keyboard-input/4
QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb ./opcgui/qt/main.py
