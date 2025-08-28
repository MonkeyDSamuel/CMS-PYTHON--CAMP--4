from dao.pharmacist.billdaoimple import BillingDaoImplementation
from models.billing import Billing

class BillingManagementLib:
    dao_service = BillingDaoImplementation()

    @staticmethod
    def add_bill():
        bill_id = input("Enter Bill ID: ")
        charge = float(input("Enter Charge: "))
        prescription_id = input("Enter Prescription ID: ")
        bill_date = input("Enter Bill Date (YYYY-MM-DD): ")

        bill = Billing(bill_id, charge, prescription_id, bill_date)
        BillingManagementLib.dao_service.add_bill(bill)
        print("✅ Bill added successfully.")

    @staticmethod
    def display_all():
        bills = BillingManagementLib.dao_service.display_all_bills()
        if not bills:
            print("No bills found.")
        for bill in bills:
            print(bill)

    @staticmethod
    def search_bill():
        bill_id = input("Enter Bill ID to search: ")
        bill = BillingManagementLib.dao_service.search_bill_by_id(bill_id)
        if bill:
            print(bill)
        else:
            print("❌ Bill not found.")

    @staticmethod
    def delete_bill():
        bill_id = input("Enter Bill ID to delete: ")
        if BillingManagementLib.dao_service.delete_bill(bill_id):
            print("✅ Bill deleted successfully.")
        else:
            print("❌ Bill not found.")
