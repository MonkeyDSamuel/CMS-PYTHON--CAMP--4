class Stock:
    """Represents medicine stock information."""

    def __init__(self, stock_id: str, medicine_id: str, current_stock: int, stock_status: str):
        self.stock_id = stock_id
        self.medicine_id = medicine_id
        self.current_stock = current_stock
        self.stock_status = stock_status

    def __str__(self):
        return (
            f"Stock(stock_id={self.stock_id}, medicine_id={self.medicine_id}, "
            f"current_stock={self.current_stock}, status={self.stock_status})"
        )
