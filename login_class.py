import sqlite3
import sys
import qdarkstyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QFrame, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QApplication
import main_window

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

class Login(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Login")
        self.widgets()
        self.layouts()

    def widgets(self):
        self.infoImg = QLabel()
        self.img = QPixmap('icons/ufv.png')
        self.infoImg.setPixmap(self.img)
        self.infoImg.setAlignment(Qt.AlignCenter)


        self.username = QLineEdit(self)
        self.QUserLabel = QLabel("Username")
        self.password = QLineEdit(self)
        self.QPasswordLabel = QLabel("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.btn_Submit = QPushButton("LOGIN")
        self.btn_Submit.clicked.connect(self.Submit_btn)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        self.topLayout.addWidget(self.infoImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow("Username: ", self.username)
        self.bottomLayout.addRow("Password: ", self.password)
        self.bottomLayout.addRow("", self.btn_Submit)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def Submit_btn(self):
        USERNAME = self.username.text()
        PASSWORD = self.password.text()

        try:
            query = "SELECT username, password FROM users WHERE username = ? AND password = ?"
            records = cur.execute(query, (USERNAME, PASSWORD)).fetchone()

            username = records[0]
            password = records[1]

            if USERNAME == username and PASSWORD == password:
                QMessageBox.information(self, "Success", "Login Successfully")
                self.close()
                self.main = main_window.Main()
                self.main.show()

        except:
            QMessageBox.information(self, "Warning", "Login Failed")
            self.username.setText("")
            self.password.setText("")


def main():
    App = QApplication(sys.argv)
    window = Login()
    window.show()
    App.setStyleSheet(qdarkstyle.load_stylesheet())
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()