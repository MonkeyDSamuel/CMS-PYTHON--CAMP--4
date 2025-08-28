import pymysql

class LabTestDAOImpl:
    def __init__(self, conn):
        self.conn = conn

    def _generate_next_test_id(self):
        """Generate next ID like TEST0001, TEST0002... based on lab_test_id column"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(lab_test_id) FROM lab_test")
        last_id = cursor.fetchone()[0]
        cursor.close()

        if last_id:
            next_num = int(last_id.replace("TEST", "")) + 1
        else:
            next_num = 1

        return f"TEST{next_num:04d}"

    def create_labtest(self, lab_test_name, category_id, rate, created_on, min_value, max_value):
        """Insert a new lab test (is_active defaults in DB)."""
        lab_test_id = self._generate_next_test_id()
        cursor = self.conn.cursor()
        sql = (
            "INSERT INTO lab_test (lab_test_id, lab_test_name, category_id, rate, created_on, min_value, max_value) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(sql, (lab_test_id, lab_test_name, category_id, rate, created_on, min_value, max_value))
        self.conn.commit()
        cursor.close()
        return lab_test_id

    def get_labtest_by_id(self, lab_test_id):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM lab_test WHERE lab_test_id = %s", (lab_test_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def list_labtests(self):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM lab_test")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def update_labtest(self, lab_test_id, lab_test_name=None, category_id=None, rate=None, min_value=None, max_value=None, is_active=None):
        fields = []
        values = []

        if lab_test_name is not None and lab_test_name != "":
            fields.append("lab_test_name = %s")
            values.append(lab_test_name)
        if category_id is not None and category_id != "":
            fields.append("category_id = %s")
            values.append(category_id)
        if rate is not None and rate != "":
            fields.append("rate = %s")
            values.append(rate)
        if min_value is not None and min_value != "":
            fields.append("min_value = %s")
            values.append(min_value)
        if max_value is not None and max_value != "":
            fields.append("max_value = %s")
            values.append(max_value)
        if is_active is not None and is_active != "":
            fields.append("is_active = %s")
            values.append(is_active)

        if not fields:
            return False

        values.append(lab_test_id)
        sql = f"UPDATE lab_test SET {', '.join(fields)} WHERE lab_test_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(values))
        self.conn.commit()
        cursor.close()
        return True

    def deactivate_labtest(self, lab_test_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE lab_test SET is_active = 0 WHERE lab_test_id = %s", (lab_test_id,))
        self.conn.commit()
        cursor.close()
        return True
