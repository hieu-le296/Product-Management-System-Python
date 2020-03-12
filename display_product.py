from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image
from datetime import datetime
import os
import sqlite3
import main_window

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()


class DisplayProduct(QWidget):
    productId = 0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Detail")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(800, 150, 400, 700)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.productDetails()
        self.widgets()
        self.layouts()
        self.setStyleSheet("QLabel {font-size: 15px}")

    def widgets(self):
        #################Top layouts wigdets#########
        self.product_Img = QLabel()
        self.img = QPixmap('img/{}'.format(self.productImg))
        self.product_Img.setPixmap(self.img)
        self.product_Img.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Update Product")
        self.titleText.setStyleSheet("QLabel {font-size: 30px}")
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

        x = datetime.now()
        global datePickEntry
        dateString = '{}/{}/{}'.format(x.day, x.month, x.year)
        datePickEntry = QLineEdit()
        datePickEntry.setText(dateString)

        self.dateBtn = QPushButton("...")
        self.dateBtn.clicked.connect(self.openCalendar)
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
        self.bottomLayout.addRow("Date: ", datePickEntry)
        self.bottomLayout.addRow("", self.dateBtn)
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
            self.productStatus = product[7]
        except:
            QMessageBox.information(self, "Error", "This product has been deleted.")

    def uploadImg(self):
        size = (320, 240)
        self.filename, ok = QFileDialog.getOpenFileName(self, 'Upload Image', '', 'Image files (*.jpg *.png)')
        if ok:
            self.productImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img/{0}".format(self.productImg))

    def openCalendar(self):
        self.open = Calendar()

    def updateProduct(self):
        global datePickEntry
        name = self.nameEntry.text()
        manufacturer = self.manufacturerEntry.text()
        price = int(self.priceEntry.text())
        quota = int(self.quotaEntry.text())
        status = self.availabilityCombo.currentText()
        defaultImg = self.productImg
        if datePickEntry.text() != '':
            productDate = datePickEntry.text()
        else:
            productDate = None

        if (name and manufacturer and price and quota != " "):
            try:
                query = "UPDATE products set product_name = ?, product_manufacturer =?, product_price = ?, product_quota = ?, product_img = ?, product_date = ?, product_availability = ? WHERE product_id = ?"
                cur.execute(query, (name, manufacturer, price, quota, defaultImg, productDate, status, self.productId))
                sqlConnect.commit()
                QMessageBox.information(self, "Info", "Product has been updated")
                self.close()
                self.main = main_window.Main()
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
                self.main = main_window.Main()
                self.main.show()
            except:
                QMessageBox.information(self, "Information", "Product has not been deleted")

    def backToMain(self):
        self.main = main_window.Main()
        self.main.show()
        self.close()

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


