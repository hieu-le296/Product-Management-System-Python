from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

defaultImg = 'img/info.png'


class Info(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(800, 150, 500, 500)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.setStyleSheet("QLabel {font-size: 20px}")

    def widgets(self):
        ##############Widgets of top layout##############
        self.infoImg = QLabel()
        self.img = QPixmap('icons/ufv.png')
        self.infoImg.setPixmap(self.img)
        self.infoImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("COMP 371 - Product Management Application v1.0")
        ##############Widgets of top layout##############
        self.prof = QLabel("Professor: Frank Zhang - Ph.D")
        self.studentName = QLabel("Student Name: Hieu Le")
        self.studentEmail = QLabel("Student Email: hieu.le@student.ufv.ca")

    def layouts(self):
        ##############Main Layout##############
        self.mainLayout = QVBoxLayout()

        ##############Add Widgets##############
        ##############Widgets of Top Layout##############
        self.mainLayout.addWidget(self.infoImg)
        self.mainLayout.addWidget(self.titleText)
        self.mainLayout.addWidget(self.prof)
        self.mainLayout.addWidget(self.studentName)
        self.mainLayout.addWidget(self.studentEmail)
        self.mainLayout.setAlignment(Qt.AlignCenter)

        ##############Add everything to main layout##############
        self.setLayout(self.mainLayout)

