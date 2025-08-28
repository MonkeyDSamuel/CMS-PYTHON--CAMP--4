from abc import ABC, abstractmethod
from typing import List
from models.lab_technician.l_billing import LabBilling  # assuming you have a LabBilling model

class AbstractBillingDAO(ABC):
    """Abstract DAO for Lab Test Billing"""

    @abstractmethod
    def create_bill(self, bill: LabBilling) -> bool:
        """Create a new Lab Test Bill"""
        pass

    @abstractmethod
    def update_bill(self, bill_id: int, bill: LabBilling) -> bool:
        """Update an existing Lab Test Bill"""
        pass

    @abstractmethod
    def find_by_bill_id(self, bill_id: int) -> LabBilling:
        """Search Lab Test Bill by BillId"""
        pass

    @abstractmethod
    def list_all_bills(self) -> List[LabBilling]:
        """List all Lab Test Bills"""
        pass

    @abstractmethod
    def list_bills_by_patient_id(self, patient_id: int) -> List[LabBilling]:
        """List Lab Test Bills by PatientId"""
        pass

    @abstractmethod
    def list_bills_by_date(self, date: str) -> List[LabBilling]:
        """List Lab Test Bills by Date"""
        pass