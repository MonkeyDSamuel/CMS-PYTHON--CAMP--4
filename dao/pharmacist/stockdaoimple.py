from dao.pharmacist.abstractdaostock import StockDaoService
from models.pharmacist.p_med_stock import Stock


class StockDaoImplementation(StockDaoService):
    def __init__(self):
        self._stocks: dict[str, Stock] = {}

    def add_stock(self, stock: Stock):
        if stock.stock_id in self._stocks:
            raise ValueError("Stock ID already exists")
        self._stocks[stock.stock_id] = stock
        return True

    def update_stock(self, stock_id: str, current_stock: int, stock_status: str):
        stock = self._stocks.get(stock_id)
        if not stock:
            return False
        stock.current_stock = current_stock
        stock.stock_status = stock_status
        return True

    def delete_stock(self, stock_id: str) -> bool:
        if stock_id in self._stocks:
            del self._stocks[stock_id]
            return True
        return False

    def search_stock_by_id(self, stock_id: str):
        return self._stocks.get(stock_id)

    def list_all(self):
        return list(self._stocks.values())


