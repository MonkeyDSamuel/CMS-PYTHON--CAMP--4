from dao.lab_technician.l_BillingDAOimple import BillingDAOimple
from models.lab_technician.l_billing import LabBilling

class LabBillingLib:
    billing_dao = BillingDAOimple()

    @staticmethod
    def generate_bill():
        try:
            bill_id = int(input("Enter Bill ID: "))
            lab_prescription_id = int(input("Enter Lab Prescription ID: "))
            charge = float(input("Enter Charge: "))
            billing_date = input("Enter Billing Date (YYYY-MM-DD): ")
            bill = LabBilling(bill_id, lab_prescription_id, charge, billing_date)
            LabBillingLib.billing_dao.create_bill(bill)
            print(" Bill generated successfully.")
        except Exception as e:
            print(f"Error generating bill: {e}")

    @staticmethod
    def display_all_bills():
        bills = LabBillingLib.billing_dao.list_all_bills()
        if bills:
            print("\n--- All Bills ---")
            for b in bills:
                print(f"BillID: {b.get_bill_id()} | LabPrescription: {b.get_lab_prescription_id()} | Charge: ₹{b.get_charge()} | Date: {b.get_billing_date()}")
        else:
            print("No bills found.")

    @staticmethod
    def search_bill_by_id():
        try:
            bill_id = int(input("Enter Bill ID: "))
            bill = LabBillingLib.billing_dao.find_by_bill_id(bill_id)
            if bill:
                print(f"Bill Found: BillID={bill.get_bill_id()} | LabPrescription={bill.get_lab_prescription_id()} | Charge=₹{bill.get_charge()} | Date={bill.get_billing_date()}")
            else:
                print("Bill not found.")
        except Exception as e:
            print(f"Error searching bill: {e}")