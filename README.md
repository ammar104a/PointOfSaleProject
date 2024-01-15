# All In One Point of Sale System

This is an all in one point of sale system created in python and pyside6.

Features:
1) View Inventory: Users Can View Their Inventory.
    - Add Product: Add a product to the inventory(ID, Name, Quantity, Price)
    - Low Stock Warnings: Users can set a minimum quantity for a product.
                    - If the product <= Min the program displays a warning.
    - Search Inventory by Product Name.
    - Search Inventory by Product ID
    - Live Editing of the Inventory Viewer: Users can edit any field by clicking it.

2) Checkout: Lets Users Check Customers out.
    - Asks for employee key to login the specific employee as all employee shift data   and sales are saved and organized.
    - Current logged in employee name also shows up on printed invoice.
    - Option to enter master key "582002" to add a new employee (ID, Name, Shift)
    - Top Half Shows Curent Inventory(Un-editable) and bottom half shows items that have been added to the invoice by the user.
    - Bottom of the window - Field for Product ID and underneath it a field for product quantity.
    - Add To Invoice Button: Adds the product to the invoice; uses the product id and the quantity given by the user.(To Be replaced by Barcode Scanner Input where the quantity is 1 by default.)
    - Print Invoice: (Asks For Customer Name and Customner Phone Number before printing the invoice.) Generates a pdf that contains all of the products added to the invoice, unit price, quantity, price(Unit Price * Quantity), Total, Grand Total, Customer name, Customer Phone Number, Current Serving Employee, Company Logo (png/jpg). 

3) Accounts: Under Development.

4) Analytics: Under Development.

5) Customers: Displays All Customers That Are Saved Manually Or Through Printing Invoices In Checkout.
    - Merge Customers: Merges all duplicate customers. If Both Name and phone number are the same, one of them is deleted. (The functionality of this button is curently being changed so that it only checks for similar phone numbers and not names.)
    - Add Customer: Add New Customers Manually.
    - Remove Customer: Select One Or More Customer(s), Select both name and number and then press this button.
    - Edit Phone Number: Edit any Customers Phone Number by selecting thier name and number and then pressing this button. WARNING: Do-Not Select More than one customer before selecting this option, you may lose customer data.
    - Export To Excel: WIll Ask the user a location to save the csv file and will then save the database as an excel sheet.

6) Employees: Shows All Employees, Their name, Key and ShiftNo.
    - Shift Number functionality still has to be added in this program as the shift number has curently no meaning.
    - Add Employee: Add Employee By name, key and shift number.
    - Remove Employee: Remove Employee By Key.
    - Change Employee Shift: Change Shift By Key.

7) Security Features:
    - 8 Digit Numerical Code for each Employee.
    - Logged In Employee will be saved in logs and their name will be printed in invoices.
    - Most Buttons Can Only be Accessed By The Master Key.

Problems:
    - MAJOR PROBLEM THROUGHOUT THE PROGRAM WHERE THE INVENTORY/CUSTOMER/EMPLOYEE DATABASES DO NOT REFRESH INSTANTANIOUSLY EVEN AFTER CHANGES HAVE BEEN MADE. PROPER STATEMENTS HAVE BEEN ADDED TO REPOPULATE THE TABLES BUT THEY REFUSE TO REFRESH. MAYBE A PYQT PROBLEM OR WE ARE MISSING SOMETHING.

Credit:
1) NEGASOL: Network & Gateway Solutions
