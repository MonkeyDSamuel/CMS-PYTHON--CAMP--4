#Data Abstract Object
from abc import ABC, abstractmethod
from typing import List
from models.receptionist.Billing import Billing

class BillingDaoService(ABC):
    @abstractmethod
    def display_all_billings(self) -> List[Billing]:
        '''fetch all billings'''
        pass

    @abstractmethod
    def insert_billings(self) ->bool:
        '''insert a billing to db'''
        pass

    @abstractmethod
    def find_by_billing_id(self, billing_id:int) -> Billing:
        '''find a billing by ID'''
        pass
    
    @abstractmethod
    def update_billing(self, billing:Billing, billing_id:int) -> bool:
        '''update a billing by its ID'''
        pass

    # @abstractmethod
    # def apply_gst(self, billing_id:int, gst_percent:float) -> bool:
    #     '''compute the gst of the billing'''
    #     pass