import mysql.connector

cnx = mysql.connector.connect(user='root', password='E@stW00D6576', host='localhost', database='library')
cursor = cnx.cursor()
QUERIES = {}
TABLES = {}
INSERT = {}
# Dictionary that contains CREATE TABLE instructions
QUERIES['test'] = (
    "SELECT `fname`, `lname`"
    "FROM users"
    )

TABLES['users'] = (
    "CREATE TABLE `users`("
    "  uid INT NOT NULL,"
    "  fname VARCHAR(25),"
    "  lname VARCHAR(25)"
    ");"
)

INSERT['john'] = (
    "INSERT INTO `users` VALUES(1, `John`, `Smith`);"
    "INSERT INTO `users` VALUES(2, `Jim`, `Rob`);"
    "INSERT INTO `users` VALUES(3, `Jimmy`, `John`);"
)

cursor.execute(INSERT['john'])
cursor.execute(QUERIES["test"])
cursor.close()
cnx.close()