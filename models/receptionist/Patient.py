from datetime import date
import re
class Patient:
    'patient fields'
    def __init__(self, patient_id = None, first_name = None, last_name = None, DOB = None,
                 phone_no = None, email = None, address = None, height = None, weight = None,
                 gender = None, blood_group = None, marital_status = None, current_medication = None,
                 emergency_contact = None, is_active = "Y"):
        self.__patient_id = patient_id
        self.__first_name = first_name
        self.__last_name = last_name 
        self.__DOB = DOB
        self.__phone_no = phone_no
        self.__email = email
        self.__address = address
        self.__height = height
        self.__weight = weight
        self.__gender = gender
        self.__blood_group = blood_group
        self.__marital_status = marital_status
        self.__current_medication = current_medication
        self.__emergency_contact = emergency_contact
        self.__is_active = is_active

#---------------------------
#GETTERS AND SETTERS
#---------------------------

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Patient ID
    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, patient_id):
        self.__patient_id = patient_id
        
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    #First Name
    @property
    def first_name(self):
        return self.__first_name
    
    @first_name.setter
    def set_first_name(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        self.__first_name = name


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Last Name
    @property
    def last_name(self):
        return self.__last_name
    
    @last_name.setter
    def set_last_name(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        self.__last_name = name
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #DOB
    @property
    def DOB(self):
        return self.__DOB

    @DOB.setter
    def DOB(self, DOB):
        if DOB and not isinstance(DOB, date):
            raise ValueError("DOB must be a date object")
        self.__DOB = DOB

        #Note: Validation must be done for 18<age<60
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Phone Number
    @property
    def phone_no(self):
        return self.__phone_no

    @phone_no.setter
    def phone_no(self, phone):
        if phone and (not phone.isdigit() or len(phone) < 10):
            raise ValueError("Phone must be numeric and at least 10 digits") # $$$$$Check this code again
        self.__phone = phone

        #Note: Validation must be done as phone numbers should begin with 9, 8 or 7
        # Also, the phone number must be exactly 10 digits, not atleast
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Email
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if email and "@" not in email:
            raise ValueError("Invalid email format")
        self.__email = email

        #Note: Proper email validation must be done (must end in .com/.in etc.,)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    #Address
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        if address and not isinstance(address, str):
            raise ValueError("Address must be text")
        self.__address = address

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Height
    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        if height is not None and (height < 0 or height > 120):
            raise ValueError("Height must be between 0 and 120")
        self.__height = height

        #Note: Proper height digit(2-3) validation must be done
        # Check if the >< symbols (height < 0 or height > 120) are in the right order
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Weight
    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        if weight is not None and (weight < 0 or weight > 120):
            raise ValueError("Weight must be between 0 and 120")
        self.__weight = weight

        #Note: Proper weight digit(1-3) validation must be done
        # Check if the >< symbols (weight < 0 or weight > 120) are in the right order
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Gender
    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender):
        if gender not in (None, "Male", "Female", "Other"):
            raise ValueError("Gender must be Male, Female or Other")
        self.__gender = gender

        #Suggestion: User should have a choice between M, F and O; The data should be stored as Male, Female or Other
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    #Blood Group
    @property
    def blood_group(self):
        return self._blood_group

    @blood_group.setter
    def blood_group(self, blood_group):
        valid_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        if blood_group and blood_group not in valid_groups:
            raise ValueError("Invalid blood group")
        self._blood_group = blood_group

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Marital Status
    @property
    def marital_status(self):
        return self.__marital_status

    @marital_status.setter
    def marital_status(self, status):
        if status not in (None, "Married", "Unmarried", "Other"):
            raise ValueError("Marital Status must be Married, Unmarried or Other")
        self.marital_status = status

        #Note: Check if "Other" is required
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    #Current Medication
    @property
    def current_medication(self):
        return self.__current_medication

    @current_medication.setter
    def current_medication(self, medication):
        if medication and not isinstance(medication, str):
            raise ValueError("Current Medication must be text")
        self.__current_medication = medication

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #Emergency Phone Number
    @property
    def emergency_contact(self):
        return self.__emergency_contact

    @emergency_contact.setter
    def emergency_contact(self, phone):
        if phone and (not phone.isdigit() or len(phone) < 10):
            raise ValueError("Phone must be numeric and at least 10 digits") # $$$$$Check this code again
        self.__emergency_contact = phone

        #Note: Validation must be done as phone numbers should begin with 9, 8 or 7
        # Also, the phone number must be exactly 10 digits, not atleast
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    #Is Active
    @property
    def is_active(self):
        return self.__is_active
    @is_active.setter
    def is_active(self, is_active):
        self.__is_active = is_active

    #override__str__
    def __str__(self):
        return f"""
        Patient ID: {self.__patient_id}
        First Name: {self.__first_name}
        Last Name: {self.__last_name}
        Date of Birth: {self.__DOB}
        Phone Number: {self.__phone_no}
        Email: {self.__email}
        Address: {self.__address}
        Height: {self.__height}
        Weight: {self.__weight}
        Gender: {self.__gender}
        Blood Group: {self.__blood_group}
        Marital Status: {self.__marital_status}
        Current Medication: {self.__current_medication}
        Emergency Contact: {self.__emergency_contact}
        IsActive: {self.__is_active}
        """