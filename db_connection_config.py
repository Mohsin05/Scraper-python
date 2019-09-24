import mysql.connector


class db_connection():

    def connection(self):
        connection = mysql.connector.connect(host='localhost',
                                             database='jobs',
                                             user='root',
                                             password='root')
        return connection
