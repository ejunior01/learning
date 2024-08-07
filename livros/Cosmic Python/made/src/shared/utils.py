from datetime import date, timedelta


def today():
    return date.today()


def tomorrow():
    return date.today() + timedelta(days=1)


def after_tomorrow():
    return date.today() + timedelta(days=2)
