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
        self.setGeometry(850, 450, 250, 150)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.text = QLabel("Select one option", self)
        self.text.move(85, 20)
        self.product = QRadioButton("Products", self)
        self.product.move(40, 50)
        self.member = QRadioButton("Membership", self)
        self.member.move(140, 50)
        self.exportBtn = QPushButton("Export PDF", self)
        self.exportBtn.move(90, 100)
        self.exportBtn.clicked.connect(self.export)

    def export(self):
        self.textEdit = QTextEdit(self)
        checked = False
        if self.product.isChecked():
            checked = True
            query = cur.execute("SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability FROM products")
            self.textEdit.append("                Product List        ")
            self.textEdit.append("(product ID, product name, manufacturer, price, quota, availability)")
            for row_data in query:
                self.textEdit.append(str(row_data))
        elif self.member.isChecked():
            checked = True
            query = cur.execute("SELECT * FROM members")
            self.textEdit.append("                Membership List        ")
            self.textEdit.append("(member id, first name, last name, phone number, address)")
            for row_member in query:
                self.textEdit.append(str(row_member))

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
