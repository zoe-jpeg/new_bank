from http.server import HTTPServer, BaseHTTPRequestHandler
import mysql.connector
import mysql_connection as mysql_con
import json
import time
import os
import random

html_content = """
<!DOCTYPE html>
<html>
<head>
    <!-- UI design for website-->
    <title>Cognito Inc. Banking</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background-color: #f4f4f4; 
            text-align: center; 
            padding-top: 50px; 
            margin-top: 100px
        }
        .bold { 
            font-weight: bold; 
            font-size: 24px; 
        }
        .italics { 
            color: #007BFF; 
            font-style: italic; 
            font-size: 20px; 
        }
        #intro, #tagline { 
            white-space: pre; 
        }
        .button { 
            background-color: #007BFF; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            font-size: 16px; 
            cursor: pointer; 
            margin: 10px; 
        }
        .button:hover { 
            background-color: #0056b3; 
        }
        .form-container {
            display: none;
            margin-top: 20px;
        }
        .form-container input {
            margin: 5px;
            padding: 10px;
            font-size: 16px;
        }
        .more-padding{
            padding-bottom: 60px;
        }
    </style>
</head>
<!--user function buttons (login, signup, deposit, etc)-->
<body>
    <div id="intro" class="bold"></div>
    <br>
    <div id="tagline" class="italics more-padding"></div>
    <button onclick="showLoginForm()" class="button" id="login_button" style="display:none;">Login In</button>
    <button onclick="showSignUpForm()" class="button" id="signup_button" style="display:none;">Create An Account</button>

    <div class="form-container" id="login_form">
        <input type="text" id="login_account_number" placeholder="Account Number" required>
        <input type="text" id="login_pin" placeholder="PIN" required>
        <button onclick="loginIn()" class="button">Submit</button>
    </div>

    <div class="form-container" id="signup_form">
        <input type="text" id="first_name" placeholder="First Name" required>
        <input type="text" id="last_name" placeholder="Last Name" required>
        <input type="date" id="date_of_birth" placeholder="Date of Birth" required>
        <input type="number" id="initial_balance" placeholder="Initial Balance" required>
        <button onclick="signUp()" class="button">Submit</button>
    </div>

    <div id="user_actions" class="form-container">
        <h2>Account Actions</h2>
        <input type="text" id="action_account_number" placeholder="Account Number" required>

        <div>
            <input type="number" id="deposit_amount" placeholder="Deposit Amount">
            <button onclick="deposit()" class="button">Deposit</button>
        </div>
        <div>
            <input type="number" id="withdraw_amount" placeholder="Withdraw Amount">
            <button onclick="withdraw()" class="button">Withdraw</button>
        </div>
        <div>
            <input type="text" id="recipient_account" placeholder="Recipient Account Number">
            <input type="number" id="transfer_amount" placeholder="Transfer Amount">
            <button onclick="transfer()" class="button">Transfer</button>
        </div>
    </div>

    <script>
        //code that runs when the buttons are pressed
        function showLoginForm() {
            document.getElementById("login_form").style.display = "block";
        }

        function loginIn() {
            const accountNumber = document.getElementById("login_account_number").value;
            const pinNumber = document.getElementById("login_pin").value;

            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ account_number: accountNumber, pin_number: pinNumber })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.account_number) {
                    showActions(data.account_number);
                }
            })
            .catch(error => console.error('Error:', error));
        }

        function showSignUpForm() {
            document.getElementById("signup_form").style.display = "block";
        }

        function signUp() {
            const firstName = document.getElementById("first_name").value;
            const lastName = document.getElementById("last_name").value;
            const dateOfBirth = document.getElementById("date_of_birth").value;
            const initialBalance = parseFloat(document.getElementById("initial_balance").value);

            fetch('/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    date_of_birth: dateOfBirth,
                    initial_balance: initialBalance
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.account_number) {
                    showActions(data.account_number);
                }
            })
            .catch(error => console.error('Error:', error));
        }

        function showActions(accountNumber) {
            document.getElementById("user_actions").style.display = "block";
            document.getElementById("action_account_number").value = accountNumber;
        }

        function deposit() {
            const account = document.getElementById("action_account_number").value;
            const amount = parseFloat(document.getElementById("deposit_amount").value);

            fetch('/deposit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ account_number: account, amount: amount })
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error:', error));
        }

        function withdraw() {
            const account = document.getElementById("action_account_number").value;
            const amount = parseFloat(document.getElementById("withdraw_amount").value);

            fetch('/withdraw', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ account_number: account, amount: amount })
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error:', error));
        }

        function transfer() {
            const sender = document.getElementById("action_account_number").value;
            const recipient = document.getElementById("recipient_account").value;
            const amount = parseFloat(document.getElementById("transfer_amount").value);

            fetch('/transfer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sender_account: sender, recipient_account: recipient, amount: amount })
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error:', error));
        }

        const introText = "Welcome to Cognito Inc. Banking.";
        const taglineText = "Financials for the Future.";

        function typeEffect(elementId, text, delay, callback) {
            let i = 0;
            const element = document.getElementById(elementId);
            const timer = setInterval(() => {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                } else {
                    clearInterval(timer);
                    if (callback) callback();
                }
            }, delay);
        }

        typeEffect("intro", introText, 70, () => {
            setTimeout(() => {
                typeEffect("tagline", taglineText, 70, () => {
                    setTimeout(() => {
                        document.getElementById("login_button").style.display = "inline-block";
                        document.getElementById("signup_button").style.display = "inline-block";
                    }, 2000);
                });
            }, 1200);
        });
    </script>
</body>
</html>
"""

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            if not post_data:
                raise ValueError("No data received")

            data = json.loads(post_data)

            #if the user wants to login
            if self.path == '/login':
                #get their pin and account number
                account_number = data.get("account_number")
                pin_number = data.get("pin_number")
                #if it matches a pin and account number in the mysql database, gets their account info and displays it in an alert
                if account_number and pin_number:
                    connection = mysql.connector.connect(host="localhost", user="root", password="Zb01101944!?*", database="example")
                    cursor = connection.cursor()
                    cursor.execute("SELECT first_name, last_name, account_number, PIN, balance FROM member_info WHERE account_number = %s AND PIN = %s", (account_number, pin_number))
                    result = cursor.fetchone()
                    if result:
                        first_name, last_name, account_number, pin_number, balance = result
                        response = {"message": f"Login successful! Welcome {first_name} {last_name}. Balance: ${balance:.2f}", "account_number": account_number}
                    else:
                        response = {"message": "Invalid account number or PIN. Please try again."}
                    cursor.close()
                    connection.close()
                else:
                    response = {"message": "Account number and PIN are required."}
            
            #if the user presses the sign up button
            elif self.path == '/signup':
                #user enters first & last name and DOB, along w how much money they are depositing
                first_name = data.get("first_name")
                last_name = data.get("last_name")
                date_of_birth = data.get("date_of_birth")
                initial_balance = data.get("initial_balance", 0.0)
                #account number and PIN are randomly generated
                account_number = random.randint(1000, 9999)
                pin_number = random.randint(1000, 9999)

                #information is added to the mysql database
                mysql_con.insert_user(first_name, last_name, date_of_birth, account_number, pin_number, initial_balance)

                #alerts user that their account has been created
                response = {
                    "message": f"Account created! Welcome {first_name} {last_name}. Account Number: {account_number}, PIN: {pin_number}, Balance: ${initial_balance:.2f}",
                    "account_number": account_number
                }

            #adds the amount entered by the user into the balance column in their account
            elif self.path == '/deposit':
                account_number = data.get("account_number")
                amount = data.get("amount", 0.0)
                connection = mysql.connector.connect(host="localhost", user="root", password="Zb01101944!?*", database="example")
                cursor = connection.cursor()
                cursor.execute("UPDATE member_info SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
                connection.commit()
                response = {"message": f"Deposited ${amount:.2f} to account {account_number}"}
                cursor.close()
                connection.close()
            #subtracts the amount entered by the user from the balance column in their account
            elif self.path == '/withdraw':
                account_number = data.get("account_number")
                amount = data.get("amount", 0.0)
                connection = mysql.connector.connect(host="localhost", user="root", password="Zb01101944!?*", database="example")
                cursor = connection.cursor()
                cursor.execute("SELECT balance FROM member_info WHERE account_number = %s", (account_number,))
                balance = cursor.fetchone()
                if balance and balance[0] >= amount:
                    cursor.execute("UPDATE member_info SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
                    connection.commit()
                    response = {"message": f"Withdrew ${amount:.2f} from account {account_number}"}
                else:
                    #if the user doesn't have enough money to withdrawl, the program will alert them and not change their balance
                    response = {"message": "Insufficient funds."}
                cursor.close()
                connection.close()

            # user enters the account number of another user, and the amount entered by the user is sent from (subtracted) their account balance to the other account (added)
            elif self.path == '/transfer':
                sender = data.get("sender_account")
                recipient = data.get("recipient_account")
                amount = data.get("amount", 0.0)
                connection = mysql.connector.connect(host="localhost", user="root", password="Zb01101944!?*", database="example")
                cursor = connection.cursor()
                cursor.execute("SELECT balance FROM member_info WHERE account_number = %s", (sender,))
                sender_balance = cursor.fetchone()
                if sender_balance and sender_balance[0] >= amount:
                    cursor.execute("UPDATE member_info SET balance = balance - %s WHERE account_number = %s", (amount, sender))
                    cursor.execute("UPDATE member_info SET balance = balance + %s WHERE account_number = %s", (amount, recipient))
                    connection.commit()
                    response = {"message": f"Transferred ${amount:.2f} from {sender} to {recipient}"}
                else:
                    response = {"message": "Transfer failed. Insufficient funds or invalid accounts."}
                cursor.close()
                connection.close()

            else:
                response = {"message": "Invalid endpoint."}

        except ValueError as ve:
            response = {"message": f"Error: {str(ve)}"}
        except json.JSONDecodeError:
            response = {"message": "Invalid JSON received."}
        except Exception as e:
            response = {"message": f"An error occurred: {str(e)}"}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))

#runs the site at localhost:8000
if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, WebHandler)
    print("Web version running at http://localhost:8000/")
    httpd.serve_forever()