from datetime import datetime
import calendar
from PyQt5.QtWidgets import QWidget, QCalendarWidget
from PyQt5.QtCore import QDate


class Calendar(QWidget):
    global currentYear, currentMonth

    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calendar')
        self.setGeometry(800, 300, 350, 250)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.move(20, 20)
        self.calendar.setGridVisible(True)

        self.calendar.setMinimumDate(QDate(currentYear, currentMonth - 1, 1))
        self.calendar.setMaximumDate(
            QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))

        self.calendar.setSelectedDate(QDate(currentYear, currentMonth, 1))

        self.calendar.clicked.connect(self.printDateInfo)

    def printDateInfo(self, qDate):
        print('{}/{}/{}'.format(qDate.day(), qDate.month(), qDate.year()))