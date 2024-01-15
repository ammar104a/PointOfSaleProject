import sys # Import System Runtime 
import sqlite3
from PySide6.QtCore import QTimer, QTime, QDate
from PySide6.QtCore import (QSize, QRect, QMetaObject, QCoreApplication ) # Import From PyQTCore
from PySide6.QtGui import (QIcon, QPixmap) # Import from PyQTGui
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QStatusBar, QMenuBar, QWidget, QStackedWidget, QLabel, QPushButton, QDialog, QTableWidget, QTableWidgetItem) # Import from PyQTQidgets
from inventoryWindow import InventoryWindow
from invoiceVerification import InvoiceVerification
from manageEmployees import ManageEmployees
from customerManagement import CustomerManagement
class Ui_MainWindow(object):
    def update_clock_and_date(self):
        # Update the clock label with the current time and day
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        current_time_12_hour = current_time.toString('h:mm:ss AP')  # 12-hour format with AM/PM
        current_day = current_date.toString('dddd')  # Full day name

        # Combine time and day
        current_time_and_day = f'{current_time_12_hour} - {current_day}'
        self.Clocklabel.setText(current_time_and_day)
        
        # Update the date label with the current date
        current_date = QDate.currentDate().toString('MM-dd-yyyy')
        self.dateandtime.setText(current_date)
        

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(u"All In One Point of Sale System")
        MainWindow.resize(1177, 778)
        MainWindow.setStyleSheet("QMainWindow {"
                         "    background-image: url('C:/Users/ammar/PythonProjects/PointOfSale/Images/Backgrounds/SportoBgFHD.jpg');\n"
                         "    background-repeat: no-repeat;"
                         "    background-position: center center;"
                         "}")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ViewInventory = QPushButton(self.centralwidget)
        self.ViewInventory.setObjectName(u"ViewInventory")
        self.ViewInventory.setGeometry(QRect(40, 100, 201, 181))
        self.ViewInventory.setStyleSheet(u"QPushButton {\n"
"    border: none; /* Removes the border */\n"
"    background-color: transparent; /* Makes the background transparent */\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(r"C:\Users\ammar\PythonProjects\PointOfSale\Images\Icons\Viewnventory1.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ViewInventory.setIcon(icon)
        self.ViewInventory.setIconSize(QSize(150, 150))
        self.ViewInventory.clicked.connect(self.openInventoryWindow)
        self.accounts = QPushButton(self.centralwidget)
        self.accounts.setObjectName(u"accounts")
        self.accounts.setGeometry(QRect(40, 500, 201, 181))
        self.accounts.setStyleSheet(u"QPushButton {\n"
"    border: none; /* Removes the border */\n"
"    background-color: transparent; /* Makes the background transparent */\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(r"C:\Users\ammar\PythonProjects\PointOfSale\Images\Icons\Accounts1.png", QSize(), QIcon.Normal, QIcon.Off)
        self.accounts.setIcon(icon1)
        self.accounts.setIconSize(QSize(150, 150))
        self.checkout = QPushButton(self.centralwidget)
        self.checkout.setObjectName(u"checkout")
        self.checkout.setGeometry(QRect(40, 300, 201, 181))
        self.checkout.setStyleSheet(u"QPushButton {\n"
"    border: none; /* Removes the border */\n"
"    background-color: transparent; /* Makes the background transparent */\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(r"C:\Users\ammar\PythonProjects\PointOfSale\Images\Icons\Checkout1.png", QSize(), QIcon.Normal, QIcon.Off)
        self.checkout.setIcon(icon2)
        self.checkout.setIconSize(QSize(150, 150))
        self.checkout.clicked.connect(self.openInvoiceVerification) # Button connected to function that opens new window
        self.Customers = QPushButton(self.centralwidget)
        self.Customers.setObjectName(u"Customers")
        self.Customers.setGeometry(QRect(940, 300, 201, 181))
        self.Customers.setStyleSheet(u"QPushButton {\n"
"    border: none; /* Removes the border */\n"
"    background-color: transparent; /* Makes the background transparent */\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(r"C:\Users\ammar\PythonProjects\PointOfSale\Images\Icons\ManageCustomers1.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Customers.setIcon(icon3)
        self.Customers.setIconSize(QSize(800, 800))
        self.Customers.clicked.connect(self.openCustomerManagement)
        self.analytics = QPushButton(self.centralwidget)
        self.analytics.setObjectName(u"analytics")
        self.analytics.setGeometry(QRect(940, 100, 200, 181))
        self.analytics.setStyleSheet(u"QPushButton {\n"
"    border: none; /* Removes the border */\n"
"    background-color: transparent; /* Makes the background transparent */\n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(r"C:\Users\ammar\PythonProjects\PointOfSale\Images\Icons\Analytics1.png", QSize(), QIcon.Normal, QIcon.Off)
        self.analytics.setIcon(icon4)
        self.analytics.setIconSize(QSize(150, 150))
        self.employees = QPushButton(self.centralwidget)
        self.employees.setObjectName(u"employees")
        self.employees.setGeometry(QRect(940, 500, 201, 181))
        self.employees.setStyleSheet(u"QPushButton {\n"
"    border: none; /* Removes the border */\n"
"    background-color: transparent; /* Makes the background transparent */\n"
"}\n"
"")
        icon5 = QIcon()
        icon5.addFile(r"C:\Users\ammar\PythonProjects\PointOfSale\Images\Icons\ManageEmployees1.png", QSize(), QIcon.Normal, QIcon.Off)
        self.employees.setIcon(icon5)
        self.employees.setIconSize(QSize(150, 150))
        self.employees.clicked.connect(self.openManageEmployees) # Button connected to function that opens new window

        
        self.Clocklabel = QLabel(self.centralwidget)
        self.Clocklabel.setObjectName(u"Clocklabel")
        self.Clocklabel.setGeometry(QRect(460, 30, 150, 21))
        self.Clocklabel.setStyleSheet("color: white;")
        self.dateandtime = QLabel(self.centralwidget)
        self.dateandtime.setObjectName(u"dateandtime")
        self.dateandtime.setGeometry(QRect(660, 30, 121, 21))
        self.dateandtime.setStyleSheet("color: white;")

        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.update_clock_and_date)
        self.timer.start(1000)  # Update every second

        self.Activation = QLabel(self.centralwidget)
        self.Activation.setObjectName(u"Activation")
        self.Activation.setStyleSheet("color: white;")
        self.Activation.setGeometry(QRect(50, 30, 201, 16))
        self.Negasol = QPushButton(self.centralwidget)
        self.Negasol.setObjectName(u"Negasol")
        self.Negasol.setGeometry(QRect(1070, 10, 81, 81))
        self.Negasol.setStyleSheet(u"QPushButton {\n"
"    border: none; /* Removes the border */\n"
"    background-color: transparent; /* Makes the background transparent */\n"
"}\n"
"")
        icon6 = QIcon()
        icon6.addFile(r"C:\Users\ammar\PythonProjects\PointOfSale\Images\Logos\NEGASOL-logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Negasol.setIcon(icon6)
        self.Negasol.setIconSize(QSize(100, 100))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1177, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        MainWindow.setToolTip(QCoreApplication.translate("MainWindow", u"Visit Negasol", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ViewInventory.setToolTip(QCoreApplication.translate("MainWindow", u"View Inventory", None))
#endif // QT_CONFIG(tooltip)
        self.ViewInventory.setText("")
#if QT_CONFIG(tooltip)
        self.accounts.setToolTip(QCoreApplication.translate("MainWindow", u"Accounts", None))
#endif // QT_CONFIG(tooltip)
        self.accounts.setText("")
#if QT_CONFIG(tooltip)
        self.checkout.setToolTip(QCoreApplication.translate("MainWindow", u"Checkout", None))
#endif // QT_CONFIG(tooltip)
        self.checkout.setText("")
#if QT_CONFIG(tooltip)
        self.Customers.setToolTip(QCoreApplication.translate("MainWindow", u"Customers", None))
#endif // QT_CONFIG(tooltip)
        self.Customers.setText("")
#if QT_CONFIG(tooltip)
        self.analytics.setToolTip(QCoreApplication.translate("MainWindow", u"Analytics", None))
#endif // QT_CONFIG(tooltip)
        self.analytics.setText("")
#if QT_CONFIG(tooltip)
        self.employees.setToolTip(QCoreApplication.translate("MainWindow", u"Manage Employees", None))
#endif // QT_CONFIG(tooltip)
        self.employees.setText("")
        self.Clocklabel.setText(QCoreApplication.translate("MainWindow", u"clockLabel", None))
        self.dateandtime.setText(QCoreApplication.translate("MainWindow", u"Date and time", None))
        self.Activation.setText(QCoreApplication.translate("MainWindow", u"Activation Status: <font color='green'>Active</font>", None))
        self.Negasol.setText("")
    # retranslateUi
## Funtions for open Windows for every respective button
    def openInventoryWindow(self):
        print("Opening Inventory Window")  # Debugging print
        self.inventoryWindow = InventoryWindow(self)
        self.inventoryWindow.show()    

    def openInvoiceVerification(self):
        print("Opening Invoice Verification Window")  # Debugging print
        self.invoiceVerification = InvoiceVerification(self)
        self.invoiceVerification.show() 

    def openManageEmployees(self):
        print("Opening Manage Employees Window") # Debugging Print
        self.manageEmployees = ManageEmployees()  # Remove the 'self' parameter
        self.manageEmployees.show()  # Show the window

    def openCustomerManagement(self):
        print("Opening Customer Management Window") # Debugging Print
        self.customerManagement = CustomerManagement()  # Remove the 'self' parameter
        self.customerManagement.show()  # Show the window 
   

if __name__ == "__main__":
    app = QApplication([])
    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec())
