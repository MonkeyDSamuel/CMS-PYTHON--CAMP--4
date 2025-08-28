from db.db_connection import DBConnection
from lib.receptionist.PatientManagementLib import PatientManagementLib
from lib.receptionist.AppointmentManagementLib import AppointmentManagementLib
from lib.receptionist.BillingManagementLib import BillingManagementLib


def main():
    patient_lib = PatientManagementLib()
    appointment_lib = AppointmentManagementLib()
    billing_lib = BillingManagementLib()

    while True:
        print("\n======= PATIENT MANAGEMENT SYSTEM =======")
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
            print("1. Add new patient")
            print("2. List all patients")
            print("3. Find patient by ID")
            print("4. Find patients by Name")
            print("5. Update patient")
            print("6. De-activate patient")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                PatientManagementLib.add_patient()
            elif sub_choice == "2":
                PatientManagementLib.display_all()
            elif sub_choice == "3":
                PatientManagementLib.search_by_id()
            elif sub_choice == "4":
                PatientManagementLib.search_by_name()
            elif sub_choice == "5":
                PatientManagementLib.update_patient()
            elif sub_choice == "6":
                PatientManagementLib.disable_patient()

        # ======================
        # APPOINTMENT MANAGEMENT
        # ======================
        elif choice == "2":
            print("\n--- Appointment Management ---")
            print("1. Create new appointment")
            print("2. List all appointments")
            print("3. Find appointment by ID")
            print("4. View appointments by date")
            print("5. View appointments by doctor ID")
            print("6. View pending appointments by date")
            print("7. Cancel appointment")
            print("8. Update appointment date")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                appointment_lib.create_appointment()
            elif sub_choice == "2":
                appointment_lib.display_all_appointments()
            elif sub_choice == "3":
                appointment_lib.find_appointment_by_id()
            elif sub_choice == "4":
                appointment_lib.search_appointments_by_date()
            elif sub_choice == "5":
                appointment_lib.view_appointments_by_doctor()
            elif sub_choice == "6":
                appointment_lib.view_pending_appointments_by_date()
            elif sub_choice == "7":
                appointment_lib.cancel_appointment()
            elif sub_choice == "8":
                appointment_lib.update_appointment_date()

        # ======================
        # BILLING MANAGEMENT
        # ======================
        elif choice == "3":
            print("\n--- Billing Management ---")
            print("1. Create new bill")
            print("2. List all bills")
            print("3. Find bill by ID")
            print("4. View bills by date")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                billing_lib.create_bill()
            elif sub_choice == "2":
                billing_lib.display_all_bills()
            elif sub_choice == "3":
                bid = input("Enter bill ID: ")
                billing_lib.find_by_bill_id(bid)
            elif sub_choice == "4":
                billing_lib.search_bills_by_date()

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
