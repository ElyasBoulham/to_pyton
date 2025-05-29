from struct import Struct  # Assuming you saved Struct class in struct.py

class StructPeriodic(Struct):
    def __init__(self, id: int = -1):
        super().__init__(id)
        self.period = None  # Will be a PeriodStruct object

    def get_period(self):
        return self.period

    def set_period(self, period):
        self.period = period

    def get_filter_by_date(self, begin: str, end: str) -> str:
        return (
            f"SELECT * FROM {self.DBTname} "
            f"WHERE `begin` >= '{begin}' AND `end` <= '{end}' ORDER BY begin"
        )

    def get_filter_by_period_is_in_period_from_query(self, sqlquery: str, begin: str, end: str) -> str:
        return (
            f"SELECT * FROM ({sqlquery}) AS aa "
            f"WHERE `begin` >= '{begin}' AND `end` <= '{end}' ORDER BY begin"
        )

    def get_filter_by_date_in_period_from_query(self, sqlquery: str, begin: str, end: str) -> str:
        return (
            f"SELECT * FROM ({sqlquery}) AS aa "
            f"WHERE `payment_date` >= '{begin}' AND `payment_date` <= '{end}' ORDER BY payment_date"
        )

class PeriodStruct:
    def __init__(self, begin_month=None, begin_year=None, end_month=None, end_year=None):
        from datetime import date
        self.begin_month = begin_month or date.today().month
        self.begin_year = begin_year or date.today().year
        self.end_month = end_month or self.begin_month
        self.end_year = end_year or self.begin_year

    def get_begin_date(self):
        from utils import get_first_day_of_month
        return get_first_day_of_month(self.begin_month, self.begin_year)

    def get_end_date(self):
        from utils import get_last_day_of_month
        return get_last_day_of_month(self.end_month, self.end_year)

    def __str__(self):
        return f"{self.begin_month}/{self.begin_year} - {self.end_month}/{self.end_year}"
