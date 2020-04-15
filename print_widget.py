from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

class Print(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Print Preview")
        self.setWindowIcon(QIcon('icons/printer.svg'))
        self.setGeometry(850, 450, 250, 180)
        self.setFixedSize(self.size())
        self.widgets()
        self.layouts()
        self.setWindowIcon(QIcon('icons/printer.svg'))
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
        self.product.setChecked(True)
        self.member = QRadioButton("Membership", self)
        self.selling = QRadioButton('Selling History', self)
        self.previewBtn = QPushButton("Print Preview", self)
        self.previewBtn.clicked.connect(self.printPreviewDialog)
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

        self.bottomLayout.addWidget(self.previewBtn)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

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


    def printPreviewDialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()

    def printPreview(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        if self.product.isChecked():
            self.displayProduct()
            self.handlePrintedView(self.productTable, cursor, printer)
        elif self.member.isChecked():
            self.displayMember()
            self.handlePrintedView(self.memberTable, cursor, printer)
        elif self.selling.isChecked():
            self.displaySellingRecord()
            self.handlePrintedView(self.sellingTable, cursor, printer)
        document.print_(printer)

    def handlePrintedView(self, table, cursor, printer):
        self.displayProduct()
        new_table = cursor.insertTable(
            table.rowCount(), table.columnCount())
        for row in range(new_table.rows()):
            for col in range(new_table.columns()):
                cursor.insertText(table.item(row, col).text())
                cursor.movePosition(QTextCursor.NextCell)



