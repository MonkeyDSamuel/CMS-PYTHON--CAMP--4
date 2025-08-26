from dao.receptionist.AbstractAppointmentDAO import AppointmentDaoService
from db.db_connection import DBConnection
from models.receptionist.Appointment import Appointment
from typing import List, Optional
from pymysql.cursors import DictCursor


class AppointmentDaoImplementation(AppointmentDaoService):
    """Implementation for Appointment DAO"""

    DISPLAY_ALL = "SELECT * FROM appointment"
    FIND_BY_APPOINTMENT_ID = "SELECT * FROM appointment WHERE Appointment_id = %s"
    FIND_BY_PATIENT_ID = "SELECT * FROM appointment WHERE Patient_id = %s"
    FIND_BY_DOCTOR_ID = "SELECT * FROM appointment WHERE Doctor_id = %s"
    INSERT_APPOINTMENT = (
        "INSERT INTO appointment (Appointment_id, Patient_id, Doctor_id, Appointment_date, reason, token_no) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    UPDATE_APPOINTMENT = (
        "UPDATE appointment SET Patient_id = %s, Doctor_id = %s, Appointment_date = %s, reason = %s, token_no = %s "
        "WHERE Appointment_id = %s"
    )
    DELETE_APPOINTMENT = "DELETE FROM appointment WHERE Appointment_id = %s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def display_all_appointments(self) -> List[Appointment]:
        appointments = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                appointments.append(Appointment(
                    appointment_id=row["Appointment_id"],
                    patient_id=row["Patient_id"],
                    doctor_id=row["Doctor_id"],
                    appointment_date=row["Appointment_date"],
                    reason=row["reason"],
                    token_no=row["token_no"]
                ))
        except Exception as e:
            print("Error fetching appointments:", e)
        finally:
            cursor.close()
        return appointments

    def find_by_appointment_id(self, appointment_id: str) -> Optional[Appointment]:
        appointment = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_APPOINTMENT_ID, (appointment_id,))
            row = cursor.fetchone()
            if row:
                appointment = Appointment(
                    appointment_id=row["Appointment_id"],
                    patient_id=row["Patient_id"],
                    doctor_id=row["Doctor_id"],
                    appointment_date=row["Appointment_date"],
                    reason=row["reason"],
                    token_no=row["token_no"]
                )
        except Exception as e:
            print("Error finding appointment by ID:", e)
        finally:
            cursor.close()
        return appointment

    def find_by_patient_id(self, patient_id: str) -> List[Appointment]:
        appointments = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_PATIENT_ID, (patient_id,))
            rows = cursor.fetchall()
            for row in rows:
                appointments.append(Appointment(
                    appointment_id=row["Appointment_id"],
                    patient_id=row["Patient_id"],
                    doctor_id=row["Doctor_id"],
                    appointment_date=row["Appointment_date"],
                    reason=row["reason"],
                    token_no=row["token_no"]
                ))
        except Exception as e:
            print("Error finding appointments by patient ID:", e)
        finally:
            cursor.close()
        return appointments

    def find_by_doctor_id(self, doctor_id: str) -> List[Appointment]:
        appointments = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_DOCTOR_ID, (doctor_id,))
            rows = cursor.fetchall()
            for row in rows:
                appointments.append(Appointment(
                    appointment_id=row["Appointment_id"],
                    patient_id=row["Patient_id"],
                    doctor_id=row["Doctor_id"],
                    appointment_date=row["Appointment_date"],
                    reason=row["reason"],
                    token_no=row["token_no"]
                ))
        except Exception as e:
            print("Error finding appointments by doctor ID:", e)
        finally:
            cursor.close()
        return appointments

    def insert_appointment(self, appointment: Appointment) -> bool:
        try:
            cursor = self.conn.cursor()
            values = (
                appointment.appointment_id,
                appointment.patient_id,
                appointment.doctor_id,
                appointment.appointment_date,
                appointment.reason,
                appointment.token_no,
            )
            cursor.execute(self.INSERT_APPOINTMENT, values)
            self.conn.commit()
            return True
        except Exception as e:
            print("Error inserting appointment:", e)
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def update_appointment(self, appointment: Appointment, appointment_id: str) -> bool:
        try:
            cursor = self.conn.cursor()
            values = (
                appointment.patient_id,
                appointment.doctor_id,
                appointment.appointment_date,
                appointment.reason,
                appointment.token_no,
                appointment_id,
            )
            cursor.execute(self.UPDATE_APPOINTMENT, values)
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error updating appointment:", e)
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def cancel_appointment(self, appointment_id: str) -> bool:
        # If a status column exists, consider updating it instead of deleting.
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.DELETE_APPOINTMENT, (appointment_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error cancelling appointment:", e)
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass
