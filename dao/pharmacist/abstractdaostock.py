from abc import ABC, abstractmethod
from models.pharmacist.p_med_stock import Stock


class StockDaoService(ABC):

    @abstractmethod
    def add_stock(self, stock: Stock):
        pass

    @abstractmethod
    def update_stock(self, stock_id: str, current_stock: int, stock_status: str):
        pass

    @abstractmethod
    def delete_stock(self, stock_id: str) -> bool:
        pass

    @abstractmethod
    def search_stock_by_id(self, stock_id: str):
        pass

    @abstractmethod
    def list_all(self):
        pass


