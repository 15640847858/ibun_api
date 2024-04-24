# -*- coding: utf-8 -*-

import mysql.connector as connector
from mysql.connector import errorcode


class MySQLDB:
    def __init__(self, port, host, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = connector.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database")
        except connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Access denied, please check your username and password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist")
            else:
                print("Error:", err)

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except connector.Error as err:
            print("Error:", err)
            return None

    def execute_update(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully")
        except connector.Error as err:
            print("Error:", err)
            self.connection.rollback()

    def insert_record(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute_update(query, tuple(data.values()))

    def update_record(self, table, data, condition):
        set_values = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        self.execute_update(query, tuple(data.values()))

    def delete_record(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_update(query)

    def select_records(self, table, condition=None):
        query = f"SELECT * FROM {table}"
        # 如果有条件，则添加到查询语句中
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query)


# 示例用法
# if __name__ == "__main__":
#     db_host = "mysqlxxx"
#     db_port = 3306
#     db_database = "xxx"
#     db_username = "xxx"
#     db_password = "xxx"
#
#     # 替换以下信息为你的 MySQL 远程数据库连接信息
#     db = MySQLDB(host=db_host, port= db_port,username=db_username, password=db_password, database=db_database)
#     db.connect()

    # 插入示例
    # data_to_insert = {'username': 'John', 'password': 'testpsd', 'phone_number': '18811112222'}
    # db.insert_record('user_info', data_to_insert)

    # 更新示例
    # data_to_update = {'age': 31, 'city': 'Los Angeles'}
    # db.update_record('user_info', data_to_update, 'name = "John"')

    # 删除示例
    # db.delete_record('user_info', 'name = "John"')

    # 查询示例
    # records = db.select_records('user_info')
    # if records:
    #     for record in records:
    #         print(record)

    # 如果报错，Exception ignored in: <function BaseMySQLSocket.__del__ at 0x000002B26E3501F0>
    # 则使用 pip 命令来更新 mysql-connector-python 模块到最新版本。
    # pip install --upgrade mysql-connector-python
    # db.disconnect()
