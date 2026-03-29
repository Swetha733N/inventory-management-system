import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sweth@733",  
        database="inventory_db"
    )