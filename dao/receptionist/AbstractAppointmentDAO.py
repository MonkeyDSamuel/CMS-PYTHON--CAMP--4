#Data Abstract Object
from abc import ABC, abstractmethod
from typing import List
from models.receptionist.Appointment import Appointment
from models.receptionist.Patient import Patient 
# import doc

class AppointmentDaoService(ABC):
    @abstractmethod
    def display_all_appointments(self) -> List[Appointment]:
        '''fetch all appointments'''
        pass

    @abstractmethod
    def insert_appointment(self) ->bool:
        '''insert a appointment to db'''
        pass

    @abstractmethod
    def find_by_appointment_id(self, appointment_id:int) -> Appointment:
        '''find a ppointment by ID'''
        pass

    @abstractmethod
    def find_by_patient_id(self, patient_id:int) -> Patient:
        '''find a patient by ID'''
        pass

    # @abstractmethod
    # def find_by_doctor_id(self, doctor_id:int) -> Doctor:
    #     '''find a doctor by ID and check availability''' #$$$$$$$$$$$$$$$
    #     pass

    @abstractmethod
    def update_appointment(self, appointment:Appointment, appointment_id:int) -> bool:
        '''update a appointment by ID'''
        pass

    # @abstractmethod
    # def apply_gst(self, patient_id:int, gst_percent:float) -> bool:
    #     '''compute the gst of the patient'''
    #     pass