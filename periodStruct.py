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
