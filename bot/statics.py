import math
from datetime import datetime as DateTime


def jid_to_username(jid):
    return jid.split("@")[0][0:-4]


def get_config():
    from json import loads

    with open("config.json") as account_file:
        return loads(account_file.read())


def timestamp_to_datetime(ts):
    """
    Epoch timestamp to datetime
    :param ts: the timestamp
    :return: datetime object
    """
    return DateTime.utcfromtimestamp(ts)


def ago(then: DateTime) -> str:
    now = DateTime.utcnow()
    diff = now - then
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff > 0:
        return days_ago(day_diff)
    elif day_diff == 0:
        return less_than_day_ago(second_diff)
    return "sometime in the future?!"


def less_than_day_ago(second_diff):
    if second_diff < 10:
        return "just now"
    if second_diff < 60:
        return f"{second_diff} seconds ago"
    if second_diff < 120:
        return "a minute ago"
    if second_diff < 3600:
        return f"{math.floor(second_diff / 60)} minutes ago"
    if second_diff < 7200:
        return "an hour ago"
    return f"{math.floor(second_diff / 3600)} hours ago"


def days_ago(day_diff):
    if day_diff == 1:
        return "yesterday"
    if day_diff < 7:
        return f"{day_diff} days ago"
    if day_diff < 14:
        return "a week ago"
    if day_diff < 56:
        return f"{math.floor(day_diff / 7)} weeks ago"
    if day_diff < (30.437 * 2):
        return "a month ago"
    if day_diff < 365.26:
        return f"{math.floor(day_diff / 30.437)} months ago"
    if day_diff < (365.26 * 2):
        return "a year ago"
    return f"{math.floor(day_diff / 365.26)} years ago"
