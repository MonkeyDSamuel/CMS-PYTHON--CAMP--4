from dao.pharmacist.abstractdaobill import BillingDaoService
from models.billing import Billing

class BillingDaoImplementation(BillingDaoService):
    def __init__(self):
        self.bills = {}  # bill_id -> Billing object

    def add_bill(self, bill: Billing):
        if bill.bill_id in self.bills:
            raise ValueError("Bill ID already exists.")
        self.bills[bill.bill_id] = bill
        return True

    def display_all_bills(self):
        return list(self.bills.values())

    def search_bill_by_id(self, bill_id: str):
        return self.bills.get(bill_id, None)

    def delete_bill(self, bill_id: str):
        if bill_id in self.bills:
            del self.bills[bill_id]
            return True
        return False
