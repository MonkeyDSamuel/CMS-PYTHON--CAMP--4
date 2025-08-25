from db.db_connection import DBConnection
from dao.receptionist.patient import Check
def main():
    while True:
        print("---------WELCOME TO CLINIC MANAGEMENT SYSTEM---------")
        Check.checking()
        break

        

if __name__ == "__main__":
    main()

