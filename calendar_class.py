import sqlite3

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()


class Calendar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calendar')
        self.setWindowIcon(QIcon("icons/calendar.svg"))
        self.UI()
        self.show()

    def UI(self):
        vbox = QVBoxLayout()
        self.setGeometry(1000, 300, 350, 300)

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked[QDate].connect(self.showDate)

        vbox.addWidget(cal)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText('{}/{}/{}'.format(date.day(), date.month(), date.year()))

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

    def showDate(self, date):
        date_format = '{}/{}/{}'.format(date.day(), date.month(), date.year())
        query = "SELECT COUNT(selling_id) FROM sellings WHERE selling_date = ?"
        number_of_records = cur.execute(query, (date_format,)).fetchall()

        self.lbl.setText(date_format + " - " + str(number_of_records[0][0]) + " records found.")

