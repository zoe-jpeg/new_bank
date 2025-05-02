import time
import os
import sys
import mysql.connector

#color/style variables
red = '\033[91m'
green = '\033[92m'
blue = '\033[94m'
bold = '\033[1m'
italics = '\033[3m'
underline = '\033[4m'
end = '\033[0m'

#introduction function / greet user
def introduction():
     os.system("clear")
     intro = "Welcome to Cognito Inc. Banking."
     for letter in intro:
          sys.stdout.write(bold + letter + end)
          sys.stdout.flush()
          time.sleep(0.07)
          

     time.sleep(1.2)

     print()
     print()

     tagline = "Financials for the Future."
     for letter in tagline:
          sys.stdout.write(blue + italics + letter + end)
          sys.stdout.flush()
          time.sleep(0.07)
     print()

def user_login():
     os.system("clear")
     message = "LOGIN TO YOUR ACCOUNT"
     for letter in message:
          sys.stdout.write(bold + letter + end)
          sys.stdout.flush()
          time.sleep(0.07)
     time.sleep(0.8)
     print()
     account_number = input("\nAccount Number: ")
     pin_number = input("PIN: ")
     #my sql stuff, a lot of errors here
     '''cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
     row = cursor.fetchone()
     if row is None:
        print("User not found!")
        return
     user_id, username, stored_pin, email, address = row
     if account_number == '''

def account_options():
     os.system("clear")
     print(bold + "Account Options" + end)
     print("1. Check Balance")
     print("2. Deposit Funds")
     print("3. Withdraw Funds")
     print("4. Transfer Funds")
     print("5. Exit")

     choice = input("\nSelect an option (1-5): ")
     if choice == 1:
          print("Checking Balance...")
          # add code to check balance
     elif choice == 2:
          print("Depositing Funds...")
          deposit_amount = input("Please enter the amount to deposit:")
          # add code to deposit funds
     elif choice == 3:
          print("Withdrawing Funds...")
          withdrawl_amount = input("Please enter the amount to withdraw:")
          # add code to withdraw funds
     elif choice == 4:
          print("Transferring Funds...")
          transfer_amount = input("Please enter the amount to transfer:")
          new_account_number = input("Please enter the recipient's account number:")
          # add code to transfer funds
     elif choice == 5:
          exit_program()

def exit_program():
    os.system("clear")
    print(bold + "Thank you for using Cognito Inc. Banking!" + end)
    print("We hope to see you again soon.")
    time.sleep(2)
    sys.exit()