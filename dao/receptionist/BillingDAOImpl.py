from db.db_connection import DBConnection
from dao.receptionist.AbstractBillingDAO import BillingDaoService
from models.receptionist.Billing import Billing
from datetime import date
from typing import List


class BillingDaoImplementation(BillingDaoService):

    # =============================
    # SQL Queries
    # =============================
    QUERY_DISPLAY_ALL = """
        SELECT bill_id, appointment_id, total_bill, Billing_date 
        FROM appointment_billing
    """
    QUERY_INSERT = """
        INSERT INTO appointment_billing (bill_id, appointment_id, total_bill) 
        VALUES (%s, %s, %s)
    """
    QUERY_FIND_BY_ID = """
        SELECT bill_id, appointment_id, total_bill, Billing_date 
        FROM appointment_billing WHERE bill_id = %s
    """
    QUERY_UPDATE = """
        UPDATE appointment_billing 
        SET appointment_id = %s, total_bill = %s 
        WHERE bill_id = %s
    """
    QUERY_DELETE = """
        DELETE FROM appointment_billing WHERE bill_id = %s
    """
    QUERY_FIND_BY_DATE = """
        SELECT bill_id, appointment_id, total_bill, Billing_date 
        FROM appointment_billing WHERE DATE(Billing_date) = %s
    """
    QUERY_GET_LAST_ID = """
        SELECT bill_id FROM appointment_billing ORDER BY bill_id DESC LIMIT 1
    """
    QUERY_DOCTOR_FEE_BY_APPT = """
        SELECT d.Charge
        FROM appointment a
        JOIN doctor d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_id = %s
    """
    QUERY_UPDATE_APPT_STATUS_ACTIVE = """
        UPDATE appointment SET app_status = %s WHERE Appointment_id = %s
    """

    # =============================
    # Constructor (DB connection)
    # =============================
    def __init__(self, host="localhost", user="root", password="", database="clinic_db"):
        try:
            # Reuse the shared DB connection configured via db_config.ini
            self.conn = DBConnection().get_connection()
            self.cursor = self.conn.cursor()
        except Exception as err:
            print("Database connection error:", err)
            raise

    # =============================
    # Helper: Generate next Bill ID
    # =============================
    def generate_bill_id(self) -> str:
        self.cursor.execute(self.QUERY_GET_LAST_ID)
        last_id = self.cursor.fetchone()

        if last_id is None:
            return "B00001"
        else:
            last_num = int(last_id[0][1:])  # strip 'B' and convert
            new_num = last_num + 1
            return f"B{new_num:05d}"

    # =============================
    # Helper: Fetch Doctor Fee
    # =============================
    def fetch_doctor_fee_by_appointment(self, appointment_id: str) -> int:
        self.cursor.execute(self.QUERY_DOCTOR_FEE_BY_APPT, (appointment_id,))
        row = self.cursor.fetchone()
        return row[0] if row else 0

    # =============================
    # Display all bills
    # =============================
    def display_all_bills(self):
        self.cursor.execute(self.QUERY_DISPLAY_ALL)
        rows = self.cursor.fetchall()
        return [
            Billing(
                bill_id=row[0],
                appointment_id=row[1],
                doctor_fee=row[2],
                bill_date=row[3]
            )
            for row in rows
        ]

    # =============================
    # Insert bill
    # =============================
    def insert_bill(self, billing: Billing) -> bool:
        try:
            # Auto-generate Bill ID
            billing.bill_id = self.generate_bill_id()
            # Ensure total is computed (doctor_fee + additional_charges)
            if billing.total_bill is None:
                billing.calculate_total_bill()

            values = (billing.bill_id, billing.appointment_id, billing.total_bill)
            # Insert bill
            self.cursor.execute(self.QUERY_INSERT, values)
            # Update appointment status to ACTIVE after successful billing insert
            self.cursor.execute(self.QUERY_UPDATE_APPT_STATUS_ACTIVE, ("ACTIVE", billing.appointment_id))
            # Commit both operations together
            self.conn.commit()
            return True
        except Exception as e:
            print("Error inserting bill:", e)
            try:
                self.conn.rollback()
            except Exception:
                pass
            return False

    # =============================
    # Find bill by ID
    # =============================
    def find_by_bill_id(self, bill_id: str):
        self.cursor.execute(self.QUERY_FIND_BY_ID, (bill_id,))
        row = self.cursor.fetchone()
        if row:
            return Billing(
                bill_id=row[0],
                appointment_id=row[1],
                doctor_fee=row[2],
                bill_date=row[3]
            )
        return None

    # =============================
    # Update bill
    # =============================
    def update_bill(self, billing: Billing, bill_id: str) -> bool:
        try:
            values = (billing.appointment_id, billing.total_bill, bill_id)
            self.cursor.execute(self.QUERY_UPDATE, values)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print("Error updating bill:", e)
            return False

    # =============================
    # Delete bill
    # =============================
    def delete_bill(self, bill_id: str) -> bool:
        try:
            self.cursor.execute(self.QUERY_DELETE, (bill_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print("Error deleting bill:", e)
            return False

    def find_bills_by_date(self, search_date) -> List[Billing]:
        """Find bills by specific date"""
        try:
            self.cursor.execute(self.QUERY_FIND_BY_DATE, (search_date,))
            rows = self.cursor.fetchall()
            return [
                Billing(
                    bill_id=row[0],
                    appointment_id=row[1],
                    doctor_fee=row[2],
                    bill_date=row[3]
                )
                for row in rows
            ]
        except Exception as e:
            print("Error finding bills by date:", e)
            return []
