from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

defaultImg = 'img/store.png'


class AddMember(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Member")
        self.setWindowIcon(QIcon('icons/users.svg'))
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
                   background-color: #35A69B; 
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
        ##############widgets of top layout################
        self.addMemberImg = QLabel()
        self.img = QPixmap('icons/users.svg')
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add Membership")
        self.titleText.setStyleSheet("QLabel {font-size: 30px}")
        self.titleText.setAlignment(Qt.AlignCenter)

        ##############widgets of bottom layout################
        self.fnameEntry = QLineEdit()
        self.fnameEntry.setPlaceholderText("Enter first name")
        self.lnameEntry = QLineEdit()
        self.lnameEntry.setPlaceholderText("Enter last name")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter phone #")
        self.addressEntry = QLineEdit()
        self.addressEntry.setPlaceholderText("Enter full address")
        self.submitBtn = QPushButton("Add")
        self.submitBtn.clicked.connect(self.addMember)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QVBoxLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        ##############Add Widgets################
        self.topLayout.addWidget(self.addMemberImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addWidget(self.fnameEntry)
        self.bottomLayout.addWidget(self.lnameEntry)
        self.bottomLayout.addWidget(self.phoneEntry)
        self.bottomLayout.addWidget(self.addressEntry)
        self.bottomLayout.addWidget(self.submitBtn)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)

    def addMember(self):
        fname = self.fnameEntry.text()
        lname = self.lnameEntry.text()
        phone = self.phoneEntry.text()
        address = self.addressEntry.text()
        emptyString = ""

        if fname != "" and lname == "" and phone == "" and address == "":
            try:
                query = "INSERT INTO 'members' (member_fname, member_lname, member_phone, member_address) VALUES (?,?,?,?)"
                cur.execute(query, (fname, emptyString, emptyString, emptyString))
                sqlConnect.commit()
                QMessageBox.information(self, "Info", "New member has been added")
                self.close()
            except:
                QMessageBox.information(self, "Info", "New member has not been added")
        elif fname and lname and phone and address != "":
            try:
                query = "INSERT INTO 'members' (member_fname, member_lname, member_phone, member_address) VALUES (?,?,?,?)"
                cur.execute(query, (fname, lname, phone, address))
                sqlConnect.commit()
                QMessageBox.information(self, "Info", "New member has been added")
                self.close()
            except:
                QMessageBox.information(self, "Info", "New member has not been added")

        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty!")