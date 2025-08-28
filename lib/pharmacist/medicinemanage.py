from dao.pharmacist.medicinedaoimpl import PharmacistDaoImplementation
from dao.pharmacist.abstractdaomedicine import PharmacistDaoService

class PharmacistManagementLib:
    dao_service: PharmacistDaoService = PharmacistDaoImplementation()

    @staticmethod
    def add_medicine():
        category_id = input("Enter Category ID: ")
        medicine_name = input("Enter Medicine Name: ")
        company_name = input("Enter Company Name: ")
        common_name = input("Enter Common Name: ")
        strength = float(input("Enter Strength: "))
        rate_per_unit = float(input("Enter Rate per Unit: "))

        try:
            med = PharmacistManagementLib.dao_service.add_medicine(
                category_id,
                medicine_name,
                company_name,
                common_name,
                strength,
                rate_per_unit,
            )
            print(f" Medicine {med.medicine_id} added successfully!\n")
        except ValueError as ve:
            print(f" Error: {ve}\n")

    @staticmethod
    def display_all():
        meds = PharmacistManagementLib.dao_service.display_all_medicines()
        if not meds:
            print("⚠ No medicines available!\n")
            return
        print("\nMedicine ID | Category ID | Medicine Name | Company | Common Name | Strength | Rate/unit")
        print("-" * 90)
        for m in meds:
            print(f"{m.medicine_id} | {m.category_id} | {m.medicine_name} | {m.company_name} | {m.common_name} | {m.strength} | {m.rate_per_unit:.2f}")
        print()

    @staticmethod
    def search_medicine():
        med_id = input("Enter Medicine ID (e.g. med0001): ")
        med = PharmacistManagementLib.dao_service.search_medicine(med_id)
        print(med if med else " Medicine not found!")

    @staticmethod
    def update_medicine():
        med_id = input("Enter Medicine ID to update: ")
        new_name = input("Enter new Medicine Name (leave blank to keep old): ")
        new_company = input("Enter new Company Name (leave blank to keep old): ")
        new_common = input("Enter new Common Name (leave blank to keep old): ")
        new_strength = input("Enter new Strength (leave blank to keep old): ")
        new_rate = input("Enter new Rate (leave blank to keep old): ")
        updates = {}
        if new_name:
            updates["Medicine_name"] = new_name
        if new_company:
            updates["Company_name"] = new_company
        if new_common:
            updates["Common_name"] = new_common
        if new_strength:
            try:
                updates["Strength"] = float(new_strength)
            except ValueError:
                pass
        if new_rate:
            updates["Rate_per_unit"] = float(new_rate)
        if PharmacistManagementLib.dao_service.update_medicine(med_id, **updates):
            print(" Updated successfully")
        else:
            print(" Medicine not found")

    @staticmethod
    def delete_medicine():
        med_id = input("Enter Medicine ID to delete: ")
        if PharmacistManagementLib.dao_service.delete_medicine(med_id):
            print(f"🗑 Medicine {med_id} deleted successfully")
        else:
            print(" Medicine not found")

    @staticmethod
    def view_stock():
        PharmacistManagementLib.dao_service.display_table()
