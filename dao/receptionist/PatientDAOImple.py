from dao.receptionist.AbstractPatientDAO import PatientDaoService
from db.db_connection import DBConnection
from models.receptionist.Patient import Patient
from typing import List
# from pymysql.cursors import DictCursor #Check this once

class PatientDaoImplementation(PatientDaoService):
    'Implementation for abstract class'
    #SQL queries
    DISPLAY_ALL = "SELECT * from patients WHERE isActive = 'Y'"
    INSERT_PATIENT = "INSERT INTO patients(first_name, last_name, DOB, phone_no," \
                    "email, address, height, weight" \
                    "gender, blood_group, marital_status, current_medication," \
                    "emergency_contact, is_active" \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
    FIND_BY_ID = "SELECT * FROM patients WHERE patient_id = %s"
    UPDATE_PATIENT  = "UPDATE patients set patient_name = %s, unitprice = %s WHERE patient_id = %s" #$$$$$$$$$$$$
    DISABLE_PATIENT = "UPDATE patients set isActive = %s WHERE patient_id = %s"
    # APPLY_GST = "CALL apply_gst_to_patient(%s, %s)"
    
    def __init__(self):
        self.conn = DBConnection().get_connection()

    def insert_patients(self, patient:Patient) -> bool:
        try:
            cursor = self.conn.cursor() #create a cursor object
            cursor.execute(self.INSERT_PATIENT,
                           (patient.first_name(),
                           patient.last_name(),
                           patient.DOB(),
                           patient.phone_no(),
                           patient.email(),
                           patient.address(),
                           patient.height(),
                           patient.weight(),
                           patient.gender(),
                           patient.blood_group(),
                           patient.marital_status(),
                           patient.current_medication(),
                           patient.emergency_contact(),
                           patient.is_active()))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting patient: ", e)
            return False
        finally:
            cursor.close()

    def display_all_patients(self) -> List[Patient]:
        patients = [] #to store the records from db
        try:
            cursor = self.conn.cursor() #(DictCursor) #returns data in dictionary format $$$$$$$$$$
            cursor.execute(self.DISPLAY_ALL) #fire the query
            rows = cursor.fetchall()
            for row in rows:
                patients.append(Patient(patient_id = row["patient_id"],
                                        first_name = row["first_name"],
                                        last_name = row["last_name"],
                                        DOB = row["DOB"],
                                        phone_no = row["phone_no"],
                                        email = row["email"],
                                        address = row["address"],
                                        height = row["height"],
                                        weight = row["weight"],
                                        gender = row["gender"],
                                        blood_group = row["blood_group"],
                                        marital_status = row["marital_status"],
                                        current_medication = row["current_medication"],
                                        last_name = row["emergency_contact"],
                                        is_active = row["isActive"]))
        except Exception as e:
            print("Error fetching patients: ", e)
        finally:
            cursor.close()
        return patients
    
    def find_by_patient_id(self, patient_id:int):
        patient = None
        try:
            cursor = self.conn.cursor() #(DictCursor) $$$$$$$$$$$$$
            cursor.execute(self.FIND_BY_ID, (patient_id,))
            row = cursor.fetchone()
            if row:
                patient = Patient(
                    patient_id = row["patient_id"],
                    first_name = row["first_name"],
                    last_name = row["last_name"],
                    DOB = row["DOB"],
                    phone_no = row["phone_no"],
                    email = row["email"],
                    address = row["address"],
                    height = row["height"],
                    weight = row["weight"],
                    gender = row["gender"],
                    blood_group = row["blood_group"],
                    marital_status = row["marital_status"],
                    current_medication = row["current_medication"],
                    last_name = row["emergency_contact"],
                    is_active = row["isActive"]
                    )
        except Exception as e:
            print("Error finding patient: ", e)
        finally:
            cursor.close()
        return patient

    def update_patient(self, patient:Patient, patient_id:int) ->bool:
        try:
            cursor = self.conn.cursor() #(DictCursor) $$$$$$$$$$$$$$$
            cursor.execute(self.UPDATE_PATIENT,
                           (patient.first_name(),
                           patient.last_name(),
                           patient.DOB(),
                           patient.phone_no(),
                           patient.email(),
                           patient.address(),
                           patient.height(),
                           patient.weight(),
                           patient.gender(),
                           patient.blood_group(),
                           patient.marital_status(),
                           patient.current_medication(),
                           patient.emergency_contact(),
                           patient.is_active()))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating patient: ", e)
            return False
        finally:
            cursor.close()

    def disable_patient(self, patient:Patient, patient_id:int) ->bool:
        try:
            cursor = self.conn.cursor() #(DictCursor) $$$$$$$$$$$$$$$
            cursor.execute(self.DISABLE_PATIENT,
                           (patient.is_active(),
                            patient_id))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating patient: ", e)
            return False
        finally:
            cursor.close()

    # def apply_gst(self, patient_id:int, gst_percent:float) ->bool:
    #     cursor = None
    #     try:
    #         cursor = self.conn.cursor()
    #         cursor.execute(self.APPLY_GST, (patient_id, gst_percent))
    #         self.conn.commit()
    #         return cursor.rowcount >=0 #since sp returns 0 if already applied
    #     except Exception as e:
    #         print("Error applying GST: ", e)
    #         return False
    #     finally:
    #         if cursor:
    #             cursor.close()
                