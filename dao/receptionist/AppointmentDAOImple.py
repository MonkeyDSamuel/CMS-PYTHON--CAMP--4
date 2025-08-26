from dao.receptionist.AbstractAppointmentDAO import AppointmentDaoService
from db.db_connection import DBConnection
from models.receptionist.Appointment import Appointment
from typing import List
# from pymysql.cursors import DictCursor

class AppointmentDaoImplementation(AppointmentDaoService):
    'Implementation for abstract class'
    #SQL queries
    DISPLAY_ALL = "SELECT * from appointments WHERE isActive = 'Y'"
    INSERT_APPOINTMENT = "INSERT INTO appointments(patient_id, doctor_id, appointment_date, token_no, reason) VALUES (%s, %s, %s, %s, %s)" 
    FIND_BY_ID = "SELECT * FROM appointments WHERE appointment_id = %s"
    UPDATE_APPOINTMENT  = "UPDATE appointments set appointmentname = %s, unitprice = %s WHERE appointment_id = %s" #$$$$$$$$$$$$
    DISABLE_APPOINTMENT = "UPDATE appointments set isActive = %s WHERE appointment_id = %s"
    # APPLY_GST = "CALL apply_gst_to_appointment(%s, %s)"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def insert_appointments(self, appointment:Appointment) -> bool:
        try:
            cursor = self.conn.cursor() #create a cursor object
            cursor.execute(self.INSERT_APPOINTMENT,
                           (appointment.patient_id(),
                           appointment.doctor_id(),
                           appointment.appointment_date(),
                           appointment.token_no(),
                           appointment.reason()))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting appointment: ", e)
            return False
        finally:
            cursor.close()

    def display_all_appointments(self) -> List[Appointment]:
        appointments = [] #to store the records from db
        try:
            cursor = self.conn.cursor() #(DictCursor) #returns data in dictionary format $$$$$$$$$
            cursor.execute(self.DISPLAY_ALL) #fire the query
            rows = cursor.fetchall()
            for row in rows:
                appointments.append(Appointment(
                            appointment_id = row["appointment_id"],
                            patient_id = row["patient_id"],
                            doctor_id = row["doctor_id"],
                            appointment_date = row["appointment_date"],
                            token_no = row["token_no"],
                            reason = row["reason"]
                            ))
        except Exception as e:
            print("Error fetching appointments: ", e)
        finally:
            cursor.close()
        return appointments
        
    def find_by_appointment_id(self, appointment_id:int):
        appointment = None
        try:
            cursor = self.conn.cursor() #(DictCursor) $$$$$$$$$$$$$
            cursor.execute(self.FIND_BY_ID, (appointment_id,))
            row = cursor.fetchone()
            if row:
                appointment = Appointment(
                            appointment_id = row["appointment_id"],
                            patient_id = row["patient_id"],
                            doctor_id = row["doctor_id"],
                            appointment_date = row["appointment_date"],
                            token_no = row["token_no"],
                            reason = row["reason"]
                            )
        except Exception as e:
            print("Error finding appointment: ", e)
        finally:
            cursor.close()
        return appointment

    def update_appointment(self, appointment:Appointment, appointment_id:int) ->bool:
        try:
            cursor = self.conn.cursor() #(DictCursor) $$$$$$$$$$
            cursor.execute(self.UPDATE_APPOINTMENT,
                           (appointment.patient_id(),
                           appointment.doctor_id(),
                           appointment.appointment_date(),
                           appointment.token_no(),
                           appointment.reason()))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating appointment: ", e)
            return False
        finally:
            cursor.close()

    # def disable_appointment(self, appointment:Appointment, appointment_id:int) ->bool:
    #     try:
    #         cursor = self.conn.cursor() #(DictCursor) $$$$$$$$$$$$$$$$$$$$
    #         cursor.execute(self.DISABLE_APPOINTMENT,
    #                        (appointment.get_is_active(),
    #                         appointment_id))
    #         self.conn.commit()
    #         return cursor.rowcount == 1
    #     except Exception as e:
    #         print("Error updating appointment: ", e)
    #         return False
    #     finally:
    #         cursor.close()

    # def apply_gst(self, appointment_id:int, gst_percent:float) ->bool:
    #     cursor = None
    #     try:
    #         cursor = self.conn.cursor()
    #         cursor.execute(self.APPLY_GST, (appointment_id, gst_percent))
    #         self.conn.commit()
    #         return cursor.rowcount >=0 #since sp returns 0 if already applied
    #     except Exception as e:
    #         print("Error applying GST: ", e)
    #         return False
    #     finally:
    #         if cursor:
    #             cursor.close()
                