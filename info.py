from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

defaultImg = 'img/info.png'


class Info(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon('icons/info.svg'))
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
                           <p>COMP 371: Object Oriented Modeling and Design<p>
                           <p>Professor: Frank Zhang - Ph.D<p>
                           <p>&copy; {} Hieu Le - hieu.le@student.ufv.ca</p>

                       </html>
                       """.format("1.0 ", "2020" + ("" if year == 2020 else " - " + str(year))))
        self.label.setEnabled(False)

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

