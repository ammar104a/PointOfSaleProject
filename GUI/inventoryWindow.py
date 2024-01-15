import sys # Import System Runtime 
import sqlite3
from PySide6.QtCore import (QSize, QRect, QCoreApplication ) # Import From PyQTCore
from PySide6.QtGui import (QIcon, QPixmap) # Import from PyQTGui
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QLabel, QPushButton, QDialog, QTableWidget, QTableWidgetItem, 
    QLineEdit, QFormLayout, QDialogButtonBox, QDialog, QMessageBox, QHeaderView) # Import from PyQTQidgets


class InventoryWindow(QMainWindow):

    def setupSearch(self):
        # Search by Name
        self.searchNameLineEdit = QLineEdit(self)
        self.searchNameLineEdit.setPlaceholderText("Search by Name")
        self.searchNameLineEdit.setGeometry(970, 10, 200, 30)
        self.searchNameLineEdit.textChanged.connect(self.searchByName)

        # Search by ID
        self.searchIDLineEdit = QLineEdit(self)
        self.searchIDLineEdit.setPlaceholderText("Search by ID")
        self.searchIDLineEdit.setGeometry(970, 50, 200, 30)
        self.searchIDLineEdit.textChanged.connect(self.searchByID)

    def searchByName(self, text):
        # Loop through the table and hide rows that don't match the search query
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 1)  # column 1 is Name
            self.tableWidget.setRowHidden(row, text.lower() not in item.text().lower())

    def searchByID(self, text):
        # Loop through the table and hide rows that don't match the search query
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)  # column 0 is ID
            self.tableWidget.setRowHidden(row, text.lower() not in item.text().lower())

    def __init__(self, parent=None):
        super().__init__(None)
        self.setWindowTitle("Inventory")
        self.resize(1177, 778)
        self.initUI() 
        # Add more UI setup code here (like tables, buttons, etc.)
    
    def initUI(self):
        # Create a table widget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(10, 10, 945, 778)  # Adjust as needed

        # Connect to the database
        connection = sqlite3.connect(r'C:\Users\ammar\PythonProjects\PointOfSale\appData\your_database.db')
        cursor = connection.cursor()

        # Retrieve data from the database
        cursor.execute("SELECT * FROM products")
        records = cursor.fetchall()

        # Assuming your table has columns: id, name, quantity, price
        headers = ["ID", "Name", "Quantity", "Price"]

        # Setup table dimensions
        self.tableWidget.setRowCount(len(records))
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # Stretch all columns equally
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Populate the table with the data
        for row_index, row_data in enumerate(records):
            for column_index, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(cell_data)))

        # Close the database connection
        connection.close()

        self.tableWidget.itemChanged.connect(self.updateDatabase)

        self.setupSearch()

        # Create a label for low stock warnings
        self.lowStockLabel = QLabel(self)
        self.lowStockLabel.setGeometry(970, 100, 212, 100)  # Adjust as needed
        self.lowStockLabel.setStyleSheet("color: White;")  # Set text color to red
        self.updateLowStockWarnings()

        button_width = 200
        button_height = 40
        margin = 10  # Margin from the right border
        self.addProductButton = QPushButton("Add Product", self)
        right_edge_x_position = self.width() - button_width - margin
        self.addProductButton.setGeometry(right_edge_x_position, self.height() - button_height - margin, button_width, button_height)
        self.addProductButton.clicked.connect(self.addProductDialog)

    def addProductDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Product")

        # Form layout for product details
        layout = QFormLayout(dialog)
        
        nameLineEdit = QLineEdit(dialog)
        quantityLineEdit = QLineEdit(dialog)
        priceLineEdit = QLineEdit(dialog)
        layout.addRow("Name:", nameLineEdit)
        layout.addRow("Quantity:", quantityLineEdit)
        layout.addRow("Price:", priceLineEdit)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=dialog)
        layout.addRow(buttons)

        buttons.accepted.connect(lambda: self.add_product(nameLineEdit.text(), int(quantityLineEdit.text()), float(priceLineEdit.text())))
        buttons.rejected.connect(dialog.reject)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def updateLowStockWarnings(self):
        # Connect to the database
        connection = sqlite3.connect(r'C:\Users\ammar\PythonProjects\PointOfSale\appData\your_database.db')
        cursor = connection.cursor()

        # Retrieve products with low stock
        low_stock_threshold = 3
        cursor.execute("SELECT name FROM products WHERE quantity < ?", (low_stock_threshold,))
        low_stock_items = cursor.fetchall()

        # Generate and display the warning message
        if low_stock_items:
            names = [item[0] for item in low_stock_items]
            warning_message = "Warning, Low stock:\n\n" + "\n".join(names)
            self.lowStockLabel.setText(warning_message)
        else:
            self.lowStockLabel.setText("Products are sufficiently stocked.")

        # Close the database connection
        connection.close()

    def add_product(self, name, quantity, price):
        try:
            # Connect to the database
            connection = sqlite3.connect(r'C:\Users\ammar\PythonProjects\PointOfSale\appData\your_database.db')
            cursor = connection.cursor()

            # Check if the product already exists in the database
            cursor.execute("SELECT * FROM products WHERE name=?", (name,))
            existing_product = cursor.fetchone()

            if existing_product:
                # Product already exists
                QMessageBox.warning(self, 'Error', f"The product '{name}' already exists.")
                return
            else:
                # Product doesn't exist, insert a new product
                cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
                connection.commit()
                QMessageBox.information(self, 'Success', f"New product '{name}' added to the database.")

            # Refresh the table to show new product
            self.initUI()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {e}")
        finally:
            # Close the database connection
            connection.close()

    def updateDatabase(self, item):
        # Get the row and column of the edited item
        row = item.row()
        column = item.column()

        # Get the product ID from the first column
        product_id = self.tableWidget.item(row, 0).text()

        # Define the database column we're updating
        columns = ["name", "quantity", "price"]
        db_column = columns[column - 1]  # Adjust the index to match the database columns

        # Get the new value from the edited cell
        new_value = item.text()

        # Update the database
        connection = sqlite3.connect(r'C:\Users\ammar\PythonProjects\PointOfSale\appData\your_database.db')
        cursor = connection.cursor()
        query = f"UPDATE products SET {db_column}=? WHERE id=?"
        cursor.execute(query, (new_value, product_id))
        connection.commit()
        connection.close()