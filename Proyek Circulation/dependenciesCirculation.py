from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    def __init__(self, connection):
        self.connection = connection

    def add_circulation(self, id_room, id_item, id_employee, id_purchase, qty, status):
        cursor = self.connection.cursor(dictionary=True)
        sql = "insert into circulation values (0,{},{},{},{},{}, CURDATE(),{})".format(id_room, id_item, id_employee, id_purchase, qty, status)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        self.update_room_item(id_room, id_item, qty)
        return "sukses add circulation"

    def add_room_item(self, id_room, id_item, qty):
        cursor = self.connection.cursor(dictionary=True)
        sql = "insert into room_item values (0, {}, {}, {})".format(id_room, id_item, qty)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "sukses add room item"

    def get_room_item_by_id(self, id_room, id_item):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM room_item WHERE id_room = {} and id_item = {}".format(id_room, id_item)
        cursor.execute(sql)
        result = cursor.fetchone()
        #print("Result:" + result)
        cursor.close()
        return result

    def update_room_item(self, id_room, id_item, qty):
        cursor = self.connection.cursor(dictionary=True)
        cekqty = self.get_room_item_by_id(id_room, id_item)
        #updated_qty = cekqty['qty'] + qty
        #print(cekqty)
        if ((cekqty['qty'] + qty) >= 0 and cekqty['qty'] is not None):
            sql = "update room_item set qty = {} where id = {}".format(cekqty['qty'] + qty, cekqty['id'])
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return "sukses update qty room item"
        else:
            cursor.close()
            return "Gagal update qty room item"
       

class Database(DependencyProvider):
    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='proyek_soa_2',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())