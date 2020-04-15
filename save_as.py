import csv
import os

from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.Qt import QFileInfo
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

class SaveAs(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save As")
        self.setWindowIcon(QIcon('icons/pdf.svg'))
        self.setGeometry(850, 450, 250, 180)
        self.setFixedSize(self.size())
        self.widgets()
        self.layouts()
        self.show()

    def widgets(self):
        self.productTable = QTableWidget()
        self.productTable.setColumnCount(7)
        self.memberTable = QTableWidget()
        self.memberTable.setColumnCount(5)
        self.sellingTable = QTableWidget()
        self.sellingTable.setColumnCount(9)
        self.text = QLabel("Select one option", self)
        self.product = QRadioButton("Products", self)
        self.member = QRadioButton("Membership", self)
        self.selling = QRadioButton('Selling History', self)
        self.exportCSVBtn = QPushButton("CSV", self)
        self.exportCSVBtn.clicked.connect(self.exportCSV)
        self.exportPDFBtn = QPushButton("PDF", self)
        self.exportPDFBtn.clicked.connect(self.exportPDF)
        self.setStyleSheet("QLabel {font-size: 15px} QRadioButton {font-size: 12px}")

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.topFrame = QFrame()

        self.topLayout.addWidget(self.text)
        self.topLayout.addWidget(self.product)
        self.topLayout.addWidget(self.member)
        self.topLayout.addWidget(self.selling)
        self.topLayout.setAlignment(Qt.AlignCenter)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addWidget(self.exportCSVBtn)
        self.bottomLayout.addWidget(self.exportPDFBtn)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def exportPDF(self):
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
                self.textEdit.append("-----------------------------------------------------")
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
                self.textEdit.append("-----------------------------------------------------")

        elif self.selling.isChecked():
            checked = True
            query = "SELECT products.product_name, products.product_manufacturer, products.product_price, members.member_fname, sellings.selling_quantity, sellings.selling_amount, sellings.selling_date FROM products, members, sellings WHERE products.product_id = sellings.selling_product_id AND members.member_id = sellings.selling_member_id"
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
                self.textEdit.append("-----------------------------------------------------")

        if checked is True:
            fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
            if fn != '':
                if QFileInfo(fn).suffix() == "": fn += '.pdf'
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(fn)
                self.textEdit.document().print_(printer)
                QMessageBox.information(self, "Success", "Exported to PDF successfully")
                self.close()
        else:
            QMessageBox.information(self, "Warning", "Please select one")

    def displayProduct(self):
        for i in reversed(range(self.productTable.rowCount())):
            self.productTable.removeRow(i)

        query = cur.execute(
            "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_date, product_availability FROM products")
        for row_data in query:
            row_number = self.productTable.rowCount()
            self.productTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def displayMember(self):
        for i in reversed(range(self.memberTable.rowCount())):
            self.memberTable.removeRow(i)

        members = cur.execute("SELECT * FROM members")
        for row_data in members:
            row_number = self.memberTable.rowCount()
            self.memberTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.memberTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def displaySellingRecord(self):
        for i in reversed(range(self.sellingTable.rowCount())):
            self.sellingTable.removeRow(i)

        query = "SELECT sellings.selling_id, products.product_name, products.product_manufacturer, products.product_price, members.member_fname, sellings.selling_quantity, sellings.discount_rate, sellings.selling_amount, sellings.selling_date " \
                "FROM products, members, sellings " \
                "WHERE products.product_id = sellings.selling_product_id AND members.member_id = sellings.selling_member_id"
        records = cur.execute(query)
        for row_data in records:
            row_number = self.sellingTable.rowCount()
            self.sellingTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.sellingTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def exportCSV(self):
        checked = False
        if self.product.isChecked():
            checked = True
            self.displayProduct()
            self.saveSheet(self.productTable)
        elif self.member.isChecked():
            checked = True
            self.displayMember()
            self.saveSheet(self.memberTable)
        elif self.selling.isChecked():
            checked = True
            self.displaySellingRecord()
            self.saveSheet(self.sellingTable)

        if checked is True:
            QMessageBox.information(self, "Success", "Saved As CSV successfully")
            self.close()
        else:
            QMessageBox.information(self, "Warning", "Please select one")


    # Reference: https://gist.github.com/anonymous/50d1eb86c957d35df2967d6be8479d22
    def saveSheet(self, table):
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(table.rowCount()):
                    row_data = []
                    for column in range(table.columnCount()):
                        item = table.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)