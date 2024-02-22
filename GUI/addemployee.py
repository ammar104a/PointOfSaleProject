import sqlite3
from getpass import getpass
#Hello
# Set your database path
database_path = '/Users/ammar/Projects/Python/PointOfSaleProject/appData/employees.db'

# Connect to the SQLite database
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# Function to insert a new employee
def add_new_employee(employee_name, employee_key, shift):
    try:
        cursor.execute("INSERT INTO employees (name, key, shift) VALUES (?, ?, ?)", (employee_name, employee_key, shift))
        connection.commit()
        print("New employee added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Prompt for master key
master_key = "582002"  # Replace with the actual master key
input_master_key = getpass("Enter the master key to add a new employee: ")

if input_master_key == master_key:
    # Prompt for new employee details
    employee_name = input("Enter the new employee's name: ")
    employee_key = input("Enter the new employee's key: ")
    shift = int(input("Enter the new employee's shift (1-3): "))

    # Validate shift input
    if not 1 <= shift <= 3:
        print("Shift must be 1, 2, or 3.")
    else:
        # Add the new employee
        add_new_employee(employee_name, employee_key, shift)
else:
    print("Invalid master key.")

# Close the connection to the database
connection.close()
