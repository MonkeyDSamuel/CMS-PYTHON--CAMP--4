class LabTest:
    def __init__(self, lab_test_id: int, lab_test_name: str, category_id: int,
                 rate: float, created_on: datetime, min_value: float, max_value: float, is_active: bool = True):
        self.__lab_test_id = lab_test_id
        self.__lab_test_name = lab_test_name
        self.__category_id = category_id
        self.__rate = rate
        self.__created_on = created_on
        self.__min_value = min_value
        self.__max_value = max_value
        self.__is_active = is_active

    # Getters
    def get_lab_test_id(self): return self.__lab_test_id
    def get_lab_test_name(self): return self.__lab_test_name
    def get_category_id(self): return self.__category_id
    def get_rate(self): return self.__rate
    def get_created_on(self): return self.__created_on
    def get_min_value(self): return self.__min_value
    def get_max_value(self): return self.__max_value
    def get_is_active(self): return self.__is_active

    # Setters
    def set_lab_test_id(self, lab_test_id): self.__lab_test_id = lab_test_id
    def set_lab_test_name(self, name): self.__lab_test_name = name
    def set_category_id(self, category_id): self.__category_id = category_id
    def set_rate(self, rate): self.__rate = rate
    def set_created_on(self, created_on): self.__created_on = created_on
    def set_min_value(self, min_value): self.__min_value = min_value
    def set_max_value(self, max_value): self.__max_value = max_value
    def set_is_active(self, status: bool): self.__is_active = status

    def __repr__(self):
        return f"LabTest(ID={self.__lab_test_id}, Name='{self.__lab_test_name}', Active={self.__is_active})"

