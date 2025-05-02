import mysql.connector

def insert_user(first_name, last_name, birth_date, account_number, pin_number, balance):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Zb01101944!?*",
            database="example"
        )

        cursor = connection.cursor()

        query = '''
        INSERT INTO example.member_info (first_name, last_name, birth_date, account_number, PIN, balance)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        values = (first_name, last_name, birth_date, account_number, pin_number, balance)
        cursor.execute(query, values)

        connection.commit()
        print("User inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()