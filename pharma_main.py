from lib.pharmacist.medicinemanage import PharmacistManagementLib
from lib.pharmacist.categorymanage import CategoryManagementLib
from lib.pharmacist.billmanage import BillingManagementLib
from lib.pharmacist.stockmanage import StockManagementLib


def run_medicine_menu():
    while True:
        print("\n-- Medicine Management --")
        print("1. Add Medicine")
        print("2. Display All Medicines")
        print("3. Search Medicine by ID")
        print("4. Update Medicine by ID")
        print("5. Delete Medicine by ID")
        print("6. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            PharmacistManagementLib.add_medicine()
        elif choice == "2":
            PharmacistManagementLib.display_all()
        elif choice == "3":
            PharmacistManagementLib.search_medicine()
        elif choice == "4":
            PharmacistManagementLib.update_medicine()
        elif choice == "5":
            PharmacistManagementLib.delete_medicine()
        elif choice == "6":
            break
        else:
            print(" Invalid choice! Please try again.\n")


def run_category_menu():
    while True:
        print("\n-- Category Management --")
        print("1. Add Category")
        print("2. Display All Categories")
        print("3. Search Category by ID")
        print("4. Delete Category")
        print("5. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            CategoryManagementLib.add_category()
        elif choice == "2":
            CategoryManagementLib.display_categories()
        elif choice == "3":
            CategoryManagementLib.search_category()
        elif choice == "4":
            CategoryManagementLib.delete_category()
        elif choice == "5":
            break
        else:
            print(" Invalid choice! Please try again.\n")


def run_billing_menu():
    while True:
        print("\n-- Bill Management --")
        print("1. Add Bill")
        print("2. Display All Bills")
        print("3. Search Bill by ID")
        print("4. Delete Bill")
        print("5. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            BillingManagementLib.add_bill()
        elif choice == "2":
            BillingManagementLib.display_all()
        elif choice == "3":
            BillingManagementLib.search_bill()
        elif choice == "4":
            BillingManagementLib.delete_bill()
        elif choice == "5":
            break
        else:
            print(" Invalid choice! Please try again.\n")


def run_dashboard():
    while True:
        print("\n==== Pharmacist Dashboard ====")
        print("1. Medicine Management")
        print("2. Category Management")
        print("3. Bill Management")
        print("4. View Stock Table")
        print("5. Stock Management")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            run_medicine_menu()
        elif choice == "2":
            run_category_menu()
        elif choice == "3":
            run_billing_menu()
        elif choice == "4":
            PharmacistManagementLib.view_stock()
        elif choice == "5":
            run_stock_menu()
        elif choice == "6":
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice! Please try again.\n")


def run_stock_menu():
    while True:
        print("\n-- Stock Management --")
        print("1. Add Stock")
        print("2. Update Stock")
        print("3. Delete Stock")
        print("4. Search Stock by ID")
        print("5. List All Stock")
        print("6. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            StockManagementLib.add_stock()
        elif choice == "2":
            StockManagementLib.update_stock()
        elif choice == "3":
            StockManagementLib.delete_stock()
        elif choice == "4":
            StockManagementLib.search_stock()
        elif choice == "5":
            StockManagementLib.list_all()
        elif choice == "6":
            break
        else:
            print(" Invalid choice! Please try again.\n")
def run_billing_menu():
    while True:
        print("---- Billing Menu ----")
        print("1. Add Bill")
        print("2. Display All Bills")
        print("3. Search Bill by ID")
        print("4. Delete Bill")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            BillingManagementLib.add_bill()
        elif choice == "2":
            BillingManagementLib.display_all()
        elif choice == "3":
            BillingManagementLib.search_bill()
        elif choice == "4":
            BillingManagementLib.delete_bill()
        elif choice == "5":
            print(" Exiting Billing Menu...")
            break
        else:
            print(" Invalid choice! Please try again.\n")
    


if __name__ == "__main__":
    run_dashboard()