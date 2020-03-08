import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
from PIL import Image
import main

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

defaultImg = 'img/store.png'

class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(850, 150, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##############Widgets of top layout##############
        self.addProductImg = QLabel()
        self.img = QPixmap('icons/addproduct.png')
        self.addProductImg.setPixmap(self.img)
        self.addProductImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add Product")
        self.titleText.setAlignment(Qt.AlignCenter)
        ##############Widgets of top layout##############
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter product name")
        self.manufactureEntry = QLineEdit()
        self.manufactureEntry.setPlaceholderText("Enter manufacture namne")
        self.priceEntry  = QLineEdit()
        self.priceEntry.setPlaceholderText("Enter product price")
        self.quotaEntry = QLineEdit()
        self.quotaEntry.setPlaceholderText("Enter number of products")
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addProduct)
        self.backBtn = QPushButton("Back to Main")
        self.backBtn.clicked.connect(self.backToMain)

    def layouts(self):
        ##############Main Layout##############
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        ##############Add Widgets##############
        ##############Widgets of Top Layout##############
        self.topLayout.addWidget(self.addProductImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        ##############Widgets of Form layout##############
        self.bottomLayout.addRow("Name: ", self.nameEntry)
        self.bottomLayout.addRow("Manufacture: ", self.manufactureEntry)
        self.bottomLayout.addRow("Price: ", self.priceEntry)
        self.bottomLayout.addRow("Quota: ", self.quotaEntry)
        self.bottomLayout.addRow("Product Image: ", self.uploadBtn)
        self.bottomLayout.addRow("", self.backBtn)
        self.bottomLayout.addRow("", self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        ##############Add everything to main layout##############
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def uploadImg(self):
        global defaultImg
        size = (256, 256)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image File (*.jpg *.png)")
        if ok:
            print(self.filename)
            defaultImg = os.path.basename(self.filename)
            print(defaultImg)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img/{0}".format(defaultImg))

    def addProduct(self):
        global defaultImg
        name = self.nameEntry.text()
        manufacturer = self.manufactureEntry.text()
        price = self.priceEntry.text()
        quota = self.quotaEntry.text()

        if name and manufacturer and price and quota != "":
            try:
                query = "INSERT INTO 'products' (product_name, product_manufacturer, product_price, product_quota,product_img) VALUES (?,?,?,?,?)"
                cur.execute(query, (name, manufacturer, price, quota, defaultImg))
                sqlConnect.commit()
                QMessageBox.information(self, "Info", "New product has been added")
                self.close()
                self.main = main.Main()
                self.main.show()
            except:
                QMessageBox.information(self, "Info", "Product has not been added")

        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty!")

    def backToMain(self):
        self.main = main.Main()
        self.main.show()
        self.close()

