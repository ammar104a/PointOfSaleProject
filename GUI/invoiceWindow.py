import sys
from PySide6.QtWidgets import QHeaderView, QTableView, QApplication, QInputDialog, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QDialog, QFormLayout, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QIcon, QPixmap
import datetime
import sqlite3  # Assuming you're using SQLite for employee verification
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PySide6.QtGui import QStandardItemModel, QStandardItem

# Add necessary imports for PDF generation
# Example: from reportlab.pdfgen import canvas

class InvoiceWindow(QMainWindow):
    def __init__(self, employee_name="", parent=None):
        super().__init__(parent)
        self.employee_name = employee_name
        self.setWindowTitle(f"Checkout - {self.employee_name}" if self.employee_name else "Checkout - Guest")
        self.resize(1177, 778)
        self.initUI()
    def initialize_customer_db():
        connection = sqlite3.connect('/Users/ammar/POS Project/POSPY/appData/customers.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                name TEXT,
                phone TEXT
            )
        ''')
        connection.commit()
        connection.close()

    # Call the function to ensure the database is ready
    initialize_customer_db()
    def initUI(self):
        self.layout = QVBoxLayout()

        
        # Inventory Table
        self.inventoryTable = QTableView(self)  # Use QTableView instead of QTableWidget // Didnt work
        self.inventoryModel = QStandardItemModel()
        self.inventoryTable.setModel(self.inventoryModel)  # Set the model to the QTableView
        self.populateInventoryTable()
        self.layout.addWidget(self.inventoryTable)

        # Initialize the inventory model and set it to the table
        self.inventoryTable.setModel(self.inventoryModel)
        self.populateInventoryTable()  # Now populate the table

        # Invoice Table
        self.invoiceTable = QTableWidget(self)
        self.invoiceTable.setColumnCount(4)  # ID, Name, Quantity, Unit Price, Total Price
        self.invoiceTable.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Unit Price", "Total Price"])
        self.layout.addWidget(self.invoiceTable)

        # Add to initUI method
        self.productIdInput = QLineEdit(self)
        self.layout.addWidget(self.productIdInput)

        self.quantityInput = QLineEdit(self)
        self.layout.addWidget(self.quantityInput)

        self.addProductButton = QPushButton("Add to Invoice", self)
        self.addProductButton.clicked.connect(self.addProductToInvoice)
        self.layout.addWidget(self.addProductButton)

        # Print Button
        self.printButton = QPushButton("Print Invoice", self)
        self.printButton.clicked.connect(self.generatePDF)
        self.layout.addWidget(self.printButton)

        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

        self.newCheckoutButton = QPushButton("New Checkout", self)
        self.newCheckoutButton.clicked.connect(self.resetCheckout)
        self.layout.addWidget(self.newCheckoutButton)


    def checkAndUpdateInventory(self, productId, quantity):
        connection = sqlite3.connect('/Users/ammar/POS Project/POSPY/appData/your_database.db')
        cursor = connection.cursor()
        try:
            # Fetch the current inventory for the product
            cursor.execute("SELECT quantity FROM products WHERE id = ?", (productId,))
            result = cursor.fetchone()
            if result:
                current_quantity = result[0]
                if current_quantity >= quantity:
                    # Update the inventory
                    new_quantity = current_quantity - quantity
                    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, productId))
                    connection.commit()
                    return True
                else:
                    # Not enough quantity in inventory
                    QMessageBox.warning(self, "Error", "Not enough quantity in inventory")
                    return False
            else:
                QMessageBox.warning(self, "Error", "Product ID not found in inventory")
                return False
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Database Error", str(e))
            return False
        finally:
            connection.close()
    def fetchInventory(self):
        try:
            # Correct the path if the database file is in 'appData' folder
            connection = sqlite3.connect('/Users/ammar/POS Project/POSPY/appData/your_database.db')
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, price FROM products")  # Ensure these are the correct column names
            rows = cursor.fetchall()
            connection.close()
            return rows
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e.args[0]}")
        return []
    def populateInventoryTable(self):
        try:
            connection = sqlite3.connect('/Users/ammar/POS Project/POSPY/appData/your_database.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM products")
            records = cursor.fetchall()
            connection.close()

            self.inventoryModel.clear()  # Clear existing items
            self.inventoryModel.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Price"])

            for row_data in records:
                items = [QStandardItem(str(cell_data)) for cell_data in row_data]
                self.inventoryModel.appendRow(items)
        except Exception as e:
            QMessageBox.warning(self, "Error", "Failed to populate inventory table: " + str(e))

    def resetCheckout(self):
        # Clear the invoice table
        self.invoiceTable.setRowCount(0)

        # Clear any other fields if necessary (e.g., input fields)
        self.productIdInput.clear()
        self.quantityInput.clear()

        # Optionally, re-populate the inventory table if needed
        self.populateInventoryTable()

        # Any other reset operations go here
    def generatePDF(self):
        # Get customer details
        name, ok1 = QInputDialog.getText(self, 'Customer Name', 'Enter customer name:')
        if not ok1:
            return  # Exit if the user cancels the input dialog

        phone, ok2 = QInputDialog.getText(self, 'Customer Phone', 'Enter customer phone number:')
        if not ok2:
            return  # Exit if the user cancels the input dialog

        # Save customer details to the database
        connection = sqlite3.connect('/Users/ammar/POS Project/POSPY/appData/customers.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO customers (name, phone) VALUES (?, ?)', (name, phone))
        connection.commit()
        connection.close()
        # Generate filename with format mmhhDDMMYY and employee name
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H%M%d%m%y")  # Format: hourMinuteDayMonthYear
        if self.employee_name:
            filename = f"/Users/ammar/POS Project/POSPY/GUI/invoice_{formatted_time}_{self.employee_name}.pdf"
        else:
            filename = f"/Users/ammar/POS Project/POSPY/GUI/invoice_{formatted_time}_Guest.pdf"

        documentTitle = 'Invoice'
        title = 'Sporto Club'
        subTitle = f"Generated on {current_time.strftime('%Y-%m-%d %H:%M')}"

        pdf = canvas.Canvas(filename, pagesize=letter)
        pdf.setTitle(documentTitle)

        # Create story elements for the PDF
        story = []
        # Define the image path
        image_path = '/Users/ammar/POS Project/POSPY/Testing/MGUI-1-1/logosporto.jpg'

        # Calculate the position to place the image at the bottom-left corner
        image_x = 70  # X-coordinate
        image_y = 70  # Y-coordinate

        # Draw the image at the specified position
        pdf.drawImage(image_path, image_x, image_y, width=100, height=100)

        # Draw the title and subtitle
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(300, 770, title)
        pdf.setFont("Helvetica", 12)
        pdf.drawCentredString(290, 750, subTitle)

        # Draw the table headers
        headers = ('ID', 'Name', 'Quantity', 'Unit Price', 'Total Price')
        header_y = 700
        for index, header in enumerate(headers):
            pdf.drawString(70 + (index * 100), header_y, header)

        # Draw the table rows
        y = header_y - 20
        total_price = 0
        if self.invoiceTable.rowCount() > 0:
            for row in range(self.invoiceTable.rowCount()):
                id_item = self.invoiceTable.item(row, 0)
                name_item = self.invoiceTable.item(row, 1)
                quantity_item = self.invoiceTable.item(row, 2)
                unit_price_item = self.invoiceTable.item(row, 3)

                # Validate and convert quantity and unit price to the correct types
                try:
                    quantity = int(quantity_item.text())
                    unit_price = float(unit_price_item.text())
                except ValueError:
                    QMessageBox.warning(self, "Error", "Invalid quantity or unit price format in invoice table.")
                    return

                # Calculate the total price for the current row
                row_total_price = quantity * unit_price

                # Draw the row values
                pdf.drawString(70, y, str(id_item.text() if id_item else ''))
                pdf.drawString(170, y, str(name_item.text() if name_item else ''))
                pdf.drawString(270, y, str(quantity))
                pdf.drawString(370, y, f"Rs{unit_price:.2f}")
                pdf.drawString(470, y, f"Rs{row_total_price:.2f}")
        
                # Move to the next row position
                y -= 20

                # Update the total price
                total_price += row_total_price

        # Draw the total price
        pdf.drawString(70, y - 20, "Total Price:")
        pdf.drawString(470, y - 20, f"Rs{total_price:.2f}")

        # After setting up the PDF, add customer details at the bottom
        pdf.drawString(70, 50, f"Customer Name: {name}")
        pdf.drawString(70, 35, f"Phone Number: {phone}")
        pdf.drawString(70, 20, f"Serving Employee: {self.employee_name}")


        # Save the PDF file
        pdf.save()
        QMessageBox.information(self, "PDF Generated", f"Invoice saved as {filename}")

    def addProductToInvoice(self):
        productId = self.productIdInput.text()
        quantity = self.quantityInput.text()
        try:
            quantity = int(quantity)
            if self.handleInvoiceEntry(productId, quantity):
                self.refreshInventoryTable()  # Only one call needed here
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid integer for quantity")

    def refreshInventoryTable(self):
        self.populateInventoryTable()
        QApplication.processEvents()  # Force the GUI to process all pending events
    def handleInvoiceEntry(self, productId, quantity):
        # First, check and update inventory
        if not self.checkAndUpdateInventory(productId, quantity):
            return  # Exit if inventory check fails
        # Convert quantity to integer if it's passed as a string
        quantity = int(quantity)

        # Fetch product data from the database
        connection = sqlite3.connect('/Users/ammar/POS Project/POSPY/appData/your_database.db')
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT name, price FROM products WHERE id = ?", (productId,))
            product = cursor.fetchone()

            if product:
                product_name, unit_price = product
                total_price = quantity * unit_price

                # Check if the product is already in the invoice
                product_exists = False
                for row in range(self.invoiceTable.rowCount()):
                    if self.invoiceTable.item(row, 0).text() == str(productId):
                        existing_qty = int(self.invoiceTable.item(row, 2).text())
                        new_qty = existing_qty + quantity
                        self.invoiceTable.item(row, 2).setText(str(new_qty))  # Update the quantity
                        new_total = new_qty * unit_price
                        self.invoiceTable.item(row, 4).setText(str(new_total))  # Update the total price
                        product_exists = True
                        break

                if not product_exists:
                    # Add entry to invoice table
                    rowPosition = self.invoiceTable.rowCount()
                    self.invoiceTable.insertRow(rowPosition)
                    self.invoiceTable.setItem(rowPosition, 0, QTableWidgetItem(str(productId)))
                    self.invoiceTable.setItem(rowPosition, 1, QTableWidgetItem(product_name))
                    self.invoiceTable.setItem(rowPosition, 2, QTableWidgetItem(str(quantity)))
                    self.invoiceTable.setItem(rowPosition, 3, QTableWidgetItem(str(unit_price)))
                    self.invoiceTable.setItem(rowPosition, 4, QTableWidgetItem(str(total_price)))

            else:
                QMessageBox.warning(self, "Error", "Product ID not found")

        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid quantity")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Database Error", str(e))
        finally:
            connection.close()  
