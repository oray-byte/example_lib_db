# MySQL API
# MySQL API Documentation: https://dev.mysql.com/doc/connector-python/en/
from getpass import getpass
from typing import List, Tuple, TypedDict
from datetime import datetime, timedelta
from datetime import date
import mysql.connector
import mysql.connector.cursor
import os
import json


# Debugging purposes
connecting = True

# Current date
todayDate = datetime(date.today().year, date.today().month, date.today().day)

# For formatting output
displayLength = 80
formatCenter = "| {:^76} |"
formatLeft = "| {:<76} |"

# For database connection
cnx: mysql.connector = None

def databaseConnection() -> mysql.connector:
    userInput: str = ""
    pathToConfig: str = os.path.join(os.getcwd(), "config.json")
    user: str = ""
    password: str = ""
    host: str = ""
    database: str = ""
    
    if (os.path.exists(pathToConfig)):
        while True:
            userInput = input("Would you like to use your saved login info (y/n): ")
            if (userInput.lower() == "y"):
                with open("config.json", "r") as openfile:
                    jsonObject = json.load(openfile)
                    user = jsonObject["username"]
                    password = jsonObject["password"]
                    host = jsonObject["host"]
                    database = jsonObject["database"]
                    return mysql.connector.connect(user=user, password=password, host=host, database=database)
            elif (userInput.lower() == "n"):
                break
            else:
                print("Please enter valid response")
                continue
    
    user = input("Enter username: ")
    password = getpass("Enter password: ")
    host = input("Enter host: ")
    database = input("Enter database: ")
    
    while True: 
        userInput = input("Would you like to save your login information (y/n): ")
        print(userInput.lower())
        if (userInput.lower() == "y"):
            jsonData = {
                "username": user,
                "password": password,
                "host": host,
                "database": database
            }
            jsonObject = json.dumps(jsonData, indent=4)
            with open("config.json", "w") as outfile:
                outfile.write(jsonObject)
            break
        elif (userInput.lower() == "n"):
            break
        else:
            print("Please enter valid response")
            continue
            
    return mysql.connector.connect(user=user, password=password, host=host, database=database)

print("Connecting to database...\n")

# Method to connect to MySQL server
# See https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html for list of arguements
if connecting:
    cnx = databaseConnection()
    cursor: mysql.connector.cursor = cnx.cursor()

# curser() instantiates objects that can execute operations such as SQL statements. Interacts with MySQL server through MySQLConnection object
# Visit https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html for full documentation
    
# Clears console
def clearConsole() -> None:
    if (os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")

# Handles stock when a user is deleted and room reservation
def onUserDelete(id: int) -> None:
    bookQuery: str = ""
    clearDeletion: str = ""
    rows: List[Tuple[str]] = []
    outstandingBooks: TypedDict[str, int] = {}
    
    bookQuery = (
                "SELECT B.isbn, B.stock "
                "FROM users AS U, checkout AS CO, books as B "
                "WHERE U.uid = CO.c_uid and U.uid = %s and CO.c_isbn = B.isbn"%(id)
                )

    cursor.execute(bookQuery)
    rows = cursor.fetchall()
    
    for (isbn, stock) in rows:
        outstandingBooks[isbn] = stock
        
    for isbn in outstandingBooks:
        clearDeletion = (
                        "UPDATE books "
                        "SET stock = %s "
                        "WHERE isbn = %s"%((outstandingBooks[isbn] + 1), isbn)
                        )
        cursor.execute(clearDeletion)

# Error handling for input involving integer ids
def getID(type: str) -> int:
    userID: int = -1
    while True:
        try:
            userID = int(getpass(prompt=(formatLeft.format("Enter {type}: ".format(type=type)))))
        except ValueError as err:
            print(formatLeft.format("Oops! That was not a valid number. Please try again..."))
            continue
        if (type == "phone number"):
            if (userID < 1000000000 or userID > 9999999999):
                print(formatLeft.format("Please enter a valid phone number"))
                continue
        break
                      
    return userID

# Handles getting input for a menu and handles errors
def getMenuChoice(minChoice: int, maxChoice: int) -> int:
    menuChoice: int = -1
    while True:
        try:
            menuChoice = int(input("Please enter an option: "))
        except ValueError as err:
            print("Oops! That was not a valid number. Please try again...")
            continue
        if (menuChoice < minChoice or menuChoice > maxChoice):
            print("Invalid option. Please try again...")
        else:
            break
    return menuChoice

# Quick method I threw together to check errors for integer input (makes sure they can be casted to ints)
def getIntInput(sentence: str) -> int:
    input: int = -1
    while True:
        try:
            input = int(getpass(prompt=(formatLeft.format(sentence.format(type=type)))))
        except ValueError as err:
            print(formatLeft.format("Oops! That was not a valid number. Please try again..."))
            continue
        break
    return input

# Simple function that handles printing back to our "main menu." Duplicate code
def printToMenu() -> None:
    print(formatLeft.format(" "))
    input(formatLeft.format("Press 'enter' to go back to menu"))
    print(("-" * displayLength) + "\n")

"""
    Name: optionONE()
    Description: Handles functionality for option one
    Params: None
    Scope: Public 
    Summary: Search a computer with its commputerID and print if it is available or not
"""
def optionONE() -> None:
    # Variables used in this method
    computerID: int = -1
    computerQuery: str = ""
    rows: List[Tuple[str]] = []
    
    print("-" * displayLength)
    print(formatCenter.format("**** Check if particular computer is available ****"))
    print(formatLeft.format("To check if a computer is available, please the computer's ID"))
    
    # Get computer ID and make sure it 
    computerID = getID("computer ID") # It isn't a user ID but same logic
    
    print(formatLeft.format("Searching for computer of ID: " + str(computerID)))
    
    # SQL query: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
    # Return all of the available computers
    computerQuery = ("SELECT C.comp_id, C.comp_loc "
                  "FROM computers AS C "
                  "WHERE C.comp_id NOT IN (SELECT CU.c_comp_id FROM computeruse AS CU)")
    cursor.execute(computerQuery)
    rows = cursor.fetchall()
    
    # Check list of all available computers to see if specific computer is available
    for (comp_id, comp_loc) in rows:
        if comp_id == computerID:
            print(formatLeft.format("Computer {id} is available on the {floor}".format(id=computerID, floor=comp_loc)))
            printToMenu()
            return
    
    print(formatLeft.format("Computer {id} is unavailable.".format(id=computerID)))        
    printToMenu()

"""
    Name: optionTWO()
    Description: Handles functionality for option two
    Params: None
    Scope: Public 
    Summary: Print a list of all available computers in the library
"""  
def optionTWO() -> None:
    # Variables used in this method
    computerQuery: str = ""
    rows: List[Tuple[str]] = []
    
    print("-" * displayLength)
    print(formatCenter.format('**** List of available computers ****'))

    #**SQL QUERY of the list of available computers, show computerID and location**
    computerQuery = ("SELECT C.comp_id, C.comp_loc "
                "FROM computers AS C "
                "WHERE C.comp_id NOT IN (SELECT CU.c_comp_id FROM computeruse AS CU)")
    cursor.execute(computerQuery)
    rows = cursor.fetchall()
    
    # Check to see if there are no returned rows
    if (len(rows) == 0):
        print(formatLeft.format("There are no available computers"))
    else:
        # Print out all available computers
        for (comp_id, comp_loc) in rows:
            print(formatLeft.format("Computer {id} is available on floor {floor}".format(id=comp_id, floor=comp_loc)))


    printToMenu()

"""
    Name: optionTHREE()
    Description: Handles functionality for option three
    Params: None
    Scope: Public 
    Summary: Print a list of all available apps on computers
"""  
def optionTHREE() -> None:
    # Variables used in this method
    appQuery: str = ""
    rows: List[Tuple[str]] = []
    
    print("-" * displayLength)
    print(formatCenter.format('**** See all available computer apps****'))

    #SQL query show list of available apps from all computers.
    appQuery = (
                "SELECT * "
                "FROM apps"
                )
    cursor.execute(appQuery)
    rows = cursor.fetchall()

    # Print out all available apps
    for (_aid, app_name) in rows: # Weird bug where we HAD to include app id to print properly
        print(formatLeft.format("Application name: {app}".format(app=app_name)))

    printToMenu()

"""
    Name: optionFOUR()
    Description: Handles functionality for option four
    Params: None
    Scope: Public 
    Summary:Search a room with its roomNumber and print if it is available or not
"""  
def optionFOUR() -> None:
    # Variables used in this method
    roomNumber: int = -1
    roomQuery: str = ""
    rows: List[Tuple[str]] = []
    
    print("-" * displayLength)
    print(formatCenter.format('**** Checking if a particular room is available ****'))
    print(formatLeft.format('To check if a room is available, please enter room number.'))
    roomNumber = getID("room number")
    
    #SQL query of room number and room floor
    roomQuery = ("SELECT R.room_num, R.floor "
                  "FROM rooms AS R "
                  "WHERE R.room_num NOT IN (SELECT RU.r_room_num FROM roomuse AS RU)")
    cursor.execute(roomQuery)
    rows = cursor.fetchall()
    
    for (room_num, floor) in rows:
        if (room_num == roomNumber):
            print(formatLeft.format("Room {id} is available on floor {num}".format(id=room_num, num=floor)))
            printToMenu()
            return
    
    print(formatLeft.format("Room {id} is unavailable.".format(id=roomNumber)))        
    printToMenu()

"""
    Name: optionFIVE()
    Description: Handles functionality for option five
    Params: None
    Scope: Public 
    Summary: Print a list of all available roosm in the library
"""  
def optionFIVE() -> None:
    # Variables used in this method
    roomQuery: str = ""
    rows: List[Tuple[str]] = []
    
    print("-" * displayLength)
    print(formatCenter.format('**** List of available rooms ****'))
    
    #SQL query showing the LIST of available rooms, show its room number and floor
    roomQuery = (
                "SELECT R.room_num, R.floor "
                "FROM rooms AS R "
                "WHERE R.room_num NOT IN (SELECT RU.r_room_num FROM roomuse AS RU)"
                )
    cursor.execute(roomQuery)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print("There are no available rooms")
    else:
        for (room_num, floor) in rows:
            print(formatLeft.format("Room {id} is available on floor {num}".format(id=room_num, num=floor)))
    
    printToMenu()

"""
    Name: optionSIX()
    Description: Handles functionality for option six
    Params: None
    Scope: Public 
    Summary: Checks to see if a book is in stock
"""  
def optionSIX() -> None:
    bookISBN: str = ""
    bookQuery: str = ""
    rows: List[Tuple[str]] = []
    
    print("-" * displayLength)
    print(formatCenter.format('**** Checking if book is in stock ****'))
    print(formatLeft.format('To check if a book is in stock, please enter book ISBN(13-digit)'))
    
    # TODO: Come back and redo this input check. Check constraints for ISBN
    while True:
        try:
            bookISBN = (getpass(prompt=(formatLeft.format("Enter book ISBN(13-digit): "))))
        except ValueError as err:
            print(formatLeft.format("Oops! That was not a valid number. Please try again..."))
            continue
        break
    print(formatLeft.format("Checking to see if a book with ISBN " + bookISBN + " exists..."))
    print(formatLeft.format(" "))

    #SQL query show book-ISBN, booktitle, book-author, book-quantityinstock, book-location
    bookQuery = (
            "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location "
            "FROM books AS B, authors AS A "
            "WHERE B.baid = A.aid and %s = B.isbn and B.stock > 0"%(bookISBN)
            )
    
    cursor.execute(bookQuery)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print(formatLeft.format("We could not find a book with ISBN: {id} that's in stock".format(id=bookISBN)))
    else:
        print(formatCenter.format("**** Book Information ****"))
        print(formatLeft.format("Title: {tit}".format(tit=rows[0][0])))
        print(formatLeft.format("Author name: {name}".format(name=(rows[0][2] + ", " + rows[0][1]))))
        print(formatLeft.format("ISBN: {id}".format(id=rows[0][3])))
        print(formatLeft.format("Book stock: {stock}".format(stock=rows[0][4])))
        print(formatLeft.format("Book location: {loc}".format(loc=rows[0][5])))
        
    
    printToMenu()

"""
    Name: optionSEVEN()
    Description: Handles functionality for option seven
    Params: None
    Scope: Public 
    Summary: Using userID, checks to see when each checked out book is due
"""  
def optionSEVEN() -> None:
    # Variables used in this method
    userID: int = -1
    bookQuery: str = ""
    rows: List[Tuple[str]] = []
    date: datetime = None
    daysDifference: int = -1
    
    print("-" * displayLength)
    print(formatCenter.format('**** Checking if book is due ****'))
    print(formatLeft.format('To check if a book is due, please enter in userID.'))
    userID = getID("user ID")
    
    bookQuery = (
        "SELECT CO.due_date, B.title "
        "FROM users AS U, checkout AS CO, books as B "
        "WHERE U.uid = CO.c_uid and U.uid = %s and CO.c_isbn = B.isbn"%(userID)
        )
    cursor.execute(bookQuery)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print(formatLeft.format("User of ID: {id} has no checkouts".format(id=userID)))
    else:
        for (due_date, title) in rows:
            date = datetime(due_date.year, due_date.month, due_date.day)
            daysDifference = (date - todayDate).days
            date = date.strftime("%m/%d/%Y")
            
            if (daysDifference > 0):
                print(formatLeft.format("{tit} due date is {due}".format(tit=title, due=date)))
            else:
                print(formatLeft.format("{tit} was due {num} days ago".format(tit=title, num=abs(daysDifference))))
            
    printToMenu() 

"""
    Name: optionEIGHT()
    Description: Handles functionality for option eight
    Params: None
    Scope: Public 
    Summary: Search for a book using different criteria
"""  
def optionEIGHT() -> None:
    # Come back and tidy. Also, comment
    outerQuery = ("")
    # Used if user is looking up by date
    temp = None
    print("-" * displayLength)
    print(formatCenter.format('**** Search for book ****'))
    print(formatLeft.format("1) Search by title"))
    print(formatLeft.format("2) Search by author"))
    print(formatLeft.format("3) Search by date (year)"))
    menuChoice = getMenuChoice(1, 3)

    if (menuChoice == 1):
        temp = getpass(prompt=formatLeft.format("Please enter the title of the book you are looking for: "))
        outerQuery = (
                    "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location, B.pub_date "
                    "FROM books AS B, authors AS A "
                    "WHERE B.baid = A.aid and %s = B.title and B.stock > 0"%(temp)
                    )
    elif (menuChoice == 2):
        temp = getpass(prompt=formatLeft.format("Please enter the author of the book of which you are looking for: "))
        outerQuery = (
                    "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location, B.pub_date "
                    "FROM books AS B, authors AS A "
                    "WHERE B.baid = A.aid and %s = A.afname and %s = A.alname and B.stock > 0"%(temp.split(' ')[0], temp.split(' ')[1])
                    )
    elif (menuChoice == 3):
        temp = getIntInput("Please enter the publication date of the book of which you are looking for: ")
        print(formatLeft.format("1) Greater than {date}".format(date=temp)))
        print(formatLeft.format("2) Less than {date}".format(date=temp)))
        menuChoice = getMenuChoice(1, 2)
        if (menuChoice == 1):
            outerQuery = (
                        "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location, B.pub_date "
                        "FROM books AS B, authors AS A "
                        "WHERE B.baid = A.aid and B.pub_date >= %s and B.stock > 0"%(temp)
                        )
        elif (menuChoice == 2):
            outerQuery = (
                        "SELECT B.title, A.afname, A.alname, B.isbn, B.stock, B.location, B.pub_date "
                        "FROM books AS B, authors AS A "
                        "WHERE B.baid = A.aid and B.pub_date < %s and B.stock > 0"%(temp)
                        )
            
    cursor.execute(outerQuery)
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
            
        
    printToMenu()

"""
    Name: optionNINE()
    Description: Handles functionality for option nine
    Params: None
    Scope: Public 
    Summary: Using userID and ISBN, allows user to check out a book by adding tuple from checkout table
"""  
def optionNINE() -> None:
    # Variables used in this method
    rows: List[Tuple[str]] = []
    bookQuery: str = ""
    checkoutInsertion: str = ""
    bookISBN: str = ""
    userID: int = -1
    bookStock: int = -1
    checkoutUpdate: str = ""
    dueDate = None
    date: datetime = None
    
    print("-" * displayLength)
    print(formatCenter.format("**** Checkout book ****"))
    while len(bookISBN) != 13:
        bookISBN = getpass(prompt=formatLeft.format("Please enter the ISBN of the book you are wishing to check out: "))
    
    bookQuery = (
                "SELECT B.isbn, B.stock "
                "FROM books as B "
                "WHERE B.isbn = %s and B.stock > 0"%(bookISBN)
                )
    cursor.execute(bookQuery)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print(formatLeft.format("There is no book with ISBN {id}".format(id=bookISBN)))
        printToMenu()
        return
    
    bookStock = rows[0][1] - 1
    dueDate = (todayDate + timedelta(days=14))
    date = datetime(dueDate.year, dueDate.month, dueDate.day)
    # date = date.strftime("%Y-%m-%d")
    userID = getID("user ID")
    
    checkoutInsertion = (
                        "INSERT INTO checkout "
                        "VALUES (%s, %s, '%s')"%(userID, bookISBN, dueDate)
                        )
    try:
        cursor.execute(checkoutInsertion)
        cnx.commit()
    except mysql.connector.errors.IntegrityError as err:
        print(formatLeft.format("You already have the book of ISBN {id} checked out".format(id=bookISBN)))
        printToMenu()
        return

    checkoutUpdate = (
                     "UPDATE books "
                     "SET stock = %s "
                     "WHERE isbn = %s"%(bookStock, bookISBN)
                     )
    
    cursor.execute(checkoutUpdate)
    cnx.commit()
    
    printToMenu()
    

"""
    Name: optionTEN()
    Description: Handles functionality for option ten
    Params: None
    Scope: Public 
    Summary: Using userID and ISBN, allows user to return a book by deleting tuple from checkout table
"""  
def optionTEN() -> None:
    # Variables used in this method
    rows: List[Tuple[str]] = []
    checkedOutBooks: List[str] = {}
    checkoutQuery: str = ""
    checkoutDeletion: str = ""
    bookISBN: str = ""
    userID: int = -1
    returnUpdate: str = ""
    bookStock: int = -1
    date: datetime = None
    
    print("-" * 60)
    print(formatCenter.format("**** Return book ****"))
    print(formatLeft.format("To return a book, please enter your ID to see list of outstanding checkouts"))
    userID = getID("user ID")
    checkoutQuery = (
                "SELECT B.title, A.afname, A.alname, B.isbn, B.pub_date, CO.due_date, B.stock "
                "FROM checkout as CO, books as B, authors as A "
                "WHERE CO.c_uid = %s and CO.c_isbn = B.isbn and B.baid = A.aid"%(userID)
                )
    cursor.execute(checkoutQuery)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print(formatLeft.format("You do no have any outstanding checkouts"))
        printToMenu()
        return
    
    print(formatLeft.format(" "))
    print(formatCenter.format("**** Checked out books ****"))
    for (title, fname, lname, isbn, pub_date, due_date, stock) in rows:
            # Format due_date
            date = datetime(due_date.year, due_date.month, due_date.day).strftime("%m/%d/%Y")
            print(formatLeft.format("Title: {tit}".format(tit=title)))
            print(formatLeft.format("Author name: {ln}, {fn}".format(ln=lname, fn=fname)))
            print(formatLeft.format("ISBN: {id}".format(id=isbn)))
            print(formatLeft.format("Publication date: {date}".format(date=pub_date)))
            print(formatLeft.format("Due date: {ddate}".format(ddate=date)))
            print(formatLeft.format(" "))
            checkedOutBooks[isbn] = stock
            
    while bookISBN not in checkedOutBooks:
        bookISBN = getpass(prompt=formatLeft.format("Please enter the ISBN of the book you are wishing to return: "))
    
    bookStock = checkedOutBooks[bookISBN] + 1
    checkoutDeletion = (
                        "DELETE FROM checkout "
                        "WHERE c_uid = %s and c_isbn = %s"%(userID, bookISBN)
                       )
    
    cursor.execute(checkoutDeletion)
    cnx.commit()
    
    returnUpdate = (
                   "UPDATE books "
                   "SET stock = %s "
                   "WHERE isbn = %s"%(bookStock, bookISBN)
                   )
    cursor.execute(returnUpdate)
    cnx.commit()
    
    printToMenu()
    

"""
    Name: optionELEVEN()
    Description: Handles functionality for option eleven
    Params: None
    Scope: Public 
    Summary: Using userID and roomNumber, allows user to reserve a room that is not reserved
"""  
def optionELEVEN() -> None:
    # Variables used in this method
    roomNumber: int = -1
    roomQuery: str = ""
    userID: int = -1
    roomInsertion: str = ""
    
    print("-" * displayLength)
    print(formatCenter.format("**** Reserve room ****"))
    print(formatLeft.format("To reserve a room, you must provide the room number"))
    roomNumber = getID("room number")
    roomQuery = (
                "SELECT * "
                "FROM roomuse AS RU "
                "WHERE r_room_num = %s"%(roomNumber)
                )
    cursor.execute(roomQuery)
    rows = cursor.fetchall()
    
    if (len(rows) > 0):
        print(formatLeft.format("Room {num} is already reserved, please try a different room".format(num=roomNumber)))
        printToMenu()
        return
    
    print(formatLeft.format("Enter your userID to reserve room {rnum}".format(rnum=roomNumber)))
    userID = getID("user ID")
    
    roomInsertion = (
                    "INSERT INTO roomuse "
                    "VALUES (%s, %s)"%(userID, roomNumber)
                    )
    cursor.execute(roomInsertion)
    cnx.commit()
    
    printToMenu()
    

"""
    Name: optionTWELVE()
    Description: Handles functionality for option twelve
    Params: None
    Scope: Public 
    Summary: Using userID and roomNumber, allows user to end a reservation
"""  
def optionTWELVE() -> None:
    # Variables used in this method
    userID: int = -1
    roomQuery: str = ""
    rows: List[Tuple[str]] = []
    reservedRooms: List[int] = []
    roomNumber: int = -1
    reservationDeletion: str = []
    
    print("-" * displayLength)
    print(formatCenter.format("**** End reservation ****"))
    print(formatLeft.format("Please enter user ID to see currently reserved rooms"))
    userID = getID("user ID")
    
    roomQuery = (
                "SELECT * "
                "FROM roomuse AS RU "
                "WHERE RU.r_uid = %s"%(userID)
                )
    
    cursor.execute(roomQuery)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print(formatLeft.format("You do not have any currently reserved rooms"))
        printToMenu()
        return
    
    print(formatLeft.format(" "))
    print(formatCenter.format("**** Currently reserved rooms ****"))
    for (_r_uid, r_room_num) in rows:
        print(formatLeft.format("Room {num}".format(num=r_room_num)))
        reservedRooms.append(r_room_num)
        
    print(formatLeft.format("Enter the room number of which you would like to cancel your reservation"))
    while roomNumber not in reservedRooms:
        roomNumber = getID("room number")
    
    reservationDeletion = (
                          "DELETE FROM roomuse "
                          "WHERE r_room_num = %s"%(roomNumber)
                          )
    
    cursor.execute(reservationDeletion)
    cnx.commit()
    
    printToMenu()
      
"""
    Name: optionTHIRTEEN()
    Description: Handles functionality for option thirteen
    Params: None
    Scope: Public 
    Summary: Allows user to add another user to library
"""  
def optionTHIRTEEN() -> None:
    phoneNUM: int = -1
    print("-" * displayLength)
    print(formatCenter.format('**** Adding user ****'))
    firstname = getpass(prompt=formatLeft.format("Enter first name: "))
    lastname = getpass(prompt=formatLeft.format("Enter last name: "))
    while (phoneNUM < 1000000000 or phoneNUM > 9999999999):
        phoneNUM = getIntInput("Enter phone number: ")

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
    print(formatLeft.format("The new user's id is {id}".format(id=uid)))
    printToMenu()

"""
    Name: optionFOURTEEN()
    Description: Handles functionality for option fourteen
    Params: None
    Scope: Public 
    Summary: Allows user to delete another user by entering uid
"""  
def optionFOURTEEN() -> None:
    print("-" * displayLength)
    print(formatCenter.format('**** Deleting user ****'))
    uid = int(getpass(prompt=formatLeft.format("Enter userID: ")))
    
    # SQL deletion of a user
    delete_user = (
                "DELETE FROM users "
                "WHERE uid = %s"%(uid)
                )
    # delete user
    onUserDelete(uid)
    cursor.execute(delete_user)
    
    
    printToMenu()

"""
    Name: optionFIFTEEN()
    Description: Handles functionality for option fifteen
    Params: None
    Scope: Public 
    Summary: Prints a list of all users
"""  
def optionFIFTEEN() -> None:
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

    printToMenu()

"""
    Name: optionSIXTEEN()
    Description: Handles functionality for option sixteen
    Params: None
    Scope: Public 
    Summary: Allows user to add a new book into the library
"""  
def optionSIXTEEN() -> None:
    bookISBN: str = ""
    bookTitle: str = ""
    bookAfname: str = ""
    bookAlname: str = ""
    bookPubDate: int = -1
    bookStock: int = -1
    bookLocation: str = -1
    
    print("-" * displayLength)
    print(formatCenter.format('**** Adding book ****'))
    # Maybe add error handler for DB restraints
    while len(bookISBN) != 13:
        bookISBN = getpass(prompt=formatLeft.format("Enter new book ISBN (13-digit): "))
    bookTitle = getpass(prompt=formatLeft.format("Enter new book title: "))
    bookAfname = getpass(prompt=formatLeft.format("Enter new book author FIRST name: "))
    bookAlname = getpass(prompt=formatLeft.format("Enter new book author LAST name: "))
    # Error handling for strings
    bookPubDate = getIntInput("Enter new book publication date (year): ")
    while bookStock < 0:
        bookStock = getIntInput("Enter the amount of quantity of new book: ")
    bookLocation = "Aisle " + str(getIntInput("Enter the new book aisle number : "))
    
     # SQL insertion of author, fname and lname
    add_author = ("INSERT INTO authors "
                 "(afname, alname) "
                 "VALUES (%s, %s)")
    data_author = (bookAfname, bookAlname)

    # Insert new author
    cursor.execute(add_author, data_author)
    aid = cursor.lastrowid #used for auto increment column, adding an author

   
    #SQL insertion book: isbn, pub_date, stock, location, and title
    add_book = ("INSERT INTO books "
               "(isbn, baid, pub_date, stock, location, title) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
    data_book = (bookISBN, aid, bookPubDate , bookStock, bookLocation, bookTitle)

    # Insert new book
    cursor.execute(add_book, data_book)

    
    # Make sure data is committed to the database
    cnx.commit()
    
    printToMenu()

"""
    Name: optionSEVENTEEN()
    Description: Handles functionality for option seventeen
    Params: None
    Scope: Public 
    Summary: Allows user to remove all books from the library given an isbn
"""  
def optionSEVENTEEN() -> None:
    bookISBN: str = ""
    print("-" * displayLength)
    print(formatCenter.format('**** Deleting book ****'))
    while len(bookISBN) != 13:
        bookISBN = getpass(prompt=formatLeft.format("Enter bookISBN: "))
    
    #SQL deletion of a book
    delete_book = (
                "DELETE FROM books "
                "WHERE isbn = %s"%(bookISBN)
                )
    # delete book
    cursor.execute(delete_book)
    
    
    printToMenu()

"""
    Name: optionEIGHTTEEN()
    Description: Handles functionality for option eightteen
    Params: None
    Scope: Public 
    Summary: Prints a list of all available books in the library
"""  
def optionEIGHTTEEN() -> None:
    print("-" * displayLength)
    print(formatCenter.format('**** List of all available books ****'))

    # ** SQL showing all available books
    outerQuery = (
                  "SELECT B.isbn, A.afname, A.alname, B.pub_date, B.stock, B.location, B.title "
                  "FROM books AS B, authors AS A "
                  "WHERE B.stock > 0 and A.aid = B.baid"
                  )
    cursor.execute(outerQuery)
    rows = cursor.fetchall()

    # Check to see if there are no returned rows
    if (len(rows) == 0):
        print(formatLeft.format("There are no available books"))
    else:
        # Print out all available book info
        for (isbn, afname, alname, pub_date, stock, location, title) in rows:
            print(formatLeft.format("ISBN: {ISBN} ".format(ISBN=isbn)))
            print(formatLeft.format("Book Title: {TITLE}".format(TITLE=title)))
            print(formatLeft.format("Author: {Alname}, {Afname}".format(Alname=alname, Afname=afname)))
            print(formatLeft.format("Publication date: {PUB_DATE}".format(PUB_DATE=pub_date)))
            print(formatLeft.format("Stock: {STOCK} ".format(STOCK=stock)))
            print(formatLeft.format("Location: {LOCATION}".format(LOCATION=location)))
            print(formatLeft.format(" "))
    
    printToMenu()

"""
    Name: optionNINETEEN()
    Description: Handles functionality for option nineteen
    Params: None
    Scope: Public 
    Summary: Prompts family member phone number and returns user id
"""  
def optionNINETEEN() -> None:
    print("-" * displayLength)
    print(formatCenter.format('**** Get User ID for family member ****'))
    familyPhone = getID("phone number")
    
    outerQuery = ("SELECT * "
                  "FROM familymembers "
                  "WHERE fam_phone = %s"%(familyPhone))
    cursor.execute(outerQuery)
    rows = cursor.fetchall()

    # Check to see if there are no returned rows
    if (len(rows) == 0):
        print(formatLeft.format("There is no family member with this phone number."))
    else:
        # Print out user id of family member
        for (fam_phone, fam_id) in rows:
            print(formatLeft.format("Your user ID is: {id}".format(id=fam_id)))

    printToMenu()

"""
    Name: optionTWENTY()
    Description: Handles functionality for option twenty
    Params: None
    Scope: Public 
    Summary: Adds family member to library database
"""  
def optionTWENTY() -> None:
    print("-" * displayLength)
    print(formatCenter.format('**** Add family member ****'))
    famPhoneNum = getID("phone number")
    famID = getID("user ID: ")
    
    #Check that user with famID exists"
    check_user = (
                "SELECT uid "
                "FROM users "
                "WHERE uid = %s"%(famID)
                )
    cursor.execute(check_user)
    rows = cursor.fetchall()
    
    if (len(rows) == 0):
        print(formatLeft.format("There is no user with this user ID."))
    else:
        #SQL addition of a family member
        add_familyMember = (
                    "INSERT INTO familymembers "
                    "VALUES (%s, %s)"%(famPhoneNum, famID)
                    )
        # add family member
        cursor.execute(add_familyMember)
        print(formatLeft.format("Family member successfully added."))
    
    printToMenu()

"""
    Name: optionTWENTYONE()
    Description: Handles functionality for option twenty-one
    Params: None
    Scope: Public 
    Summary: Removes family member from library database
"""  
def optionTWENTYONE() -> None:
    print("-" * displayLength)
    print(formatCenter.format('**** Remove family member ****'))
    famPhoneNum = getID("phone number")
    
    #SQL deletion of a family member
    delete_familyMember = (
                "DELETE FROM familymembers "
                "WHERE fam_phone = %s"%(famPhoneNum)
                )
    # delete family member
    cursor.execute(delete_familyMember)
    
    
    printToMenu()


def optionQUIT() -> None:
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
    1  : optionONE,
    2  : optionTWO,
    3  : optionTHREE,
    4  : optionFOUR,
    5  : optionFIVE,
    6  : optionSIX, 
    7  : optionSEVEN,
    8  : optionEIGHT,
    9  : optionNINE,
    10 : optionTEN,
    11 : optionELEVEN,
    12 : optionTWELVE,
    13 : optionTHIRTEEN,
    14 : optionFOURTEEN,
    15 : optionFIFTEEN,
    16 : optionSIXTEEN,
    17 : optionSEVENTEEN,
    18 : optionEIGHTTEEN,
    19 : optionNINETEEN,
    20 : optionTWENTY,
    21 : optionTWENTYONE,
    22 : optionQUIT
}

if __name__ == "__main__":
    # clearConsole()
    while True:
        clearConsole()
        clearConsole()
        # Useful documenation about Python string formatting: https://docs.python.org/3/library/string.html and https://www.w3schools.com/python/ref_string_format.asp
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
        print("-" * displayLength)
        print(formatCenter.format("**** Family Member Access ****"))
        print(formatLeft.format("19) Get User ID"))
        print(formatLeft.format("20) Add Family Member"))
        print(formatLeft.format("21) Remove Family Member"))
        print("-" * displayLength)
        print(formatLeft.format("22) Quit"))
        print("-" * displayLength)

        # Error handling
        menuChoice = getMenuChoice(1, 22)

        # Handles user input by calling appropriate function
        input_handler[menuChoice]()