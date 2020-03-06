import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image
import sqlite3

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

defaultImg = 'img/store.png'


class SellProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selling Product")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.fetchData()

    def widgets(self):
        ##############Widgets of Top Layout##############
        self.productImg = QLabel()
        self.img = QPixmap('icons/shop.png')
        self.productImg.setPixmap(self.img)
        self.productImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Sell Product")
        self.titleText.setAlignment(Qt.AlignCenter)
        ##############Widgets of Bottom Layout##############
        self.productCombo = QComboBox()
        self.productCombo.currentIndexChanged.connect(self.changeComboValue)
        self.memberCombo = QComboBox()
        self.quantityCombo = QComboBox()
        self.submitBtn = QPushButton("Submit")

        # query1 = "SELECT * FROM products WHERE product_availability =?"
        # query2 = "SELECT member_id, member_fname from members"
        # products = cur.execute(query1, ('Available',)).fetchall()
        # members = cur.execute(query2).fetchall()
        # quantity = products[0][4]
        #
        # for product in products:
        #     self.productCombo.addItem(product[1], product[0])
        #
        # for member in members:
        #     self.memberCombo.addItem(member[1], member[0])
        #
        # for i in range(1, quantity + 1):
        #     self.quantityCombo.addItem(str(i))


    def layouts(self):
        ##############Main Layout##############
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        ##############Add Widgets##############
        ##############Widgets of Top Layout##############
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.productImg)
        self.topFrame.setLayout(self.topLayout)

        ##############Widgets of Bottom Layout##############
        self.bottomLayout.addRow(QLabel("Product: "), self.productCombo)
        self.bottomLayout.addRow(QLabel("Selling to: "), self.memberCombo)
        self.bottomLayout.addRow(QLabel("Quantity: "), self.quantityCombo)
        self.bottomLayout.addRow(QLabel(": "), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def fetchData(self):
        query1 = "SELECT * FROM products WHERE product_availability =?"
        query2 = "SELECT member_id, member_fname from members"
        products = cur.execute(query1, ('Available',)).fetchall()
        members = cur.execute(query2).fetchall()
        quantity = products[0][4]


        for product in products:
            self.productCombo.addItem(product[1], product[0])

        for member in members:
            self.memberCombo.addItem(member[1], member[0])

        self.quantityCombo.clear()

        for i in range(1, quantity + 1):
            self.quantityCombo.addItem(str(i))

    def changeComboValue(self):
        self.quantityCombo.clear()
        product_id = self.productCombo.currentData()
        query = ("SELECT product_quota FROM products WHERE product_id =?")
        quota = cur.execute(query, (product_id,)).fetchone()

        for i in range(1, quota[0] + 1):
            self.quantityCombo.addItem(str(i))





