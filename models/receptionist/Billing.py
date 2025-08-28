from datetime import date

class Billing:
    """Billing entity representing a patient's bill record"""

    def __init__(self, bill_id=None, appointment_id=None, doctor_fee=None, additional_charges=0, bill_date=None):
        self.__bill_id = bill_id
        self.__appointment_id = appointment_id
        self.__doctor_fee = doctor_fee
        self.__additional_charges = additional_charges
        self.__total_bill = None  # will be auto-calculated
        self.__bill_date = bill_date if bill_date else date.today()

        # Calculate total bill when object is created
        self.calculate_total_bill()

    # =========================
    # Getters and Setters
    # =========================

    # Bill ID
    @property
    def bill_id(self):
        return self.__bill_id

    @bill_id.setter
    def bill_id(self, bill_id):
        if bill_id and not isinstance(bill_id, str):
            raise ValueError("Bill ID must be a string like 'B00001'")
        self.__bill_id = bill_id

    # Appointment ID
    @property
    def appointment_id(self):
        return self.__appointment_id

    @appointment_id.setter
    def appointment_id(self, appointment_id):
        if appointment_id and not isinstance(appointment_id, str):
            raise ValueError("Appointment ID must be a string like 'A00001'")
        self.__appointment_id = appointment_id

    # Doctor Fee
    @property
    def doctor_fee(self):
        return self.__doctor_fee

    @doctor_fee.setter
    def doctor_fee(self, doctor_fee):
        if doctor_fee and not isinstance(doctor_fee, int):
            raise ValueError("Doctor Fee must be an integer")
        self.__doctor_fee = doctor_fee
        self.calculate_total_bill()

    # Additional Charges
    @property
    def additional_charges(self):
        return self.__additional_charges

    @additional_charges.setter
    def additional_charges(self, additional_charges):
        if additional_charges and not isinstance(additional_charges, int):
            raise ValueError("Additional charges must be an integer")
        self.__additional_charges = additional_charges
        self.calculate_total_bill()

    # Total Bill
    @property
    def total_bill(self):
        return self.__total_bill

    def calculate_total_bill(self):
        """Automatically calculates the total bill based on doctor fee + additional charges"""
        self.__total_bill = (self.__doctor_fee if self.__doctor_fee else 0) + \
                            (self.__additional_charges if self.__additional_charges else 0)

    # Bill Date
    @property
    def bill_date(self):
        return self.__bill_date

    @bill_date.setter
    def bill_date(self, bill_date):
        if bill_date and not isinstance(bill_date, date):
            raise ValueError("Bill Date must be a date object")
        self.__bill_date = bill_date if bill_date else date.today()

    # =========================
    # String Representation
    # =========================
    def __str__(self):
        return (
            f"\nBill ID: {self.__bill_id}\n"
            f"Appointment ID: {self.__appointment_id}\n"
            f"Doctor Fee: {self.__doctor_fee}\n"
            f"Additional Charges: {self.__additional_charges}\n"
            f"Total Bill: {self.__total_bill}\n"
            f"Bill Date: {self.__bill_date}\n"
        )
