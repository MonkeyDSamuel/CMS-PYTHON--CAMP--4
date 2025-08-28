from typing import List
from dao.lab_technician.l_AbstractCategory import AbstractCategoryDAO
from models.lab_technician.l_category import LabCategory
from db.db_connection import DBConnection
import pymysql

class CategoryDAOimple(AbstractCategoryDAO):
    """Implementation of Category DAO"""

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def _generate_next_category_id(self) -> str:
        """Generate next ID like CAT0001, CAT0002..."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(category_id) FROM test_category")
        last_id = cursor.fetchone()[0]
        cursor.close()
        if last_id:
            next_num = int(last_id.replace("CAT", "")) + 1
        else:
            next_num = 1
        return f"CAT{next_num:04d}"

    def create_category(self, category: LabCategory) -> bool:
        if self.conn is None:
            return False
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO test_category (category_id, category_name) VALUES (%s, %s)",
            (category.category_id, category.category_name),
        )
        self.conn.commit()
        cursor.close()
        return True

    def create_category_by_name(self, category_name: str) -> LabCategory:
        new_id = self._generate_next_category_id()
        category = LabCategory(new_id, category_name)
        self.create_category(category)
        return category

    def update_category(self, category_id: int, category: LabCategory) -> bool:
        if self.conn is None:
            return False
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE test_category SET category_name = %s WHERE category_id = %s",
            (category.category_name, category_id),
        )
        self.conn.commit()
        cursor.close()
        return True

    def deactivate_category(self, category_id: int) -> bool:
        # No is_active field mentioned; perform no-op or delete if needed
        return True

    def find_by_category_id(self, category_id: int) -> LabCategory:
        if self.conn is None:
            return None
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT category_id, category_name FROM test_category WHERE category_id = %s", (category_id,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return LabCategory(row["category_id"], row["category_name"])

    def list_all_categories(self) -> List[LabCategory]:
        if self.conn is None:
            return []
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT category_id, category_name FROM test_category ORDER BY category_id")
        rows = cursor.fetchall()
        cursor.close()
        return [LabCategory(r["category_id"], r["category_name"]) for r in rows]