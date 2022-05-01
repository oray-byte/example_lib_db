# MySQL API
# MySQL API Documentation: https://dev.mysql.com/doc/connector-python/en/
import mysql.connector

print("Connecting to database...\n")
# Debugging purposes
connecting = False

# Method to connect to MySQL server
# See https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html for list of arguements

if connecting:
    try:
        cnx = mysql.connector.connect(user=input("Enter username: "), password=input("Enter password: "), host=input("Enter host: "), database=input("Enter database name: "))
    except mysql.connector.Error as err:
        if err.errno == err.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Username or password is incorrect...\nRun the script again...")
            exit()
        elif err.errno == err.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist...\nRun the script again...")
            exit()
        else:
            print(err)
            print("Run script again...")
            exit()
    else:
        cnx.close()

# curser() instantiates objects that can execute operations such as SQL statements. Interacts with MySQL server through MySQLConnection object
# Visit https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html for full documentation
if connecting:
    cursor = cnx.cursor()

# Exits the program. Option # 9
def onExit():
    if (connecting):
        cursor.close()
        cnx.close()

    print('Quiting program...')
    print('Thanks for using Forbidden Cucumber Knowledge software! Good bye!')
    exit()

# Handles input by assigning options to functions
# Must define the functions before this
input_handler = {
    1 : "do option 1", # TODO: Inplement options 
    2 : "do option 2",
    3 : "do option 3",
    4 : "do option 4",
    5 : "do option 5",
    6 : "do option 6", 
    7 : "do option 7",
    8 : "do option 8",
    9 : onExit
}

if __name__ == "__main__":
    while True: 
        # Useful documenation about Python string formatting: https://docs.python.org/3/library/string.html and https://www.w3schools.com/python/ref_string_format.asp
        print("-"*60)
        print("| {:^56} |".format("**** Library Menu ****"))
        print("| {:<56} |".format("1) Check if a particular computer is available"))
        print("| {:<56} |".format("2) See the list of available computers"))
        print("| {:<56} |".format("3) See available apps on computers"))
        print("| {:<56} |".format("4) Check if a particular room is available"))
        print("| {:<56} |".format("5) See the list of available rooms"))
        print("| {:<56} |".format("6) Check if a book is in stock"))
        print("| {:<56} |".format("7) Check when book is due"))
        print("| {:<56} |".format("8) Search for book"))
        print("| {:<56} |".format("9) Quit"))
        print("-"*60)

        # Error handling
        while True:
            try:
                menuChoice = int(input("Please enter an option: "))

            except ValueError as err:
                print("Oops! That was not a valid number. Please try again...")
                continue

            if (menuChoice < 1 or menuChoice > 9):
                print("Invalid option. Please try again...")
            else:
                break

        # Handles user input by calling appropriate function
        input_handler[menuChoice]()
