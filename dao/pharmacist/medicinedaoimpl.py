import pymysql
from dataclasses import dataclass
from prettytable import PrettyTable

from db.db_connection import DBConnection


@dataclass
class Medicine:
    medicine_id: str
    category_id: str
    medicine_name: str
    company_name: str
    common_name: str
    strength: float
    rate_per_unit: float


class PharmacistDaoImplementation:
    def __init__(self):
        # Use shared DB connection
        self.conn = DBConnection().get_connection()
        self.cursor = self.conn.cursor()
        # Schema is managed via SQL dump; no runtime DDL here

    def _generate_id(self) -> str:
        """Generate sequential medicine_id like MED0001, MED0002..."""
        self.cursor.execute("SELECT Medicine_id FROM medicine ORDER BY Medicine_id DESC LIMIT 1")
        last_id = self.cursor.fetchone()
        if last_id:
            last_num = int(last_id[0][3:])  # strip 'MED' and convert to int
            new_id = f"MED{last_num+1:04d}"
        else:
            new_id = "MED0001"
        return new_id

    def add_medicine(
        self,
        category_id: str,
        medicine_name: str,
        company_name: str,
        common_name: str,
        strength: float,
        rate_per_unit: float,
    ) -> Medicine:
        # Validate foreign key for category
        self.cursor.execute(
            "SELECT 1 FROM medicine_category WHERE Category_id=%s LIMIT 1",
            (category_id,),
        )
        if self.cursor.fetchone() is None:
            raise ValueError(f"Invalid Category ID: {category_id}. Please create the category first.")
        med_id = self._generate_id()
        sql = """
            INSERT INTO medicine (
                Medicine_id, Category_id, Medicine_name, Company_name, Common_name, Strength, Rate_per_unit
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            sql,
            (
                med_id,
                category_id,
                medicine_name,
                company_name,
                common_name,
                strength,
                rate_per_unit,
            ),
        )
        self.conn.commit()
        return Medicine(
            med_id,
            category_id,
            medicine_name,
            company_name,
            common_name,
            strength,
            rate_per_unit,
        )

    def display_all_medicines(self):
        self.cursor.execute(
            "SELECT Medicine_id, Category_id, Medicine_name, Company_name, Common_name, Strength, Rate_per_unit FROM medicine"
        )
        rows = self.cursor.fetchall()
        return [Medicine(*row) for row in rows]

    def display_table(self):
        self.cursor.execute(
            "SELECT Medicine_id, Category_id, Medicine_name, Company_name, Common_name, Strength, Rate_per_unit FROM medicine"
        )
        rows = self.cursor.fetchall()
        if not rows:
            print("⚠ No medicines available!")
            return
        table = PrettyTable()
        table.field_names = [
            "Medicine ID",
            "Category ID",
            "Medicine Name",
            "Company Name",
            "Common Name",
            "Strength",
            "Rate per Unit (₹)",
        ]
        for row in rows:
            table.add_row([row[0], row[1], row[2], row[3], row[4], row[5], f"{row[6]:.2f}"])
        print(table)

    def search_medicine(self, med_id: str):
        self.cursor.execute(
            "SELECT Medicine_id, Category_id, Medicine_name, Company_name, Common_name, Strength, Rate_per_unit FROM medicine WHERE Medicine_id=%s",
            (med_id,),
        )
        row = self.cursor.fetchone()
        return Medicine(*row) if row else None

    def update_medicine(self, med_id: str, **kwargs):
        updates = []
        values = []
        for field, value in kwargs.items():
            updates.append(f"{field}=%s")
            values.append(value)
        if not updates:
            return False
        values.append(med_id)
        sql = f"UPDATE medicine SET {', '.join(updates)} WHERE Medicine_id=%s"
        self.cursor.execute(sql, tuple(values))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_medicine(self, med_id: str):
        self.cursor.execute("DELETE FROM medicine WHERE Medicine_id=%s", (med_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
