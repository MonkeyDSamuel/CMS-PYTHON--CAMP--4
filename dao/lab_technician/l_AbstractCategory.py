from abc import ABC, abstractmethod
from typing import List
from models.lab_technician.l_category import LabCategory  # assuming you have a LabCategory model

class AbstractCategoryDAO(ABC):
    """Abstract DAO for Lab Test Category"""

    @abstractmethod
    def create_category(self, category: LabCategory) -> bool:
        """Create a new Lab Test Category"""
        pass

    @abstractmethod
    def create_category_by_name(self, category_name: str) -> LabCategory:
        """Create a new category with auto-generated ID and return it"""
        pass

    @abstractmethod
    def update_category(self, category_id: int, category: LabCategory) -> bool:
        """Update Lab Test Category"""
        pass

    @abstractmethod
    def deactivate_category(self, category_id: int) -> bool:
        """Deactivate Lab Test Category"""
        pass

    @abstractmethod
    def find_by_category_id(self, category_id: int) -> LabCategory:
        """Find Lab Test Category by ID"""
        pass

    @abstractmethod
    def list_all_categories(self) -> List[LabCategory]:
        """List all Lab Test Categories"""
        pass