from dataclasses import dataclass
from datetime import date

class Category:
    def __init__(self, category_id=None, category_name=None):
        self.__category_id = category_id
        self.__category_name = category_name

    # Getters
    def get_category_id(self):
        return self.__category_id

    def get_category_name(self):
        return self.__category_name

    # Setters
    def set_category_id(self, category_id):
        self.__category_id = category_id

    def set_category_name(self, category_name):
        self.__category_name = category_name

    def __str__(self):
        return f"Category[ID={self.__category_id}, Name={self.__category_name}]"
