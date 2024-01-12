import sys
from PySide6.QtWidgets import (
    QHeaderView, QTableView, QApplication, QInputDialog, QMainWindow,
    QPushButton, QVBoxLayout, QWidget, QDialog, QFormLayout, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import sqlite3
from PySide6.QtGui import QStandardItemModel, QStandardItem

class ManageEmployees(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Employees")
        self.resize(1177, 778)
        self.initUI()
        self.load_employees()

    def initUI(self):
        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a table to display employees
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(3)
        self.employee_table.setHorizontalHeaderLabels(["Name", "Key", "Shift"])
        self.employee_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.employee_table)

        # Create buttons to interact with employees
        add_button = QPushButton("Add Employee")
        remove_button = QPushButton("Remove Employee")
        check_sales_button = QPushButton("Check Sales")
        change_shift_button = QPushButton("Change Employee Shift")

        # Connect buttons to their respective functions
        add_button.clicked.connect(self.add_employee)
        remove_button.clicked.connect(self.remove_employee)
        check_sales_button.clicked.connect(self.check_sales)
        change_shift_button.clicked.connect(self.change_shift)

        # Add buttons to the layout
        button_layout = QVBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(check_sales_button)
        button_layout.addWidget(change_shift_button)
        layout.addLayout(button_layout)

    def load_employees(self):
        # Connect to your SQLite database and retrieve employee data
        conn = sqlite3.connect("/Users/ammar/POS Project/POSPY/appData/employees.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, key, shift FROM employees")
        employees = cursor.fetchall()
        conn.close()

        # Populate the table with employee data
        self.employee_table.setRowCount(len(employees))
        for row, employee in enumerate(employees):
            for col, value in enumerate(employee):
                item = QTableWidgetItem(str(value))
                self.employee_table.setItem(row, col, item)

    def add_employee(self):
        # Ask for employee details
        name, ok_name = QInputDialog.getText(self, 'Enter Name', 'Enter the employee name:')
        key, ok_key = QInputDialog.getText(self, 'Enter Key', 'Enter the 8-digit employee key:')
        shift, ok_shift = QInputDialog.getInt(self, 'Enter Shift', 'Enter the shift number (1-3):', 1, 1, 3)

        # Validate inputs
        if not ok_name or not name:
            QMessageBox.warning(self, 'Input Error', 'Employee name is required.')
            return
        if not ok_key or not key.isdigit() or len(key) != 8:
            QMessageBox.warning(self, 'Input Error', 'Employee key must be an 8-digit number.')
            return
        if not ok_shift or shift < 1 or shift > 3:
            QMessageBox.warning(self, 'Input Error', 'Shift number must be between 1 and 3.')
            return

        # Add the employee to the database
        connection = sqlite3.connect('/Users/ammar/POS Project/POSPY/appData/employees.db')
        cursor = connection.cursor()

        # Check if the key already exists in the database
        cursor.execute("SELECT COUNT(*) FROM employees WHERE key=?", (key,))
        count = cursor.fetchone()[0]
        if count > 0:
            QMessageBox.warning(self, 'Duplicate Key', 'An employee with this key already exists.')
            connection.close()
            return

        # Insert the employee into the database
        cursor.execute("INSERT INTO employees (name, key, shift) VALUES (?, ?, ?)", (name, key, shift))
        connection.commit()
        QMessageBox.information(self, 'Employee Added', 'Employee added successfully.')

        # Close the database connection
        connection.close()

        # Clear and repopulate the employee table to reflect the changes
        self.clear_employee_table()
        self.populate_employee_table()


    def remove_employee(self):
        # Get the employee's key from user input
        key, ok = QInputDialog.getText(self, 'Enter Employee Key', 'Enter the 8-digit key:')
    
        # Check if the input is valid and the user clicked OK
        if ok and len(key) == 8 and key.isdigit():
            # Search for the employee with the given key in the database
            connection = sqlite3.connect('/Users/ammar/POS Project/POSPY/appData/employees.db')
            cursor = connection.cursor()
        
            # Check if the employee exists
            cursor.execute("SELECT * FROM employees WHERE key=?", (key,))
            employee = cursor.fetchone()
        
            if employee:
                # Ask for confirmation before removing
                reply = QMessageBox.question(self, 'Confirm Removal', 'Are you sure you want to remove this employee?', 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # Remove the employee from the database
                    cursor.execute("DELETE FROM employees WHERE key=?", (key,))
                    connection.commit()
                    QMessageBox.information(self, 'Employee Removed', 'Employee removed successfully.')
                    # Clear the existing data in the employee table
                    self.clear_employee_table()

                    # Fetch and populate the updated data in the employee table
                    self.populate_employee_table()
                else:
                    QMessageBox.information(self, 'Operation Cancelled', 'Employee removal operation cancelled.')
            else:
                QMessageBox.warning(self, 'Employee Not Found', 'Employee with the provided key was not found in the database.')
        
            # Close the database connection
            connection.close()
        else:
            QMessageBox.warning(self, 'Invalid Key', 'Please enter a valid 8-digit key.')

    # call this function to remove an employee


    def check_sales(self):
        # Implement this function to check employee sales
        pass

    def change_shift(self):
        # Implement this function to change employee shifts
        pass

    def clear_employee_table(self):
        # Clear the data in the employee table
        self.employee_table.setRowCount(0)

    def populate_employee_table(self):
        # Fetch data from the database and populate the employee table
        connection = sqlite3.connect('/Users/ammar/POS Project/POSPY/appData/employees.db')
        cursor = connection.cursor()

        # Fetch all employees from the database
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        # Populate the employee table
        for row_num, employee in enumerate(employees):
            self.employee_table.insertRow(row_num)
            for col_num, data in enumerate(employee):
                item = QTableWidgetItem(str(data))
                self.employee_table.setItem(row_num, col_num, item)

        # Close the database connection
        connection.close()