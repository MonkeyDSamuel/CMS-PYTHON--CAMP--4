from dao.receptionist.AppointmentDAOImple import AppointmentDaoImplementation
from models.receptionist.Appointment import Appointment


class AppointmentManagementLib:
    """Library layer for managing appointments"""

    def __init__(self):
        self.appointment_dao = AppointmentDaoImplementation()

    def generate_appointment_id(self) -> str:
        """
        Generate a new appointment ID in format A0000001.
        """
        appointments = self.appointment_dao.display_all_appointments()
        if not appointments:
            return "A0000001"

        def extract_num(appt_id: str) -> int:
            try:
                if appt_id and appt_id.startswith("A"):
                    return int(appt_id[1:])
                return 0
            except Exception:
                return 0

        max_num = 0
        for appt in appointments:
            max_num = max(max_num, extract_num(appt.appointment_id))
        return f"A{max_num + 1:07d}"

    def _read_patient_id(self) -> str:
        while True:
            patient_id = input("Enter Patient ID: ").strip()
            if not patient_id:
                print("❌ Patient ID is required.")
                continue
            if not self.appointment_dao.patient_exists(patient_id):
                print("❌ Patient doesn't exist")
                continue
            return patient_id

    def _read_doctor_id(self) -> str:
        while True:
            doctor_id = input("Enter Doctor ID: ").strip()
            if not doctor_id:
                print("❌ Doctor ID is required.")
                continue
            if not self.appointment_dao.doctor_exists(doctor_id):
                print("❌ Doctor doesn't exist")
                continue
            return doctor_id

    def _read_reason(self) -> str:
        while True:
            reason = input("Enter Reason for Appointment: ").strip()
            if not reason:
                print("❌ Reason is required.")
                continue
            return reason

    def _read_and_validate_date(self, doctor_id: str):
        from datetime import datetime, timedelta
        while True:
            date_input = input("Enter Appointment Date (dd/mm/yyyy) (press Enter to accept current date): ").strip()
            # Parse dd/mm/yyyy; accept blank as today
            today = datetime.today().date()
            if not date_input:
                appt_date = today
            else:
                try:
                    appt_date = datetime.strptime(date_input, "%d/%m/%Y").date()
                except ValueError:
                    print("❌ Invalid date format. Please use dd/mm/yyyy.")
                    continue

            max_date = today + timedelta(days=15)

            # Window validation
            if appt_date < today:
                print("❌ Incorrect date! Try again")
                continue
            if appt_date > max_date:
                print("❌ Can't be booked soo early")
                continue

            # Doctor availability by day name
            consult_days_str = self.appointment_dao.get_doctor_consultation_days(doctor_id)
            if not consult_days_str:
                print("❌ Doctor availability not configured. Try another doctor or contact admin.")
                continue
            # Normalize: 'Monday, Tuesday, Thursday' -> set of lower-case names
            allowed_days = {d.strip().lower() for d in consult_days_str.split(',') if d.strip()}
            day_name = appt_date.strftime('%A').lower()
            if day_name not in allowed_days:
                # Show friendly error
                shown_input = appt_date.strftime('%d/%m/%Y')
                print(f"❌ Doctor not available today/ on {shown_input}")
                print(f"Doctor is available on: {consult_days_str}")
                continue

            return appt_date

    def _get_or_request_token_for_date(self, doctor_id: str, desired_date):
        from datetime import datetime
        # Loop until token available for chosen date (or user picks another date)
        while True:
            # Check token availability (<=25 per day)
            count = self.appointment_dao.count_tokens_for_doctor_on_date(doctor_id, desired_date)
            if count >= 25:
                # unavailable -> ask another day, guided by doctor availability
                date_str = desired_date.strftime('%d/%m/%Y')
                print(f"❌ Token unavailable for {date_str}, please choose another day")
                consult_days_str = self.appointment_dao.get_doctor_consultation_days(doctor_id) or ""
                print(f"Doctor is available on: {consult_days_str}")
                desired_date = self._read_and_validate_date(doctor_id)
                continue

            # Compute next token
            next_token = self.appointment_dao.get_next_token_for_doctor_on_date(doctor_id, desired_date)
            if next_token < 1:
                next_token = 1
            if next_token > 25:
                # Recheck loop
                continue

            # Insert into app_token table
            token_id = self.appointment_dao.generate_next_app_token_id()
            if self.appointment_dao.insert_app_token(token_id, doctor_id, next_token, desired_date):
                return next_token, desired_date
            else:
                print("❌ Failed to reserve token, retrying...")
                # Rare DB race; loop to retry

    def create_appointment(self):
        """Create a new appointment with validations and token generation"""
        try:
            patient_id = self._read_patient_id()
            doctor_id = self._read_doctor_id()
            reason = self._read_reason()

            # Read date (dd/mm/yyyy) with validations and availability
            appointment_date = self._read_and_validate_date(doctor_id)

            # Ensure token reservation for the chosen date (or alternate date loop)
            token_no, final_date = self._get_or_request_token_for_date(doctor_id, appointment_date)

            appointment_id = self.generate_appointment_id()

            appointment = Appointment(
                appointment_id=appointment_id,
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=final_date,
                reason=reason,
                token_no=token_no
            )

            if self.appointment_dao.insert_appointment(appointment):
                print("✅ Appointment created successfully.")
                print(f"Appointment ID: {appointment_id}")
                print(f"Token Number: {token_no}")
                print(f"Date: {final_date.strftime('%d/%m/%Y')}")
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
                # appt.appointment_date might be a date or string from DB; handle nicely
                try:
                    date_str = appt.appointment_date.strftime('%d/%m/%Y')
                except Exception:
                    date_str = str(appt.appointment_date)
                print(f"ID: {appt.appointment_id}, Patient: {appt.patient_id}, "
                      f"Doctor: {appt.doctor_id}, Date: {date_str}, "
                      f"Reason: {appt.reason}, Token: {appt.token_no}, Status: {getattr(appt, 'app_status', None)}")
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
                try:
                    date_str = appointment.appointment_date.strftime('%d/%m/%Y')
                except Exception:
                    date_str = str(appointment.appointment_date)
                print(f"Date: {date_str}")
                print(f"Reason: {appointment.reason}")
                print(f"Token: {appointment.token_no}")
                print(f"Status: {getattr(appointment, 'app_status', None)}")
            else:
                print("No appointment found with this ID.")
        except Exception as e:
            print("Error finding appointment:", e)

    def search_appointments_by_date(self):
        """Search appointments by date (defaults to today if left empty)"""
        try:
            from datetime import datetime, date
            
            date_input = input("Enter Date to search (dd/mm/yyyy) (press Enter for today): ").strip()
            
            if not date_input:
                search_date = date.today()
                print(f"Searching for appointments on: {search_date.strftime('%d/%m/%Y')}")
            else:
                try:
                    search_date = datetime.strptime(date_input, "%d/%m/%Y").date()
                except ValueError:
                    print("❌ Invalid date format. Please use dd/mm/yyyy format.")
                    return
            
            appointments = self.appointment_dao.find_appointments_by_date(search_date)
            
            if not appointments:
                print(f"No appointments found for {search_date.strftime('%d/%m/%Y')}")
                return
            
            print(f"\n--- Appointments on {search_date.strftime('%d/%m/%Y')} ---")
            for appt in appointments:
                try:
                    date_str = appt.appointment_date.strftime('%d/%m/%Y')
                except Exception:
                    date_str = str(appt.appointment_date)
                print(f"ID: {appt.appointment_id}, Patient: {appt.patient_id}, "
                      f"Doctor: {appt.doctor_id}, Date: {date_str}, "
                      f"Reason: {appt.reason}, Token: {appt.token_no}, Status: {getattr(appt, 'app_status', None)}")
                      
        except Exception as e:
            print("Error searching appointments by date:", e)

    def view_appointments_by_doctor(self):
        """View all appointments for a specific doctor"""
        try:
            doctor_id = input("Enter Doctor ID: ").strip()
            if not doctor_id:
                print("❌ Doctor ID is required.")
                return

            appointments = self.appointment_dao.find_by_doctor_id(doctor_id)
            
            if not appointments:
                print(f"No appointments found for Doctor ID: {doctor_id}")
                return
            
            print(f"\n--- Appointments for Doctor ID: {doctor_id} ---")
            for appt in appointments:
                try:
                    date_str = appt.appointment_date.strftime('%d/%m/%Y')
                except Exception:
                    date_str = str(appt.appointment_date)
                print(f"ID: {appt.appointment_id}, Patient: {appt.patient_id}, "
                      f"Date: {date_str}, Reason: {appt.reason}, Token: {appt.token_no}, Status: {getattr(appt, 'app_status', None)}")
                      
        except Exception as e:
            print("Error viewing appointments by doctor:", e)

    def cancel_appointment(self):
        """Cancel an appointment, set status to CANCELLED and free its token."""
        try:
            appt_id = input("Enter Appointment ID to cancel: ").strip()
            if not appt_id:
                print("❌ Appointment ID is required.")
                return
            appt = self.appointment_dao.find_by_appointment_id(appt_id)
            if not appt:
                print("❌ Appointment not found.")
                return
            confirm = input(f"Are you sure you want to cancel appointment {appt_id}? (y/n): ")
            if confirm.lower() != 'y':
                return
            if self.appointment_dao.cancel_appointment(appt_id):
                print("✅ Appointment cancelled. Token freed.")
            else:
                print("❌ Failed to cancel appointment.")
        except Exception as e:
            print("Error cancelling appointment:", e)

    def update_appointment_date(self):
        """Update appointment date; free old token; if ACTIVE, auto-assign token for new date."""
        try:
            from datetime import datetime
            appt_id = input("Enter Appointment ID to update: ").strip()
            if not appt_id:
                print("❌ Appointment ID is required.")
                return
            appt = self.appointment_dao.find_by_appointment_id(appt_id)
            if not appt:
                print("❌ Appointment not found.")
                return
            new_date_input = input("Enter new date (dd/mm/yyyy): ").strip()
            try:
                new_date = datetime.strptime(new_date_input, "%d/%m/%Y").date()
            except ValueError:
                print("❌ Invalid date format. Use dd/mm/yyyy.")
                return
            confirm = input(f"Confirm changing {appt_id} to {new_date.strftime('%d/%m/%Y')}? (y/n): ")
            if confirm.lower() != 'y':
                return
            if self.appointment_dao.update_appointment_date(appt_id, new_date):
                print("✅ Appointment date updated. Token adjusted accordingly.")
            else:
                print("❌ Failed to update appointment date (token limit or error).")
        except Exception as e:
            print("Error updating appointment date:", e)

    def view_pending_appointments_by_date(self):
        """View appointments with app_status='PENDING' for a given date (default today)."""
        try:
            from datetime import datetime, date

            date_input = input("Enter Date to view pending (dd/mm/yyyy) (press Enter for today): ").strip()

            if not date_input:
                search_date = date.today()
                print(f"Searching for pending appointments on: {search_date.strftime('%d/%m/%Y')}")
            else:
                try:
                    search_date = datetime.strptime(date_input, "%d/%m/%Y").date()
                except ValueError:
                    print("❌ Invalid date format. Please use dd/mm/yyyy format.")
                    return

            appointments = self.appointment_dao.find_pending_appointments_by_date(search_date)

            if not appointments:
                print(f"No pending appointments found for {search_date.strftime('%d/%m/%Y')}")
                return

            print(f"\n--- Pending Appointments on {search_date.strftime('%d/%m/%Y')} ---")
            for appt in appointments:
                try:
                    date_str = appt.appointment_date.strftime('%d/%m/%Y')
                except Exception:
                    date_str = str(appt.appointment_date)
                print(f"ID: {appt.appointment_id}, Patient: {appt.patient_id}, "
                      f"Doctor: {appt.doctor_id}, Date: {date_str}, "
                      f"Reason: {appt.reason}, Token: {appt.token_no}, Status: {getattr(appt, 'app_status', None)}")
        except Exception as e:
            print("Error viewing pending appointments by date:", e)
