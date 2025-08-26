from dao.receptionist.BillingDAOImpl import BillingDaoImplementation
from dao.receptionist.AbstractBillingDAO import BillingDaoService
from models.receptionist.Billing import Billing
from datetime import datetime

class BillingManagementLib:
    'handles CRUD logic'
    dao_service:BillingDaoService = BillingDaoImplementation()

    @staticmethod
    def display_all():
        billings = BillingManagementLib.dao_service.display_all_billings()
        for billing in billings:
            print(billing)
    
    @staticmethod
    def add_billing():
        billing = Billing()
        appointment_id = input("Enter the appointment id: ")
        billing.appointment_id(appointment_id)
        categoryid = int(input("Enter the Category Id: "))
        billing.set_category_id(categoryid)
        # m_date = input("Enter manufacture Date(dd/mm/yyyy): ")
        # util_date = datetime.strptime(m_date, "%d/%m/%Y")
        # conv_m_date = util_date.date()
        # billing.set_manufacture_date(conv_m_date)
        # bill_date #$$$$$$$$$$$$$$$$$$$$$$

        if BillingManagementLib.dao_service.insert_billings(billing):
            print("Inserted Successfully!!")
        else:
            print("Something went wrong.....")

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&        

    @staticmethod
    def update_billing():
        searchId = int(input("Enter the billing ID: "))
        #create a method in DAO
        billing = BillingManagementLib.dao_service.find_by_billing_id(searchId)
        if not billing:
            print("Billing not found")
            return
        print(billing)
        confirm = input("Do you want to edit this data? (y/n)")
        if confirm.lower() == 'y':
            billing.set_billing_name(input("Enter new billing Name: ") or billing.get_billingname())
            billing.set_unitprice(float(input("Enter New Unit Price: ")) or billing.get_unitprice())

            #pass the object to dao update
            if BillingManagementLib.dao_service.update_billing(billing, searchId):
                print("updated successfully ....")
            else:
                print("something went wrong ....")

    @staticmethod
    def search_by_id():
        searchId = int(input("Enter the billing ID: "))
        #create a method in DAO
        billing = BillingManagementLib.dao_service.find_by_billing_id(searchId)
        if not billing:
            print("Billing not found")
            return
        print(billing)
    
    @staticmethod
    def disable_billing():
        searchId = int(input("Enter the billing ID: "))
        #create a method in DAO
        billing = BillingManagementLib.dao_service.find_by_billing_id(searchId)
        if not billing:
            print("Billing not found")
            return
        print(billing)
        billing.set_is_active("N")

        #pass the object to dao update
        if BillingManagementLib.dao_service.disable_billing(billing, searchId):
            print("updated successfully ....")
        else:
            print("something went wrong ....")

        # if BillingManagementLib.dao_service.disable_billing(billing, searchId):

    @staticmethod
    def apply_gst_to_billing():
        billing_id = int(input("Enter the billing ID to apply GST: "))
        gst_percent = float(input("Enter GST percentage to apply: "))
        if BillingManagementLib.dao_service.apply_gst(billing_id, gst_percent):
            print(f"GST of {gst_percent} applied to billing ID (billing_id)")
        else:
            print("failed to apply GST")