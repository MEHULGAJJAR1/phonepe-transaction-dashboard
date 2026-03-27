import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="phonepe_db"
    )
    return connection