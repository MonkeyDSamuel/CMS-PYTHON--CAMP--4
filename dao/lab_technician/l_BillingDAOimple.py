from typing import List
from dao.lab_technician.l_AbstractBillingDAO import AbstractBillingDAO
from models.lab_technician.l_billing import LabBilling

class BillingDAOimple(AbstractBillingDAO):
    """Implementation of Billing DAO"""

    def __init__(self):
        self._bills: List[LabBilling] = []  # In-memory store (replace with DB logic)

    def create_bill(self, bill: LabBilling) -> bool:
        self._bills.append(bill)
        return True

    def update_bill(self, bill_id: int, bill: LabBilling) -> bool:
        for i, b in enumerate(self._bills):
            if b.bill_id == bill_id:
                self._bills[i] = bill
                return True
        return False

    def find_by_bill_id(self, bill_id: int) -> LabBilling:
        for b in self._bills:
            if b.bill_id == bill_id:
                return b
        return None

    def list_all_bills(self) -> List[LabBilling]:
        return self._bills

    def list_bills_by_patient_id(self, patient_id: int) -> List[LabBilling]:
        return [b for b in self._bills if b.patient_id == patient_id]

    def list_bills_by_date(self, date: str) -> List[LabBilling]:
        return [b for b in self._bills if b.date == date]