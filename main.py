import sqlite3
import os

ADMIN_PASS = 'password4321' #super duper hard password
DB_NAME = 'userdb'

def menu():
    print("****************************************")
    print("*       WELCOME TO YOUR DATABASE       *")
    print("****************************************")
    print("* Choose from the following commands:  *")
    print("*                                      *")
    print("* Add = Adds file to database          *")
    print("* Open = Opens file from database      *")
    print("* Delete = Deletes file from database  *")
    print("* QUIT = Quits the program             *")
    print("****************************************")


def createTable(csr, database):
    csr.execute(
        '''
            CREATE TABLE files
                            (
                            id INTEGER PRIMARY KEY,
                            file_name TEXT,
                            file_type TEXT,
                            file_password TEXT,
                            file_directory TEXT
                            )
        '''
    )
    database.commit()
    print("Database has been created")


def addFile(fileName, fileType, filePassword, fileDir, csr, db):
    csr.execute(
        '''
            INSERT INTO files (file_name, file_type, file_password, file_directory)
            VALUES (?,?,?,?)
        ''',(fileName, fileType, filePassword, fileDir)
    )
    db.commit()

def openFile(fileName, csr):
        csr.execute(
            '''
                SELECT file_directory
                FROM files
                WHERE file_name=?
            ''',(fileName,)
        )
        file = csr.fetchone()
        print("File that is opening: " + file[0] + "\n")
        fd = os.open( file[0], os.O_RDONLY )
        print(os.read(fd, 1024))

userEnteredPassword = input("Password: ")

while userEnteredPassword != ADMIN_PASS:
    print("Password was entered incorrectly, please retry.\n")
    userEnteredPassword = input("Password: ")

db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

try:
    cursor.execute(''' SELECT id FROM files ''')

except:
    createTable(cursor, db)

menu()

userInput = input("")

while userInput != "QUIT":
    if userInput == "Add":
        fileName = input("Enter the file name: ")
        fileType = input("Enter the file type: ")
        filePassword = input("Enter the file password: ")
        fileDirectory = input("Enter the file directory: ")
        addFile(fileName, fileType, filePassword, fileDirectory, cursor, db)
        menu()
        userInput = input("")

    elif userInput == "Open":
        fileName = input("Enter file name: ")
        openFile(fileName, cursor)
        menu()
        userInput = input("")
db.close()
