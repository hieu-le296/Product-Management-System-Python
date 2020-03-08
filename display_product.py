from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image
import os
import sqlite3
import styles
import main

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()


class DisplayProduct(QWidget):
    productId = 0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Detail")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(850, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.productDetails()
        self.widgets()
        self.layouts()
        self.styles()

    def widgets(self):
        #################Top layouts wigdets#########
        self.product_Img = QLabel()
        self.img = QPixmap('{}'.format(self.productImg))
        self.product_Img.setPixmap(self.img)
        self.product_Img.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Update Product")
        self.titleText.setAlignment(Qt.AlignCenter)

        ##############Bottom Layout's widgets###########
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.productName)
        self.manufacturerEntry = QLineEdit()
        self.manufacturerEntry.setText(self.productManufacturer)
        self.priceEntry = QLineEdit()
        self.priceEntry.setText(str(self.productPrice))
        self.quotaEntry = QLineEdit()
        self.quotaEntry.setText(str(self.productQuota))
        self.availabilityCombo = QComboBox()
        self.availabilityCombo.addItems(["Available", "UnAvailable"])
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteProduct)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateProduct)
        self.backBtn = QPushButton("Back to Main")
        self.backBtn.clicked.connect(self.backToMain)


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        ###########Add Widgets##########
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.product_Img)
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacture: "), self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Price: "), self.priceEntry)
        self.bottomLayout.addRow(QLabel("Quota: "), self.quotaEntry)
        self.bottomLayout.addRow(QLabel("Status: "), self.availabilityCombo)
        self.bottomLayout.addRow(QLabel("Image: "), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)
        self.bottomLayout.addRow(QLabel(""), self.backBtn)
        self.bottomLayout.addRow(QLabel(""), self.updateBtn)

        ###########Set Layouts##########
        self.topFrame.setLayout(self.topLayout)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def productDetails(self):
        try:
            query = ("SELECT * FROM products WHERE product_id=?")
            product = cur.execute(query, (self.productId,)).fetchone()  # single item tuple = (1,)
            self.productName = product[1]
            self.productManufacturer = product[2]
            self.productPrice = product[3]
            self.productQuota = product[4]
            self.productImg = product[5]
            self.productStatus = product[6]
        except:
            QMessageBox.information(self, "Error", "This product has been deleted.")

    def uploadImg(self):
        size = (256, 256)
        self.filename, ok = QFileDialog.getOpenFileName(self, 'Upload Image', '', 'Image files (*.jpg *.png)')
        if ok:
            self.productImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img{0}".format(self.productImg))

    def updateProduct(self):
        name = self.nameEntry.text()
        manufacturer = self.manufacturerEntry.text()
        price = int(self.priceEntry.text())
        quota = int(self.quotaEntry.text())
        status = self.availabilityCombo.currentText()
        defaultImg = self.productImg

        if (name and manufacturer and price and quota != " "):
            try:
                query = "UPDATE products set product_name = ?, product_manufacturer =?, product_price = ?, product_quota = ?, product_img = ?, product_availability =? WHERE product_id = ?"
                cur.execute(query, (name, manufacturer, price, quota, defaultImg, status, self.productId))
                sqlConnect.commit()
                QMessageBox.information(self, "Info", "Product has been updated")
                self.close()
                self.main = main.Main()
                self.main.show()
            except:
                QMessageBox.information(self, "Info", "Product has not been updated")

        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")

    def deleteProduct(self):
        mbox = QMessageBox.question(self, "Wanrning", "Are you sure to delete this product?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (mbox == QMessageBox.Yes):
            try:
                cur.execute("DELETE FROM products WHERE product_id=?", (self.productId,))
                sqlConnect.commit()
                QMessageBox.information(self, "Information", "Product has been deleted")
                self.close()
                self.main = main.Main()
                self.main.show()
            except:
                QMessageBox.information(self, "Information", "Product has not been deleted")

    def backToMain(self):
        self.main = main.Main()
        self.main.show()
        self.close()

    def styles(self):
        self.bottomFrame.setStyleSheet(styles.productBottomFrame())
        self.topFrame.setStyleSheet(styles.productTopFrame())
