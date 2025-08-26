from datetime import date

class Appointment:
    """Appointment entity class"""

    def __init__(
        self,
        appointment_id: str = None,
        patient_id: str = None,
        doctor_id: str = None,
        appointment_date: date = None,
        reason: str = None,
        token_no: int = None
    ):
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__doctor_id = doctor_id
        self.__appointment_date = appointment_date
        self.__reason = reason
        self.__token_no = token_no

    # ---------------------------
    # Appointment ID
    # ---------------------------
    @property
    def appointment_id(self):
        return self.__appointment_id

    @appointment_id.setter
    def appointment_id(self, appointment_id: str):
        if appointment_id and not isinstance(appointment_id, str):
            raise ValueError("Appointment ID must be a string (e.g., A00001)")
        self.__appointment_id = appointment_id

    # ---------------------------
    # Patient ID
    # ---------------------------
    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, patient_id: str):
        if patient_id and not isinstance(patient_id, str):
            raise ValueError("Patient ID must be a string (e.g., P00001)")
        self.__patient_id = patient_id

    # ---------------------------
    # Doctor ID
    # ---------------------------
    @property
    def doctor_id(self):
        return self.__doctor_id

    @doctor_id.setter
    def doctor_id(self, doctor_id: str):
        if doctor_id and not isinstance(doctor_id, str):
            raise ValueError("Doctor ID must be a string (e.g., D00001)")
        self.__doctor_id = doctor_id

    # ---------------------------
    # Appointment Date
    # ---------------------------
    @property
    def appointment_date(self):
        return self.__appointment_date

    @appointment_date.setter
    def appointment_date(self, appointment_date: date):
        if appointment_date and not isinstance(appointment_date, date):
            raise ValueError("Appointment date must be a date object")
        self.__appointment_date = appointment_date

    # ---------------------------
    # Reason
    # ---------------------------
    @property
    def reason(self):
        return self.__reason

    @reason.setter
    def reason(self, reason: str):
        if reason and not isinstance(reason, str):
            raise ValueError("Reason must be a string")
        self.__reason = reason

    # ---------------------------
    # Token Number
    # ---------------------------
    @property
    def token_no(self):
        return self.__token_no

    @token_no.setter
    def token_no(self, token_no: int):
        if token_no is not None:
            if not isinstance(token_no, int):
                raise ValueError("Token number must be an integer")
            if token_no < 1 or token_no > 25:
                raise ValueError("Token number must be between 1 and 25")
        self.__token_no = token_no

    # ---------------------------
    # String representation
    # ---------------------------
    def __str__(self):
        return f"""
        Appointment ID   : {self.__appointment_id}
        Patient ID       : {self.__patient_id}
        Doctor ID        : {self.__doctor_id}
        Appointment Date : {self.__appointment_date}
        Reason           : {self.__reason}
        Token Number     : {self.__token_no}
        """
