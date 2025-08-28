# Data Abstract Object
from abc import ABC, abstractmethod
from typing import List
from models.receptionist.Billing import Billing

class BillingDaoService(ABC):

    @abstractmethod
    def display_all_bills(self) -> List[Billing]:
        """Fetch all bills from DB"""
        pass

    @abstractmethod
    def insert_bill(self, billing: Billing) -> bool:
        """Insert a new bill record into DB"""
        pass

    @abstractmethod
    def find_by_bill_id(self, bill_id: str) -> Billing:
        """Find a bill by Bill ID"""
        pass

    @abstractmethod
    def update_bill(self, billing: Billing, bill_id: str) -> bool:
        """Update bill details by Bill ID"""
        pass

    @abstractmethod
    def delete_bill(self, bill_id: str) -> bool:
        """Delete a bill record by Bill ID"""
        pass

    # =========================
    # New Abstract Methods
    # =========================

    @abstractmethod
    def generate_bill_id(self) -> str:
        """Generate the next Bill ID in the format B00001, B00002..."""
        pass

    @abstractmethod
    def fetch_doctor_fee_by_appointment(self, appointment_id: str) -> int:
        """
        Get the consultation fee of the doctor 
        for the given appointment_id.
        """
        pass
