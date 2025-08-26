# dao/receptionist/AbstractAppointmentDAO.py
from abc import ABC, abstractmethod
from typing import List, Optional
from models.receptionist.Appointment import Appointment


class AppointmentDaoService(ABC):
    """Abstract DAO for Appointment"""

    @abstractmethod
    def display_all_appointments(self) -> List[Appointment]:
        """Fetch all appointments"""
        pass

    @abstractmethod
    def insert_appointment(self, appointment: Appointment) -> bool:
        """Insert a new appointment"""
        pass

    @abstractmethod
    def find_by_appointment_id(self, appointment_id: int) -> Optional[Appointment]:
        """Find appointment by its ID"""
        pass

    @abstractmethod
    def update_appointment(self, appointment: Appointment, appointment_id: int) -> bool:
        """Update appointment details"""
        pass

    @abstractmethod
    def cancel_appointment(self, appointment_id: int) -> bool:
        """Cancel appointment (status = Cancelled)"""
        pass

    @abstractmethod
    def find_by_patient_id(self, patient_id: int) -> List[Appointment]:
        """Get all appointments for a given patient"""
        pass

    @abstractmethod
    def find_by_doctor_id(self, doctor_id: int) -> List[Appointment]:
        """Get all appointments for a given doctor"""
        pass
