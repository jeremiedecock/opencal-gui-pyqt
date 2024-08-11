import datetime
from opencal.card import Card

from opencal.core.data import RIGHT_ANSWER_STR, WRONG_ANSWER_STR

def datetime_to_date(d):
    '''If the object is an instance of datetime.datetime then convert it to a datetime.datetime.date object.

    If it's already a date object, do nothing.'''

    if isinstance(d, datetime.datetime):
        d = d.date()
    return d


def has_been_created_today(card, today=None) -> bool:
    if today is None:
        today = datetime.date.today()

    return datetime_to_date(card["cdate"]) == today


def has_been_reviewed_today(
        card: Card,
        wrong_answers_only: bool = False,
        today=None) -> bool:
    ret = False

    if today is None:
        today = datetime.date.today()

    for review in card.consolidation_reviews:
        if (datetime_to_date(review["rdate"]) == today) and ((not wrong_answers_only) or (review["result"] == WRONG_ANSWER_STR)):
            ret = True

    return ret