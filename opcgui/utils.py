import datetime

def datetime_to_date(d):
    '''If the object is an instance of datetime.datetime then convert it to a datetime.datetime.date object.

    If it's already a date object, do nothing.'''

    if isinstance(d, datetime.datetime):
        d = d.date()
    return d