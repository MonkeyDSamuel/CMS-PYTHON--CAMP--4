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
	FIND_BY_DATE = "SELECT * FROM appointment WHERE DATE(Appointment_date) = %s"
	FIND_PENDING_BY_DATE = "SELECT * FROM appointment WHERE DATE(Appointment_date) = %s AND app_status = 'PENDING'"
	CANCEL_APPOINTMENT_STATUS = "UPDATE appointment SET app_status = %s WHERE Appointment_id = %s"
	DELETE_TOKEN_FOR_APPT = (
		"DELETE t FROM app_token t "
		"JOIN appointment a ON a.Doctor_id = t.doc_id "
		"AND a.token_no = t.token "
		"AND DATE(a.Appointment_date) = t.token_date "
		"WHERE a.Appointment_id = %s"
	)
	GET_APPT_DOCTOR_AND_STATUS = "SELECT Doctor_id, app_status FROM appointment WHERE Appointment_id = %s"
	UPDATE_APPT_DATE_CLEAR_TOKEN = "UPDATE appointment SET Appointment_date = %s, token_no = NULL WHERE Appointment_id = %s"
	UPDATE_APPT_TOKEN = "UPDATE appointment SET token_no = %s WHERE Appointment_id = %s"

	# New helper queries
	QUERY_PATIENT_EXISTS = "SELECT 1 FROM patient WHERE patient_id = %s AND is_active = 1"
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
					token_no=row["token_no"],
					app_status=row.get("app_status") or row.get("App_status") or row.get("APP_STATUS")
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
					token_no=row["token_no"],
					app_status=row.get("app_status") or row.get("App_status") or row.get("APP_STATUS")
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
					token_no=row["token_no"],
					app_status=row.get("app_status") or row.get("App_status") or row.get("APP_STATUS")
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
					token_no=row["token_no"],
					app_status=row.get("app_status") or row.get("App_status") or row.get("APP_STATUS")
				))
		except Exception as e:
			print("Error finding appointments by doctor ID:", e)
		finally:
			cursor.close()
		return appointments

	def find_appointments_by_date(self, date: str) -> List[Appointment]:
		appointments = []
		try:
			cursor = self.conn.cursor(DictCursor)
			cursor.execute(self.FIND_BY_DATE, (date,))
			rows = cursor.fetchall()
			for row in rows:
				appointments.append(Appointment(
					appointment_id=row["Appointment_id"],
					patient_id=row["Patient_id"],
					doctor_id=row["Doctor_id"],
					appointment_date=row["Appointment_date"],
					reason=row["Reason"],
					token_no=row["token_no"],
					app_status=row.get("app_status") or row.get("App_status") or row.get("APP_STATUS")
				))
		except Exception as e:
			print("Error finding appointments by date:", e)
		finally:
			cursor.close()
		return appointments

	def find_pending_appointments_by_date(self, date: str) -> List[Appointment]:
		appointments = []
		try:
			cursor = self.conn.cursor(DictCursor)
			cursor.execute(self.FIND_PENDING_BY_DATE, (date,))
			rows = cursor.fetchall()
			for row in rows:
				appointments.append(Appointment(
					appointment_id=row["Appointment_id"],
					patient_id=row["Patient_id"],
					doctor_id=row["Doctor_id"],
					appointment_date=row["Appointment_date"],
					reason=row["Reason"],
					token_no=row["token_no"],
					app_status=row.get("app_status") or row.get("App_status") or row.get("APP_STATUS")
				))
		except Exception as e:
			print("Error finding pending appointments by date:", e)
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
		# New behavior: set status to CANCELLED and free the reserved token
		try:
			cursor = self.conn.cursor()
			# Update status
			cursor.execute(self.CANCEL_APPOINTMENT_STATUS, ("CANCELLED", appointment_id))
			# Free token
			cursor.execute(self.DELETE_TOKEN_FOR_APPT, (appointment_id,))
			self.conn.commit()
			return True
		except Exception as e:
			print("Error cancelling appointment:", e)
			try:
				self.conn.rollback()
			except Exception:
				pass
			return False
		finally:
			try:
				cursor.close()
			except Exception:
				pass

	def update_appointment_date(self, appointment_id: str, new_date) -> bool:
		"""Update appointment date, free old token, and assign new token if ACTIVE."""
		try:
			cursor = self.conn.cursor()
			# Get doctor and current status
			cursor.execute(self.GET_APPT_DOCTOR_AND_STATUS, (appointment_id,))
			row = cursor.fetchone()
			if not row:
				return False
			doctor_id, status = row[0], row[1]
			# Free old token tied to this appointment
			cursor.execute(self.DELETE_TOKEN_FOR_APPT, (appointment_id,))
			# Update date and clear token
			cursor.execute(self.UPDATE_APPT_DATE_CLEAR_TOKEN, (new_date, appointment_id))
			# If active, assign a new token for the new date
			if status == 'ACTIVE':
				# Compute next token and ensure within limit
				cursor2 = self.conn.cursor()
				try:
					cursor2.execute(self.QUERY_MAX_TOKEN_FOR_DAY, (doctor_id, new_date))
					row2 = cursor2.fetchone()
					current_max = int(row2[0]) if row2 and row2[0] is not None else 0
					next_token = current_max + 1
					if next_token > 25:
						raise Exception('Token limit reached for selected date')
					# Insert token reservation
					cursor2.execute(self.QUERY_LAST_TOKEN_ID)
					last = cursor2.fetchone()
					next_id = 1 if not last or last[0] is None else int(last[0]) + 1
					cursor.execute(self.INSERT_TOKEN, (next_id, doctor_id, next_token, new_date))
					# Update appointment with new token
					cursor.execute(self.UPDATE_APPT_TOKEN, (next_token, appointment_id))
				finally:
					try:
						cursor2.close()
					except Exception:
						pass
			self.conn.commit()
			return True
		except Exception as e:
			print("Error updating appointment date:", e)
			try:
				self.conn.rollback()
			except Exception:
				pass
			return False
		finally:
			try:
				cursor.close()
			except Exception:
				pass
