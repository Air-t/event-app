from datetime import datetime, timedelta


def now_plus_15_min():
    """Return actual datetime plus 15min ahead"""
    return datetime.now() + timedelta(minutes=15)
