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

        # First Name validation loop
        while True:
            first_name = input("Enter the patient's first name: ").strip()
            try:
                patient.first_name = first_name
                break
            except ValueError as e:
                print(f"❌ {e}. Please try again.")

        # Last Name validation loop
        while True:
            last_name = input("Enter the patient's last name: ").strip()
            try:
                patient.last_name = last_name
                break
            except ValueError as e:
                print(f"❌ {e}. Please try again.")

        # Date of Birth validation loop
        while True:
            dob_str = input("Enter Date of Birth (dd/mm/yyyy): ").strip()
            try:
                patient.DOB = datetime.strptime(dob_str, "%d/%m/%Y").date()
                break
            except ValueError:
                print("❌ Invalid date format. Please use dd/mm/yyyy format.")

        # Phone Number validation loop
        while True:
            phone_no = input("Enter the Phone number: ").strip()
            try:
                patient.phone_no = phone_no
                break
            except ValueError as e:
                print(f"❌ {e}. Please try again.")

        # Email validation loop with improved regex
        while True:
            email = input("Enter the email: ").strip()
            try:
                patient.email = email
                break
            except ValueError as e:
                print(f"❌ {e}. Please try again.")

        # Address validation loop
        while True:
            address = input("Enter the address: ").strip()
            try:
                patient.address = address
                break
            except ValueError as e:
                print(f"❌ {e}. Please try again.")

        # Height validation loop
        while True:
            try:
                height_input = input("Enter the height (in cm): ").strip()
                height = float(height_input)
                patient.height = height
                break
            except ValueError:
                print("❌ Height must be a valid number. Please try again.")

        # Weight validation loop
        while True:
            try:
                weight_input = input("Enter the weight (in kg): ").strip()
                weight = float(weight_input)
                patient.weight = weight
                break
            except ValueError:
                print("❌ Weight must be a valid number. Please try again.")

        # Gender validation loop with format guidance
        print("Gender options: 'm' (Male), 'f' (Female), 'o' (Other)")
        while True:
            gender = input("Enter the gender (m/f/o): ").strip().lower()
            try:
                patient.gender = gender
                break
            except ValueError as e:
                print(f"❌ {e}. Please enter 'm', 'f', or 'o'.")

        # Blood Group validation loop (accept lowercase, will display uppercase)
        print("Blood group options: A+, A-, B+, B-, O+, O-, AB+, AB-")
        while True:
            blood_group = input("Enter the blood group: ").strip()
            try:
                patient.blood_group = blood_group
                break
            except ValueError as e:
                print(f"❌ {e}. Please try again.")

        # Marital Status validation loop
        print("Marital status options: 'm' (Married), 'um' (Unmarried), 'o' (Other)")
        while True:
            marital_status = input("Enter the marital status (m/um/o): ").strip().lower()
            try:
                patient.marital_status = marital_status
                break
            except ValueError as e:
                print(f"❌ {e}. Please enter 'm', 'um', or 'o'.")

        # Current Medications validation loop
        while True:
            current_medications = input("Enter the current medications: ").strip()
            try:
                patient.current_medications = current_medications
                break
            except ValueError as e:
                print(f"❌ {e}. Please try again.")

        # Emergency Contact validation loop
        while True:
            emergency_contact = input("Enter emergency contact number: ").strip()
            try:
                patient.emergency_contact = emergency_contact
                break
            except ValueError as e:
                print(f"❌ {e}. Please try again.")

        if PatientManagementLib.dao_service.insert_patient(patient):
            print("✅ Insertion successful.")
            print(f"Patient ID: {patient.patient_id}")
        else:
            print("❌ Something went wrong...")

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
