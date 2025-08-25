from abc import ABC, abstractmethod
from typing import List
from models.lab_models import LabTest, LabTestResult, LabBilling, TestCategory

class LabDaoService(ABC):
    """Abstract DAO for Lab Technician Module"""

    # Test Category
    @abstractmethod
    def add_test_category(self, category: TestCategory) -> bool: pass
    @abstractmethod
    def list_test_categories(self) -> List[TestCategory]: pass

    # Lab Test
    @abstractmethod
    def add_lab_test(self, test: LabTest) -> bool: pass
    @abstractmethod
    def update_lab_test(self, test_id: int, updated_test: LabTest) -> bool: pass
    @abstractmethod
    def deactivate_lab_test(self, test_id: int) -> bool: pass
    @abstractmethod
    def get_lab_test_by_id(self, test_id: int) -> LabTest: pass
    @abstractmethod
    def list_lab_tests(self) -> List[LabTest]: pass

    # Lab Test Result
    @abstractmethod
    def add_lab_test_result(self, result: LabTestResult) -> bool: pass
    @abstractmethod
    def update_lab_test_result(self, result_id: int, updated_result: LabTestResult) -> bool: pass
    @abstractmethod
    def get_lab_test_result_by_id(self, result_id: int) -> LabTestResult: pass
    @abstractmethod
    def list_lab_test_results(self) -> List[LabTestResult]: pass

    # Lab Billing
    @abstractmethod
    def create_bill(self, bill: LabBilling) -> bool: pass
    @abstractmethod
    def get_bill_by_id(self, bill_id: int) -> LabBilling: pass
    @abstractmethod
    def list_bills(self) -> List[LabBilling]: pass
