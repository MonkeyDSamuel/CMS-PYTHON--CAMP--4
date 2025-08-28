from abc import ABC, abstractmethod
from models.billing import Billing

class BillingDaoService(ABC):

    @abstractmethod
    def add_bill(self, bill: Billing):
        pass

    @abstractmethod
    def display_all_bills(self):
        pass

    @abstractmethod
    def search_bill_by_id(self, bill_id: str):
        pass

    @abstractmethod
    def delete_bill(self, bill_id: str):
        pass
