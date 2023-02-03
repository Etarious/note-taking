import mysql.connector

_db_conn = mysql.connector.connect(
    host="localhost",
    user="etarious",
    password="password",
    database="note_taking"
)

def createUsersTable():
    cursor = _db_conn.cursor()
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
    cursor.close()

def createNotesTable():
    cursor = _db_conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS `notes`(
                `id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                `note_author_id` INT NOT NULL,
                `note_title` LONGTEXT NOT NULL,
                `note_content` LONGTEXT NOT NULL,
                `date_created` TIMESTAMP
            )
         """)
    cursor.close()


def checkIfUserExists(username, password):
    cursor = _db_conn.cursor()
    _db_conn.commit()
    cursor.execute("SELECT * FROM `users` WHERE `username` = '"+ username + "' AND `password` ='" +password + "' LIMIT 1")
    for result in cursor:
        if result is not None:
            cursor.close()
            return result
        else:
            cursor.close()
            return None


def checkIfUsernameIsTaken(username):
    cursor = _db_conn.cursor()
    _db_conn.commit()
    cursor.execute("SELECT * FROM `users` WHERE `username` = '" + username + "' LIMIT 1")
    for result in cursor:
        if result != None:
            cursor.close()
            return True
        else:
            cursor.close()
            return None


def registerUser():
    cursor = _db_conn.cursor()
    errors = []
    fullname = input("Enter your fullname: ").strip()
    email = input("Enter your email address: ").strip()
    gender = input("Enter 'male', 'female' or 'others': ").strip()
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    password_confirmation = input('Enter password again: ').strip()

    if len(fullname) == 0:
        errors.append("\nYou did not enter your full name")

    if len(email) == 0:
        errors.append("\nYou did not enter email")

    if len(gender) == 0:
        errors.append("\nYou did not enter gender")

    if gender != 'male' and gender != 'female' and gender != 'others':
        errors.append("Enter 'male', 'female' or 'others' for gender")

    if len(username) == 0:
        errors.append("\nYou did not enter username: ")
    
    if len(password) == 0:
        errors.append("\nYou did not enter password")
    
    if len(password_confirmation) == 0:
        errors.append("\nYou did not enter password confirmation")
    
    if password != password_confirmation:
        errors.append("\nPassword and Password confirmation must match!")

    if len(errors) == 0:
        # there are no errors
        # It's time to check if the username already exists before you register...
        result = checkIfUsernameIsTaken(username)
        if result == None:
            # The username has not been taken, register the user...
            cursor.execute("INSERT INTO `users` (`fullname`, `email`, `gender`, `username`, `password`) VALUES ('" + fullname + "', '" + email + "', '" + gender + "', '" + username + "', '" + password + "')")
            # print("Registered Successfully!")
            _db_conn.commit()
            # print(cursor)
            cursor.close()
            return True
    else:
        # there are errors
        for err in errors:
            print(err)

        cursor.close()

def loginUser():
    cursor = _db_conn.cursor()
    errors = []
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if len(username) == 0:
        errors.append("\nYou did not enter your username!")

    if len(password) == 0:
        errors.append("\nYou did not enter your password!")

    if len(errors) == 0:

        result = checkIfUserExists(username, password) 
        cursor.close()
        return result
    else:
        for err in errors:
            print(err)

        cursor.close()

def createNote(author_id):
    cursor = _db_conn.cursor()
    errors = []
    note_title = input("Enter Title: ").strip().lower()
    note_content = input("Enter Content: ").strip()

    if len(note_title) == 0:
        errors.append("\nPleaese enter a Title for your note!")

    if len(note_content) == 0:
        errors.append("\nPlease enter the Contents of your note!")

    if len(errors) == 0:
        # there are no errors

        query = "INSERT INTO `notes` (`note_author_id`, `note_title`, `note_content`) VALUES (%s, %s, %s)"
        data = (author_id, note_title, note_content)
        cursor.execute(query, data)
        _db_conn.commit()
        return True
    else:
        # there are errors
        for err in errors:
            print(err)

        cursor.close()
        return False

def whatNextDo(author_id):
    cursor = _db_conn.cursor()
    whatNext = input("\nTo create new note enter 'N', to read your saved notes enter 'R', and to cancel the program enter 'C': ").upper()

    if whatNext == "N":
        # print(result[0])
        note = createNote(author_id)

        if note:
            print("Note Created Successfully!")
            cursor.close()
            return True
    elif whatNext == "R":
        # print("Reading note still under development!")
        title = input("Enter the title of the note: ").strip().lower()

        if len(title) == 0:
            cont = input("\nNo title entered! Enter 'T' to try again; Enter 'C' to end program: ").upper()

            if cont == "T":
                cursor.close()
            elif cont == "C":
                print("Thank you for your patronage!")
                exit()
            else:
                print("\nIncorrect inputs!")
                cursor.close()
        else:
            read_query = "SELECT * FROM `notes` WHERE `note_author_id` = '%s' AND `note_title` = '" + title + "' LIMIT 1"
            read_data = (author_id,)
            cursor.execute(read_query, read_data)
            # cursor.execute("SELECT * FROM `notes` WHERE `note_author_id` = '" + author_id + "' AND `note_title` = '" + title + "' LIMIT 1")
            for result in cursor:
                if result != None:
                    cursor.close()
                    return result
                elif result == None:
                    cursor.close()
                    return None
    elif whatNext == "C":
        print("\nThank you for your patronage!")
        exit()
    else:
        print("\nInvalid input!")
        cursor.close()