from datetime import date
import re
class Appointment:
    'Appointment fields'
    def __init__(self, appointment_id = None, patient_id = None,
                 doctor_id = None, appointment_date = None,
                 token_no = None, reason = None):
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id= doctor_id 
        self.__appointment_date = appointment_date
        self.__token_no = token_no
        self.__reason = reason

#---------------------------
#GETTERS AND SETTERS
#---------------------------

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Appointment ID
    @property
    def appointment_id(self):
        return self.__appointment_id

    @appointment_id.setter
    def appointment_id(self, appointment_id):
        if appointment_id is not None and not isinstance(appointment_id, int):
            raise ValueError("Appointment ID must be an integer")
        self.__appointment_id = appointment_id
        
        # Note: ID must be a str as per set in mysql sequence (P00001)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Patient ID
    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, patient_id):
        self.__patient_id = patient_id
        
        # Note: ID must be a str as per set in mysql sequence (P00001)
        # Figure out how to check if this value exists in the 'patient' table and raise another error if it doesn't
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Doctor ID
    @property
    def doctor_id(self):
        return self.__doctor_id

    @doctor_id.setter
    def doctor_id(self, doctor_id):
        if doctor_id is not None and not isinstance(doctor_id, int):
            raise ValueError("patient_id must be an integer")
        self.__doctor_id = doctor_id
        
        # Note: ID must be a str as per set in mysql sequence (P00001)
        # Figure out how to check if this value exists in the 'doctor' table and raise another error if it doesn't
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Appointment Date
    @property
    def appointment_date(self):
        return self.__appointment_date

    @appointment_date.setter
    def appointment_date(self, appointment_date):
        if appointment_date and not isinstance(appointment_date, date):
            raise ValueError("DOB must be a date object")
        self.__appointment_date = appointment_date

        #Note: Validation must be done for appointment to be in current and future dates(+14 days only)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Token Number
    @property
    def token_no(self):
        return self.__token_no

    @token_no.setter
    def token_no(self, token_no):
        if token_no and (not token_no.isdigit() or len(token_no) < 10):
            raise ValueError("Phone must be numeric and at least 10 digits") # $$$$$Check this code again
        self.__token_no = token_no

        #Note: Code must be restructured altogether so as to auto count for each doctor
        # Validation must be done as token numbers should not exceed a value of 30
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    #Reason
    @property
    def reason(self):
        return self.__reason

    @reason.setter
    def reason(self, reason):
        if reason and not isinstance(reason, str):
            raise ValueError("Reason must be text")
        self.__reason = reason

    # #Is Active
    # @property
    # def is_active(self):
    #     return self.__is_active
    # @is_active.setter
    # def is_active(self, is_active):
    #     self.__is_active = is_active
    #check it's need

    
    #override__str__
    def __str__(self):
        return f"""
        Appointment ID: {self.__appointment_id}
        Patient ID: {self.__patient_id}
        Doctor ID: {self.__doctor_id}
        Appointment Date: {self.__appointment_date}
        Token Number: {self.__token_no}
        Reason: {self.__reason}
        """