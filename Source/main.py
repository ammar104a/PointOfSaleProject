import sqlite3
import prettytable
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox
import sqlite3
import prettytable
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox

# Connect to the SQLite database (create a new one if it doesn't exist)
conn = sqlite3.connect('your_database.db')
# Create a cursor object to execute SQL queries
cursor = conn.cursor()
# Example: Create a products table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        quantity INTEGER,
        price REAL
    )
''')
conn.commit() # Commit the changes


# Add Product To Inventory
def add_product(name, quantity, price):
    try:
        # Check if the product already exists in the database
        cursor.execute("SELECT * FROM products WHERE name=?", (name,)) # cursor.execute: This function is used to execute a SQL query on the database. In this case, the query being executed is a SELECT query.
        # "SELECT * FROM products WHERE name=?": This is the SQL SELECT query itself. It selects all columns (*) from the table named "products" where the value in the "name" column matches a parameter that will be provided.
        # name,): This is a tuple containing a single element, which is the value you want to substitute for the placeholder (?) in the SQL query. The value is provided by the variable name.
        existing_product = cursor.fetchone()
        # existing_product = cursor.fetchone(): After executing the SQL query, this line fetches the first row of the result set returned by the query and assigns it to the variable existing_product.
        # The result set contains the data from the columns specified in the SELECT query for the row(s) that match the specified condition.
        if existing_product:
            # Product already exists
            existing_quantity = existing_product[2]
            existing_price = existing_product[3]
            # Update the quantity and/or price if specified
            new_quantity = existing_quantity + quantity
            new_price = price if price is not None else existing_price
            cursor.execute("UPDATE products SET quantity=?, price=? WHERE name=?", (new_quantity, new_price, name))
            conn.commit()
            if quantity > 0:
                print(f"Product '{name}' already exists. Quantity updated to '{new_quantity}'.")
            if price is not None:
                print(f"Product '{name}' already exists. Price updated to '{new_price}'.")
        else:
            # Product doesn't exist, insert a new product
            cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
            conn.commit()
            print(f"New product '{name}' added to the database with quantity '{quantity}' and price '{price}'.")
    except Exception as e:
        print(f"Error: {e}")
# Remove product from database by quantity.
def remove_quantity(product_name, quantity_to_remove):
    try:
        # Check if the product exists
        cursor.execute("SELECT * FROM products WHERE name=?", (product_name,))
        product = cursor.fetchone()

        if product:
            current_quantity = product[2]  # Assuming quantity is at index 2
            if current_quantity >= quantity_to_remove:
                new_quantity = current_quantity - quantity_to_remove
                cursor.execute("UPDATE products SET quantity=? WHERE name=?", (new_quantity, product_name))
                conn.commit()
                print(f"Removed {quantity_to_remove} units of '{product_name}'. New quantity: {new_quantity}")
            else:
                print(f"Error: Not enough quantity of '{product_name}' to remove.")
        else:
            print(f"Error: Product '{product_name}' not found.")
    except Exception as e:
        print(f"Error: {e}")
# View Database
def view_database():
    try:
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        if not rows:
            print("No products found in the database.")
            return

        table = prettytable.PrettyTable()
        table.field_names = ["ID", "Product Name", "Quantity", "Price"]

        for row in rows:
            table.add_row([row[0], row[1], row[2], row[3]])

        print(table)
    except Exception as e:
        print(f"Error: {e}")
# Get Product Price From Database
def fetch_price(product_name):
        cursor.execute("SELECT price FROM products WHERE name=?", (product_name,))
        result = cursor.fetchone()
        return result[0] if result else None
# Update Quantity of Products after Stuff has Been sold
def update_quantity(product_name, quantity):
        cursor.execute("SELECT quantity FROM products WHERE name=?", (product_name,))
        result = cursor.fetchone()
        if result:
            current_quantity = result[0]
            new_quantity = max(0, current_quantity - quantity)  # Ensure the quantity doesn't go below 0
            cursor.execute("UPDATE products SET quantity=? WHERE name=?", (new_quantity, product_name))
            conn.commit()
            print(f"Updated quantity for '{product_name}' to {new_quantity}.")
        else:
            print(f"Error: Product '{product_name}' not found in the database.")
# Create Invoice
def create_invoice_pdf(products):
        pdf = FPDF()
        # Add a page to the PDF
        pdf.add_page()
        # Set font
        pdf.set_font("Arial", size=12)
        # Display header
        pdf.cell(200, 10, txt="Invoice", ln=True, align='C')
        # Display table headers
        pdf.cell(50, 10, txt="Product Name", border=1)
        pdf.cell(30, 10, txt="Quantity", border=1)
        pdf.cell(30, 10, txt="Unit Price", border=1)
        pdf.cell(30, 10, txt="Total Price", border=1)
        pdf.ln()
        total_price = 0

        # Display product details
        for product in products:
            unit_price = fetch_price(product['name'])
            
            if unit_price is not None:
                total_price += unit_price * product['quantity']

                pdf.cell(50, 10, txt=product['name'], border=1)
                pdf.cell(30, 10, txt=str(product['quantity']), border=1)
                pdf.cell(30, 10, txt=f"Rs{unit_price:.2f}", border=1)
                pdf.cell(30, 10, txt=f"Rs{unit_price * product['quantity']:.2f}", border=1)
                pdf.ln()

                # Update the quantity in the database
                update_quantity(product['name'], product['quantity'])
            else:
                print(f"Error: Product '{product['name']}' not found in the database.")

            # Display total
        pdf.ln(10)
        pdf.cell(140, 10, txt="Total:", border=1)
        pdf.cell(30, 10, txt=f"Rs{total_price:.2f}", border=1)

        # Save the PDF file
        pdf.output("invoice.pdf")
# Remove the whole Product
def remove_product_by_name(product_name):
    try:
        # Check if the product exists
        cursor.execute("SELECT * FROM products WHERE name=?", (product_name,))
        product = cursor.fetchone()

        if product:
            # Execute the DELETE statement
            cursor.execute("DELETE FROM products WHERE name=?", (product_name,))
            conn.commit()

            print(f"Product '{product_name}' removed successfully.")
        else:
            print(f"Error: Product '{product_name}' not found.")

    except Exception as e:
        print(f"Error: {e}")


print("Welcome!")
print("Press 1 to make an Invoice,")
print("Press 2 to view Inventory.")
print("Press 3 to add to Inventory.")
print("Press 4 to delete from Inventory.")
print("Press 5 to view previous Invoices.")
print("Press 6 to view Customers and their contact info.")
print("Press 7 for accounts.")


# Taking user input from The User
user_integer = int(input("Select an Option: "))

if user_integer == 1:
    # Connect to the SQLite database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    if __name__ == "__main__":
        # Prompt user for product names and quantities
        products_list = []
        while True:
            product_name = input("Enter product name (type 'exit' to finish): ")
            if product_name.lower() == 'exit':
                break

            quantity = int(input("Enter quantity: "))
            products_list.append({"name": product_name, "quantity": quantity})

        # Call the function with the list of products
        create_invoice_pdf(products_list)

    # Close the database connection
    conn.close()

if user_integer == 2:
    view_database()

if user_integer == 3:
    nme = input("Enter the product name: ")
    qtty = int(input("Enter quantity to add: "))
    price = input("Enter product price: ")
    add_product(nme, qtty, price)

if user_integer == 4:
    print("Press 1 to Remove a product from the database and 2 to remove product by quantity.")
    user_input = int(input("Enter an integer: "))
    if user_input == 2:
        nme = input("Enter a product name: ")
        qtty = int(input("Enter Quantity to remove: "))
        remove_quantity(nme, qtty)
    elif user_input == 1:
        nme = input("Enter a product name: ")
        remove_product_by_name(nme)
        

