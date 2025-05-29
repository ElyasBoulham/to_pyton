from datetime import date, timedelta

def get_first_day_of_month(month, year):
    """Returns the first day of the given month and year."""
    return date(year, month, 1)

def get_last_day_of_month(month, year):
    """Returns the last day of the given month and year."""
    if month == 12:
        return date(year, 12, 31)
    return date(year, month + 1, 1) - timedelta(days=1)
