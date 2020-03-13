from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QFrame, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3
import hashlib


sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()


class ChangePassword(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Change Password")
        self.widgets()
        self.layout()
        self.show()

    def widgets(self):
        self.infoImg = QLabel()
        self.img = QPixmap('icons/ufv.png')
        self.infoImg.setPixmap(self.img)
        self.infoImg.setAlignment(Qt.AlignCenter)

        self.currentPassword = QLineEdit(self)
        self.currentPassword.setEchoMode(QLineEdit.Password)
        self.newPassword = QLineEdit()
        self.newPassword.setEchoMode(QLineEdit.Password)
        self.confirmNewPassword = QLineEdit()
        self.confirmNewPassword.setEchoMode(QLineEdit.Password)
        self.btn_Submit = QPushButton("Change Password")
        self.btn_Submit.clicked.connect(self.Submit_btn)

    def layout(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        self.topLayout.addWidget(self.infoImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow("Current Password: ", self.currentPassword)
        self.bottomLayout.addRow("New Password: ", self.newPassword)
        self.bottomLayout.addRow("Confirm New Password: ", self.confirmNewPassword)
        self.bottomLayout.addRow("", self.btn_Submit)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        print(user_password)
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    def Submit_btn(self):
        current_password = self.currentPassword.text()
        new_password = self.newPassword.text()
        confirm_password = self.confirmNewPassword.text()
        current_password_hashed = self.hash_password(current_password)

        try:
            query = "SELECT user_id, password FROM users WHERE password = ?"
            records = cur.execute(query, (current_password_hashed,)).fetchone()

            userId = records[0]
            oldPassword = records[1]

            if current_password_hashed == oldPassword:
                if new_password == confirm_password:
                    confirm_password_hashed = self.hash_password(confirm_password)
                    passwordQuery = "UPDATE users set password = ? WHERE user_id = ?"
                    cur.execute(passwordQuery, (confirm_password_hashed, userId))
                    sqlConnect.commit()
                    QMessageBox.information(self, "Info", "Password Updated Successfully!")
                    self.close()
                else:
                    QMessageBox.information(self, "Warning", "Confirmed Password does not match New Password")
        except:
            QMessageBox.information(self, "Warning", "Change Password Failed")
            self.currentPassword.setText("")
            self.newPassword.setText("")
            self.confirmNewPassword.setText("")
