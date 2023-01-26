import mysql.connector

_db_conn = mysql.connector.connect(
    host="localhost",
    user="etarious",
    password="password",
    database="note_taking"
)

cursor = _db_conn.cursor()

def createUsersTable():
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS `users`(
                `id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                `fullname` VARCHAR(300) NOT NULL,
                `email` VARCHAR(300) UNIQUE NOT NULL,
                `username` VARCHAR(300) UNIQUE NOT NULL,
                `password` VARCHAR(300) NOT NULL,
                `gender` VARCHAR(7) NOT NULL,
                `date_created` TIMESTAMP
            )
         """)

def createNotesTable():
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS `notes`(
                `id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                `author_id` INT NOT NULL,
                `note_title` LONGTEXT NOT NULL,
                `note_content` LONGTEXT NOT NULL,
                `date_created` TIMESTAMP
            )
         """)


def checkIfUserExists(username, password):
    cursor.execute("SELECT * FROM `users` WHERE `username` = '"+ username + "' AND `password` ='" +password + "' LIMIT 1")
    for result in cursor:
        if result is not None:
            return result
        else:
            return None


def checkIfUsernameIsTaken(username):
    cursor.execute("SELECT * FROM `users` WHERE `username` = '" + username + "' LIMIT 1")
    for result in cursor:
        if result != None:
            return result
        else:
            return None


def registerUser():
    errors = []
    fullname = input("Enter your fullname: ").strip()
    email = input("Enter your email address: ").strip()
    gender = input("Enter 'male', 'female' or 'others': ").strip()
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    password_confirmation = input('Enter password again: ').strip()

    if len(fullname) == 0:
        errors.append("You did not enter your full name")

    if len(email) == 0:
        errors.append("You did not enter email")

    if len(gender) == 0:
        errors.append("You did not enter gender")

    if gender != 'male' and gender != 'female' and gender != 'others':
        errors.append("Enter 'male', 'female' or 'others' for gender")

    if len(username) == 0:
        errors.append("You did not enter username: ")
    
    if len(password) == 0:
        errors.append("You did not enter password")
    
    if len(password_confirmation) == 0:
        errors.append("You did not enter password confirmation")
    
    if password != password_confirmation:
        errors.append("Password and Password confirmation must match!")

    if len(errors) == 0:
        # there are no errors
        # It's tim eot check if the username already exists before you register...
        # print("No errors")
        result = checkIfUsernameIsTaken(username)

        # cursor.execute("SHOW TABLES")
        # for tb in cursor:
        #     print(tb)
        if result == None:
            # The username has not been taken, register the user...
            cursor.execute("INSERT INTO `users` (`fullname`, `email`, `gender`, `username`, `password`) VALUES ('" + fullname + "', '" + email + "', '" + gender + "', '" + username + "', '" + password + "')")
            # print("Registered Successfully!")
            print(cursor)
            # for res in cursor:
            #     if res != None:
            #         return res
            #     else:
            #         return None
    else:
        # there are errors
        for err in errors:
            print(err)

        # registerUser()
        # print(gender != 'male')

def loginUser():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    result = checkIfUserExists(username, password) 
    return result