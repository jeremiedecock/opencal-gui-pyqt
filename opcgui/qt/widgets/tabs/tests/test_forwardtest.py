#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains unit tests for the "opencal.core.professor.ltm.berenice" module.
"""

from opcgui.qt.widgets.tabs.forwardtest import review_card

from opencal.core.mocks import DateMock

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

import copy
import datetime
import pytest

BOGUS_CURRENT_DATE = datetime.date(year=2000, month=1, day=1)

DateMock.set_today(BOGUS_CURRENT_DATE)

###############################################################################
# CARDS                                                                       #
###############################################################################

CARD_WITHOUT_REVIEW_1 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_WITHOUT_REVIEW_2 = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
        "reviews": [],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_WITHOUT_TAG = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
        "reviews": [],
        'tags': [],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_WITH_WRONG_TAG = {
        "cdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
        "reviews": [],
        'tags': ['foo', 'bar'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_MADE_TODAY = {
        "cdate": BOGUS_CURRENT_DATE,
        "reviews": [],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_MADE_TODAY_WITH_TIME = {
        "cdate": datetime.datetime(year=2000, month=1, day=1, hour=0, minute=1),
        "reviews": [],
        'tags': ['baz'],
        'hidden': False,
        'question': 'foo',
        'answer': 'bar'
    }

CARD_REVIEWED_TODAY_1 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE,
                    "result": RIGHT_ANSWER_STR
                }
            ],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_REVIEWED_TODAY_2 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE,
                    "result": RIGHT_ANSWER_STR
                }
            ],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_REVIEWED_TODAY_3 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE,
                    "result": WRONG_ANSWER_STR
                }
            ],
            'tags': ['baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_TO_REVIEWED_1 = {
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=6),
            'reviews': [
                {
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=5),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=4),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=3),
                    "result": WRONG_ANSWER_STR
                },{
                    "rdate": BOGUS_CURRENT_DATE - datetime.timedelta(days=2),
                    "result": WRONG_ANSWER_STR
                }
            ],
            'tags': ['foo', 'baz'],
            'hidden': False,
            'question': 'foo',
            'answer': 'bar'
        }

CARD_HIDDEN = {
            'reviews': [],
            'tags': ['baz'],
            'cdate': BOGUS_CURRENT_DATE - datetime.timedelta(days=1),
            'hidden': True,
            'question': 'foo',
            'answer': 'bar'
        }


###############################################################################
# TEST THE "review_card" FUNCTION                                             #
###############################################################################

def test_hidden_card():
    assert review_card(CARD_HIDDEN, selected_tag='baz', date_mock=DateMock) == False

def test_made_today_card():
    assert review_card(CARD_MADE_TODAY, selected_tag='baz', date_mock=DateMock) == False
    assert review_card(CARD_MADE_TODAY_WITH_TIME, selected_tag='baz', date_mock=DateMock) == False

def test_reviewed_today_card():
    assert review_card(CARD_REVIEWED_TODAY_1, selected_tag='baz', date_mock=DateMock) == False
    assert review_card(CARD_REVIEWED_TODAY_2, selected_tag='baz', date_mock=DateMock) == False
    assert review_card(CARD_REVIEWED_TODAY_3, selected_tag='baz', date_mock=DateMock) == False

def test_card_without_review():
    assert review_card(CARD_WITHOUT_REVIEW_1, selected_tag='baz', date_mock=DateMock) == True
    assert review_card(CARD_WITHOUT_REVIEW_2, selected_tag='baz', date_mock=DateMock) == True

def test_card_without_tag():
    assert review_card(CARD_WITHOUT_TAG, selected_tag='baz', date_mock=DateMock) == False

def test_card_without_requested_tag():
    assert review_card(CARD_WITH_WRONG_TAG, selected_tag='baz', date_mock=DateMock) == False

def test_card_to_review():
    assert review_card(CARD_TO_REVIEWED_1, selected_tag='baz', date_mock=DateMock) == True