from abc import ABC, abstractmethod
from models.pharmacist.p_medicine import Medicine


class PharmacistDaoService(ABC):
    @abstractmethod
    def add_medicine(self, category_id, medicine_name, company_name, common_name, strength, rate_per_unit) -> Medicine:
        pass

    @abstractmethod
    def display_all_medicines(self):
        pass

    # @abstractmethod
    # def search_medicine(self, med_id: str):
    #     pass

    @abstractmethod
    def update_medicine(self, med_id: str, **kwargs):
        pass

    # @abstractmethod
    # def delete_medicine(self, med_id: str):
    #     pass
