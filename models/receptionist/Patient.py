from datetime import date
import re


class Patient:
    """Patient entity with validation and auto-generated ID"""

    __id_counter = 0  # Class-level counter for auto ID generation

    def __init__(self, patient_id=None, first_name=None, last_name=None, DOB=None,
                 phone_no=None, email=None, address=None, height=None, weight=None,
                 gender=None, blood_group=None, marital_status=None, current_medications=None,
                 emergency_contact=None, is_active="Y"):

        # Auto-generate patient_id if not provided
        if patient_id is None:
            Patient.__id_counter += 1
            self.__patient_id = f"P{Patient.__id_counter:07d}"  # P0000001 format
        else:
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
        self.__current_medications = current_medications
        self.__emergency_contact = emergency_contact
        self.__is_active = is_active

    # ---------------------------
    # Getters & Setters
    # ---------------------------

    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        if not value.startswith("P") or not value[1:].isdigit():
            raise ValueError("Patient ID must be in format P0000001")
        self.__patient_id = value

    # First Name
    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("First name must be a non-empty string")
        self.__first_name = value.strip().title()

    # Last Name
    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Last name must be a non-empty string")
        self.__last_name = value.strip().title()

    # DOB
    @property
    def DOB(self):
        return self.__DOB

    @DOB.setter
    def DOB(self, value: date):
        if value and not isinstance(value, date):
            raise ValueError("DOB must be a datetime.date object")
        self.__DOB = value

    # Phone Number
    @property
    def phone_no(self):
        return self.__phone_no

    @phone_no.setter
    def phone_no(self, value: str):
        if value:
            if not (value.isdigit() and len(value) == 10 and value[0] in "987"):
                raise ValueError("Phone number must be 10 digits starting with 9, 8, or 7")
        self.__phone_no = value

    # Blood Group
    @property
    def blood_group(self):
        return self.__blood_group

    @blood_group.setter
    def blood_group(self, value: str):
        if value is None:
            self.__blood_group = None
            return
        # Accept lowercase input and convert to uppercase
        normalized = value.strip().upper()
        valid_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        if normalized in valid_groups:
            self.__blood_group = normalized
        else:
            raise ValueError("Invalid blood group. Must be one of: A+, A-, B+, B-, O+, O-, AB+, AB-")

    # Email
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value: str):
        if value is None:
            self.__email = None
            return
        if not isinstance(value, str):
            raise ValueError("Email must be a string")
        
        # Check for @ symbol
        if '@' not in value:
            raise ValueError("Email must contain '@' symbol")
        
        # Check for dot after @
        parts = value.split('@')
        if len(parts) != 2:
            raise ValueError("Invalid email format")
        
        domain_part = parts[1]
        if '.' not in domain_part:
            raise ValueError("Email domain must contain a dot (.)")
        
        # Check for 2-3 letters after the last dot
        domain_parts = domain_part.split('.')
        if len(domain_parts) < 2:
            raise ValueError("Invalid domain format")
        
        tld = domain_parts[-1]
        if not (2 <= len(tld) <= 3):
            raise ValueError("Domain extension must be 2-3 letters (e.g., com, in, org)")
        
        self.__email = value.strip()

    # Address
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value: str):
        if value and not isinstance(value, str):
            raise ValueError("Address must be text")
        self.__address = value

    # Height (cm)
    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value: int):
        if value is not None and not (50 <= value <= 250):
            raise ValueError("Height must be between 50 and 250 cm")
        self.__height = value

    # Weight (kg)
    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value: int):
        if value is not None and not (2 <= value <= 300):
            raise ValueError("Weight must be between 2 and 300 kg")
        self.__weight = value

    # Gender
    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value: str):
        if value is None:
            self.__gender = None
            return
        # Normalize input: accept 'M'/'F'/'O' and full words (case-insensitive)
        normalized = value.strip()
        if not normalized:
            self.__gender = None
            return
        upper_val = normalized.upper()
        if upper_val in ("M", "F", "O"):
            mapping = {"M": "Male", "F": "Female", "O": "Other"}
            self.__gender = mapping[upper_val]
            return
        title_val = normalized.title()
        if title_val in ("Male", "Female", "Other"):
            self.__gender = title_val
            return
        raise ValueError("Gender must be M, F, O or Male, Female, Other")

    # Marital Status
    @property
    def marital_status(self):
        return self.__marital_status

    @marital_status.setter
    def marital_status(self, value: str):
        if value is None:
            self.__marital_status = None
            return
        normalized = value.strip()
        if not normalized:
            self.__marital_status = None
            return
        upper_val = normalized.upper()
        # Accept short codes M, UM, O
        if upper_val in ("M", "UM", "O"):
            mapping = {"M": "Married", "UM": "Unmarried", "O": "Other"}
            self.__marital_status = mapping[upper_val]
            return
        title_val = normalized.title()
        if title_val in ("Married", "Unmarried", "Other"):
            self.__marital_status = title_val
            return
        raise ValueError("Marital Status must be M, Um, O or Married, Unmarried, Other")

    # Current Medication
    @property
    def current_medications(self):
        return self.__current_medications

    @current_medications.setter
    def current_medications(self, value: str):
        if value and not isinstance(value, str):
            raise ValueError("Current Medications must be text")
        self.__current_medications = value

    # Emergency Contact
    @property
    def emergency_contact(self):
        return self.__emergency_contact

    @emergency_contact.setter
    def emergency_contact(self, value: str):
        if value:
            if not (value.isdigit() and len(value) == 10 and value[0] in "987"):
                raise ValueError("Emergency contact must be 10 digits starting with 9, 8, or 7")
        self.__emergency_contact = value

    # Is Active
    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value: str):
        if value not in ("Y", "N"):
            raise ValueError("is_active must be 'Y' or 'N'")
        self.__is_active = value

    # String Representation
    def __str__(self):
        return f"""
        Patient ID: {self.__patient_id}
        Name      : {self.__first_name} {self.__last_name}
        DOB       : {self.__DOB}
        Phone     : {self.__phone_no}
        Email     : {self.__email}
        Address   : {self.__address}
        Height    : {self.__height} cm
        Weight    : {self.__weight} kg
        Gender    : {self.__gender}
        Blood Grp : {self.__blood_group}
        Marital   : {self.__marital_status}
        Medications: {self.__current_medications}
        Emergency : {self.__emergency_contact}
        Active    : {self.__is_active}
        """
