import getpass
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        database ='indigo',
        # password = getpass.getpass("Enter your password: ")
        password = os.getenv("MY_SECRET_PASSWORD")
        )
    mycursur = connection.cursor()
    print("Connected to MySQL database")
except Error as e:
    print(f"Error while connecting to MySQL: {e}")

def create_database(db_name):
    try:
        mycursur.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully")
    except Error as e:
        print(f"Error creating database: {e}")


# Uncomment the line below to create a database named 'indigo'
# create_database('indigo')

# to create a table
def create_table():
    try:
        mycursur.execute("USE indigo") # use this database or specify db while connecting
        mycursur.execute("""
            CREATE TABLE users (
                airport_id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(255) NOT NULL,
                city VARCHAR(255) NOT NULL,
                name VARCHAR(255)
            )
        """)
        print("Table 'users' created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

# Uncomment the line below to create the 'users' table

# create_table()

def insert_user(code, city, name):
    try:
        sql = "INSERT INTO users (code, city, name) VALUES (%s, %s, %s)"
        val = (code, city, name)
        mycursur.execute(sql, val)
        connection.commit()
        print(f"User '{code}' inserted successfully")

    except Error as e:
        print(f"Error inserting user: {e}")

# Example usage:
# insert_user('DEL', 'New Delhi', 'Indira Gandhi Intl')
# insert_user('CCU', 'Kolkata', 'Netaji Subhas Chandra Bose Intl')
# insert_user('BOM', 'Mumbai', 'Chhatrapati Shivaji Maharaj Intl')

# search/or retrieve data
def get_user_by_code(code):
    try:
        mycursur.execute("SELECT * FROM users WHERE airport_id > %s", (code,))
        # result = mycursur.fetchone()
        result = mycursur.fetchall()
        return result
    except Error as e:
        print(f"Error retrieving user: {e}")
        return None

# Example usage:
# user = get_user_by_code('0')

# if user:
#     print("User found:", user)
# else:
#     print("User not found")


def update_user(airport_id, new_name):
    try:
        sql = "UPDATE users SET city = %s WHERE airport_id = %s"
        val = (new_name, airport_id)
        mycursur.execute(sql, val)
        connection.commit()
        print(f"User with airport_id '{airport_id}' updated successfully")
    except Error as e:
        print(f"Error updating user: {e}")

# Example usage:
# update_user(1, 'Delhi')
