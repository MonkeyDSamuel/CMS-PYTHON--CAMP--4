from dao.receptionist.BillingDAOImpl import BillingDaoImplementation
from models.receptionist.Billing import Billing
from datetime import date

class BillingManagementLib:

    def __init__(self):
        self.dao = BillingDaoImplementation()

    # =================================
    # 1. Display all bills
    # =================================
    def display_all_bills(self):
        bills = self.dao.display_all_bills()
        if not bills:
            print("No bills found.")
        else:
            for bill in bills:
                print(bill)

    # =================================
    # 2. Insert new bill
    # =================================
    def insert_bill(self, appointment_id, total_bill):
        try:
            bill = Billing(
                appointment_id=appointment_id,
                total_bill=total_bill,
                bill_date=date.today()
            )
            if self.dao.insert_bill(bill):
                print("✅ Bill inserted successfully!")
                # After insertion, bill.bill_id will already be set in DAO
                print(bill)
            else:
                print("❌ Failed to insert bill.")
        except Exception as e:
            print("Error inserting bill:", e)

    # =================================
    # 3. Find bill by ID
    # =================================
    def find_by_bill_id(self, bill_id):
        bill = self.dao.find_by_bill_id(bill_id)
        if bill:
            print("✅ Bill found:")
            print(bill)
            return bill
        else:
            print(f"❌ No bill found with ID {bill_id}")
            return None

    # =================================
    # 4. Update bill
    # =================================
    def update_bill(self, bill_id, appointment_id=None, total_bill=None):
        bill = self.dao.find_by_bill_id(bill_id)
        if not bill:
            print(f"❌ Bill ID {bill_id} not found.")
            return False

        if appointment_id:
            bill.appointment_id = appointment_id
        if total_bill:
            bill.total_bill = total_bill

        bill.bill_date = date.today()  # always refresh date on update

        if self.dao.update_bill(bill, bill_id):
            print("✅ Bill updated successfully!")
            print(bill)
            return True
        else:
            print("❌ Failed to update bill.")
            return False

    # =================================
    # 5. Delete bill
    # =================================
    def delete_bill(self, bill_id):
        if self.dao.delete_bill(bill_id):
            print(f"✅ Bill {bill_id} deleted successfully.")
            return True
        else:
            print(f"❌ Failed to delete bill {bill_id}.")
            return False

    # =================================
    # 6. Create new bill (interactive)
    # =================================
    def create_bill(self):
        try:
            appointment_id = input("Enter Appointment ID: ").strip()
            total_bill_str = input("Enter Total Bill (leave blank to auto): ").strip()
            total_bill = int(total_bill_str) if total_bill_str else 0

            self.insert_bill(appointment_id, total_bill)
        except ValueError:
            print("❌ Invalid amount entered for total bill.")
        except Exception as e:
            print("Error creating bill:", e)
