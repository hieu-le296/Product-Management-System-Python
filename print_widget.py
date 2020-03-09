from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

class Print(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Export to PDF")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(850, 450, 250, 150)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.text = QLabel("Select one option", self)
        self.text.move(85, 20)
        self.product = QRadioButton("Products", self)
        self.product.setChecked(True)
        self.product.move(40, 50)
        self.member = QRadioButton("Membership", self)
        self.member.move(140, 50)
        self.printBtn = QPushButton("Open Print Dialog", self)
        self.printBtn.move(90, 100)
        self.printBtn.clicked.connect(self.printPreviewDialog)

    def printPreviewDialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()

    def printPreview(self, printer):
        self.textEdit = QTextEdit(self)
        if self.product.isChecked():
            query = cur.execute(
                "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability FROM products")
            self.textEdit.append("                Product List        ")
            self.textEdit.append("(product ID, product name, manufacturer, price, quota, availability)")
            for row_data in query:
                self.textEdit.append(str(row_data))
        elif self.member.isChecked():
            query = cur.execute("SELECT * FROM members")
            self.textEdit.append("                Membership List        ")
            self.textEdit.append("(member id, first name, last name, phone number, address)")
            for row_member in query:
                self.textEdit.append(str(row_member))

        self.textEdit.document().print_(printer)



