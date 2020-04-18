import os
import re

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime

import sqlite3
from PIL import Image

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

defaultImg = 'store.png'

# Create mouse clicked event for QLineEdit
class ClickedQLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def __init__(self, widget):
        super().__init__(widget)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()


class AddProduct(QDialog):
    date = ''

    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon('icons/add.svg'))
        self.UI()
        style_sheet = """
        

        QLabel {
            font-size: 30px;
        }

        QLineEdit {
            background-color: #f7f7f7; 
            color: #000000; 
            padding-top: 5px; 
            padding-left: 10px;
        }

        QPushButton {
            color: #ffffff;
            border-radius: 10px;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
        }



        """
        self.setStyleSheet(style_sheet)
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##############Widgets of top layout##############
        self.addProductImg = QLabel()
        self.img = QPixmap('icons/add.svg')
        self.addProductImg.setPixmap(self.img)
        self.addProductImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add Product")
        self.titleText.setAlignment(Qt.AlignCenter)

        ##############Widgets of top layout##############
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Name")
        self.manufactureEntry = QLineEdit(self)
        self.manufactureEntry.setPlaceholderText("Enter Manufacturer")
        self.priceEntry = QLineEdit(self)
        self.priceEntry.setPlaceholderText("Enter Price")
        self.quotaEntry = QLineEdit(self)
        self.quotaEntry.setPlaceholderText("Enter Quantity")

        x = datetime.now()
        global datePickEntry
        dateString = '{}/{}/{}'.format(x.day, x.month, x.year)
        datePickEntry = ClickedQLineEdit(self)
        datePickEntry.setText(dateString)
        datePickEntry.setReadOnly(True)
        datePickEntry.clicked.connect(self.openCalendar)

        self.uploadBtn = QPushButton("Browse Product Image")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.uploadBtn.setStyleSheet("background-color: #35A69B;")
        self.submitBtn = QPushButton("Add")
        self.submitBtn.clicked.connect(self.addProduct)
        self.submitBtn.setStyleSheet("background-color: #5AA1C2;")

    def layouts(self):
        ##############Main Layout##############
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QVBoxLayout()
        self.topFrame = QFrame()

        ##############Add Widgets##############
        ##############Widgets of Top Layout##############
        self.topLayout.addWidget(self.addProductImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        ##############Widgets of Bottom layout##############
        self.bottomLayout.addWidget(self.nameEntry)
        self.bottomLayout.addWidget(self.manufactureEntry)
        self.bottomLayout.addWidget(self.priceEntry)
        self.bottomLayout.addWidget(self.quotaEntry)
        self.bottomLayout.addWidget(datePickEntry)
        self.bottomLayout.addWidget(self.uploadBtn)
        self.bottomLayout.addWidget(self.submitBtn)

        ##############Add everything to main layout##############
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def uploadImg(self):
        global defaultImg
        size = (320, 240)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image File (*.jpg *.png)")
        if ok:
            defaultImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img/{0}".format(defaultImg))

    def addProduct(self):
        global defaultImg
        global datePickEntry
        name = self.nameEntry.text()
        manufacturer = self.manufactureEntry.text()
        num_format = re.compile(r'^\-?[1-9][0-9]*\.?[0-9]*')
        price = self.priceEntry.text()
        quota = self.quotaEntry.text()
        if (not num_format.match(price)) or (not num_format.match(quota)):
            QMessageBox.information(self, "Info", "Price or quota must be a number")
            checked = False
        else:
            checked = True

        if datePickEntry.text() != '':
            productDate = datePickEntry.text()
        else:
            productDate = None
        if name and manufacturer and price and quota != "" and checked is True:
            try:
                query = "INSERT INTO 'products' (product_name, product_manufacturer, product_price, product_quota,product_img, product_date) VALUES (?,?,?,?,?,?)"
                cur.execute(query, (name, manufacturer, price, quota, defaultImg, productDate))
                sqlConnect.commit()
                QMessageBox.information(self, "Info", "New product has been added")
                self.close()

            except:
                QMessageBox.information(self, "Info", "Product has not been added")

        else:
            QMessageBox.information(self, "Info", "Product has not been added")

    def openCalendar(self):
        self.open = Calendar()


class Calendar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calendar')
        self.UI()
        self.show()

    def UI(self):
        vbox = QVBoxLayout()
        self.setGeometry(1100, 300, 350, 300)
        self.setWindowTitle('Calendar')

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked[QDate].connect(self.showDate)

        vbox.addWidget(cal)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        global dateSelected
        dateSelected = '{}/{}/{}'.format(date.day(), date.month(), date.year())
        self.lbl.setText(dateSelected)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

    def showDate(self, date):
        global datePickEntry
        dateSelected = '{}/{}/{}'.format(date.day(), date.month(), date.year())
        self.lbl.setText(dateSelected)
        datePickEntry.setText(dateSelected)


