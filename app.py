from db import connection

## initialize our tables
connection.createUsersTable()
connection.createNotesTable()

print("""
--- Welcome to the Notes Application ---
 """)

result = connection.loginUser()



if result == None:
    print("\n--------------------------------------------------")
    print("\nUser with that account does not exist. \nDo you want to register?")
    response = input("Enter 'Y' for Yes or 'N' for No: ").upper()

    if response == "N":
        print("Goodbye!")
        exit()
    elif response == "Y":
        register_result = connection.registerUser()
        print(register_result)
    else:
    	print("You were to enter either 'Y' or 'N'!")
    	print("Thank You!")
    	exit()
        



## check if the username and password exist
