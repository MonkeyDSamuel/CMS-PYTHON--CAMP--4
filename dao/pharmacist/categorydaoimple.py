from dao.pharmacist.abstractcategory import CategoryDaoService
from models.pharmacist.p_category import Category
from db.db_connection import DBConnection

class CategoryDaoImplementation(CategoryDaoService):
    INSERT_CATEGORY = "INSERT INTO medicine_category (Category_id, Category_name) VALUES (%s, %s)"
    SELECT_ALL = "SELECT Category_id, Category_name FROM medicine_category"
    SEARCH_BY_ID = "SELECT Category_id, Category_name FROM medicine_category WHERE Category_id=%s"
    DELETE_CATEGORY = "DELETE FROM medicine_category WHERE Category_id=%s"
    LAST_ID_QUERY = "SELECT Category_id FROM medicine_category ORDER BY Category_id DESC LIMIT 1"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    # helper to auto-generate category id
    def generate_category_id(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute(self.LAST_ID_QUERY)
        last = cursor.fetchone()
        if last:
            last_id = last[0]   # e.g. CAT002
            num = int(last_id.replace("CAT", "")) + 1
            new_id = f"CAT{num:03d}"
        else:
            new_id = "CAT001"
        cursor.close()
        return new_id

    def add_category(self, category: Category) -> bool:
        try:
            cursor = self.conn.cursor()
            new_id = self.generate_category_id()
            cursor.execute(self.INSERT_CATEGORY, (new_id, category.get_category_name()))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error adding category:", e)
            return False
        finally:
            cursor.close()

    def get_all_categories(self):
        categories = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.SELECT_ALL)
            rows = cursor.fetchall()
            for row in rows:
                # Expected order: (Category_id, Category_name)
                categories.append(Category(row[0], row[1]))
        except Exception as e:
            print("Error fetching categories:", e)
        finally:
            cursor.close()
        return categories

    def search_category(self, category_id: str):
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.SEARCH_BY_ID, (category_id,))
            row = cursor.fetchone()
            if row:
                return Category(row[0], row[1])
            return None
        except Exception as e:
            print("Error searching category:", e)
            return None
        finally:
            cursor.close()

    def delete_category(self, category_id: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.DELETE_CATEGORY, (category_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error deleting category:", e)
            return False
        finally:
            cursor.close()
