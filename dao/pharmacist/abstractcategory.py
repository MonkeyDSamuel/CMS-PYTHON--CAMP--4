from abc import ABC, abstractmethod
from models.pharmacist.p_category import Category
from typing import List

class CategoryDaoService(ABC):

    @abstractmethod
    def add_category(self, category: Category) -> bool:
        pass

    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def search_category(self, category_id: str) -> Category:
        pass

    @abstractmethod
    def delete_category(self, category_id: str) -> bool:
        pass
