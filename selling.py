from PyQt5 import QtPrintSupport, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from datetime import datetime
import sqlite3
import styles
import main

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

defaultImg = 'img/store.png'


class SellProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selling Product")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(800, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.fetchData()
        self.styles()

    def widgets(self):
        ##############Widgets of Top Layout##############
        self.productImg = QLabel(self)
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
        self.submitBtn.clicked.connect(self.sellProduct)
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
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.productImg)
        self.topFrame.setLayout(self.topLayout)

        ##############Widgets of Bottom Layout##############
        self.bottomLayout.addRow(QLabel("Product: "), self.productCombo)
        self.bottomLayout.addRow(QLabel("Selling to: "), self.memberCombo)
        self.bottomLayout.addRow(QLabel("Quantity: "), self.quantityCombo)
        self.bottomLayout.addRow(QLabel(""), self.backBtn)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
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

    def sellProduct(self):
        global productName, productId, memberName, memberId, quantity
        productName = self.productCombo.currentText()
        productId = self.productCombo.currentData()
        memberName = self.memberCombo.currentText()
        memberId = self.memberCombo.currentData()
        quantity = int(self.quantityCombo.currentText())
        self.confirm = ConfirmWindow()
        self.close()

    def backToMain(self):
        self.main = main.Main()
        self.main.show()
        self.close()

    def styles(self):
        self.topFrame.setStyleSheet(styles.sellProductTopFrame())
        self.bottomFrame.setStyleSheet(styles.sellProductBottomFrame())


class ConfirmWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sell Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(850, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.styles()

    def widgets(self):
        ##############widgets of top layout################
        self.productImg = QLabel()
        self.img = QPixmap('icons/shop.png')
        self.productImg.setPixmap(self.img)
        self.productImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Sell Product")
        self.titleText.setAlignment(Qt.AlignCenter)

        ##############widgets of bottom layout################
        global productName, productId, memberName, memberId, quantity, price
        priceQuery = "SELECT product_price FROM products WHERE product_id =?"
        price = cur.execute(priceQuery, (productId,)).fetchone()
        self.amount = quantity * price[0]

        self.productName = QLabel()
        self.productName.setText(productName)
        self.memberName = QLabel()
        self.memberName.setText(memberName)
        self.amountLabel = QLabel()
        self.amountLabel.setText(str(price[0]) + "x" + str(quantity) + " = $" + str(self.amount))
        x = datetime.now()
        self.dateString = '{}/{}/{}'.format(x.day, x.month, x.year)
        self.dateSold = QLabel()
        self.dateSold.setText(self.dateString)
        self.confirmBtn = QPushButton("Confirm")
        self.confirmBtn.clicked.connect(self.confirm)

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.append("Selling Receipt")
        self.textEdit.append("Product: " + productName)
        self.textEdit.append("Customer Name: " + memberName)
        self.textEdit.append("Quantity: " + str(quantity))
        self.textEdit.append("Amount: $" + str(price[0]) + "x" + str(quantity) + " = $" + str(self.amount))

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        ##############Add Widgets################
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.productImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addWidget(self.textEdit)
        self.bottomLayout.addRow(QLabel(""), self.confirmBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def confirm(self):
        global productName, productId, memberName, memberId, quantity

        try:
            sellQuery = "INSERT INTO 'sellings' (selling_product_id, selling_member_id, selling_quantity, selling_amount, selling_date) VALUES (?,?,?,?,?)"
            quotaQuery = ("SELECT product_quota FROM products WHERE product_id =?")
            cur.execute(sellQuery, (productId, memberId, quantity, self.amount, self.dateString))
            self.quota = cur.execute(quotaQuery, (productId,)).fetchone()
            sqlConnect.commit()

            if (quantity == self.quota[0]):
                updateQuotaQuery = "UPDATE products set product_quota =?, product_availability =? WHERE product_id =? "
                cur.execute(updateQuotaQuery, (0, 'UnAvailable', productId))
                sqlConnect.commit()
            else:
                newQuota = (self.quota[0] - quantity)
                updateQuotaQuery = "UPDATE products set product_quota =? WHERE product_id =?"
                cur.execute(updateQuotaQuery, (newQuota, productId))
                sqlConnect.commit()

            mbox = QMessageBox.question(self, "Success", "Would you like to print a selling receipt?", QMessageBox.Yes | QMessageBox.No)
            if mbox == QMessageBox.Yes:
                self.printReceipt()

            self.close()
            self.main = main.Main()
            self.main.show()
        except:
            QMessageBox.information(self, "Info", "Something went wrong")

    def printReceipt(self):
        # Create printer
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.textEdit.document().print_(dialog.printer())
    def styles(self):
        self.topFrame.setStyleSheet(styles.confirmProductTopFrame())
        self.bottomFrame.setStyleSheet(styles.confirmProductBottomFrame())
