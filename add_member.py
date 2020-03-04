import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
from PIL import Image

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

defaultImg = 'img/store.png'

class AddMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Member")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 350, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##############widgets of top layout################
        self.addMemberImg = QLabel()
        self.img = QPixmap('icons/addmember.png')
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add Member")
        self.titleText.setAlignment(Qt.AlignCenter)

        ##############widgets of bottom layout################
        self.fnameEntry = QLineEdit()
        self.fnameEntry.setPlaceholderText("Enter member first name")
        self.lnameEntry = QLineEdit()
        self.lnameEntry.setPlaceholderText("Enter member last name")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter member phone")
        self.addressEntry = QLineEdit()
        self.addressEntry.setPlaceholderText("Enter member full address")
        self.submitBtn = QPushButton("Submit")



    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        ##############Add Widgets################
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.addMemberImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("First Name: "), self.fnameEntry)
        self.bottomLayout.addRow(QLabel("Last Name: "), self.lnameEntry)
        self.bottomLayout.addRow(QLabel("Phone Number: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel("Full Address: "), self.addressEntry)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

