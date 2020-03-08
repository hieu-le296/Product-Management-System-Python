from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import main

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
        self.product.move(40, 50)
        self.member = QRadioButton("Membership", self)
        self.member.move(140, 50)
        self.printBtn = QPushButton("Export PDF", self)
        self.printBtn.move(90, 100)
        self.printBtn.clicked.connect(self.printPreviewDialog)

    def printPreviewDialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()

    def printPrewview(self, printer):
        self.textEdit = QTextEdit()
        self.textEdit.document().print_(printer)
