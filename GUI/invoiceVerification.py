import sys
from PySide6.QtWidgets import QApplication, QInputDialog, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QDialog, QFormLayout, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QIcon, QPixmap
import datetime
import sqlite3  # Assuming you're using SQLite for employee verifications
from invoiceWindow import InvoiceWindow
from manageEmployees import ManageEmployees
## Add nee button should redirect to the employee management page
class InvoiceVerification(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(None)
        self.setWindowTitle("Employee Verification")
        self.resize(250, 100)
        self.database_path = r'/Users/ammar/Projects/Python/PointOfSaleProject/appData/employees.db'
        self.master_key = "582002"
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.employeeKeyInput = QLineEdit(self)
        self.layout.addWidget(self.employeeKeyInput)

        self.verifyButton = QPushButton("Login", self)
        self.verifyButton.clicked.connect(self.verifyEmployee)
        self.layout.addWidget(self.verifyButton)

        self.addButton = QPushButton("Add New Employee", self)
        self.addButton.clicked.connect(self.addEmployee)
        self.layout.addWidget(self.addButton)
        
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

    def verifyEmployee(self):
        key = self.employeeKeyInput.text()
        if self.isEmployeeExists(key):
            employee_name = self.getEmployeeName(key)
            QMessageBox.information(self, "Welcome", f"Welcome: {employee_name}")
            
            # Pass the employee name to InvoiceWindow
            self.invoiceWindow = InvoiceWindow(employee_name, self)
            self.invoiceWindow.show()
        else:
            QMessageBox.warning(self, "Error", "Invalid Employee Key")
    


    def addEmployee(self):
        key = self.employeeKeyInput.text()
        if key == self.master_key:
            self.openManageEmployees()
        else:
            QMessageBox.warning(self, "Error", "Invalid Master Key")

    def isEmployeeExists(self, key):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM employees WHERE key = ?", (key,))
        count = cursor.fetchone()[0]
        connection.close()
        return count > 0

    def getEmployeeName(self, key):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM employees WHERE key = ?", (key,))
        name = cursor.fetchone()[0]
        connection.close()
        return name
    
    def openManageEmployees(self):
        print("Opening Manage Employees Window") # Debugging Print
        self.manageEmployees = ManageEmployees()  # Remove the 'self' parameter
        self.manageEmployees.show()  # Show the window
