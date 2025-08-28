from models.lab_technician.l_lab_test import LabTest
# from dao.l_TestDAOimple import TestDAOimple   # create later
from db.db_connection import DBConnection
from dao.lab_technician.l_labtestDAOimpl import LabTestDAOImpl

class LabTestLib:
    # test_dao = TestDAOimple()  # Uncomment when DAO ready

    @staticmethod
    def add_test():
        try:
            print("\n--- Add New Lab Test ---")
            lab_test_name = input("Enter Test Name: ")
            category_id = input("Enter Category ID (e.g., CAT0001): ").strip()
            rate = float(input("Enter Rate: "))
            created_on = input("Enter Created On (YYYY-MM-DD): ")
            min_value = float(input("Enter Min Range: "))
            max_value = float(input("Enter Max Range: "))

            conn = DBConnection().get_connection()
            if conn is None:
                print("Database connection not available.")
                return
            dao = LabTestDAOImpl(conn)
            new_id = dao.create_labtest(
                lab_test_name=lab_test_name,
                category_id=category_id,
                rate=rate,
                created_on=created_on,
                min_value=min_value,
                max_value=max_value,
            )
            print(f"Test created successfully with ID: {new_id}")
        except Exception as e:
            print(f"Error adding test: {e}")

    @staticmethod
    def display_all_tests():
        print("\n--- All Lab Tests ---")
        try:
            conn = DBConnection().get_connection()
            if conn is None:
                print("Database connection not available.")
                return
            dao = LabTestDAOImpl(conn)
            rows = dao.list_labtests()
            if not rows:
                print("No lab tests found.")
                return
            for row in rows:
                # Columns per schema: lab_test_id, lab_test_name, category_id, rate, created_on, min_value, max_value, is_active
                print(
                    f"{row.get('lab_test_id')} | {row.get('lab_test_name')} | Cat: {row.get('category_id')} | "
                    f"Rate: {row.get('rate')} | Range: {row.get('min_value')}-{row.get('max_value')} | "
                    f"Active: {row.get('is_active')}"
                )
        except Exception as e:
            print(f"Error fetching lab tests: {e}")

    @staticmethod
    def update_test():
        try:
            print("\n--- Update Lab Test ---")
            lab_test_id = input("Enter Test ID: ")
            new_name = input("New Name (leave blank to skip): ").strip()
            new_category = input("New Category ID (e.g., CAT0001; leave blank to skip): ").strip()
            new_rate = input("New Rate (leave blank to skip): ").strip()
            new_min = input("New Min Range (leave blank to skip): ").strip()
            new_max = input("New Max Range (leave blank to skip): ").strip()

            conn = DBConnection().get_connection()
            if conn is None:
                print("Database connection not available.")
                return
            dao = LabTestDAOImpl(conn)
            updated = dao.update_labtest(
                lab_test_id,
                lab_test_name=new_name if new_name else None,
                category_id=new_category if new_category else None,
                rate=float(new_rate) if new_rate else None,
                min_value=float(new_min) if new_min else None,
                max_value=float(new_max) if new_max else None,
            )
            if updated:
                print("Test updated successfully.")
            else:
                print("Nothing to update.")
        except Exception as e:
            print(f"Error updating test: {e}")

    @staticmethod
    def deactivate_test():
        try:
            print("\n--- Deactivate Lab Test ---")
            lab_test_id = input("Enter Test ID to deactivate: ")
            conn = DBConnection().get_connection()
            if conn is None:
                print("Database connection not available.")
                return
            dao = LabTestDAOImpl(conn)
            ok = dao.deactivate_labtest(lab_test_id)
            if ok:
                print("Test deactivated successfully.")
        except Exception as e:
            print(f"Error deactivating test: {e}")