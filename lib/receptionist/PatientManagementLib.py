from dao.receptionist.PatientDAOImple import PatientDaoImplementation
from dao.receptionist.AbstractPatientDAO import PatientDaoService
from models.receptionist.Patient import Patient
from datetime import datetime


class PatientManagementLib:
    """Handles CRUD logic for Patient"""
    dao_service: PatientDaoService = PatientDaoImplementation()

    @staticmethod
    def display_all():
        patients = PatientManagementLib.dao_service.display_all_patients()
        if not patients:
            print("No patients found.")
            return
        for patient in patients:
            print(patient)

    @staticmethod
    def add_patient():
        patient = Patient()

        patient.first_name = input("Enter the patient's first name: ")
        patient.last_name = input("Enter the patient's last name: ")

        dob_str = input("Enter Date of Birth (dd/mm/yyyy): ")
        patient.DOB = datetime.strptime(dob_str, "%d/%m/%Y").date()

        patient.phone_no = input("Enter the Phone number: ").strip()
        patient.email = input("Enter the email: ")
        patient.address = input("Enter the address: ")
        patient.height = float(input("Enter the height (in cm): "))
        patient.weight = float(input("Enter the weight (in kg): "))
        patient.gender = input("Enter the gender: ")
        patient.blood_group = input("Enter the blood group: ")
        patient.marital_status = input("Enter the marital status: ")
        patient.current_medications = input("Enter the current medications: ")
        patient.emergency_contact = input("Enter emergency contact number: ").strip()

        if PatientManagementLib.dao_service.insert_patient(patient):
            print("Inserted Successfully!!")
        else:
            print("Something went wrong...")

    @staticmethod
    def update_patient():
        search_id = input("Enter the patient ID (e.g., P0000001): ").strip()
        patient = PatientManagementLib.dao_service.find_by_patient_id(search_id)

        if not patient:
            print("Patient not found")
            return

        print("Current details:", patient)
        confirm = input("Do you want to edit this data? (y/n): ")
        if confirm.lower() != 'y':
            return

        # Update only if user provides a value, else keep old
        new_first_name = input(f"Enter new first name ({patient.first_name}): ") or patient.first_name
        new_last_name = input(f"Enter new last name ({patient.last_name}): ") or patient.last_name
        new_phone = input(f"Enter new phone no ({patient.phone_no}): ") or patient.phone_no
        new_email = input(f"Enter new email ({patient.email}): ") or patient.email
        new_address = input(f"Enter new address ({patient.address}): ") or patient.address

        # Assign back
        patient.first_name = new_first_name
        patient.last_name = new_last_name
        patient.phone_no = new_phone.strip()
        patient.email = new_email
        patient.address = new_address

        if PatientManagementLib.dao_service.update_patient(patient, search_id):
            print("Updated successfully.")
        else:
            print("Something went wrong...")

    @staticmethod
    def search_by_id():
        search_id = input("Enter the patient ID (e.g., P0000001): ").strip()
        patient = PatientManagementLib.dao_service.find_by_patient_id(search_id)

        if not patient:
            print("Patient not found")
        else:
            print(patient)

    @staticmethod
    def disable_patient():
        search_id = input("Enter the patient ID (e.g., P0000001): ").strip()
        patient = PatientManagementLib.dao_service.find_by_patient_id(search_id)

        if not patient:
            print("Patient not found")
            return

        confirm = input(f"Are you sure you want to disable patient {patient.first_name} {patient.last_name}? (y/n): ")
        if confirm.lower() != 'y':
            return

        # set status to 'N' and send both patient entity and id to DAO
        patient.is_active = 'N'
        if PatientManagementLib.dao_service.disable_patient(patient, search_id):
            print("Patient disabled successfully.")
        else:
            print("Something went wrong...")
