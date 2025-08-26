from db.db_connection import DBConnection
from lib.receptionist.PatientManagementLib import PatientManagementLib
from lib.receptionist.AppointmentManagementLib import AppointmentManagementLib
from lib.receptionist.BillingManagementLib import BillingManagementLib


def main():
    patient_lib = PatientManagementLib()
    appointment_lib = AppointmentManagementLib()
    billing_lib = BillingManagementLib()

    while True:
        print("\n======= HOSPITAL MANAGEMENT SYSTEM =======")
        print("1. Patient Management")
        print("2. Appointment Management")
        print("3. Billing Management")
        print("0. Exit")

        choice = input("Enter your choice: ")

        # ======================
        # PATIENT MANAGEMENT
        # ======================
        if choice == "1":
            print("\n--- Patient Management ---")
            print("1. Display all patients")
            print("2. Find patient by ID")
            print("3. Add new patient")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                PatientManagementLib.display_all()
            elif sub_choice == "2":
                PatientManagementLib.search_by_id()
            elif sub_choice == "3":
                PatientManagementLib.add_patient()

        # ======================
        # APPOINTMENT MANAGEMENT
        # ======================
        elif choice == "2":
            print("\n--- Appointment Management ---")
            print("1. Display all appointments")
            print("2. Find appointment by ID")
            print("3. Create new appointment")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                appointment_lib.display_all_appointments()
            elif sub_choice == "2":
                appointment_lib.find_appointment_by_id()
            elif sub_choice == "3":
                appointment_lib.create_appointment()

        # ======================
        # BILLING MANAGEMENT
        # ======================
        elif choice == "3":
            print("\n--- Billing Management ---")
            print("1. Display all bills")
            print("2. Find bill by ID")
            print("3. Create new bill")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                billing_lib.display_all_bills()
            elif sub_choice == "2":
                bid = input("Enter bill ID: ")
                billing_lib.find_by_bill_id(bid)
            elif sub_choice == "3":
                billing_lib.create_bill()

        # ======================
        # EXIT
        # ======================
        elif choice == "0":
            print("Exiting system. Goodbye 👋")
            break
        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
