from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

defaultImg = 'img/info.png'


class Help(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon('icons/help.svg'))
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##############Widgets of top layout##############
        self.infoImg = QLabel()
        self.img = QPixmap('icons/ufv.png')
        self.infoImg.setPixmap(self.img)
        self.infoImg.setAlignment(Qt.AlignCenter)
        ##############Widgets of top layout##############
        self.label = QTextEdit()
        year = datetime.now().year
        self.label.setText("""
                       <html style="color: white; font-size: 15px;">
                           <span style="font-size: 20px; font-weight: bold;">Product Management System v{}</span>
                           <p>Features: Add Product, Add Membership, Sell Product, Print, Export to PDF, Change Password<p>
                           <p>Usage:<p>
                           <p>+For each time you add product, add membership or sell the product, or update something please click on Refresh icon to populate data<p>
                           <p>+When you click on the item or member on the table row, the information will be shown on the right<p>
                           <p>+If you want to update the product or membership, simply double click on the table row<p>
                           <p>Some useful shortcuts:<p>
                           <p>+Ctrl+A (Command+A in Mac): Add a product<p>
                           <p>+Ctrl+M (Command+M in Mac): Add a member<p>
                           <p>+Ctrl+P (Command+P in Mac): Print<p>
                           <p>+Ctrl+S (Command+S in Mac): Export to PDF file<p>
                           <p>+Ctrl+E (Command+E in Mac): Selling a product<p>
                           <p>+Ctrl+O (Command+O in Mac): Logout<p>
                           <p>+Ctrl+R (Command+R in Mac): Refresh the window<p>
                       </html>
                       """.format("1.0 ", "2020" + ("" if year == 2020 else " - " + str(year))))
        self.label.setReadOnly(True)

    def layouts(self):
        ##############Main Layout##############
        self.mainLayout = QVBoxLayout()

        ##############Add Widgets##############
        ##############Widgets of Top Layout##############
        self.mainLayout.addWidget(self.infoImg)
        self.mainLayout.addWidget(self.label)
        self.mainLayout.setAlignment(Qt.AlignCenter)

        ##############Add everything to main layout##############
        self.setLayout(self.mainLayout)

