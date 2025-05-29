from datetime import date
from utils import get_first_day_of_month, get_last_day_of_month
from periodStruct import PeriodStruct



class PaymentStruct:
    ID_LOCATAIRE = 0
    PERIOD_START_INDEX = 1
    PERIOD_END_INDEX = 2
    AMOUNT_INDEX = 3
    PAYMENT_DATE_INDEX = 4
    STATUS = 5
    ID_PAYMENT_SET = 6

    def __init__(self, id=-1, idbien=-1, idlocataire=-1, period=None,
                 amount=0.0, status="", payment_date=None, idpayment_set=-1):
        self.id = id
        self.idbien = idbien
        self.idlocataire = idlocataire
        self.period = period 
        self.amount = amount
        self.status = status
        self.payment_date = payment_date or date.today()
        self.idpayment_set = idpayment_set

        self.column_names = [
            "الحالة", "تاريخ الدفع", "المبلغ", "نهاية الفترة", "بداية الفترة", "رقم المؤجر", "مجموعة الدفع"
        ]
        self.db_table = "payments"

    def __str__(self):
        return str(self.payment_date.year) if self.id>=0 else "سنة التسديد"

    def to_search(self):
        return f"{self.period}{self.amount}{self.payment_date}"

    def getColumnNames(self):
        return self.column_names

    def getEmptyOne(self):
        return PaymentStruct()

    def get_all_query(self):
        return f"SELECT * FROM {self.db_table}"

    def get_insert_query(self):
        return f"""INSERT INTO {self.db_table} 
                   (`idbien`, `idlocataire`, `begin`, `end`, `amount`, `payment_date`, `status`, `idpayment_set`)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    def get_update_query(self):
        return f"""UPDATE {self.db_table} SET 
                   `idbien`=%s, `idlocataire`=%s, `begin`=%s, `end`=%s,
                   `amount`=%s, `payment_date`=%s, `status`=%s, `idpayment_set`=%s
                   WHERE `id`=%s"""

    def get_delet_query(self, id_name):
        return f"DELETE FROM {self.db_table} WHERE {id_name} = %s"

    def from_result_set(self, row):
        # Accept both tuple and dict row, and always build a PeriodStruct
        if isinstance(row, dict):
            begin = row.get("begin")
            end = row.get("end")
            id = row.get("id", -1)
            idbien = row.get("idbien", -1)
            idlocataire = row.get("idlocataire", -1)
            amount = row.get("amount", 0.0)
            payment_date = row.get("payment_date")
            status = row.get("status", "")
            idpayment_set = row.get("idpayment_set", -1)
        else:
            begin = row[3]
            end = row[4]
            id = row[0]
            idbien = row[1]
            idlocataire = row[2]
            amount = row[5]
            payment_date = row[6]
            status = row[7]
            idpayment_set = row[8] if len(row) > 8 else -1
        # Convert begin/end dates to PeriodStruct
        period = None
        if begin and end:
            period = PeriodStruct(begin.month, begin.year, end.month, end.year)
        return PaymentStruct(
            id=id,
            idbien=idbien,
            idlocataire=idlocataire,
            period=period,
            amount=amount,
            payment_date=payment_date,
            status=status,
            idpayment_set=idpayment_set
        )

    def get_filter_one_query(self, id_, nameid):
        return f"SELECT * FROM {self.db_table} WHERE {nameid} = {id_}"

    def get_filter_set_query(self, ids_string, nameid):
        return f"SELECT * FROM {self.db_table} WHERE {nameid} IN ({ids_string})"

    def get_filter_FROM_myqery_query(self, base_query, id_, nameid):
        return f"SELECT * FROM ({base_query}) AS temp WHERE {nameid} = {id_}"

    def get_grouping_by(self, fieldname):
        return f"SELECT * FROM {self.db_table} GROUP BY {fieldname}"

    def get_fields_for_insert(self):
        return (
            self.idbien,
            self.idlocataire,
            self.period.get_begin_date(),
            self.period.get_end_date(),
            self.amount,
            self.payment_date,
            self.status,
            self.idpayment_set
        )

    def get_fields_for_update(self):
        return (
            self.idbien,
            self.idlocataire,
            self.period.get_begin_date(),
            self.period.get_end_date(),
            self.amount,
            self.payment_date,
            self.status,
            self.idpayment_set,
            self.id  # for WHERE clause
        )

    def set_to_paint(self, column):
        if column == self.ID_LOCATAIRE:
            return self.id
        elif column == self.PERIOD_START_INDEX:
            # Handle tuple period (begin, end)
            if isinstance(self.period, tuple):
                return self.period[0]
            return self.period.get_begin_date() if self.period else ""
        elif column == self.PERIOD_END_INDEX:
            if isinstance(self.period, tuple):
                return self.period[1]
            return self.period.get_end_date() if self.period else ""
        elif column == self.AMOUNT_INDEX:
            return self.amount
        elif column == self.PAYMENT_DATE_INDEX:
            return self.payment_date
        elif column == self.STATUS:
            return self.status
        elif column == self.ID_PAYMENT_SET:
            return self.idpayment_set
    
