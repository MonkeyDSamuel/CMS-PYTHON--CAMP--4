class LabTestResult:
    def __init__(self, result_id: int, lab_test_id: int, lab_prescription_id: int, status: str, date: datetime):
        self.__result_id = result_id
        self.__lab_test_id = lab_test_id
        self.__lab_prescription_id = lab_prescription_id
        self.__status = status
        self.__date = date

    # Getters
    def get_result_id(self): return self.__result_id
    def get_lab_test_id(self): return self.__lab_test_id
    def get_lab_prescription_id(self): return self.__lab_prescription_id
    def get_status(self): return self.__status
    def get_date(self): return self.__date

    # Setters
    def set_result_id(self, result_id): self.__result_id = result_id
    def set_lab_test_id(self, lab_test_id): self.__lab_test_id = lab_test_id
    def set_lab_prescription_id(self, lab_prescription_id): self.__lab_prescription_id = lab_prescription_id
    def set_status(self, status): self.__status = status
    def set_date(self, date): self.__date = date

    def __repr__(self):
        return f"LabTestResult(ID={self.__result_id}, Status='{self.__status}')"