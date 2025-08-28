from dao.pharmacist.stockdaoimple import StockDaoImplementation
from models.pharmacist.p_med_stock import Stock


class StockManagementLib:
    dao_service = StockDaoImplementation()

    @staticmethod
    def add_stock():
        stock_id = input("Enter Stock ID: ")
        medicine_id = input("Enter Medicine ID: ")
        current_stock = int(input("Enter Current Stock: "))
        stock_status = input("Enter Stock Status (e.g., LOW/NORMAL/HIGH): ")
        stock = Stock(stock_id, medicine_id, current_stock, stock_status)
        StockManagementLib.dao_service.add_stock(stock)
        print(" Stock added successfully")

    @staticmethod
    def update_stock():
        stock_id = input("Enter Stock ID to update: ")
        current_stock = int(input("Enter New Current Stock: "))
        stock_status = input("Enter New Stock Status: ")
        if StockManagementLib.dao_service.update_stock(stock_id, current_stock, stock_status):
            print(" Stock updated successfully")
        else:
            print(" Stock not found")

    @staticmethod
    def delete_stock():
        stock_id = input("Enter Stock ID to delete: ")
        if StockManagementLib.dao_service.delete_stock(stock_id):
            print(" Stock deleted successfully")
        else:
            print(" Stock not found")

    @staticmethod
    def search_stock():
        stock_id = input("Enter Stock ID to search: ")
        stock = StockManagementLib.dao_service.search_stock_by_id(stock_id)
        if stock:
            print(stock)
        else:
            print(" Stock not found")

    @staticmethod
    def list_all():
        stocks = StockManagementLib.dao_service.list_all()
        if not stocks:
            print(" No stock records available")
        for s in stocks:
            print(s)


