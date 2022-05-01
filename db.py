# MySQL API
import mysql.connector

cnx = mysql.connector.connect(user='root', password='[ENTER PASSWORD]', host='localhost', database='library')
cursor = cnx.cursor()

# SQL Commands are stored as dictionary values where the name of the query is the key and the query logic is the data
QUERIES = {}

def menu():
    pass


if __name__ == "__main__":
    cursor.execute(QUERIES["test"])
    cursor.close()
    cnx.close()