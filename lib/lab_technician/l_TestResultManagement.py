from models.lab_technician.l_test_result import LabTestResult

class LabResultLib:
    # simple in-memory store in lieu of a DAO
    _results = []

    @staticmethod
    def add_result():
        try:
            result_id = int(input("Enter Result ID: "))
            lab_test_id = int(input("Enter Lab Test ID: "))
            lab_prescription_id = int(input("Enter Lab Prescription ID: "))
            status = input("Enter Status: ")
            date = input("Enter Date (YYYY-MM-DD): ")
            result = LabTestResult(result_id, lab_test_id, lab_prescription_id, status, date)
            LabResultLib._results.append(result)
            print(" Result added successfully.")
        except Exception as e:
            print(f" Error adding result: {e}")

    @staticmethod
    def update_result():
        try:
            result_id = int(input("Enter Result ID to update: "))
            existing = next((r for r in LabResultLib._results if r.get_result_id() == result_id), None)
            if not existing:
                print(" Result not found.")
                return
            status = input("Enter New Status: ")
            date = input("Enter New Date (YYYY-MM-DD): ")
            existing.set_status(status)
            existing.set_date(date)
            print(" Result updated successfully.")
        except Exception as e:
            print(f" Error updating result: {e}")

    @staticmethod
    def display_all_results():
        results = LabResultLib._results
        if results:
            print("\n--- All Results ---")
            for r in results:
                print(f"ResultID: {r.get_result_id()} | LabTestID: {r.get_lab_test_id()} | LabPrescription: {r.get_lab_prescription_id()} | Status: {r.get_status()} | Date: {r.get_date()}")
        else:
            print(" No results found.")

    @staticmethod
    def search_result_by_id():
        try:
            result_id = int(input("Enter Result ID: "))
            r = next((r for r in LabResultLib._results if r.get_result_id() == result_id), None)
            if r:
                print(f" Found: ResultID={r.get_result_id()} | LabPrescription={r.get_lab_prescription_id()} | LabTest={r.get_lab_test_id()} | Status={r.get_status()} | Date={r.get_date()}")
            else:
                print("Result not found.")
        except Exception as e:
            print(f"Error searching result: {e}")