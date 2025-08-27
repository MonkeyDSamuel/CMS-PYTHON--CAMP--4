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

	# New helper queries
	QUERY_PATIENT_EXISTS = "SELECT 1 FROM patient WHERE patient_id = %s"
	QUERY_DOCTOR_EXISTS = "SELECT 1 FROM doctor WHERE doctor_id = %s"
	QUERY_DOCTOR_DAYS = "SELECT Consultation_days FROM doctor WHERE doctor_id = %s"
	QUERY_TOKEN_COUNT_FOR_DAY = (
		"SELECT COUNT(*) FROM app_token WHERE doc_id = %s AND token_date = %s"
	)
	QUERY_MAX_TOKEN_FOR_DAY = (
		"SELECT COALESCE(MAX(token), 0) FROM app_token WHERE doc_id = %s AND token_date = %s"
	)
	QUERY_LAST_TOKEN_ID = "SELECT id FROM app_token ORDER BY id DESC LIMIT 1"
	INSERT_TOKEN = "INSERT INTO app_token (id, doc_id, token, token_date) VALUES (%s, %s, %s, %s)"

	def __init__(self):
		self.conn = DBConnection().get_connection()

	# -------- Helper methods for validation and tokens --------
	def patient_exists(self, patient_id: str) -> bool:
		cursor = None
		try:
			cursor = self.conn.cursor()
			cursor.execute(self.QUERY_PATIENT_EXISTS, (patient_id,))
			return cursor.fetchone() is not None
		except Exception:
			return False
		finally:
			try:
				if cursor is not None:
					cursor.close()
			except Exception:
				pass

	def doctor_exists(self, doctor_id: str) -> bool:
		cursor = None
		try:
			cursor = self.conn.cursor()
			cursor.execute(self.QUERY_DOCTOR_EXISTS, (doctor_id,))
			return cursor.fetchone() is not None
		except Exception:
			return False
		finally:
			try:
				if cursor is not None:
					cursor.close()
			except Exception:
				pass

	def get_doctor_consultation_days(self, doctor_id: str) -> str:
		cursor = None
		try:
			cursor = self.conn.cursor()
			cursor.execute(self.QUERY_DOCTOR_DAYS, (doctor_id,))
			row = cursor.fetchone()
			return row[0] if row else None
		except Exception:
			return None
		finally:
			try:
				if cursor is not None:
					cursor.close()
			except Exception:
				pass

	def count_tokens_for_doctor_on_date(self, doctor_id: str, token_date) -> int:
		cursor = None
		try:
			cursor = self.conn.cursor()
			cursor.execute(self.QUERY_TOKEN_COUNT_FOR_DAY, (doctor_id, token_date))
			row = cursor.fetchone()
			return int(row[0]) if row else 0
		except Exception:
			return 0
		finally:
			try:
				if cursor is not None:
					cursor.close()
			except Exception:
				pass

	def get_next_token_for_doctor_on_date(self, doctor_id: str, token_date) -> int:
		cursor = None
		try:
			cursor = self.conn.cursor()
			cursor.execute(self.QUERY_MAX_TOKEN_FOR_DAY, (doctor_id, token_date))
			row = cursor.fetchone()
			current_max = int(row[0]) if row and row[0] is not None else 0
			return current_max + 1
		except Exception:
			return 1
		finally:
			try:
				if cursor is not None:
					cursor.close()
			except Exception:
				pass

	def generate_next_app_token_id(self) -> int:
		cursor = None
		try:
			cursor = self.conn.cursor()
			cursor.execute(self.QUERY_LAST_TOKEN_ID)
			row = cursor.fetchone()
			if not row or row[0] is None:
				return 1
			last_id = int(row[0])
			return last_id + 1
		except Exception:
			return 1
		finally:
			try:
				if cursor is not None:
					cursor.close()
			except Exception:
				pass

	def insert_app_token(self, token_id, doctor_id: str, token_no: int, token_date) -> bool:
		cursor = None
		try:
			cursor = self.conn.cursor()
			cursor.execute(self.INSERT_TOKEN, (token_id, doctor_id, token_no, token_date))
			self.conn.commit()
			return True
		except Exception as e:
			print("Error inserting token:", e)
			return False
		finally:
			try:
				if cursor is not None:
					cursor.close()
			except Exception:
				pass

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
					reason=row["Reason"],
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
					reason=row["Reason"],
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
					reason=row["Reason"],
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
					reason=row["Reason"],
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
