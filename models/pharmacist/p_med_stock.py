# models/medicine.py

class Medicine:
    def __init__(self, med_id: int, name: str, price: float, stock: int):
        """
        Model representing a medicine item in stock.
        :param med_id: Unique identifier for medicine
        :param name: Medicine name
        :param price: Price per unit
        :param stock: Available stock quantity
        """
        self.med_id = med_id
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity: int):
        """
        Update medicine stock (positive for adding, negative for reducing).
        """
        if self.stock + quantity < 0:
            raise ValueError(f"Not enough stock for {self.name}")
        self.stock += quantity

    def is_available(self, qty: int) -> bool:
        """
        Check if required quantity is available.
        """
        return self.stock >= qty

    def __str__(self):
        return f"[{self.med_id}] {self.name} | ₹{self.price:.2f} | Stock: {self.stock}"
