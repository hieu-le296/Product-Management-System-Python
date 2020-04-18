import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QFrame, QLabel, QLineEdit, QPushButton, QMessageBox
import hashlib
import main_window

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()


class Login(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Project Management System")
        self.setFixedSize(450, 350)
        self.setWindowIcon(QIcon('icons/help.svg'))
        self.widgets()
        self.layouts()
        style_sheet = """
            QLabel {
                font-size: 15px;
            }
            
            QLineEdit {
                background-color: #f7f7f7;
                color: #000000;
                padding-top: 5px;
                padding-left: 10px;
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

    def widgets(self):
        self.infoImg = QLabel()
        self.img = QPixmap('icons/ufv.png')
        self.infoImg.setPixmap(self.img)
        self.infoImg.setAlignment(Qt.AlignCenter)

        self.titleLabel = QLabel("Project Management System")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("font: bold 24px; color: #99ca3c;")

        self.username = QLineEdit(self)
        self.QUserLabel = QLabel("Username")
        self.username.setPlaceholderText("Enter Username")
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Enter Password")
        self.QPasswordLabel = QLabel("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.btn_Submit = QPushButton("Sign in")
        self.btn_Submit.clicked.connect(self.Submit_btn)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        self.topLayout.addWidget(self.infoImg)
        self.topLayout.addWidget(self.titleLabel)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow("Username: ", self.username)
        self.bottomLayout.addRow("Password: ", self.password)
        self.bottomLayout.addWidget(self.btn_Submit)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def Submit_btn(self):
        USERNAME = self.username.text()
        PASSWORD = self.password.text()
        PASSWORD_HASHED = self.hash_password(PASSWORD)

        try:
            query = "SELECT username, password FROM users WHERE username = ? AND password = ?"
            records = cur.execute(query, (USERNAME, PASSWORD_HASHED)).fetchone()

            username = records[0]
            password = records[1]

            if USERNAME == username and PASSWORD_HASHED == password:
                QMessageBox.information(self, "Success", "Login Successfully")
                self.close()
                self.main = main_window.Main()
                self.main.show()

        except:
            QMessageBox.information(self, "Warning", "Login Failed")
            self.username.setText("")
            self.password.setText("")
