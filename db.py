# MySQL API
# MySQL API Documentation: https://dev.mysql.com/doc/connector-python/en/
from time import sleep
from getpass import getpass
from datetime import datetime
import mysql.connector
import os

# Debugging purposes
connecting = True

# For formatting output
displayLength = 80
formatCenter = "| {:^76} |"
formatLeft = "| {:<76} |"

print("Connecting to database...\n")

# Method to connect to MySQL server
# See https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html for list of arguements

if connecting:
    try:
        cnx = mysql.connector.connect(user=input("Enter username: "), password=getpass(prompt="Enter password: "), host=input("Enter host: "), database=input("Enter database name: "))
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

# curser() instantiates objects that can execute operations such as SQL statements. Interacts with MySQL server through MySQLConnection object
# Visit https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html for full documentation
if connecting:
    cursor = cnx.cursor()
    
# Clears console
def clearConsole():
    if (os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")

"""
    Name: optionONE()
    Description: Handles functionality for option one
    Params: None
    Scope: Public 
    Summary: Search a computer with its commputerID and print if it is available or not
"""
def optionONE():
    print("-" * displayLength)
    print(formatCenter.format("**** Check if particular computer is available ****"))
    print(formatLeft.format("To check if a computer is available, please the computer's ID"))
    
    # Make sure input is valid
    while True:
        try:
            computerID = int(getpass(prompt=(formatLeft.format("Enter computer ID: "))))
        except ValueError as err:
            print(formatLeft.format("Oops! That was not a valid number. Please try again..."))
            continue
        break
    
    print(formatLeft.format("Searching for computer of ID: " + str(computerID)))
    
    # SQL query: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
    # Return all of the available computers
    outerQuery = ("SELECT C.comp_id, C.comp_loc "
                  "FROM computers AS C "
                  "WHERE C.comp_id NOT IN (SELECT CU.c_comp_id FROM computeruse AS CU)")
    cursor.execute(outerQuery)
    rows = cursor.fetchall()
    
    # Check list of all available computers to see if specific computer is available
    for (comp_id, comp_loc) in rows:
        if comp_id == computerID:
            print(formatLeft.format("Computer {id} is available on the {floor}".format(id=computerID, floor=comp_loc)))
            return
    
    print(formatLeft.format("Computer {id} is unavailable.".format(id=computerID)))        
    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionTWO()
    Description: Handles functionality for option two
    Params: None
    Scope: Public 
    Summary: Print a list of all available computers in the library
"""  
def optionTWO():
    print("-" * displayLength)
    print(formatCenter.format('**** List of available computers ****'))

    #**SQL QUERY of the list of available computers, show computerID and location**
    outerQuery = ("SELECT C.comp_id, C.comp_loc "
                "FROM computers AS C "
                "WHERE C.comp_id NOT IN (SELECT CU.c_comp_id FROM computeruse AS CU)")
    cursor.execute(outerQuery)
    rows = cursor.fetchall()
    
    # Check to see if there are no returned rows
    if (len(rows) == 0):
        print(formatLeft.format("There are no available computers"))
    else:
        # Print out all available computers
        for (comp_id, comp_loc) in rows:
            print(formatLeft.format("Computer {id} is available on floor {floor}".format(id=comp_id, floor=comp_loc)))


    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionTHREE()
    Description: Handles functionality for option three
    Params: None
    Scope: Public 
    Summary: Print a list of all available apps on computers
"""  
def optionTHREE():
    # show list of available apps 
    print("-" * displayLength)
    print(formatCenter.format('**** See all available computer apps****'))

    #SQL query show list of available apps from all computers.
    outerQuery = (
                "SELECT * "
                "FROM apps"
                )
    cursor.execute(outerQuery)
    rows = cursor.fetchall()

    # Print out all available apps
    for (_aid, app_name) in rows:
        print(formatLeft.format("Application name: {app}".format(app=app_name)))

    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionFOUR()
    Description: Handles functionality for option four
    Params: None
    Scope: Public 
    Summary:Search a room with its roomNumber and print if it is available or not
"""  
def optionFOUR():
    print("-" * displayLength)
    print(formatCenter.format('**** Checking if a particular room is available ****'))
    print(formatLeft.format('To check if a room is available, please enter room number.'))
    while True:
        try:
            roomNumber = int(getpass(prompt=formatLeft.format("Enter room number: ")))
        except ValueError as err:
            print(formatLeft.format("Oops! That was not a valid number. Please try again..."))
            continue
        break
    #SQL query of room number and room floor
    outerQuery = ("SELECT R.room_num, R.floor "
                  "FROM rooms AS R "
                  "WHERE R.room_num NOT IN (SELECT RU.r_room_num FROM roomuse AS RU)")
    cursor.execute(outerQuery)
    rows = cursor.fetchall()
    
    for (room_num, floor) in rows:
        if (room_num == roomNumber):
            print(formatLeft.format("Room {id} is available on floor {num}".format(id=room_num, num=floor)))
            return
    
    print(formatLeft.format("Room {id} is unavailable.".format(id=roomNumber)))        
    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionFIVE()
    Description: Handles functionality for option five
    Params: None
    Scope: Public 
    Summary: Print a list of all available roosm in the library
"""  
def optionFIVE():
    print("-" * displayLength)
    print(formatCenter.format('**** List of available rooms ****'))
    
    #SQL query showing the LIST of available rooms, show its room number and floor
    outerQuery = (
                "SELECT R.room_num, R.floor "
                "FROM rooms AS R "
                "WHERE R.room_num NOT IN (SELECT RU.r_room_num FROM roomuse AS RU)"
                )
    cursor.execute(outerQuery)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print("There are no available rooms")
    else:
        for (room_num, floor) in rows:
            print(formatLeft.format("Room {id} is available on floor {num}".format(id=room_num, num=floor)))
    
    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionSIX()
    Description: Handles functionality for option six
    Params: None
    Scope: Public 
    Summary: Checks to see if a book is in stock
"""  
def optionSIX():
    queryList = []
    print("-" * displayLength)
    print(formatCenter.format('**** Checking if book is in stock ****'))
    print(formatLeft.format('To check if a book is in stock, please enter book ISBN(13-digit)'))

    while True:
        try:
            bookISBN = (getpass(prompt=(formatLeft.format("Enter book ISBN(13-digit): "))))
        except ValueError as err:
            print(formatLeft.format("Oops! That was not a valid number. Please try again..."))
            continue
        break
    print(formatLeft.format("Checking to see if a book with ISBN " + bookISBN + " exists..."))
    queryList.append(bookISBN)

    #SQL query show book-ISBN, booktitle, book-author, book-quantityinstock, book-location
    outerQuery = (
            "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location "
            "FROM books AS B, authors AS A "
            "WHERE B.baid = A.aid and %s = B.isbn and B.stock > 0"
            )
    
    cursor.execute(outerQuery, queryList)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print(formatLeft.format("We could not find a book with ISBN: {id} that's in stock".format(id=bookISBN)))
    else:
        print(formatCenter.format("**** Book Information ****"))
        print(formatLeft.format("Title: {tit}".format(tit=rows[0][0])))
        print(formatLeft.format("Author name: {name}").format(name=(rows[0][2] + ", " + rows[0][1])))
        print(formatLeft.format("ISBN: {id}".format(id=rows[0][3])))
        print(formatLeft.format("Book stock: {stock}".format(stock=rows[0][4])))
        print(formatLeft.format("Book location: {loc}".format(loc=rows[0][5])))
        
    
    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionSEVEN()
    Description: Handles functionality for option seven
    Params: None
    Scope: Public 
    Summary: Using userID, checks to see when each checked out book is due
"""  
def optionSEVEN():
    queryList = []
    print(formatCenter.format('**** Checking if book is due ****'))
    print(formatLeft.format('To check if a book is due, please enter in userID.'))
    while True:
        try:
            userID = int(getpass(prompt=(formatLeft.format("Enter user ID: "))))
        except ValueError as err:
            print(formatLeft.format("Oops! That was not a valid number. Please try again..."))
            continue
        break
    
    queryList.append(userID)
    outerQuery = (
        "SELECT CO.due_date, B.title "
        "FROM users AS U, checkout AS CO, books as B "
        "WHERE U.uid = CO.c_uid and U.uid = %s and CO.c_isbn = B.isbn"
        )
    cursor.execute(outerQuery, queryList)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print(formatLeft.format("User of ID: {id} has no checkouts".format(id=userID)))
    else:
        for (due_date, title) in rows:
            print(formatLeft.format("{tit} due date is {due}".format(tit=title, due=due_date)))
            
    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")   

"""
    Name: optionEIGHT()
    Description: Handles functionality for option eight
    Params: None
    Scope: Public 
    Summary: Search for a book using different criteria
"""  
def optionEIGHT():
    # Come back and tidy. Also, comment
    queryList = []
    outerQuery = ("")
    # Used if user is looking up by date
    temp = None
    print("-" * displayLength)
    print(formatCenter.format('**** Search for book ****'))
    print(formatLeft.format("1) Search by title"))
    print(formatLeft.format("2) Search by author"))
    print(formatLeft.format("3) Search by date (year)"))
    while True:
        try:
            menuChoice = int(getpass(prompt=formatLeft.format("Please enter an option: ")))
        except ValueError as err:
            print(formatLeft.format("Oops! That was not a valid number. Please try again..."))
            continue
        
        if (menuChoice < 1 or menuChoice > 3):
            print("Invalid option. Please try again...")
        else:
            break

    if (menuChoice == 1):
        temp = getpass(prompt=formatLeft.format("Please enter the title of the book you are looking for: "))
        queryList.append(temp)
        outerQuery = (
                    "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location, B.pub_date "
                    "FROM books AS B, authors AS A "
                    "WHERE B.baid = A.aid and %s = B.title and B.stock > 0"
                    )
    elif (menuChoice == 2):
        temp = getpass(prompt=formatLeft.format("Please enter the author of the book of which you are looking for: "))
        queryList.append(temp.split(' ')[0])
        queryList.append(temp.split(' ')[1])
        outerQuery = (
                    "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location, B.pub_date "
                    "FROM books AS B, authors AS A "
                    "WHERE B.baid = A.aid and %s = A.afname and %s = A.alname and B.stock > 0"
                    )
    elif (menuChoice == 3):
        temp = getpass(prompt=formatLeft.format("Please enter the publication date of the book of which you are looking for: "))
        queryList.append(temp)
        print(formatLeft.format("1) Greater than {date}".format(date=queryList[0])))
        print(formatLeft.format("2) Less than {date}".format(date=queryList[0])))
        while True:
            try:
                menuChoice = int(getpass(formatLeft.format("Please enter an option: ")))
            except ValueError as err:
                print(formatLeft.format("Oops! That was not a valid number. Please try again..."))
                continue
            
            if (menuChoice < 1 or menuChoice > 2):
                print(formatLeft.format("Invalid option. Please try again..."))
            else:
                break
        if (menuChoice == 1):
            outerQuery = (
                        "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location, B.pub_date "
                        "FROM books AS B, authors AS A "
                        "WHERE B.baid = A.aid and B.pub_date >= %s and B.stock > 0"
                        )
        elif (menuChoice == 2):
            outerQuery = (
                        "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location, B.pub_date "
                        "FROM books AS B, authors AS A "
                        "WHERE B.baid = A.aid and B.pub_date < %s and B.stock > 0"
                        )
            
    cursor.execute(outerQuery, queryList)
    rows = cursor.fetchall()
    
    print(formatLeft.format(" "))
    print(formatCenter.format("**** Book Information ****"))
    if (len(rows) == 0):
        print(formatLeft.format("We could not find the book you were looking for"))
    elif (len(rows) == 1):
        print(formatLeft.format("Title: {tit}".format(tit=rows[0][0])))
        print(formatLeft.format("Author name: {ln}, {fn}".format(ln=rows[0][2], fn=rows[0][1])))
        print(formatLeft.format("ISBN: {id}".format(id=rows[0][3])))
        print(formatLeft.format("Publication date: {date}".format(date=rows[0][6])))
        print(formatLeft.format("Book stock: {stock}".format(stock=rows[0][4])))
        print(formatLeft.format("Book location: {loc}".format(loc=rows[0][5])))
        print(formatLeft.format(" "))
    else:
        for (title, fname, lname, isbn, stock, location, pub_date) in rows:
            print(formatLeft.format("Title: {tit}".format(tit=title)))
            print(formatLeft.format("Author name: {ln}, {fn}".format(ln=lname, fn=fname)))
            print(formatLeft.format("ISBN: {id}".format(id=isbn)))
            print(formatLeft.format("Publication date: {date}".format(date=pub_date)))
            print(formatLeft.format("Book stock: {stock}".format(stock=stock)))
            print(formatLeft.format("Book location: {loc}".format(loc=location)))
            print(formatLeft.format(" "))
            
        
    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionNINE()
    Description: Handles functionality for option nine
    Params: None
    Scope: Public 
    Summary: Using userID and ISBN, allows user to check out a book by adding tuple from checkout table
"""  
def optionNINE():
    pass

"""
    Name: optionTEN()
    Description: Handles functionality for option ten
    Params: None
    Scope: Public 
    Summary: Using userID and ISBN, allows user to return a book by deleting tuple from checkout table
"""  
def optionTEN():
    pass

"""
    Name: optionELEVEN()
    Description: Handles functionality for option eleven
    Params: None
    Scope: Public 
    Summary: Using userID and roomNumber, allows user to reserve a room that is not reserved
"""  
def optionELEVEN():
    pass

"""
    Name: optionTWELVE()
    Description: Handles functionality for option twelve
    Params: None
    Scope: Public 
    Summary: Using userID and roomNumber, allows user to end a reservation
"""  
def optionTWELVE():
    pass

"""
    Name: optionTHIRTEEN()
    Description: Handles functionality for option thirteen
    Params: None
    Scope: Public 
    Summary: Using userID and roomNumber, allows user to reserve a room if the room is not reserved
"""  
def optionTHIRTEEN():
    print("-" * displayLength)
    print(formatCenter.format('**** Adding user ****'))
    firstname = getpass(prompt=formatLeft.format("Enter first name: "))
    lastname = getpass(prompt=formatLeft.format("Enter last name: "))
    phoneNUM = int(getpass(prompt=formatLeft.format("Enter phone number: ")))

    #SQL insertion of fname, lname and phone number
    add_user = ("INSERT INTO users "
               "(fname, lname, phone) "
               "VALUES (%s, %s, %s)")
    data_user = (firstname, lastname , phoneNUM)

    # Insert new user
    cursor.execute(add_user, data_user)
    uid = cursor.lastrowid #used for auto increment column
     # Make sure data is committed to the database
    cnx.commit()
    
    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionFOURTEEN()
    Description: Handles functionality for option fourteen
    Params: None
    Scope: Public 
    Summary: Allows user to delete another user by entering uid
"""  
def optionFOURTEEN():
    queryList = []
    print("-" * displayLength)
    print(formatCenter.format('**** Deleting user ****'))
    uid = int(getpass(prompt=formatLeft.format("Enter userID: ")))
    queryList.append(uid)
    
    delete_user = (
                "DELETE FROM users "
                "WHERE uid = %s "
                )
    # delete user
    cursor.execute(delete_user, queryList)
    #cnx.commit()
    
    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionFIFTEEN()
    Description: Handles functionality for option fifteen
    Params: None
    Scope: Public 
    Summary: Prints a list of all users
"""  
def optionFIFTEEN():
    print("-" * displayLength)
    print(formatCenter.format('**** List of users ****'))

    #**SQL QUERY of the list of users**
    outerQuery = ("SELECT * "
                  "FROM users")
    cursor.execute(outerQuery)
    rows = cursor.fetchall()

    # Check to see if there are no returned rows
    if (len(rows) == 0):
        print(formatLeft.format("There are no users"))
    else:
        # Print out all users
        for (uid, fname, lname, phone) in rows:
            print(formatLeft.format("User ID: {id}, Name: {first} {last}, Phone Number: {phonenumber}".format(id=uid, first=fname, last=lname, phonenumber=phone)))

    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionSIXTEEN()
    Description: Handles functionality for option sixteen
    Params: None
    Scope: Public 
    Summary: Allows user to add a new book into the library
"""  
def optionSIXTEEN():
    pass

"""
    Name: optionSEVENTEEN()
    Description: Handles functionality for option seventeen
    Params: None
    Scope: Public 
    Summary: Allows user to remove all books from the library given an isbn
"""  
def optionSEVENTEEN():
    pass

"""
    Name: optionEIGHTTEEN()
    Description: Handles functionality for option eightteen
    Params: None
    Scope: Public 
    Summary: Prints a list of all available books in the library
"""  
def optionEIGHTTEEN():
    pass

def optionQUIT():
    clearConsole()
    if connecting:
        cursor.close()
        cnx.close()
    print('Quiting program...')
    print('Thanks for using Forbidden Cucumber Knowledge software! Good bye!')
    exit()

# Handles input by assigning options to functions
# Must define the functions before this
input_handler = {
    1 : optionONE,
    2 : optionTWO,
    3 : optionTHREE,
    4 : optionFOUR,
    5 : optionFIVE,
    6 : optionSIX, 
    7 : optionSEVEN,
    8 : optionEIGHT,
    9 : optionNINE,
    10: optionTEN,
    11 : optionELEVEN,
    12 : optionTWELVE,
    13 : optionTHIRTEEN,
    14 : optionFOURTEEN,
    15 : optionFIFTEEN,
    16 : optionSIXTEEN,
    17 : optionSEVENTEEN,
    18 : optionEIGHTTEEN,
    19 : optionQUIT
}

if __name__ == "__main__":
    clearConsole()
    while True:
        # clearConsole() 
        # Useful documenation about Python string formatting: https://docs.python.org/3/library/string.html and https://www.w3schools.com/python/ref_string_format.asp
        # TODO: Reorganize the options to make sense, all the queries with queries, all additions with additions, etc...
        print("-" * displayLength)
        print(formatCenter.format("**** Library Menu ****"))
        print(formatLeft.format("1) Check if a particular computer is available"))
        print(formatLeft.format("2) See the list of available computers"))
        print(formatLeft.format("3) See available apps on computers"))
        print(formatLeft.format("4) Check if a particular room is available"))
        print(formatLeft.format("5) See the list of available rooms"))
        print(formatLeft.format("6) Check if a book is in stock"))
        print(formatLeft.format("7) Check when book is due"))
        print(formatLeft.format("8) Search for book"))
        print(formatLeft.format("9) Checkout book"))
        print(formatLeft.format("10) Return book"))
        print(formatLeft.format("11) Reserve room"))
        print(formatLeft.format("12) End room reservation"))
        print("-" * displayLength)
        print(formatCenter.format("**** Manipulating users table ****"))
        print(formatLeft.format("13) Add user"))
        print(formatLeft.format("14) Delete user"))
        print(formatLeft.format("15) Print user list"))
        print("-" * displayLength)
        print(formatCenter.format("**** Manipulating books table ****"))
        print(formatLeft.format("16) Add book"))
        print(formatLeft.format("17) Delete book"))
        print(formatLeft.format("18) Print all available books"))
        print(formatLeft.format("19) Quit"))
        print("-" * displayLength)

        # Error handling
        while True:
            try:
                menuChoice = int(input("Please enter an option: "))
            except ValueError as err:
                print("Oops! That was not a valid number. Please try again...")
                continue
            if (menuChoice < 1 or menuChoice > 13):
                print("Invalid option. Please try again...")
            else:
                break

        # Handles user input by calling appropriate function
        input_handler[menuChoice]()