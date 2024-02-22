import sys
import sys
from PySide6.QtWidgets import QHeaderView, QTableView, QFileDialog, QApplication, QInputDialog, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QDialog, QFormLayout, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QSize, QRect, QTimer
from PySide6.QtGui import QIcon, QPixmap
import datetime
import sqlite3  # Assuming you're using SQLite for employee verification
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PySide6.QtGui import QStandardItemModel, QStandardItem
import pandas as pd

class CustomerManagement(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Customers")
        self.resize(1177, 778)
        self.initUI()

    def initUI(self):
        self.load_data()

        # Layout
        layout = QVBoxLayout()

        # Setup QTimer
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.load_data)  # Replace 'your_function' with your function name
        #self.timer.start(1000)  # Timer interval set to 1000 milliseconds (1 second)

        # Buttons
        merge_button = QPushButton("Merge Customers")
        add_button = QPushButton("Add Customer")
        remove_button = QPushButton("Remove Customer")
        edit_button = QPushButton("Edit Phone Number")
        export_button = QPushButton("Export to Excel")

        layout.addWidget(self.tableView)
        layout.addWidget(merge_button)
        layout.addWidget(add_button)
        layout.addWidget(remove_button)
        layout.addWidget(edit_button)
        layout.addWidget(export_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connections
        merge_button.clicked.connect(self.merge_customers)
        add_button.clicked.connect(self.add_customer)
        remove_button.clicked.connect(self.remove_customer)
        edit_button.clicked.connect(self.edit_phone)
        export_button.clicked.connect(self.export_to_excel)

    def load_data(self):
        self.model = QStandardItemModel()
        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        connection = sqlite3.connect("/Users/ammar/Projects/Python/PointOfSaleProject/appData/customers.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()

        self.model.setHorizontalHeaderLabels(["Name", "Phone"])
        for row in rows:
            items = [QStandardItem(field) for field in row]
            self.model.appendRow(items)

        connection.close()
        self.tableView.setGeometry(QRect(10, 10, 1157, 600))

    def remove_customer(self):
        indexes = self.tableView.selectionModel().selectedRows()
        if indexes:
            reply = QMessageBox.question(self, 'Confirm Delete', 
                                        "Are you sure you want to delete the selected customer(s)?", 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                connection = sqlite3.connect("/Users/ammar/Projects/Python/PointOfSaleProject/appData/customers.db")
                cursor = connection.cursor()

                try:
                    for index in indexes:
                        name = self.model.item(index.row(), 0).text()  # Assuming 'name' is a unique identifier
                        cursor.execute("DELETE FROM customers WHERE name = ?", (name,))

                    connection.commit()
                except sqlite3.Error as error:
                    QMessageBox.critical(self, 'Error', f'An error occurred: {error}')
                finally:
                    connection.close()

                self.load_data()


    def edit_phone(self):
        indexes = self.tableView.selectionModel().selectedRows()
        if indexes:
            index = indexes[0]
            name = self.model.item(index.row(), 0).text()  # Ensure 'name' is a unique identifier

            new_phone, ok = QInputDialog.getText(self, "Edit Phone", "Enter new phone number:")
            if ok and new_phone:
                # Simple validation for phone number
                if not new_phone.isdigit() or len(new_phone) < 5:  # Adjust conditions as per your requirements
                    QMessageBox.warning(self, "Invalid Input", "Please enter a valid phone number.")
                    return

                try:
                    connection = sqlite3.connect("/Users/ammar/Projects/Python/PointOfSaleProject/appData/customers.db")
                    cursor = connection.cursor()
                    cursor.execute("UPDATE customers SET phone = ? WHERE name = ?", (new_phone, name))
                    connection.commit()
                except sqlite3.Error as error:
                    QMessageBox.critical(self, "Error", f"An error occurred: {error}")
                finally:
                    if connection:
                        connection.close()

                self.load_data()
            elif not ok:
                # Handle the case where user pressed cancel or entered an empty string
                pass


    def merge_customers(self):
        connection = sqlite3.connect("/Users/ammar/Projects/Python/PointOfSaleProject/appData/customers.db")
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM customers 
            WHERE rowid NOT IN (
                SELECT MIN(rowid) 
                FROM customers 
                GROUP BY name, phone
            )
        """)
        connection.commit()
        connection.close()
        self.load_data()  # Refresh the table view


    def export_to_excel(self):
        connection = sqlite3.connect("/Users/ammar/Projects/Python/PointOfSaleProject/appData/customers.db")
        df = pd.read_sql_query("SELECT * FROM customers", connection)
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Excel Files (*.xlsx)')
        if file_path:
            df.to_excel(file_path, index=False)
        connection.close()

    def add_customer(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Customer")  # Set the window title here
        layout = QFormLayout()
        name_edit = QLineEdit()
        phone_edit = QLineEdit()
        layout.addRow("Name:", name_edit)
        layout.addRow("Phone:", phone_edit)
        add_button = QPushButton("Add")
        layout.addWidget(add_button)
        dialog.setLayout(layout)

        def on_add_clicked():
            name = name_edit.text()
            phone = phone_edit.text()
            connection = sqlite3.connect("/Users/ammar/Projects/Python/PointOfSaleProject/appData/customers.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
            connection.commit()
            connection.close()
            self.load_data()
            dialog.close()

        add_button.clicked.connect(on_add_clicked)
        dialog.exec_()

