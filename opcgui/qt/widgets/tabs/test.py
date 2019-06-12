#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The next two lines are a workaround to fix an issue with QWebEngineView (see https://github.com/ContinuumIO/anaconda-issues/issues/9199#issuecomment-383842265)
import ctypes
ctypes.CDLL("libGL.so.1", mode=ctypes.RTLD_GLOBAL)

import datetime
import os
import re

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

from PyQt5.QtCore import Qt, QModelIndex, QSortFilterProxyModel, QUrl
from PyQt5.QtWidgets import QTableView, QWidget, QPushButton, QVBoxLayout, QAbstractItemView, \
    QAction, QPlainTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QStackedLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QSizePolicy

HTML = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <style type="text/css" media="all">
    {}
    </style>

    {}

    <script type="text/javascript" src="mathjax/MathJax.js?config=TeX-AMS_HTML-full"></script>
</head>
<body>
    {}
</body>
</html>
'''

MATHJAX = r'''<script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {inlineMath: [["$","$"],["\\(","\\)"]]}
        });
    </script>
'''

CSS = r'''
/* Copyright (c) 2006,2007,2008,2009,2010,2011 Jérémie DECOCK (jdhp.org)     */

/* ************************************************************************* */
/*                                 DEFAULT                                   */
/* ************************************************************************* */

* {
    border-width      : 0px;

    font-family       : monospace,fixed;
    font-size         : 14px;

    margin            : 0px;
    padding           : 0px;
}

div#empty {
    position          : absolute;
    text-align        : center;
    top               : 50%;
    width             : 100%;
}

/* ************************************************************************* */
/*                                 HEADER                                    */
/* ************************************************************************* */

div#informations {
    background-color  : #eeeeee;
    border-bottom     : 1px solid #dddddd;
    color             : #666666;

    font-size         : 11px;

    padding           : 1em;
}

div#informations span {
    font-size         : 11px;
}

/*
div#informations span.information {
    margin-right      : 3em;
}
*/

div#informations span.highlight {
    color             : #197cc1;
}

div#informations span.star {
    /* Image : 22x22 px */
    background-image  : url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAN1wAADdcBQiibeAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAOPSURBVDiNtZXPb1RVFMe/33vfe515b6aOtGMZC3SKaVRgIdFo4s6wdE38F9y4I27c+QcQw19hYKcmxqWJERckCJrG2BiMUto6nU6B6eu8H/d8XYClaCuo8exucu7nnu8595xDSfg/zD2t45Ur9AD5tP48PGK60ejVdhxb4r0lrirTkmIURbvNZp0PBr7odr8f/0Pwa+nubnXEzI548VmT2qSmADnI1fKcMNi9IoTVTidbBa5VTwCT4/HZ2dgmncr5eQ8dFTAjaZpEA6AHVEvMSWxTHCByd3Z2iuXZ2R/u7wdH+w/b26884309E6Jo0ZkdFzQPsAuqE0Vv9+nacVV+/KsDxwZsAfabTO1GI2kAS98AK8UB4DNJoxF3QtAJmBYpLRp1DFDPsTsXT32wRMas66+6sttbBAYAOhSmIHN5nt5PU14HHqRgD5znNsMQeoDN0+mEoD7BRUDH4+Td58gOACBJ3j9RTN7rAVgHmUIkiZpm+c7O6TtZhvV94LciX/k0OOsCOCpzPfp4weGlJRe92Yrid/Z0+egck6kPXag/PxbCt54sKoE7gEbO+T6wD7yxsTXVbtu0xI6zeCZpfnTO+TeeJ5sH/Fsiis9HUXwewGQ+1F+3y/LClqxcZ209gA6QOQCYm1PCwJRiJlaZ2Up9MPTP1oD0M2VFi0TLHLLB4HQKPOy88ZhxIGMSCYikKi9t1vUXT+x1C9etLC5WhKZMSGAWNxpVYw/cql352A0FlZMLtdlPdhhUGoWyvFgDAQAFQACQ543dPfDari+9UEooIBYgJkCdy1YPjVY2hGzNA8glTRytgFjMzd18BO71ThbmlIsYk3YPxDaAIZkenmfGTlo1gFsi7koYy2ENkO2BgcshA9cYMDLzQ4ADwK0BSf1AdoEQrtYhXK2AycPcG0GsAlgnOAD80Hu/8se7jzovmx0iH65DOgJxWrCm6eZCXXyahfqzVCpiIAFJ+OjcxLlTE8rdEnFbxjsil1vNG7f3BD0+hM60xmO87oQXQPUhHgPtKIAZQpkBnkAJ8D6ITQhrAH4h/I8bm+NP+v1bk0PAAHC2MxlXZ4PUJ9AT2SXVkdQk5AXWhBuTGBm0QXIlTRtfAtfuPlaCg+bx8vKZZGEBLzvjSUEzdJiWqQHKSa52jrsGbaPCjaxz6jvgcvhLbf9mg3Bz88VWlsUdla7rI5utYYF1NCpVDavKDf/FBvnv9jtEyeUld60tXQAAAABJRU5ErkJggg==);
    background-repeat : no-repeat;
}

/* ************************************************************************* */
/*                                  TAGS                                     */
/* ************************************************************************* */

div#tags {
    margin            : 0.5em 2em 2em 2em;
}

div#tags span.tag {
    /* Image : 15x15 px */
    background-image  : url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAAAXNSR0IArs4c6QAAAAZiS0dEAAAAAAAA+UO7fwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9sGDAsgIaQD10kAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAABjklEQVQoz32Sv2vbQBzFn1wKwRAIIiDs7cCLMGS5bv4P/B9kyN6lZO2SsUu2QCF7lyxez5u0aZOWgE+Lq6PQwB0Jwo6JI+jwMrS+GFvug5uO7+e9749Aa30L4DMArNdrbEtKGeB/0lqzTdZa5nlOkjj0OhuIMQZFUcAYAwCIoghhGKIoCh4y7myi1nUNKWVQ17X/FEIgDENkWdYK8M7bLs/rZzjnUJRPEEKg3++3A/715bV8WdJayy/XGS+uEub6kSRZVRWTJOFez845D3tdveLbj58AgJPjI9zc3fsEQgikaeoTdKSUwXw+94Df9QcsVo2H7QJ6vZ4HBORfUJZlHAwGiKIIRfmEm7t7nBwfechi1eDy/AwyPkVZljDGvA9sNBoFs9kMzjnI+BSX52etCbblnTdK05TD4XAvwWLV4PvXT3j49QBjDMbjcdB6OUopWmtJkrl+5MVVwuXLklprKqX8xA+enlKKVVX5Fe4WktyPva3pdMo4jtE0zXvUnZ4/AvhzCDCZTNjtdvcKAeANfNtm4C6e18cAAAAASUVORK5CYII=);
    background-repeat : no-repeat;

    color             : #666666;
    font-size         : 10px;
    
    margin-right      : 0.5em;

    padding-left      : 18px;
    padding-top       : 1px;
    padding-bottom    : 1px;
}

/* ************************************************************************* */
/*                          QUESTION AND ANSWER                              */
/* ************************************************************************* */

h1 {
    font-size         : 14px;
    font-family       : verdana, sans-serif;

    margin            : 0em 1em 0.5em 1em;
}

h1.question {

}

h1.answer {
    border-top        : 1px solid #dddddd;

    margin-top        : 1em;
    padding-top       : 1em;
}

div.question {
    margin            : 0em 2em 0.5em 2em;
    white-space       : pre-wrap;
}

div.question img {
    max-width         : 100%;
}

div.answer {
    margin            : 0em 2em 0.5em 2em;
    white-space       : pre-wrap;
}

div.answer img {
    max-width         : 100%;
}
'''

INFORMATION = '''<div id="informations">
    <span class="information">
        Created on <span class="highlight">{}</span>
    </span> - 
    <span class="information" title="{}">
        Checked <span class="highlight">{}</span> times
    </span> - 
    <span class="information">
        Level <span class="highlight">{}</span>
    </span>
</div>'''


def replace_html_special_chars(src):
    """Replace the five reserved characters with entities to avoid HTML interpretation of src.

    Parameters
    ----------
    src : str
        The string to process.

    Returns
    -------
    str
        A string without HTML tags.
    """

    src = src.replace("&", "&amp;")
    src = src.replace("<", "&lt;")
    src = src.replace(">", "&gt;")
    src = src.replace("\"", "&quot;")
    src = src.replace("\'", "&apos;")

    return src

IMG_SUB_PATTERN = r"&lt;img file=&quot;([0-9abcdef]{32}.(png|jpg|jpeg|gif))&quot; /&gt;"
AUDIO_SUB_PATTERN = r"&lt;audio file=&quot;([0-9abcdef]{32}.(ogg|oga|flac|spx|wav|mp3))&quot; /&gt;"
VIDEO_SUB_PATTERN = r"&lt;video file=&quot;([0-9abcdef]{32}.(ogv|vp8|avi|mp4|mpg|wmv|mov))&quot; /&gt;"

img_sub_regex = re.compile(IMG_SUB_PATTERN)       # TODO: put this in a class
audio_sub_regex = re.compile(AUDIO_SUB_PATTERN)   # TODO: put this in a class
video_sub_regex = re.compile(VIDEO_SUB_PATTERN)   # TODO: put this in a class

def question_answer_to_html(question_or_answer):

    html = replace_html_special_chars(question_or_answer)

    # Make html image tags

    html = img_sub_regex.sub(r'<img src="materials/\1" />', html)

    # Make html audio tags

    html = audio_sub_regex.sub(r'<audio controls src="materials/\1" />Your browser does not support the audio tag.<audio/>', html)

    # Make html video tags

    html = video_sub_regex.sub(r'<video controls src="materials/\1" />Your browser does not support the video tag.<video/>', html)

    return html


class TestTab(QWidget):

    def __init__(self, professor, context_directory, parent=None):
        super().__init__(parent=parent)

        self.context_directory = context_directory
        self.base_url = QUrl.fromLocalFile(self.context_directory.name + "/")  # Rem: this doesn't work without the last '/' : see https://stackoverflow.com/questions/18196069/qwebview-setbaseurl-doesnt-work

        self.professor = professor

        self.tabs = parent

        # Make widgets ####################################

        self.web_view = QWebEngineView(parent=self)
        self.control_widget = QWidget(parent=self)

        self.navigation_widget = QWidget(parent=self.control_widget)
        self.answer_widget = QWidget(parent=self.control_widget)

        self.btn_answer = QPushButton("Answer", parent=self.navigation_widget)
        self.btn_skip_card = QPushButton("Skip", parent=self.navigation_widget)
        self.btn_hide_card = QPushButton("Hide", parent=self.navigation_widget)

        self.btn_wrong_answer = QPushButton("Wrong", parent=self.answer_widget)
        self.btn_right_answer = QPushButton("Right", parent=self.answer_widget)

        # Set SizePolicy ##################################

        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)         # horizontal, vertical
        self.control_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)       # horizontal, vertical
        self.navigation_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)    # horizontal, vertical
        self.answer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)        # horizontal, vertical

        # Make layouts ####################################

        self.vbox = QVBoxLayout(self)

        self.hbox_navigation = QHBoxLayout(self.navigation_widget)
        self.hbox_answer = QHBoxLayout(self.answer_widget)

        self.stack_layout = QStackedLayout()

        # HBox

        self.hbox_navigation.addWidget(self.btn_hide_card)
        self.hbox_navigation.addWidget(self.btn_answer)
        self.hbox_navigation.addWidget(self.btn_skip_card)

        self.hbox_answer.addWidget(self.btn_wrong_answer)
        self.hbox_answer.addWidget(self.btn_right_answer)

        # VBox

        self.vbox.addWidget(self.web_view)
        self.vbox.addWidget(self.control_widget)

        # StackedLayout

        self.stack_layout.addWidget(self.navigation_widget)
        self.stack_layout.addWidget(self.answer_widget)

        self.stack_layout.setCurrentWidget(self.navigation_widget)

        # Set layouts #####################################

        self.control_widget.setLayout(self.stack_layout)

        self.navigation_widget.setLayout(self.hbox_navigation)
        self.answer_widget.setLayout(self.hbox_answer)

        self.setLayout(self.vbox)

        # Set key shortcut ################################

        # see https://stackoverflow.com/a/17631703  and  http://doc.qt.io/qt-5/qaction.html#details

        # Answer action

        answer_action = QAction(self)
        answer_action.setShortcut(Qt.Key_Space)
        answer_action.setShortcutContext(Qt.WindowShortcut)

        answer_action.triggered.connect(self.answer_btn_callback)
        self.addAction(answer_action)

        # Skip card action

        skip_card_action = QAction(self)
        skip_card_action.setShortcut(Qt.CTRL | Qt.Key_Delete)
        skip_card_action.setShortcutContext(Qt.WindowShortcut)

        skip_card_action.triggered.connect(self.skip_card_btn_callback)
        self.addAction(skip_card_action)

        # Hide card action

        hide_card_action = QAction(self)
        hide_card_action.setShortcut(Qt.Key_Delete)
        hide_card_action.setShortcutContext(Qt.WindowShortcut)

        hide_card_action.triggered.connect(self.hide_card_btn_callback)
        self.addAction(hide_card_action)

        # Right answer action

        right_answer_action = QAction(self)
        right_answer_action.setShortcut(Qt.Key_R)

        right_answer_action.triggered.connect(self.right_answer_btn_callback)
        self.addAction(right_answer_action)

        # Wrong answer action

        wrong_answer_action = QAction(self)
        wrong_answer_action.setShortcut(Qt.Key_W)

        wrong_answer_action.triggered.connect(self.wrong_answer_btn_callback)
        self.addAction(wrong_answer_action)

        # Set slots #######################################

        self.btn_answer.clicked.connect(self.answer_btn_callback)
        self.btn_skip_card.clicked.connect(self.skip_card_btn_callback)
        self.btn_hide_card.clicked.connect(self.hide_card_btn_callback)

        self.btn_right_answer.clicked.connect(self.right_answer_btn_callback)
        self.btn_wrong_answer.clicked.connect(self.wrong_answer_btn_callback)

        # Set QWebEngineView ##############################

        self.update_html(show_answer=False)


    def update_html(self, show_answer=False):
        current_card = self.professor.current_card

        if current_card is not None:

            # Informations

            reviews_str = '\n'.join(['{} : {}'.format(review['rdate'].date().isoformat(), review['result']) for review in current_card["reviews"]])

            grade = current_card['grade']

            html_body = INFORMATION.format(current_card["cdate"].date().isoformat(),
                                           reviews_str,
                                           len(current_card["reviews"]),
                                           grade)

            # Tags

            tags_str = ''.join(['<span class="tag">{}</span> '.format(tag) for tag in current_card["tags"]])
            html_body += '<div id="tags">{}</div>'.format(tags_str)

            # Question

            html_body += r'<h1 class="question">Question</h1>'
            html_body += r'<div class="question">'
            html_body += question_answer_to_html(current_card["question"])
            html_body += r'</div>'

            # Answer

            if show_answer:
                html_body += r'<h1 class="answer">Answer</h1>'
                html_body += r'<div class="answer">'
                html_body += question_answer_to_html(current_card["answer"])
                html_body += r'</div>'
        else:
            html_body = r'<div id="empty">Empty selection</div>'

        html = HTML.format(CSS, MATHJAX, html_body)

        #with open("/tmp/opcgui_card_debug.html", "w") as fd:
        #    print(html, file=fd)

        self.web_view.setHtml(html, self.base_url)

    def answer_btn_callback(self):
        self.stack_layout.setCurrentWidget(self.answer_widget)
        self.update_html(show_answer=True)

    def skip_card_btn_callback(self):
        self.professor.current_card_reply(answer="skip", duration=None, confidence=None)
        self.update_html(show_answer=False)

    def hide_card_btn_callback(self):
        self.professor.current_card_reply(answer="hide", duration=None, confidence=None)
        self.update_html(show_answer=False)

    def right_answer_btn_callback(self):
        self.professor.current_card_reply(answer=RIGHT_ANSWER_STR, duration=None, confidence=None)
        self.stack_layout.setCurrentWidget(self.navigation_widget)
        self.update_html(show_answer=False)

    def wrong_answer_btn_callback(self):
        self.professor.current_card_reply(answer=WRONG_ANSWER_STR, duration=None, confidence=None)
        self.stack_layout.setCurrentWidget(self.navigation_widget)
        self.update_html(show_answer=False)