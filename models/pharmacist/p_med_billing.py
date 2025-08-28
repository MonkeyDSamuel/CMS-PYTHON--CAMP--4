

class MedicineBilling:
    """Model class for Medicine Billing in Clinic Management System"""

    def init(self, bill_id=None, patient_id=None, medicine_id=None,
                 quantity=0, rate_per_unit=0.0, bill_date=None):
        self.__bill_id = bill_id
        self.__patient_id = patient_id
        self.__medicine_id = medicine_id
        self.__quantity = quantity
        self.__rate_per_unit = rate_per_unit
        self.__bill_date = bill_date
        self.total_amount = self.calculate_total()

    # -------------------- Private Helper --------------------
    def __calculate_total(self):
        return self.quantity * self.rate_per_unit

    # -------------------- Getters --------------------
    def get_bill_id(self):
        return self.__bill_id

    def get_patient_id(self):
        return self.__patient_id

    def get_medicine_id(self):
        return self.__medicine_id

    def get_quantity(self):
        return self.__quantity

    def get_rate_per_unit(self):
        return self.__rate_per_unit

    def get_total_amount(self):
        return self.__total_amount

    def get_bill_date(self):
        return self.__bill_date

    # -------------------- Setters --------------------
    def set_bill_id(self, bill_id):
        self.__bill_id = bill_id

    def set_patient_id(self, patient_id):
        self.__patient_id = patient_id

    def set_medicine_id(self, medicine_id):
        self.__medicine_id = medicine_id

    def set_quantity(self, quantity):
        self.__quantity = quantity
        self.total_amount = self.calculate_total()

    def set_rate_per_unit(self, rate_per_unit):
        self.__rate_per_unit = rate_per_unit
        self.total_amount = self.calculate_total()

    def set_bill_date(self, bill_date):
        self.__bill_date = bill_date

    # -------------------- Utility --------------------
    def str(self):
        return (f"BillID: {self.bill_id}, PatientID: {self.patient_id}, "
                f"MedicineID: {self.medicine_id}, Quantity: {self.quantity}, "
                f"Rate: {self.rate_per_unit}, Total: {self.total_amount}, "
                f"Date: {self.__bill_date}")