from datetime import date
import re
class Staff:
    'Staff fields'
    def __init__(self, staff_id = None, name = None, DOB = None, email = None,
                 address = None, phone_no = None, DOJ = None, Gender = None, staff_role = None,
                 marital_status = None, pan_number = None, bank_details = None, previous_exp = None,
                 blood_group = None, qualification = None, salary = None, password = None, is_active = "Y"):
        self.__staff_id = staff_id
        self.__name = name 
        self.__DOB = DOB
        self.__email = email
        self.__joining_date = DOJ if DOJ else date.today()
        self.__is_active = is_active


#---------------------------
#GETTERS AND SETTERS
#---------------------------

    #productid
    def get_product_id(self):
        return self.__staff_id
    def set_product_id(self, productid):
        self.__product_id = productid

    def get_productname(self):
        return self.__product_name
    def set_product_name(self, product_name):
        'validate product name before setting'
        pattern = re.compile(r"^[A-Za-z_]{2,30}$")

        while True:
            if pattern.match(product_name):
                self.__product_name = product_name
                break
            else:
                print("\t\t Invalid product name, must have only aplphabets & min 3 characters!!!!....")
                product_name = input("\t\tEnter Product Name again: ")

    #unitprice
    def get_unitprice(self):
        return self.__unitprice
    def set_unitprice(self, unitprice):
        self.__unitprice = unitprice
    
    #categoryid
    def get_category_id(self):
        return self.__category_id
    def set_category_id(self, categoryid):
        self.__category_id = categoryid
    
    #manufacture date
    def get_manufacture_date(self):
        return self.__manufacture_date
    def set_manufacture_date(self, manufacturedate):
        if isinstance(manufacturedate, date):
            self.__manufacture_date = manufacturedate
        else:
            raise ValueError("manufacture date must be date object")
    
    #is active
    def get_is_active(self):
        return self.__is_active
    def set_is_active(self, is_active):
        self.__is_active = is_active

    #override__str__
    def __str__(self):
        return f"""
        productID: {self.__product_id:<10}
        ProductName:{self.__product_name:<10}
        Categoryid: {self.__category_id:<10}
        UnitPrice: {self.__unitprice:<10}
        Manufacture Date: {str(self.__manufacture_date):<10}
        IsActive: {self.__is_active:<10}
        """

hello = print("Hello world")