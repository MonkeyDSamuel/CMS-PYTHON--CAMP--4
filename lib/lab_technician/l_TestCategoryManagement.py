from dao.lab_technician.l_CategoryDAOimple import CategoryDAOimple
from models.lab_technician.l_category import LabCategory

class LabCategoryLib:
    category_dao = CategoryDAOimple()

    @staticmethod
    def add_category():
        try:
            category_name = input("Enter Category Name: ")
            category = LabCategoryLib.category_dao.create_category_by_name(category_name)
            print(f" Category added successfully with ID {category.category_id}.")
        except Exception as e:
            print(f" Error adding category: {e}")

    @staticmethod
    def display_all_categories():
        categories = LabCategoryLib.category_dao.list_all_categories()
        if categories:
            print("\n--- All Categories ---")
            for c in categories:
                print(f"ID: {c.category_id} | Name: {c.category_name}")
        else:
            print(" No categories found.")