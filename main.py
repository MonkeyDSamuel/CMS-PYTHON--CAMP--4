from lib.lab_technician.l_LabTestManagement import LabTestLib
from lib.lab_technician.l_TestCategoryManagement import LabCategoryLib
from lib.lab_technician.l_LabBillingManagement import LabBillingLib
from lib.lab_technician.l_TestResultManagement import LabResultLib


def category_menu():
    while True:
        print("\n===== TEST CATEGORY MANAGEMENT =====")
        print("1. ADD NEW TEST CATEGORY")
        print("2. DISPLAY ALL CATEGORIES")
        print("0. BACK TO MAIN MENU")

        choice = input("Enter your choice: ")

        if choice == "1":
            LabCategoryLib.add_category()
        elif choice == "2":
            LabCategoryLib.display_all_categories()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again...")


def test_menu():
    while True:
        print("\n===== TEST MANAGEMENT =====")
        print("1. ADD NEW TEST")
        print("2. DISPLAY ALL TESTS")
        print("3. UPDATE TEST")
        print("4. DEACTIVATE TEST")
        print("0. BACK TO MAIN MENU")

        choice = input("Enter your choice: ")

        if choice == "1":
            LabTestLib.add_test()
        elif choice == "2":
            LabTestLib.display_all_tests()
        elif choice == "3":
            LabTestLib.update_test()
        elif choice == "4":
            LabTestLib.deactivate_test()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again...")


def result_menu():
    while True:
        print("\n===== TEST RESULT MANAGEMENT =====")
        print("1. ADD LAB TEST RESULT")
        print("2. DISPLAY ALL RESULTS")
        print("3. UPDATE LAB TEST RESULT")
        print("4. SEARCH RESULT BY ID")
        print("0. BACK TO MAIN MENU")

        choice = input("Enter your choice: ")

        if choice == "1":
            LabResultLib.add_result()
        elif choice == "2":
            LabResultLib.display_all_results()
        elif choice == "3":
            LabResultLib.update_result()
        elif choice == "4":
            LabResultLib.search_result_by_id()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again...")


def billing_menu():
    while True:
        print("\n===== TEST BILLING MANAGEMENT =====")
        print("1. GENERATE LAB BILL")
        print("2. DISPLAY ALL BILLS")
        print("3. SEARCH BILL BY ID")
        print("0. BACK TO MAIN MENU")

        choice = input("Enter your choice: ")

        if choice == "1":
            LabBillingLib.generate_bill()
        elif choice == "2":
            LabBillingLib.display_all_bills()
        elif choice == "3":
            LabBillingLib.search_bill_by_id()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again...")


# Entry point dashboard

def main():
    while True:
        print("---------WELCOME TO CLINIC MANAGEMENT SYSTEM---------")
        print("\n===== LAB TECHNICIAN DASHBOARD =====")
        print("1. Test Category Management")
        print("2. Test Management")
        print("3. Test Result Management")
        print("4. Test Billing Management")
        print("5. EXIT")

        choice = input("Enter your choice: ")

        if choice == "1":
            category_menu()
        elif choice == "2":
            test_menu()
        elif choice == "3":
            result_menu()
        elif choice == "4":
            billing_menu()
        elif choice == "5":
            print("Exiting Lab Technician Module...")
            break
        else:
            print("Invalid choice, try again...")


if __name__ == "__main__":
    main()
