class Billing:
    def __init__(self, bill_id: str, charge: float, prescription_id: str, bill_date: str):
        self.bill_id = bill_id
        self.charge = charge
        self.prescription_id = prescription_id
        self.bill_date = bill_date

    def __str__(self) -> str:
        return (
            f"Billing(bill_id={self.bill_id}, charge={self.charge}, "
            f"prescription_id={self.prescription_id}, bill_date={self.bill_date})"
        )


