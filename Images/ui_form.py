import sys # Import System Runtime 
import sqlite3
from PySide6.QtCore import (QSize, QRect, QCoreApplication ) # Import From PyQTCore
from PySide6.QtGui import (QIcon, QPixmap) # Import from PyQTGui
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QLabel, QPushButton, QDialog, QTableWidget, QTableWidgetItem) # Import from PyQTQidgets
from inventoryWindow import InventoryWindow
from invoiceVerification import InvoiceVerification

class Ui_Widget(QMainWindow): # Inherits QMainWindow From Pyside6
    def setupUi(self, Widget): # Setup the UI In the window 
        Widget.resize(1177, 778) # Set size of the main window
        ## View Inventory Button ##  ##  ##  ##  ##  ##  ##  ##  ##
        self.pushButton = QPushButton(Widget) # Button Created
        self.pushButton.setObjectName(u"pushButton") # Button Named
        self.pushButton.setGeometry(QRect(30, 70, 131, 101)) # Button Resized
        icon = QIcon() # Icon assigned
        # Icon Photo set with path
        icon.addFile(u"/Users/ammar/POS Project/POSPY/Images/Icons/view-inventory.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon) # Icon Saved
        self.pushButton.setIconSize(QSize(60, 60)) # Icon Resized
        self.pushButton.setToolTip("View Inventory") # This text will show when the cursor hovers over this button
        self.pushButton.clicked.connect(self.openInventoryWindow)
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_2 = QPushButton(Widget) # Button Declared
        self.pushButton_2.setObjectName(u"pushButton_2") # Button Name in source
        self.pushButton_2.setGeometry(QRect(30, 170, 131, 101)) # Button dimensions created
        icon1 = QIcon() # Icon Declared 
        # Icon set with path to an image
        icon1.addFile(u"/Users/ammar/POS Project/POSPY/Images/Icons/reciept.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon1) # Icon saved 
        self.pushButton_2.setIconSize(QSize(60, 60)) # Icon resized
        self.pushButton_2.setToolTip("Checkout") # This text will show when the cursor hovers over this button
        self.pushButton_2.clicked.connect(self.openInvoiceVerification) # Button connected to function that opens new window
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_3 = QPushButton(Widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(30, 270, 131, 101))
        icon2 = QIcon()
        icon2.addFile(u"clipboard.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_4 = QPushButton(Widget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(30, 370, 131, 101))
        icon3 = QIcon()
        icon3.addFile(u"inventory copy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QSize(60, 60))
        self.pushButton_5 = QPushButton(Widget)
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(30, 570, 131, 101))
        icon4 = QIcon()
        icon4.addFile(u"budget.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_6 = QPushButton(Widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(30, 470, 131, 101))
        icon5 = QIcon()
        icon5.addFile(u"inventory-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_6.setIcon(icon5)
        self.pushButton_6.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_13 = QPushButton(Widget)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setGeometry(QRect(570, 10, 51, 41))
        icon6 = QIcon()
        icon6.addFile(u"/Users/ammar/POS Project/POSPY/Images/Buttons/home.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_13.setIcon(icon6)
        self.pushButton_13.setIconSize(QSize(30, 30))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_16 = QPushButton(Widget)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setGeometry(QRect(30, 670, 131, 101))
        icon7 = QIcon()
        icon7.addFile(u"boxes.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_16.setIcon(icon7)
        self.pushButton_16.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_18 = QPushButton(Widget)
        self.pushButton_18.setObjectName(u"pushButton_18")
        self.pushButton_18.setGeometry(QRect(1010, 670, 131, 101))
        icon8 = QIcon()
        icon8.addFile(u"customer-service.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_18.setIcon(icon8)
        self.pushButton_18.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_19 = QPushButton(Widget)
        self.pushButton_19.setObjectName(u"pushButton_19")
        self.pushButton_19.setGeometry(QRect(1010, 270, 131, 101))
        self.pushButton_19.setIcon(icon4)
        self.pushButton_19.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_20 = QPushButton(Widget)
        self.pushButton_20.setObjectName(u"pushButton_20")
        self.pushButton_20.setGeometry(QRect(1010, 470, 131, 101))
        self.pushButton_20.setIcon(icon1)
        self.pushButton_20.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_21 = QPushButton(Widget)
        self.pushButton_21.setObjectName(u"pushButton_21")
        self.pushButton_21.setGeometry(QRect(1010, 370, 131, 101))
        self.pushButton_21.setIcon(icon7)
        self.pushButton_21.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_22 = QPushButton(Widget)
        self.pushButton_22.setObjectName(u"pushButton_22")
        self.pushButton_22.setGeometry(QRect(1010, 170, 131, 101))
        icon9 = QIcon()
        icon9.addFile(u"coins.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_22.setIcon(icon9)
        self.pushButton_22.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_23 = QPushButton(Widget)
        self.pushButton_23.setObjectName(u"pushButton_23")
        self.pushButton_23.setGeometry(QRect(1010, 70, 131, 101))
        self.pushButton_23.setIcon(icon2)
        self.pushButton_23.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_24 = QPushButton(Widget)
        self.pushButton_24.setObjectName(u"pushButton_24")
        self.pushButton_24.setGeometry(QRect(1010, 570, 131, 101))
        self.pushButton_24.setIcon(icon5)
        self.pushButton_24.setIconSize(QSize(60, 60))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(-190, -100, 1451, 981))
        self.label.setPixmap(QPixmap(u"../../../Downloads/cool-background-3.png"))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ## ##  
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(-10, 10, 1211, 821))
        self.label_2.setPixmap(QPixmap(u"/Users/ammar/POS Project/POSPY/Images/Logos/NEGASOL-logos_black.png"))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(-10, -10, 1211, 791))
        self.label_3.setPixmap(QPixmap(u"/Users/ammar/POS Project/POSPY/Images/Backgrounds/cool-background.png"))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_14 = QPushButton(Widget)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setGeometry(QRect(470, 10, 51, 41))
        icon10 = QIcon()
        icon10.addFile(u"/Users/ammar/POS Project/POSPY/Images/Buttons/Back Button.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_14.setIcon(icon10)
        self.pushButton_14.setIconSize(QSize(30, 30))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.pushButton_15 = QPushButton(Widget)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setGeometry(QRect(670, 10, 51, 41))
        icon11 = QIcon()
        icon11.addFile(u"/Users/ammar/POS Project/POSPY/Images/Buttons/Reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_15.setIcon(icon11)
        self.pushButton_15.setIconSize(QSize(30, 30))
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
        self.label_3.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.pushButton_3.raise_()      # These 
        self.pushButton_4.raise_()      # Will
        self.pushButton_5.raise_()      # Appear
        self.pushButton_6.raise_()      # On Top of
        self.pushButton_13.raise_()     # Other
        self.pushButton_16.raise_()     # Widgets.
        self.pushButton_2.raise_()
        self.pushButton.raise_()
        self.pushButton_18.raise_()
        self.pushButton_19.raise_()
        self.pushButton_20.raise_()
        self.pushButton_21.raise_()
        self.pushButton_22.raise_()
        self.pushButton_23.raise_()
        self.pushButton_24.raise_()
        self.pushButton_14.raise_()
        self.pushButton_15.raise_()
        ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  
    ## Funtions for open Windows for every respective button
    def openInventoryWindow(self):
        self.inventoryWindow = InventoryWindow(self)
        self.inventoryWindow.show()    

    def openInvoiceVerification(self):
        self.invoiceVerification = InvoiceVerification(self)
        self.invoiceVerification.show()    

if __name__ == "__main__":
    app = QApplication([])
    window = Ui_Widget()
    window.setupUi(window)
    window.show()
    sys.exit(app.exec())