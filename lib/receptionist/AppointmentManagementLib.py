from dao.receptionist.AppointmentDAOImple import AppointmentDaoImplementation
from models.receptionist.Appointment import Appointment


class AppointmentManagementLib:
    """Library layer for managing appointments"""

    def __init__(self):
        self.appointment_dao = AppointmentDaoImplementation()

    def generate_appointment_id(self) -> str:
        """
        Generate a new appointment ID in format A00001.
        Adjust this logic if you already have a centralized ID generator.
        """
        appointments = self.appointment_dao.display_all_appointments()
        if not appointments:
            return "A00001"

        last_id = sorted(appointments, key=lambda x: x.appointment_id)[-1].appointment_id
        num = int(last_id[1:]) + 1
        return f"A{num:05d}"

    def create_appointment(self):
        """Create a new appointment with token generation"""
        try:
            patient_id = input("Enter Patient ID: ").strip()
            doctor_id = input("Enter Doctor ID: ").strip()
            reason = input("Enter Reason for Appointment: ").strip()

            appointment_id = self.generate_appointment_id()

            appointment = Appointment(
                appointment_id=appointment_id,
                patient_id=patient_id,
                doctor_id=doctor_id,
                reason=reason
            )

            if self.appointment_dao.insert_appointment(appointment):
                print("✅ Appointment created successfully.")
            else:
                print("❌ Failed to create appointment.")

        except Exception as e:
            print("Error creating appointment:", e)

    def display_all_appointments(self):
        """Display all appointments"""
        try:
            appointments = self.appointment_dao.display_all_appointments()
            if not appointments:
                print("No appointments found.")
                return

            print("\n--- All Appointments ---")
            for appt in appointments:
                print(f"ID: {appt.appointment_id}, Patient: {appt.patient_id}, "
                      f"Doctor: {appt.doctor_id}, Date: {appt.appointment_date}, "
                      f"Reason: {appt.reason}, Token: {appt.token_no}")
        except Exception as e:
            print("Error displaying appointments:", e)

    def find_appointment_by_id(self):
        """Find an appointment by its ID"""
        try:
            appt_id = input("Enter Appointment ID: ").strip()
            appointment = self.appointment_dao.find_by_appointment_id(appt_id)
            if appointment:
                print(f"\n--- Appointment Details ---")
                print(f"ID: {appointment.appointment_id}")
                print(f"Patient: {appointment.patient_id}")
                print(f"Doctor: {appointment.doctor_id}")
                print(f"Date: {appointment.appointment_date}")
                print(f"Reason: {appointment.reason}")
                print(f"Token: {appointment.token_no}")
            else:
                print("No appointment found with this ID.")
        except Exception as e:
            print("Error finding appointment:", e)
