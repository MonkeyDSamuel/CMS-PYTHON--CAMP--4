from dao.receptionist.AbstractPatientDAO import PatientDaoService
from db.db_connection import DBConnection
from models.receptionist.Patient import Patient
from typing import List, Optional
from pymysql.cursors import DictCursor

class PatientDaoImplementation(PatientDaoService):
    """Implementation for abstract class"""

    # SQL Queries
    DISPLAY_ALL = (
        "SELECT patient_id, first_name, last_name, dob AS DOB, phone_no, email_id, address, "
        "height, weight, gender, blood_group, marital_status, current_medications, emergency_contact, is_active "
        "FROM patient WHERE is_active = 1"
    )
    
    GET_LAST_ID = "SELECT patient_id FROM patient ORDER BY patient_id DESC LIMIT 1"
    
    INSERT_PATIENT = """
        INSERT INTO patient (
            patient_id, first_name, last_name, DOB, phone_no, email_id, address,
            height, weight, gender, blood_group, marital_status,
            current_medications, emergency_contact, is_active
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    FIND_BY_ID = (
        "SELECT patient_id, first_name, last_name, dob AS DOB, phone_no, email_id, address, "
        "height, weight, gender, blood_group, marital_status, current_medications, emergency_contact, is_active "
        "FROM patient WHERE patient_id = %s"
    )
    
    UPDATE_PATIENT = """
        UPDATE patient 
        SET first_name = %s, last_name = %s, DOB = %s, phone_no = %s,
            email_id = %s, address = %s, height = %s, weight = %s,
            gender = %s, blood_group = %s, marital_status = %s,
            current_medications = %s, emergency_contact = %s
        WHERE patient_id = %s
    """
    
    DISABLE_PATIENT = "UPDATE patient SET is_active = %s WHERE patient_id = %s"
    CANCEL_APPTS_BY_PATIENT = "UPDATE appointment SET app_status = %s WHERE Patient_id = %s"
    DELETE_TOKENS_FOR_PATIENT = (
        "DELETE t FROM app_token t "
        "JOIN appointment a ON a.Doctor_id = t.doc_id "
        "AND a.token_no = t.token "
        "AND DATE(a.Appointment_date) = t.token_date "
        "WHERE a.Patient_id = %s"
    )

    FIND_BY_NAME = (
        "SELECT patient_id, first_name, last_name, dob AS DOB, phone_no, email_id, address, "
        "height, weight, gender, blood_group, marital_status, current_medications, emergency_contact, is_active "
        "FROM patient "
        "WHERE is_active = 1 AND (LOWER(first_name) LIKE LOWER(%s) OR LOWER(last_name) LIKE LOWER(%s))"
    )

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def _to_gender_code(self, gender_value: str) -> str:
        """Normalize gender to single-letter code expected by DB (M/F/O)."""
        if not gender_value:
            return None
        upper_val = gender_value.upper()
        if upper_val in ("M", "F", "O"):
            return upper_val
        mapping = {"MALE": "M", "FEMALE": "F", "OTHER": "O"}
        return mapping.get(upper_val, upper_val)

    def _to_active_tinyint(self, active_value: str) -> int:
        """Map model's 'Y'/'N' to DB tinyint 1/0."""
        if active_value is None:
            return None
        return 1 if str(active_value).upper() == 'Y' else 0

    def _generate_patient_id(self) -> str:
        """Generate next patient_id in format P0000001, P0000002..."""
        cursor = self.conn.cursor()
        cursor.execute(self.GET_LAST_ID)
        last_id_row = cursor.fetchone()
        cursor.close()

        if last_id_row and last_id_row[0]:
            last_id = last_id_row[0]   # e.g., "P0000005"
            last_num = int(last_id[1:])  # remove 'P' and convert to int
            new_num = last_num + 1
        else:
            new_num = 1  # first patient

        return f"P{new_num:07d}"  # always 7 digits (P0000001)

    def insert_patient(self, patient: Patient) -> bool:
        cursor = None
        try:
            new_patient_id = self._generate_patient_id()
            cursor = self.conn.cursor()
            cursor.execute(self.INSERT_PATIENT, (
                new_patient_id,
                patient.first_name,
                patient.last_name,
                patient.DOB,
                patient.phone_no,
                patient.email,
                patient.address,
                patient.height,
                patient.weight,
                self._to_gender_code(patient.gender),
                patient.blood_group,
                patient.marital_status,
                patient.current_medications,
                patient.emergency_contact,
                self._to_active_tinyint(patient.is_active)
            ))
            self.conn.commit()
            
            # Update the patient object with the generated ID
            patient.patient_id = new_patient_id
            
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting patient: ", e)
            return False
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass

    def display_all_patients(self) -> List[Patient]:
        patients = []
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                patients.append(Patient(
                    patient_id=row["patient_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    DOB=row["DOB"],
                    phone_no=row["phone_no"],
                    email=row["email_id"],
                    address=row["address"],
                    height=row["height"],
                    weight=row["weight"],
                    gender=row["gender"],
                    blood_group=row["blood_group"],
                    marital_status=row["marital_status"],
                    current_medications=row["current_medications"],
                    emergency_contact=row["emergency_contact"],
                    is_active=('Y' if row["is_active"] == 1 else 'N')
                ))
        except Exception as e:
            print("Error fetching patients: ", e)
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
        return patients

    def find_by_patient_id(self, patient_id: str) -> Optional[Patient]:
        patient = None
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_ID, (patient_id,))
            row = cursor.fetchone()
            if row:
                patient = Patient(
                    patient_id=row["patient_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    DOB=row["DOB"],
                    phone_no=row["phone_no"],
                    email=row["email_id"],
                    address=row["address"],
                    height=row["height"],
                    weight=row["weight"],
                    gender=row["gender"],
                    blood_group=row["blood_group"],
                    marital_status=row["marital_status"],
                    current_medications=row["current_medications"],
                    emergency_contact=row["emergency_contact"],
                    is_active=('Y' if row["is_active"] == 1 else 'N')
                )
        except Exception as e:
            print("Error finding patient: ", e)
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
        return patient

    def update_patient(self, patient: Patient, patient_id: str) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.UPDATE_PATIENT, (
                patient.first_name,
                patient.last_name,
                patient.DOB,
                patient.phone_no,
                patient.email,
                patient.address,
                patient.height,
                patient.weight,
                self._to_gender_code(patient.gender),
                patient.blood_group,
                patient.marital_status,
                patient.current_medications,
                patient.emergency_contact,
                patient_id
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating patient: ", e)
            return False
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass

    def disable_patient(self, patient: Patient, patient_id: str) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            # Begin transactional update: deactivate patient, cancel appointments, free tokens
            cursor.execute(self.DISABLE_PATIENT, (
                self._to_active_tinyint(patient.is_active),
                patient_id
            ))
            # Only proceed to cancel if deactivation intended (N -> 0)
            if self._to_active_tinyint(patient.is_active) == 0:
                # Set all appointments for this patient to CANCELLED
                cursor.execute(self.CANCEL_APPTS_BY_PATIENT, ("CANCELLED", patient_id))
                # Free tokens reserved by those appointments
                cursor.execute(self.DELETE_TOKENS_FOR_PATIENT, (patient_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error disabling patient:", e)
            try:
                self.conn.rollback()
            except Exception:
                pass
            return False

    def find_by_name(self, name: str) -> List[Patient]:
        patients = []
        cursor = None
        try:
            like_param = f"%{name.strip()}%"
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_NAME, (like_param, like_param))
            rows = cursor.fetchall()
            for row in rows:
                patients.append(Patient(
                    patient_id=row["patient_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    DOB=row["DOB"],
                    phone_no=row["phone_no"],
                    email=row["email_id"],
                    address=row["address"],
                    height=row["height"],
                    weight=row["weight"],
                    gender=row["gender"],
                    blood_group=row["blood_group"],
                    marital_status=row["marital_status"],
                    current_medications=row["current_medications"],
                    emergency_contact=row["emergency_contact"],
                    is_active=('Y' if row["is_active"] == 1 else 'N')
                ))
        except Exception as e:
            print("Error searching patients by name:", e)
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
        return patients
