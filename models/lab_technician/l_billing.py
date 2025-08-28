from datetime import datetime,date

class LabBilling:
    def __init__(self, bill_id: int, lab_prescription_id: int, charge: float, billing_date: datetime):
        self.__bill_id = bill_id
        self.__lab_prescription_id = lab_prescription_id
        self.__charge = charge
        self.__billing_date = billing_date

    # Getters
    def get_bill_id(self): return self.__bill_id
    def get_lab_prescription_id(self): return self.__lab_prescription_id
    def get_charge(self): return self.__charge
    def get_billing_date(self): return self.__billing_date

    # Setters
    def set_bill_id(self, bill_id): self.__bill_id = bill_id
    def set_lab_prescription_id(self, lab_prescription_id): self.__lab_prescription_id = lab_prescription_id
    def set_charge(self, charge): self.__charge = charge
    def set_billing_date(self, billing_date): self.__billing_date = billing_date

    def __repr__(self):
        return f"LabBilling(ID={self.__bill_id}, Charge={self.__charge})"