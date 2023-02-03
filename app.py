from db import connection


## initialize our tables
connection.createUsersTable()
connection.createNotesTable()

print("""
--- Welcome to the Notes Application ---
 """)

result = connection.loginUser()


while True:
    if result == None:
        print("\n--------------------------------------------------")
        print("\nUser with that account does not exist. \nDo you want to register?")
        response = input("Enter 'Y' for Yes or 'N' for No: ").upper()

        if response == "N":
            print("Goodbye!")
            exit()
        elif response == "Y":
            register_result = connection.registerUser()
            # print(register_result)
            if register_result:
                print("Registration Successful!")
                # connection.loginUser()
                print("\nRun the program again.")
        else:
        	print("You were to enter either 'Y' or 'N'!")
        	print("Thank You!")
        	exit()
    else:
        # print("\n-----------------------------------------------------")
        # print("\nYou are logged in Successfully!")

        # print(result[0])
        note_data = connection.whatNextDo(result[0])

        # print(type(note_data))

        if type(note_data) == 'tuple':
            print("\n-------------------------------------------------------")
            print("\n" + note_data[2].upper())
            print("\n-------------------------------------------------------")
            print("\n" + note_data[3])
            print("\n-------------------------------------------------------")
            print("\nThe End!")
        elif note_data == None:
            print("\nNote not Found!")



    ## check if the username and password exist