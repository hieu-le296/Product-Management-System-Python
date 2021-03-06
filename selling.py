from PyQt5 import QtPrintSupport, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from datetime import datetime
import sqlite3

import main_window

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

defaultImg = 'img/store.png'


class SellProduct(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selling Product")
        self.setWindowIcon(QIcon('icons/sell.svg'))
        self.UI()
        style_sheet = """
                       QLabel {
                           font-size: 15px;
                       }

                       QPushButton {
                           background-color: #5AA1C2;
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
        self.fetchData()


    def widgets(self):
        ##############Widgets of Top Layout##############
        self.productImg = QLabel(self)
        self.img = QPixmap('icons/sell.svg')
        self.productImg.setPixmap(self.img)
        self.productImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Sell Product")
        self.titleText.setStyleSheet("QLabel {font-size: 30px}")
        self.titleText.setAlignment(Qt.AlignCenter)
        ##############Widgets of Bottom Layout##############
        self.productCombo = QComboBox()
        self.productCombo.currentIndexChanged.connect(self.changeComboProductValue)
        self.memberCombo = QComboBox()
        self.quantityCombo = QComboBox()
        self.discountCombo = QComboBox()
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.sellProduct)

    def layouts(self):
        ##############Main Layout##############
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        ##############Add Widgets##############
        ##############Widgets of Top Layout##############
        self.topLayout.addWidget(self.productImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        ##############Widgets of Bottom Layout##############
        self.bottomLayout.addRow(QLabel("Product: "), self.productCombo)
        self.bottomLayout.addRow(QLabel("Selling to: "), self.memberCombo)
        self.bottomLayout.addRow(QLabel("Quantity: "), self.quantityCombo)
        self.bottomLayout.addRow(QLabel("Discount: "), self.discountCombo)
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

        self.discountCombo.clear()
        for discount in range(5, 51):
            self.discountCombo.addItem(str(discount) + "%")


    def changeComboProductValue(self):
        self.quantityCombo.clear()
        product_id = self.productCombo.currentData()
        query = ("SELECT product_quota FROM products WHERE product_id =?")
        quota = cur.execute(query, (product_id,)).fetchone()

        for i in range(1, quota[0] + 1):
            self.quantityCombo.addItem(str(i))

    def sellProduct(self):
        global productName, productId, memberName, memberId, quantity, discount, discount_text
        productName = self.productCombo.currentText()
        productId = self.productCombo.currentData()
        memberName = self.memberCombo.currentText()
        memberId = self.memberCombo.currentData()
        quantity = int(self.quantityCombo.currentText())
        discount_text = self.discountCombo.currentText()
        discount = discount_text.split("%")
        discount = int(discount[0])
        self.confirm = ConfirmWindow()
        self.close()


class ConfirmWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sell Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.UI()
        style_sheet = """
                    QLabel {
                        font-size: 15px;
                        }

                    QPushButton {
                        background-color: #5AA1C2;
                        color: #ffffff;
                        border-radius: 10px;
                        font: bold 14px;
                        min-width: 10em;
                        padding: 6px;
                        }

                    QTextEdit {
                        font-size: 15px
                        }

                    """
        self.setStyleSheet(style_sheet)
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##############widgets of top layout################
        self.productImg = QLabel()
        self.img = QPixmap('icons/sell.svg')
        self.productImg.setPixmap(self.img)
        self.productImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Sell Product")
        self.titleText.setStyleSheet("QLabel {font-size: 30px}")
        self.titleText.setAlignment(Qt.AlignCenter)

        ##############widgets of bottom layout################
        global productName, productId, memberName, memberId, quantity, price, discount, discount_text
        priceQuery = "SELECT product_price FROM products WHERE product_id =?"
        price = cur.execute(priceQuery, (productId,)).fetchone()
        discount_amount = ((quantity * price[0]) * discount) / 100
        self.amount = quantity * price[0] - discount_amount

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
        self.textEdit.append("########Selling Receipt#######")
        self.textEdit.append("Product: " + productName)
        self.textEdit.append("Customer Name: " + memberName)
        self.textEdit.append("Quantity: " + str(quantity))
        self.textEdit.append("Discount: " + str(discount_text))
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
        global productName, productId, memberName, memberId, quantity, discount

        try:
            sellQuery = "INSERT INTO 'sellings' (selling_product_id, selling_member_id, selling_quantity, discount_rate, selling_amount, selling_date) VALUES (?,?,?,?,?,?)"
            quotaQuery = ("SELECT product_quota FROM products WHERE product_id =?")
            cur.execute(sellQuery, (productId, memberId, quantity, discount, self.amount, self.dateString))
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
        except:
            QMessageBox.information(self, "Info", "Something went wrong")

    def printReceipt(self):
        # Create printer
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.textEdit.document().print_(dialog.printer())
