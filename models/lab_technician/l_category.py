from datetime import datetime

class TestCategory:
    def __init__(self, category_id: int, category_name: str):
        self.__category_id = category_id
        self.__category_name = category_name

    # Getters
    def get_category_id(self) -> int:
        return self.__category_id

    def get_category_name(self) -> str:
        return self.__category_name

    # Setters
    def set_category_id(self, category_id: int):
        self.__category_id = category_id

    def set_category_name(self, category_name: str):
        self.__category_name = category_name

    def __repr__(self):
        return f"TestCategory(ID={self.__category_id}, Name='{self.__category_name}')"

# Updated to align with SQL 'test_category' table
class LabCategory:
    def __init__(self, category_id: str, category_name: str):
        self.category_id = category_id
        self.category_name = category_name

    def __repr__(self):
        return f"LabCategory(ID={self.category_id}, Name='{self.category_name}')"

