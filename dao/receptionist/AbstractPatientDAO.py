#Data Abstract Object
from abc import ABC, abstractmethod
from typing import List
from models.receptionist.Patient import Patient

class PatientDaoService(ABC):
    @abstractmethod
    def display_all_patients(self) -> List[Patient]:
        '''fetch all patients'''
        pass

    @abstractmethod
    def insert_patient(self) ->bool:
        '''insert a patient to db'''
        pass

    @abstractmethod
    def find_by_patient_id(self, patient_id:int) -> Patient:
        '''find a patient by ID'''
        pass
    
    @abstractmethod
    def update_patient(self, patient:Patient, patient_id:int) -> bool:
        '''update a patient by ID'''
        pass

    # @abstractmethod
    # def apply_gst(self, patient_id:int, gst_percent:float) -> bool:
    #     '''compute the gst of the patient'''
    #     pass