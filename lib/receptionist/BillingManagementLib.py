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
    def insert_bill(self, appointment_id, doctor_fee=None):
        try:
            # If doctor_fee not provided, fetch it from DB using appointment_id
            if doctor_fee is None or doctor_fee == 0:
                doctor_fee = self.dao.fetch_doctor_fee_by_appointment(appointment_id)

            bill = Billing(
                appointment_id=appointment_id,
                doctor_fee=doctor_fee,
                bill_date=date.today()
            )
            if self.dao.insert_bill(bill):
                # Print per requirement
                print("Billing Successful!")
                print(f"Total bil amount = {bill.total_bill}")
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
    def update_bill(self, bill_id, appointment_id=None, doctor_fee=None, additional_charges=None):
        bill = self.dao.find_by_bill_id(bill_id)
        if not bill:
            print(f"❌ Bill ID {bill_id} not found.")
            return False

        if appointment_id:
            bill.appointment_id = appointment_id
        if doctor_fee is not None:
            bill.doctor_fee = doctor_fee
        if additional_charges is not None:
            bill.additional_charges = additional_charges

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
            if not appointment_id:
                print("❌ Appointment ID is required.")
                return

            # Auto-fetch doctor's charge based on appointment_id
            doctor_fee = self.dao.fetch_doctor_fee_by_appointment(appointment_id)
            if doctor_fee is None or doctor_fee == 0:
                print("❌ Unable to determine doctor's charge for this appointment.")
                return

            self.insert_bill(appointment_id, doctor_fee)
        except Exception as e:
            print("Error creating bill:", e)

    def search_bills_by_date(self):
        """Search bills by date (defaults to today if left empty)"""
        try:
            from datetime import datetime, date
            
            date_input = input("Enter Date to search (dd/mm/yyyy) (press Enter for today): ").strip()
            
            if not date_input:
                search_date = date.today()
                print(f"Searching for bills on: {search_date.strftime('%d/%m/%Y')}")
            else:
                try:
                    search_date = datetime.strptime(date_input, "%d/%m/%Y").date()
                except ValueError:
                    print("❌ Invalid date format. Please use dd/mm/yyyy format.")
                    return
            
            bills = self.dao.find_bills_by_date(search_date)
            
            if not bills:
                print(f"No bills found for {search_date.strftime('%d/%m/%Y')}")
                return
            
            print(f"\n--- Bills on {search_date.strftime('%d/%m/%Y')} ---")
            for bill in bills:
                print(f"Bill ID: {bill.bill_id}, Appointment: {bill.appointment_id}, "
                      f"Total: {bill.total_bill}, Date: {bill.bill_date}")
                      
        except Exception as e:
            print("Error searching bills by date:", e)
