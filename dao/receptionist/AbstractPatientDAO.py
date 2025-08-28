# Data Abstract Object
from abc import ABC, abstractmethod
from typing import List, Optional
from models.receptionist.Patient import Patient


class PatientDaoService(ABC):
    """Abstract DAO interface for Patient operations"""

    @abstractmethod
    def display_all_patients(self) -> List[Patient]:
        """Fetch all active patients"""
        pass

    @abstractmethod
    def insert_patient(self, patient: Patient) -> bool:
        """Insert a new patient into the database"""
        pass

    @abstractmethod
    def find_by_patient_id(self, patient_id: int) -> Optional[Patient]:
        """Find a patient by ID"""
        pass

    @abstractmethod
    def update_patient(self, patient: Patient, patient_id: int) -> bool:
        """Update a patient by ID"""
        pass

    @abstractmethod
    def disable_patient(self, patient_id: int) -> bool:
        """Disable (deactivate) a patient by ID"""
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> List[Patient]:
        """Find patients whose first or last name matches (case-insensitive, partial)."""
        pass