from PyQt5.QtPrintSupport import QPrinter
from PyQt5.Qt import QFileInfo
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

class ExportPDF(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Export to PDF")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(850, 450, 370, 150)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.text = QLabel("Select one option", self)
        self.text.move(150, 20)
        self.product = QRadioButton("Products", self)
        self.product.move(40, 50)
        self.member = QRadioButton("Membership", self)
        self.member.move(140, 50)
        self.selling = QRadioButton('Selling History', self)
        self.selling.move(240, 50)
        self.exportBtn = QPushButton("Export PDF", self)
        self.exportBtn.move(150, 100)
        self.exportBtn.clicked.connect(self.export)

    def export(self):
        self.textEdit = QTextEdit(self)
        checked = False
        if self.product.isChecked():
            checked = True
            products = cur.execute("SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_date, product_availability FROM products")
            self.textEdit.append("                                                                              Product List        ")
            for product in products:
                product_id = product[0]
                product_name = product[1]
                product_manu = product[2]
                product_price = product[3]
                product_quota = product[4]
                product_date = product[5]
                product_status = product[6]
                self.textEdit.append("Product ID: " + str(product_id))
                self.textEdit.append("Product Name: " + product_name)
                self.textEdit.append("Manufacturer: " + product_manu)
                self.textEdit.append("Price: $" + str(product_price))
                self.textEdit.append("Quantity: " + str(product_quota))
                self.textEdit.append("Date Added: " + str(product_date))
                self.textEdit.append("Status: " + product_status)
                self.textEdit.append("")
        elif self.member.isChecked():
            checked = True
            members = cur.execute("SELECT * FROM members")
            self.textEdit.append("                                                                                  Membership List        ")
            for member in members:
                member_id = member[0]
                member_fname = member[1]
                member_lname = member[2]
                member_phone = member[3]
                member_addr = member[4]
                self.textEdit.append("Member ID: " + str(member_id))
                self.textEdit.append("First name: " + member_fname)
                self.textEdit.append("Last name: " + str(member_lname))
                self.textEdit.append("Phone number: " + str(member_phone))
                self.textEdit.append("Address: " + str(member_addr))
                self.textEdit.append("")

        elif self.selling.isChecked():
            checked = True
            query = "SELECT products.product_name, products.product_manufacturer, product_price, members.member_fname, sellings.selling_quantity, sellings.selling_amount, sellings.selling_date FROM products, members, sellings WHERE products.product_id = sellings.selling_id AND members.member_id = sellings.selling_member_id"
            history = cur.execute(query).fetchall()
            self.textEdit.append("                                                                               Selling History        ")
            for record in history:
                product_name = record[0]
                product_manu = record[1]
                product_price = record[2]
                member_name = record[3]
                selling_quantity = record[4]
                selling_amount = record[5]
                selling_date = record[6]
                self.textEdit.append("Product Name: " + product_name)
                self.textEdit.append("Manufacturer: " + product_manu)
                self.textEdit.append("Product Price: $" + str(product_price))
                self.textEdit.append("Selling to: " + member_name)
                self.textEdit.append("Quantity: " + str(selling_quantity))
                self.textEdit.append("Amount: $" + str(selling_amount))
                self.textEdit.append("Date Sold: " + str(selling_date))
                self.textEdit.append("")

        if checked is True:
            fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
            if fn != '':
                if QFileInfo(fn).suffix() == "": fn += '.pdf'
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(fn)
                self.textEdit.document().print_(printer)
                QMessageBox.information(self, "Success", "Exporting PDF successfully")
                self.close()
        else:
            QMessageBox.information(self, "Warning", "Please select one")
