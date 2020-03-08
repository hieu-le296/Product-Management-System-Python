from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import styles
import main

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

class DisplayMember(QWidget):
    memberId = 0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Membership Detail")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(850, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.memberDetails()
        self.widgets()
        self.layouts()
        self.styles()

    def widgets(self):
        #################Top layouts wigdets#########
        self.memberImg = QLabel()
        self.img = QPixmap('icons/members.png')
        self.memberImg.setPixmap(self.img)
        self.memberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Display Membership")
        self.titleText.setAlignment(Qt.AlignCenter)

        #################Bottom layouts wigdets#########
        self.fnameEntry = QLineEdit()
        self.fnameEntry.setText(self.memberFname)
        self.lnameEntry = QLineEdit()
        self.lnameEntry.setText(self.memberLname)
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setText(self.memberPhone)
        self.addressEntry = QLineEdit()
        self.addressEntry.setText(self.memberAddress)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateMember)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteMember)
        self.backBtn = QPushButton("Back to Main")
        self.backBtn.clicked.connect(self.backToMain)



    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        #################Add wigdets#########
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.memberImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("First Name: "), self.fnameEntry)
        self.bottomLayout.addRow(QLabel("Last Name: "), self.lnameEntry)
        self.bottomLayout.addRow(QLabel("Phone: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel("Full Address: "), self.addressEntry)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)
        self.bottomLayout.addRow(QLabel(""), self.backBtn)
        self.bottomLayout.addRow(QLabel(""), self.updateBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def memberDetails(self):
        try:
            query = ("SELECT * FROM members WHERE member_id =?")
            member = cur.execute(query, (self.memberId,)).fetchone()

            self.memberFname = member[1]
            self.memberLname = member[2]
            self.memberPhone = member[3]
            self.memberAddress = member[4]
        except:
            QMessageBox.information(self, "Error", "Member has been deleted. Program exited.")



    def deleteMember(self):
        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this member?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if mbox == QMessageBox.Yes:
            try:
                query = "DELETE FROM members WHERE member_id=?"
                cur.execute(query, (DisplayMember.memberId,))
                sqlConnect.commit()
                QMessageBox.information(self, "Info", "Member has been deleted")
                self.backToMain()
                self.close()

            except:
                QMessageBox.information(self, "Info", "Member has not been deleted")


    def updateMember(self):
        fname = self.fnameEntry.text()
        lname = self.lnameEntry.text()
        phone = self.phoneEntry.text()
        address = self.addressEntry.text()
        emptyString = ""

        if fname != "" and lname == "" and phone == "" and address == "":
            try:
                query = "UPDATE members set member_fname = ?, member_lname = ?, member_phone = ?, member_address = ? WHERE member_id = ?"
                cur.execute(query, (fname, emptyString, emptyString, emptyString, self.memberId))
                sqlConnect.commit()
                QMessageBox.information(self, "Info", "Membership has been updated")
                self.backToMain()
                self.close()
            except:
                QMessageBox.information(self, "Info", "Membership has not been updated")


        elif fname and lname and phone and address != "":
            try:
                query = "UPDATE members set member_fname = ?, member_lname = ?, member_phone = ?, member_address = ? WHERE member_id = ?"
                cur.execute(query, (fname, lname, phone, address, self.memberId))
                sqlConnect.commit()
                QMessageBox.information(self, "Info", "Membership has been updated")
                self.backToMain()
                self.close()
            except:
                QMessageBox.information(self, "Info", "Membership has not been updated")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty!")

    def backToMain(self):
        self.main = main.Main()
        self.main.show()
        self.close()

    def styles(self):
        self.topFrame.setStyleSheet(styles.memberTopFrame())
        self.bottomFrame.setStyleSheet(styles.memberBottomFrame())