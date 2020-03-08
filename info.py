from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import styles

defaultImg = 'img/info.png'


class Info(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(800, 150, 450, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.styles()

    def widgets(self):
        ##############Widgets of top layout##############
        self.infoImg = QLabel()
        self.img = QPixmap('icons/ufv.png')
        self.infoImg.setPixmap(self.img)
        self.infoImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("COMP 371 - Product Management Application")
        self.titleText.setAlignment(Qt.AlignCenter)
        ##############Widgets of top layout##############
        self.prof = QLabel("Frank Zhang - Ph.D")
        self.studentName = QLabel("Hieu Le")
        self.studentID = QLabel("300148202")
        self.studentEmail = QLabel("hieu.le@student.ufv.ca")

    def layouts(self):
        ##############Main Layout##############
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        ##############Add Widgets##############
        ##############Widgets of Top Layout##############
        self.topLayout.addWidget(self.infoImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        ##############Widgets of Form layout##############
        self.bottomLayout.addRow("Professor: ", self.prof)
        self.bottomLayout.addRow("Student Name: ", self.studentName)
        self.bottomLayout.addRow("Student ID: ", self.studentID)
        self.bottomLayout.addRow("Student Email: ", self.studentEmail)

        self.bottomFrame.setLayout(self.bottomLayout)

        ##############Add everything to main layout##############
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)


    def styles(self):
        self.topFrame.setStyleSheet(styles.infoTopFrame())