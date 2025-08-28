from dao.pharmacist.categorydaoimple import CategoryDaoImplementation
from models.pharmacist.p_category import Category

class CategoryManagementLib:
    dao_service = CategoryDaoImplementation()

    @staticmethod
    def add_category():
        name = input("Enter category name: ")
        cat = Category(category_name=name)
        success = CategoryManagementLib.dao_service.add_category(cat)
        if success:
            print(" Category added successfully")
        else:
            print(" Failed to add category")

    @staticmethod
    def display_categories():
        categories = CategoryManagementLib.dao_service.get_all_categories()
        print("\n--- Category List ---")
        for cat in categories:
            print(cat)

    @staticmethod
    def search_category():
        cat_id = input("Enter category ID to search: ")
        category = CategoryManagementLib.dao_service.search_category(cat_id)
        if category:
            print(" Found:", category)
        else:
            print(" Category not found")

    @staticmethod
    def delete_category():
        cat_id = input("Enter category ID to delete: ")
        success = CategoryManagementLib.dao_service.delete_category(cat_id)
        if success:
            print(" Category deleted successfully")
        else:
            print(" Failed to delete category")
