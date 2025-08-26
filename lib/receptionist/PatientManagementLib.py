from dao.receptionist.PatientDAOImple import PatientDaoImplementation
from dao.receptionist.AbstractPatientDAO import PatientDaoService
from models.receptionist.Patient import Patient
from datetime import datetime

class PatientManagementLib:
    'handles CRUD logic'
    dao_service:PatientDaoService = PatientDaoImplementation()

    @staticmethod
    def display_all():
        patients = PatientManagementLib.dao_service.display_all_patients()
        for patient in patients:
            print(patient)
    
    @staticmethod
    def add_patient():
        patient = Patient()
        first_name = input("Enter the patient's first Name: ")
        patient.first_name(first_name)
        last_name = input("Enter the patient's last Name: ")
        patient.last_name(last_name)
        DOB = input("Enter Date of Birth Date(dd/mm/yyyy): ")
        util_date = datetime.strptime(DOB, "%d/%m/%Y")
        conv_m_date = util_date.date() #$$$$$$$$$$$$$$$$$$$$$$$$$$$ Use conversion
        patient.DOB(conv_m_date) #$$$$$$$$$$$$$$$$$$$$$$$$$$$
        phone_no = int(input("Enter the Phone number: "))
        patient.phone_no(phone_no)
        email = int(input("Enter the email "))
        patient.email(email)
        address = input("Enter the address: ")
        patient.address(address)
        height = int(input("Enter the height: "))
        patient.height(height)
        weight = int(input("Enter the weight: "))
        patient.weight(weight)
        gender = input("Enter the gender: ")
        patient.gender(gender)
        blood_group = input("Enter the blood group: ")
        patient.blood_group(blood_group)
        marital_status = input("Enter the marital status: ")
        patient.marital_status(marital_status)
        marital_status = input("Enter the marital status: ")
        patient.marital_status(marital_status)
        current_medication = input("Enter the current medication: ")
        patient.current_medication(current_medication)
        emergency_contact = int(input("Enter the Phone number: "))
        patient.emergency_contact(emergency_contact)

        if PatientManagementLib.dao_service.insert_patient(patient):
            print("Inserted Successfully!!")
        else:
            print("Something went wrong.....")

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&        

    @staticmethod
    def update_patient():
        searchId = int(input("Enter the patient ID: "))
        #create a method in DAO
        patient = PatientManagementLib.dao_service.find_by_patient_id(searchId)
        if not patient:
            print("Patient not found")
            return
        print(patient)
        confirm = input("Do you want to edit this data? (y/n)")
        if confirm.lower() == 'y':
            patient.set_patient_name(input("Enter new patient Name: ") or patient.get_patientname())
            patient.set_unitprice(float(input("Enter New Unit Price: ")) or patient.get_unitprice())

            #pass the object to dao update
            if PatientManagementLib.dao_service.update_patient(patient, searchId):
                print("updated successfully ....")
            else:
                print("something went wrong ....")

    @staticmethod
    def search_by_id():
        searchId = int(input("Enter the patient ID: "))
        #create a method in DAO
        patient = PatientManagementLib.dao_service.find_by_patient_id(searchId)
        if not patient:
            print("Patient not found")
            return
        print(patient)
    
    @staticmethod
    def disable_patient():
        searchId = int(input("Enter the patient ID: "))
        #create a method in DAO
        patient = PatientManagementLib.dao_service.find_by_patient_id(searchId)
        if not patient:
            print("Patient not found")
            return
        print(patient)
        patient.set_is_active("N")

        #pass the object to dao update
        if PatientManagementLib.dao_service.disable_patient(patient, searchId):
            print("updated successfully ....")
        else:
            print("something went wrong ....")

        # if PatientManagementLib.dao_service.disable_patient(patient, searchId):

    @staticmethod
    def apply_gst_to_patient():
        patient_id = int(input("Enter the patient ID to apply GST: "))
        gst_percent = float(input("Enter GST percentage to apply: "))
        if PatientManagementLib.dao_service.apply_gst(patient_id, gst_percent):
            print(f"GST of {gst_percent} applied to patient ID (patient_id)")
        else:
            print("failed to apply GST")