import sys
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
#Hello
class CustomerManagement(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(None)
        self.setWindowTitle("Manage Customers")
        self.resize(1177, 778)
        self.initUI() 
        # Add more UI setup code here (like tables, buttons, etc.)
    
    def initUI(self):
        pass
