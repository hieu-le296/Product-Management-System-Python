import sqlite3
import sys
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import add_member
import add_product
import display_product
import display_member
import export_pdf
import print_widget
import calendar_class
import info
import selling
import styles

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Management")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 1350, 750)
        #self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.createMenu()
        self.displayProduct()
        self.displayMember()
        self.getStat()
        self.getSellingHistory()
        self.styles()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        ############Toolbar Buttons##########
        ############Add Product##############
        self.addProduct = QAction(QIcon('icons/add.png'), "Add Product", self)
        self.addProduct.triggered.connect(self.funcAddProduct)
        self.tb.addAction(self.addProduct)
        self.tb.addSeparator()
        ############Add Member##############
        self.addMember = QAction(QIcon('icons/users.png'), "Add Membership", self)
        self.tb.addAction(self.addMember)
        self.addMember.triggered.connect(self.funcAddMember)
        self.tb.addSeparator()
        ############Selling##############
        self.sellProduct = QAction(QIcon('icons/sell.png'), "Sell Product", self)
        self.sellProduct.triggered.connect(self.funcSellProduct)
        self.tb.addAction(self.sellProduct)
        self.tb.addSeparator()
        ############Printer##############
        self.print = QAction(QIcon('icons/printer.png'), "Print", self)
        self.print.triggered.connect(self.funcPrintPreview)
        self.tb.addAction(self.print)
        self.tb.addSeparator()
        ############Export PDF##############
        self.exportPDF = QAction(QIcon('icons/pdf.png'), "Export PDF", self)
        self.exportPDF.triggered.connect(self.funcExportPdf)
        self.tb.addAction(self.exportPDF)
        self.tb.addSeparator()
        ############Calendar##############
        self.calendarToolBar = QAction(QIcon('icons/calendar.png'), "Calendar", self)
        self.calendarToolBar.triggered.connect(self.funcCalendar)
        self.tb.addAction(self.calendarToolBar)
        self.tb.addSeparator()
        ############Information##############
        self.infoToolBar = QAction(QIcon('icons/info.png'), "Info", self)
        self.infoToolBar.triggered.connect(self.funcInfo)
        self.tb.addAction(self.infoToolBar)
        self.tb.addSeparator()


    def tabWidget(self):
        self.tabs = QTabWidget()

        # Update the content dynamically every time each tab is clicked
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.tabsChanged)

        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Membership")
        self.tabs.addTab(self.tab3, "Statistics")
        self.tabs.addTab(self.tab4, "Selling History")


    def widgets(self):
        ############Tab 1 Widgets##############
        ############Main Left Layout Widget##############
        self.productTable = QTableWidget()
        self.productTable.setColumnCount(7)
        # Hide the column product id
        self.productTable.setColumnHidden(0, True)
        self.productTable.setHorizontalHeaderItem(0, QTableWidgetItem("Product ID"))
        self.productTable.setHorizontalHeaderItem(1, QTableWidgetItem("Product Name"))
        self.productTable.setHorizontalHeaderItem(2, QTableWidgetItem("Manufacture"))
        self.productTable.setHorizontalHeaderItem(3, QTableWidgetItem("Price"))
        self.productTable.setHorizontalHeaderItem(4, QTableWidgetItem("Quota"))
        self.productTable.setHorizontalHeaderItem(5, QTableWidgetItem("Date Added"))
        self.productTable.setHorizontalHeaderItem(6, QTableWidgetItem("Availability"))
        self.productTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.productTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.productTable.doubleClicked.connect(self.selectedProduct)

        ############Right Top Layout Widget##############
        self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search for products")
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.searchProduct)

        ############Right Middle Layout Widget##############
        self.allProduct = QRadioButton("All Products")
        self.allProduct.setChecked(True)
        self.availableProduct = QRadioButton("Available")
        self.notAvailableProduct = QRadioButton("Not Available")
        self.listButton = QPushButton("List")
        self.listButton.clicked.connect(self.listProduct)

        ############Tab 2 Widgets##############
        self.memberTable = QTableWidget()
        self.memberTable.setColumnCount(5)
        self.memberTable.setHorizontalHeaderItem(0, QTableWidgetItem("Member ID"))
        self.memberTable.setHorizontalHeaderItem(1, QTableWidgetItem("First Name"))
        self.memberTable.setHorizontalHeaderItem(2, QTableWidgetItem("Last Name"))
        self.memberTable.setHorizontalHeaderItem(3, QTableWidgetItem("Phone Number"))
        self.memberTable.setHorizontalHeaderItem(4, QTableWidgetItem("Address"))
        self.memberTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.memberTable.doubleClicked.connect(self.selectedMember)
        self.memberSearchText = QLabel("Search Member")
        self.memberSearchEntry = QLineEdit()
        self.memberSearchButton = QPushButton("Search")
        self.memberSearchButton.clicked.connect(self.searchMember)

        ############Tab 3 Widgets##############
        self.totalProductLabel = QLabel()
        self.totalMemberLabel = QLabel()
        self.soldProductLabel = QLabel()
        self.totalAmountLabel = QLabel()

        ############Tab 4 Widgets##############
        self.historyShow = QTextEdit()
        self.historyShow.setReadOnly(True)

    def layouts(self):
        ############Tab1 Layout##############
        self.productMainLayout = QHBoxLayout()
        self.productLeftLayout = QVBoxLayout()
        self.productRightLayout = QVBoxLayout()
        self.productRightTopLayout = QHBoxLayout()
        self.productRightMiddleLayout = QHBoxLayout()
        self.productRightBottomLayout = QVBoxLayout()


        ############Add Widgets##############
        ############Left Main Layout Widgets##############
        self.productLeftLayout.addWidget(self.productTable)

        ############Right Layouts##############
        self.topGroupBox = QGroupBox("Search Box")
        self.middleGroupBox = QGroupBox("List Box")
        self.bottomGroupBox = QGroupBox()

        ############Right Top Layout Widgets##############
        self.productRightTopLayout.addWidget(self.searchText)
        self.productRightTopLayout.addWidget(self.searchEntry)
        self.productRightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self.productRightTopLayout)
        self.productRightLayout.addWidget(self.topGroupBox, 20)


        ############Right Middle Layout Widget##############
        self.productRightMiddleLayout.addWidget(self.allProduct)
        self.productRightMiddleLayout.addWidget(self.availableProduct)
        self.productRightMiddleLayout.addWidget(self.notAvailableProduct)
        self.productRightMiddleLayout.addWidget(self.listButton)
        self.middleGroupBox.setLayout(self.productRightMiddleLayout)
        self.productRightLayout.addWidget(self.middleGroupBox, 20)

        ############Right Bottom Layout Widget##############
        self.bottomGroupBox.setLayout(self.productRightBottomLayout)
        self.productRightLayout.addWidget(self.bottomGroupBox, 60)


        ############Tab 1 Main Layouts##############
        self.productMainLayout.addLayout(self.productLeftLayout, 75)
        self.productMainLayout.addLayout(self.productRightLayout, 25)
        self.tab1.setLayout(self.productMainLayout)

        ############Tab2 Layout##############
        self.memberMainLayout = QHBoxLayout()
        self.memberLeftLayout = QVBoxLayout()
        self.memberRightLayout = QVBoxLayout()
        self.memberRightTopLayout = QHBoxLayout()


        ############Add Widgets##############
        ############Left Main Layout Widgets##############
        self.memberLeftLayout.addWidget(self.memberTable)

        ############Right Top Layout Widgets##############
        self.memberRightGroupBox = QGroupBox("Search For Member")
        self.memberRightGroupBox.setContentsMargins(10, 10, 10, 580)
        self.memberRightTopLayout.addWidget(self.memberSearchText)
        self.memberRightTopLayout.addWidget(self.memberSearchEntry)
        self.memberRightTopLayout.addWidget(self.memberSearchButton)
        self.memberRightGroupBox.setLayout(self.memberRightTopLayout)
        self.memberRightLayout.addWidget(self.memberRightGroupBox)


        ############Tab 2 Main Layouts##############
        self.memberMainLayout.addLayout(self.memberLeftLayout, 75)
        self.memberMainLayout.addLayout(self.memberRightLayout, 25)
        self.tab2.setLayout(self.memberMainLayout)

        ############Tab3 Layout##############
        self.statMainLayout = QVBoxLayout()
        self.statLayout = QFormLayout()
        self.statGroupBox = QGroupBox("Statistics")
        self.statLayout.addRow("Total Products: ", self.totalProductLabel)
        self.statLayout.addRow("Total Members: ", self.totalMemberLabel)
        self.statLayout.addRow("Sold Products: ", self.soldProductLabel)
        self.statLayout.addRow("Total Amount: ", self.totalAmountLabel)

        self.statGroupBox.setLayout(self.statLayout)
        self.statGroupBox.setFont(QFont("Times", 30))
        self.statMainLayout.addWidget(self.statGroupBox)
        self.statMainLayout.setAlignment(Qt.AlignCenter)
        self.tab3.setLayout(self.statMainLayout)

        ############Tab4 Layout##############
        self.historyMainLayout = QVBoxLayout()
        self.historyLayout = QVBoxLayout()
        self.historyGroupBox = QGroupBox("Selling History")
        self.historyLayout.addWidget(self.historyShow)



        self.historyGroupBox.setLayout(self.historyLayout)
        self.historyGroupBox.setFont(QFont("Times", 14))
        self.historyMainLayout.addWidget(self.historyGroupBox)
        self.historyMainLayout.setAlignment(Qt.AlignCenter)
        self.tab4.setLayout(self.historyMainLayout)


        # block signal for tabs
        self.tabs.blockSignals(False)

    def createMenu(self):
        ########Main Menu########
        menuBar = self.menuBar()
        file = menuBar.addMenu("File")
        product = menuBar.addMenu("Product")
        help = menuBar.addMenu("About")
        ########Sub Menu########
        addProductMenu = QAction("Add Product", self)
        addProductMenu.setIcon(QIcon("icons/add.png"))
        addProductMenu.setShortcut("Ctrl+A")
        addProductMenu.triggered.connect(self.funcAddProduct)

        addMemberMenu = QAction("Add Membership", self)
        addMemberMenu.setIcon(QIcon('icons/users.png'))
        addMemberMenu.setShortcut("Ctrl+M")
        addMemberMenu.triggered.connect(self.funcAddMember)

        printMenu = QAction("Print", self)
        printMenu.setIcon(QIcon('icons/printer.png'))
        printMenu.setShortcut("Ctrl+P")
        printMenu.triggered.connect(self.funcPrintPreview)

        exportPDF = QAction("ExportPDF", self)
        exportPDF.setShortcut("Ctrl+E")
        exportPDF.triggered.connect(self.funcExportPdf)

        sellProductMenu = QAction("Sell Product", self)
        sellProductMenu.setIcon(QIcon('icons/sell.png'))
        sellProductMenu.setShortcut("Ctrl+S")
        sellProductMenu.triggered.connect(self.funcSellProduct)

        infoMenu = QAction("Information", self)
        infoMenu.setIcon(QIcon('icons/info.png'))
        infoMenu.triggered.connect(self.funcInfo)

        file.addAction(addProductMenu)
        file.addAction(addMemberMenu)
        file.addAction(printMenu)
        file.addAction(exportPDF)
        product.addAction(sellProductMenu)
        help.addAction(infoMenu)

    def funcAddProduct(self):
        self.newProduct = add_product.AddProduct()
        self.close()

    def funcAddMember(self):
        self.newMember = add_member.AddMember()
        self.close()

    def funcSellProduct(self):
        self.sell = selling.SellProduct()
        self.close()

    def funcExportPdf(self):
        self.export = export_pdf.ExportPDF()

    def funcPrintPreview(self):
        self.printDiaglog = print_widget.Print()

    def funcCalendar(self):
        self.calendarDialog = calendar_class.Calendar()

    def funcInfo(self):
        self.info = info.Info()

    def getStat(self):
        countProducts = cur.execute("SELECT count(product_id) FROM products").fetchall()
        countProducts = countProducts[0][0]

        countMember = cur.execute("SELECT count(member_id) FROM members").fetchall()
        countMember = countMember[0][0]

        soldProducts = cur.execute("SELECT sum(selling_quantity) FROM sellings").fetchall()
        soldProducts = soldProducts[0][0]

        totalAmount = cur.execute("SELECT sum(selling_amount) FROM sellings").fetchall()
        totalAmount = totalAmount[0][0]

        self.totalProductLabel.setText(str(countProducts))
        self.totalMemberLabel.setText(str(countMember))
        self.soldProductLabel.setText(str(soldProducts))
        self.totalAmountLabel.setText("$ " + str(totalAmount))

    def getSellingHistory(self):
        query = "SELECT products.product_name, products.product_manufacturer, product_price, members.member_fname, sellings.selling_quantity, sellings.selling_amount, sellings.selling_date FROM products, members, sellings WHERE products.product_id = sellings.selling_id AND members.member_id = sellings.selling_member_id"
        history = cur.execute(query).fetchall()
        for element in history:
            product_name = element[0]
            product_manu = element[1]
            product_price = element[2]
            member_name = element[3]
            selling_quantity = element[4]
            selling_amount = element[5]
            selling_date = element[6]
            self.historyShow.append("Product Name: " + product_name)
            self.historyShow.append("Manufacturer: " + product_manu)
            self.historyShow.append("Product Price: $" + str(product_price))
            self.historyShow.append("Selling to: " + member_name)
            self.historyShow.append("Quantity: " + str(selling_quantity))
            self.historyShow.append("Amount: $" + str(selling_amount))
            self.historyShow.append("Date Sold: " + str(selling_date))
            self.historyShow.append("")


    def tabsChanged(self):
        self.getStat()
        self.displayProduct()
        self.displayMember()


    def displayProduct(self):
        self.productTable.setFont(QFont("Times", 12))
        for i in reversed(range(self.productTable.rowCount())):
            self.productTable.removeRow(i)

        query = cur.execute("SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_date, product_availability FROM products")
        for row_data in query:
            row_number = self.productTable.rowCount()
            self.productTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.productTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def displayMember(self):
        self.memberTable.setFont(QFont("Times", 12))
        for i in reversed(range(self.memberTable.rowCount())):
            self.memberTable.removeRow(i)

        members = cur.execute("SELECT * FROM members")
        for row_data in members:
            row_number = self.memberTable.rowCount()
            self.memberTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.memberTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.memberTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getProductIdFromCurrentRow(self):
        listProduct = []
        for i in range(0, 6):
            listProduct.append(self.productTable.item(self.productTable.currentRow(), i).text())
        global productId
        productId = listProduct[0]
        return productId

    def selectedProduct(self):
        productId = self.getProductIdFromCurrentRow()
        display_product.DisplayProduct.productId = productId
        self.displayP = display_product.DisplayProduct()
        self.displayP.show()
        self.close()

    def getMemberIdFromCurrentRow(self):
        listMember = []
        for i in range(0, 5):
            listMember.append(self.memberTable.item(self.memberTable.currentRow(), i).text())

        memberId = listMember[0]
        return memberId

    def selectedMember(self):
        memberId = self.getMemberIdFromCurrentRow()
        display_member.DisplayMember.memberId = memberId
        self.displayM = display_member.DisplayMember()
        self.displayM.show()
        self.close()

    def searchProduct(self):
        value = self.searchEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search query cannot be empty")
        else:
            self.searchEntry.setText("")
            query = "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_date, product_availability FROM products WHERE product_name LIKE ? or product_manufacturer LIKE ? "
            results = cur.execute(query, ('%' + value + '%', '%' + value + '%')).fetchall()

            if results == []:
                QMessageBox.information(self, "Warning", "There is no such a product or manufacturer")
            else:
                for i in reversed(range(self.productTable.rowCount())):
                    self.productTable.removeRow(i)

                for row_data in results:
                    row_number = self.productTable.rowCount()
                    self.productTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def listProduct(self):
        products = None
        if self.allProduct.isChecked():
            query = "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_date, product_availability FROM products"
            products = cur.execute(query).fetchall()

        elif self.availableProduct.isChecked():
            query = "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_date, " \
                    "product_availability FROM products WHERE product_availability = 'Available'"
            products = cur.execute(query).fetchall()

        elif self.notAvailableProduct.isChecked():
            query = "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, " \
                    "product_date, product_availability FROM products WHERE product_availability = 'UnAvailable'"
            products = cur.execute(query).fetchall()


        for i in reversed(range(self.productTable.rowCount())):
            self.productTable.removeRow(i)

        for row_data in products:
            row_number = self.productTable.rowCount()
            self.productTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def searchMember(self):
        value = self.memberSearchEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search query cannot be empty.")
        else:
            self.memberSearchEntry.setText("")
            query = "SELECT * FROM members WHERE member_fname LIKE ? or member_lname LIKE ? or member_phone LIKE ? or member_address LIKE ?"
            results = cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()
            if results == []:
                QMessageBox.information(self, "Warning", "There is no such a member")
            else:
                for i in reversed(range(self.memberTable.rowCount())):
                    self.memberTable.removeRow(i)

                for row_data in results:
                    row_number = self.memberTable.rowCount()
                    self.memberTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.memberTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def styles(self):
        self.topGroupBox.setStyleSheet(styles.searchBoxStyle())
        self.middleGroupBox.setStyleSheet(styles.listBoxStyle())
        self.searchButton.setStyleSheet(styles.searchButtonStyle())
        self.listButton.setStyleSheet(styles.listButtonStyle())


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()

