class Medicine:
    def __init__(self, medicine_id, category_id,medicine_name, common_name, strength, rate_per_unit):
        self.medicine_id = medicine_id
        self.category_id = category_id
        self.medicine_name = medicine_name
        self.common_name = common_name
        self.strength = strength
        self.rate_per_unit = rate_per_unit

    # Getter methods
    def get_medicine_id(self):
        return self.medicine_id

    def get_medicine_name(self):
        return self.medicine_name
    
    def get_category_id(self):
        return self.category_id

    def get_common_name(self):
        return self.common_name

    def get_strength(self):
        return self.strength

    def get_rate_per_unit(self):
        return self.rate_per_unit

    # Setter methods
    def set_medicine_name(self, medicine_name):
        self.medicine_name = medicine_name

    def set_common_name(self, common_name):
        self.common_name = common_name

    def set_category_id(self,category_id):
         self.category_id = category_id

    def set_strength(self, strength):
        self.strength = strength

    def set_rate_per_unit(self, rate_per_unit):
        self.rate_per_unit = rate_per_unit

    # Display object details
    def __str__(self):
        return (f"Medicine[ID={self.medicine_id},category={self.category_id} Name={self.medicine_name}, "
                f"Common={self.common_name}, Strength={self.strength}, "
                f"Rate={self.rate_per_unit}]")
