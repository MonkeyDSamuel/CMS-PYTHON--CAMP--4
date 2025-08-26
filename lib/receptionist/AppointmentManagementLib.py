from dao.receptionist.AppointmentDAOImple import AppointmentDaoImplementation
from dao.receptionist.AbstractAppointmentDAO import AppointmentDaoService
from models.receptionist.Appointment import Appointment
from datetime import datetime

class AppointmentManagementLib:
    'handles CRUD logic'
    dao_service:AppointmentDaoService = AppointmentDaoImplementation()

    @staticmethod
    def display_all():
        appointments = AppointmentManagementLib.dao_service.display_all_appointments()
        for appointment in appointments:
            print(appointment)
    
    @staticmethod
    def add_appointment():
        appointment = Appointment()
        patient_id = input("Enter the appointment Name: ")
        appointment.patient_id(patient_id)
        doctor_id = input("Enter the appointment Name: ")
        appointment.doctor_id(doctor_id)
        appointment_date = input("Enter manufacture Date(dd/mm/yyyy): ") #or current date.today
        util_date = datetime.strptime(appointment_date, "%d/%m/%Y")
        conv_m_date = util_date.date()
        appointment.appointment_date(conv_m_date)
        reason = input("Enter the appointment Name: ")
        appointment.reason(reason)

        if AppointmentManagementLib.dao_service.insert_appointments(appointment):
            print("Inserted Successfully!!")
        else:
            print("Something went wrong.....")
        
#token is auto generated
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&        


    @staticmethod
    def update_appointment():
        searchId = int(input("Enter the appointment ID: "))
        #create a method in DAO
        appointment = AppointmentManagementLib.dao_service.find_by_appointment_id(searchId)
        if not appointment:
            print("Appointment not found")
            return
        print(appointment)
        confirm = input("Do you want to edit this data? (y/n)")
        if confirm.lower() == 'y':
            appointment.set_appointment_name(input("Enter new appointment Name: ") or appointment.get_appointmentname())
            appointment.set_unitprice(float(input("Enter New Unit Price: ")) or appointment.get_unitprice())

            #pass the object to dao update
            if AppointmentManagementLib.dao_service.update_appointment(appointment, searchId):
                print("updated successfully ....")
            else:
                print("something went wrong ....")

    @staticmethod
    def search_by_id():
        searchId = int(input("Enter the appointment ID: "))
        #create a method in DAO
        appointment = AppointmentManagementLib.dao_service.find_by_appointment_id(searchId)
        if not appointment:
            print("Appointment not found")
            return
        print(appointment)
    
    @staticmethod
    def disable_appointment():
        searchId = int(input("Enter the appointment ID: "))
        #create a method in DAO
        appointment = AppointmentManagementLib.dao_service.find_by_appointment_id(searchId)
        if not appointment:
            print("Appointment not found")
            return
        print(appointment)
        appointment.set_is_active("N")

        #pass the object to dao update
        if AppointmentManagementLib.dao_service.disable_appointment(appointment, searchId):
            print("updated successfully ....")
        else:
            print("something went wrong ....")

        # if AppointmentManagementLib.dao_service.disable_appointment(appointment, searchId):

    @staticmethod
    def apply_gst_to_appointment():
        appointment_id = int(input("Enter the appointment ID to apply GST: "))
        gst_percent = float(input("Enter GST percentage to apply: "))
        if AppointmentManagementLib.dao_service.apply_gst(appointment_id, gst_percent):
            print(f"GST of {gst_percent} applied to appointment ID (appointment_id)")
        else:
            print("failed to apply GST")