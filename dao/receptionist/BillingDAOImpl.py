from dao.receptionist.AbstractBillingDAO import BillingDaoService
from db.db_connection import DBConnection
from models.receptionist.Billing import Billing
from typing import List
# from pymysql.cursors import DictCursor

class BillingDaoImplementation(BillingDaoService):
    'Implementation for abstract class'
    #SQL queries
    DISPLAY_ALL = "SELECT * from billings WHERE isActive = 'Y'"
    INSERT_BILLING = "INSERT INTO billings(appointment_id, total_bill, bill_date) VALUES (%s, %s, %s)" 
    FIND_BY_ID = "SELECT * FROM billings WHERE billingid = %s"
    UPDATE_BILLING  = "UPDATE billings set billingname = %s, unitprice = %s WHERE billingid = %s" #$$$$$$$$$$$$
    DISABLE_BILLING = "UPDATE billings set isActive = %s WHERE billingid = %s" #$$$$$$$$$$$$
    # APPLY_GST = "CALL apply_gst_to_billing(%s, %s)"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def insert_billings(self, billing:Billing) -> bool:
        try:
            cursor = self.conn.cursor() #create a cursor object
            cursor.execute(self.INSERT_BILLING,
                           (billing.appointment_id(),
                           billing.total_bill(),
                           billing.bill_date(),
                           ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting billing: ", e)
            return False
        finally:
            cursor.close()

    def display_all_billings(self) -> List[Billing]:
        billings = [] #to store the records from db
        try:
            cursor = self.conn.cursor() #(DictCursor) #returns data in dictionary format
            cursor.execute(self.DISPLAY_ALL) #fire the query
            rows = cursor.fetchall()
            for row in rows:
                billings.append(Billing(billing_id = row["billing_id"],
                                        appointment_id = row["appointment_id"],
                                        unitprice = row["unitprice"],
                                        categoryid = row["categoryid"],
                                        manufacturedate = row["manufacturedate"],
                                        is_active = row["isActive"]))
        except Exception as e:
            print("Error fetching billings: ", e)
        finally:
            cursor.close()
        return billings
    
    def find_by_billing_id(self, billing_id:int):
        billing = None
        try:
            cursor = self.conn.cursor() #(DictCursor) #$$$$$$$$$$$$
            cursor.execute(self.FIND_BY_ID, (billing_id,))
            row = cursor.fetchone()
            if row:
                billing = Billing(
                    billingid = row["billingid"],
                    appointment_id = row["appointment_id"],
                    total_bill = row["total_bill"],
                    bill_date = row["bill_date"],
                    )
        except Exception as e:
            print("Error finding billing: ", e)
        finally:
            cursor.close()
        return billing

    def update_billing(self, billing:Billing, billing_id:int) ->bool:
        try:
            cursor = self.conn.cursor() #(DictCursor) #$$$$$$$$$$$$
            cursor.execute(self.UPDATE_BILLING,
                           (billing.appointment_id(),
                            billing.total_bill(),
                            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating billing: ", e)
            return False
        finally:
            cursor.close()

    # def disable_billing(self, billing:Billing, billing_id:int) ->bool:
    #     try:
    #         cursor = self.conn.cursor() #(DictCursor) #$$$$$$$$$$$$
    #         cursor.execute(self.DISABLE_BILLING,
    #                        (billing.get_is_active(),
    #                         billing_id))
    #         self.conn.commit()
    #         return cursor.rowcount == 1
    #     except Exception as e:
    #         print("Error updating billing: ", e)
    #         return False
    #     finally:
    #         cursor.close()

    # def apply_gst(self, billing_id:int, gst_percent:float) ->bool:
    #     cursor = None
    #     try:
    #         cursor = self.conn.cursor()
    #         cursor.execute(self.APPLY_GST, (billing_id, gst_percent))
    #         self.conn.commit()
    #         return cursor.rowcount >=0 #since sp returns 0 if already applied
    #     except Exception as e:
    #         print("Error applying GST: ", e)
    #         return False
    #     finally:
    #         if cursor:
    #             cursor.close()
                