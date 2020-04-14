import sqlite3
import sys

import qdarkstyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import *
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice


import add_member
import add_product
import display_product
import display_member
import export_pdf
import help_class
import login_class
import print_widget
import calendar_class
import info
import selling
from change_password import ChangePassword

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Management")
        self.setWindowIcon(QIcon('icons/logo.png'))
        self.setGeometry(400, 200, 1800, 900)
        self.UI()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.createMenu()
        self.displayProduct()
        self.displayMember()
        self.displaySellingRecord()
        self.getStat()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        ############Toolbar Buttons##########
        ############Add Product##############
        self.addProduct = QAction(QIcon('icons/add.svg'), "Add Product", self)
        self.addProduct.triggered.connect(self.funcAddProduct)
        self.tb.addAction(self.addProduct)
        self.tb.addSeparator()
        ############Add Member##############
        self.addMember = QAction(QIcon('icons/users.svg'), "Add Membership", self)
        self.tb.addAction(self.addMember)
        self.addMember.triggered.connect(self.funcAddMember)
        self.tb.addSeparator()
        ############Selling##############
        self.sellProduct = QAction(QIcon('icons/sell.svg'), "Sell Product", self)
        self.sellProduct.triggered.connect(self.funcSellProduct)
        self.tb.addAction(self.sellProduct)
        self.tb.addSeparator()
        ############Refresh##############
        self.refresh = QAction(QIcon('icons/refresh.svg'), "Refresh", self)
        self.refresh.triggered.connect(self.funcRefresh)
        self.tb.addAction(self.refresh)
        self.tb.addSeparator()
        ############Printer##############
        self.print = QAction(QIcon('icons/printer.svg'), "Print", self)
        self.print.triggered.connect(self.funcPrintPreview)
        self.tb.addAction(self.print)
        self.tb.addSeparator()
        ############Export PDF##############
        self.exportPDF = QAction(QIcon('icons/pdf.svg'), "Export PDF", self)
        self.exportPDF.triggered.connect(self.funcExportPdf)
        self.tb.addAction(self.exportPDF)
        self.tb.addSeparator()
        ############Calendar##############
        self.calendarToolBar = QAction(QIcon('icons/calendar.svg'), "Calendar", self)
        self.calendarToolBar.triggered.connect(self.funcCalendar)
        self.tb.addAction(self.calendarToolBar)
        self.tb.addSeparator()
        ############Information##############
        self.infoToolBar = QAction(QIcon('icons/info.svg'), "Info", self)
        self.infoToolBar.triggered.connect(self.funcInfo)
        self.tb.addAction(self.infoToolBar)
        self.tb.addSeparator()
        self.logout = QAction(QIcon('icons/logout.svg'), "Logout", self)
        self.logout.triggered.connect(self.funcLogout)
        self.tb.addAction(self.logout)
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
        self.tabs.addTab(self.tab3, "Selling Records")
        self.tabs.addTab(self.tab4, "Statistics")

    def widgets(self):
        ############Tab 1 Widgets##############
        ############Main Left Layout Widget##############
        self.productTable = QTableWidget()
        self.productTable.setColumnCount(7)
        # Hide the column product id
        #self.productTable.setColumnHidden(0, True)
        self.productTable.setStyleSheet("font-size: 15px")
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
        self.productTable.clicked.connect(self.viewProductItem)

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

        ############Right Bottom Layout Widget##############
        self.product_name = QLabel()
        self.product_name.setAlignment(Qt.AlignCenter)
        self.product_manu = QLabel()
        self.product_manu.setAlignment(Qt.AlignCenter)
        self.product_price = QLabel()
        self.product_price.setAlignment(Qt.AlignCenter)
        self.product_quantity = QLabel()
        self.product_quantity.setAlignment(Qt.AlignCenter)
        self.product_date = QLabel()
        self.product_date.setAlignment(Qt.AlignCenter)
        self.product_status = QLabel()
        self.product_status.setAlignment(Qt.AlignCenter)
        self.product_Img = QLabel()
        self.product_Img.setAlignment(Qt.AlignCenter)

        self.updateProductBtn = QPushButton("Update")
        self.updateProductBtn.clicked.connect(self.updateProduct)


        ############Tab 2 Widgets##############
        self.memberTable = QTableWidget()
        self.memberTable.setColumnCount(5)
        self.memberTable.setStyleSheet("font-size: 15px")
        self.memberTable.setHorizontalHeaderItem(0, QTableWidgetItem("Member ID"))
        self.memberTable.setHorizontalHeaderItem(1, QTableWidgetItem("First Name"))
        self.memberTable.setHorizontalHeaderItem(2, QTableWidgetItem("Last Name"))
        self.memberTable.setHorizontalHeaderItem(3, QTableWidgetItem("Phone"))
        self.memberTable.setHorizontalHeaderItem(4, QTableWidgetItem("Address"))
        self.memberTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.memberTable.doubleClicked.connect(self.selectedMember)
        self.memberTable.clicked.connect(self.viewSelectedMember)

        ############Right Top Layout Widget##############
        self.memberSearchText = QLabel("Search")
        self.memberSearchEntry = QLineEdit()
        self.memberSearchButton = QPushButton("Search")
        self.memberSearchButton.clicked.connect(self.searchMember)

        ############Right Bottom Layout Widget##############
        self.member_fname = QLabel()
        self.member_fname.setAlignment(Qt.AlignCenter)
        self.member_lname = QLabel()
        self.member_lname.setAlignment(Qt.AlignCenter)
        self.member_phone = QLabel()
        self.member_phone.setAlignment(Qt.AlignCenter)
        self.member_address = QLabel()
        self.member_address.setAlignment(Qt.AlignCenter)

        self.updateMemberBtn = QPushButton("Update")
        self.updateMemberBtn.clicked.connect(self.updateMember)

        ############Tab 3 Widgets##############
        self.sellingTable = QTableWidget()
        self.sellingTable.setColumnCount(9)
        self.sellingTable.setStyleSheet("font-size: 15px")
        self.sellingTable.setHorizontalHeaderItem(0, QTableWidgetItem("Receipt #"))
        self.sellingTable.setHorizontalHeaderItem(1, QTableWidgetItem("Product Name"))
        self.sellingTable.setHorizontalHeaderItem(2, QTableWidgetItem("Manufacturer"))
        self.sellingTable.setHorizontalHeaderItem(3, QTableWidgetItem("Price"))
        self.sellingTable.setHorizontalHeaderItem(4, QTableWidgetItem("Selling To"))
        self.sellingTable.setHorizontalHeaderItem(5, QTableWidgetItem("Quantity"))
        self.sellingTable.setHorizontalHeaderItem(6, QTableWidgetItem("Discount (%)"))
        self.sellingTable.setHorizontalHeaderItem(7, QTableWidgetItem("Amount"))
        self.sellingTable.setHorizontalHeaderItem(8, QTableWidgetItem("Date"))
        self.sellingTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.sellingTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.sellingTable.clicked.connect(self.viewSelectedRecord)

        self.historySearchText = QLabel("Search")
        self.historySearchEntry = QLineEdit()
        self.historySearchButton = QPushButton("Search")
        self.historySearchButton.clicked.connect(self.searchRecord)

        self.historyShow = QTextEdit()
        self.historyShow.append("###########Reciept###########")
        self.historyShow.setStyleSheet("font-size: 20px")
        self.historyShow.setReadOnly(True)
        self.printReceiptButton = QPushButton("Print Receipt")
        self.printReceiptButton.clicked.connect(self.printReceipt)
        self.deleteRecordBtn = QPushButton("Delete this record")
        self.deleteRecordBtn.clicked.connect(self.deleteOneRecord)
        self.deleteAllRecordsBtn = QPushButton("Delete all records")
        self.deleteAllRecordsBtn.clicked.connect(self.deleteHistory)

        ############Tab 4 Widgets##############
        self.totalProductLabel = QLabel()
        self.totalMemberLabel = QLabel()
        self.totalInStockLabel = QLabel()
        self.soldItemLabel = QLabel()
        self.totalAmountLabel = QLabel()
        self.totalAmountEarnedLabel = QLabel()

    def layouts(self):
        ############Tab1 Layout##############
        self.productMainLayout = QHBoxLayout()
        self.productLeftLayout = QVBoxLayout()
        self.productRightLayout = QVBoxLayout()
        self.productRightTopLayout = QHBoxLayout()
        self.productRightMiddleLayout = QHBoxLayout()
        self.productRightBottomLayout = QVBoxLayout()
        self.productRightBottomLayout1 = QVBoxLayout()

        ############Add Widgets##############
        ############Left Main Layout Widgets##############
        self.productLeftLayout.addWidget(self.productTable)

        ############Right Layouts##############
        self.topGroupBox = QGroupBox("Search for Products")
        self.topGroupBox.setStyleSheet("QLabel {font-size: 15px}")
        self.middleGroupBox = QGroupBox("List Box")
        self.middleGroupBox.setStyleSheet("QLabel {font-size: 20px}")
        self.bottomGroupBox = QGroupBox()
        self.bottomGroupBox.setStyleSheet("QLabel {font-size: 16px}")

        ############Right Top Layout Widgets##############
        self.productRightTopLayout.addWidget(self.searchText)
        self.productRightTopLayout.addWidget(self.searchEntry)
        self.productRightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self.productRightTopLayout)
        self.productRightLayout.addWidget(self.topGroupBox, 10)

        ############Right Middle Layout Widget##############
        self.productRightMiddleLayout.addWidget(self.allProduct)
        self.productRightMiddleLayout.addWidget(self.availableProduct)
        self.productRightMiddleLayout.addWidget(self.notAvailableProduct)
        self.productRightMiddleLayout.addWidget(self.listButton)
        self.middleGroupBox.setLayout(self.productRightMiddleLayout)
        self.productRightLayout.addWidget(self.middleGroupBox, 10)

        ############Right Bottom Layout Widget##############
        self.productBottomForm = QFormLayout()
        self.productBottomForm.addRow("", self.product_Img)
        self.productBottomForm.addRow("", self.product_name)
        self.productBottomForm.addRow("", self.product_manu)
        self.productBottomForm.addRow("", self.product_price)
        self.productBottomForm.addRow("", self.product_quantity)
        self.productBottomForm.addRow("", self.product_date)
        self.productBottomForm.addRow("", self.product_status)
        self.bottomGroupBox.setLayout(self.productBottomForm)
        self.productRightBottomLayout1.addWidget(self.updateProductBtn)
        self.productRightLayout.addWidget(self.bottomGroupBox, 80)
        self.productRightLayout.addLayout(self.productRightBottomLayout1)

        ############Tab 1 Main Layouts##############
        self.productMainLayout.addLayout(self.productLeftLayout, 75)
        self.productMainLayout.addLayout(self.productRightLayout, 25)
        self.tab1.setLayout(self.productMainLayout)

        ############Tab2 Layout##############
        self.memberMainLayout = QHBoxLayout()
        self.memberLeftLayout = QVBoxLayout()
        self.memberRightLayout = QVBoxLayout()
        self.memberRightTopLayout = QHBoxLayout()
        self.memberRightBottomLayout = QVBoxLayout()

        ############Right Layouts##############
        self.memberRightBottomGroupBox = QGroupBox()
        self.memberRightGroupBox = QGroupBox("Search for Member")
        self.memberRightGroupBox.setStyleSheet("QLabel {font-size: 15px}")
        self.memberRightBottomGroupBox.setStyleSheet("QLabel {font-size: 20px}")

        ############Add Widgets##############
        ############Left Main Layout Widgets##############
        self.memberLeftLayout.addWidget(self.memberTable)

        ############Right Top Layout Widgets##############
        self.memberRightGroupBox.setContentsMargins(10, 10, 10, 580)
        self.memberRightTopLayout.addWidget(self.memberSearchText)
        self.memberRightTopLayout.addWidget(self.memberSearchEntry)
        self.memberRightTopLayout.addWidget(self.memberSearchButton)
        self.memberRightGroupBox.setLayout(self.memberRightTopLayout)
        self.memberRightLayout.addWidget(self.memberRightGroupBox, 10)

        ############Right Bottom Layout Widget##############
        self.memberBottomForm = QFormLayout()
        self.memberBottomForm.addRow("", self.member_fname)
        self.memberBottomForm.addRow("", self.member_lname)
        self.memberBottomForm.addRow("", self.member_phone)
        self.memberBottomForm.addRow("", self.member_address)
        self.memberRightBottomLayout.addWidget(self.updateMemberBtn)
        self.memberRightBottomGroupBox.setLayout(self.memberBottomForm)
        self.memberRightLayout.addWidget(self.memberRightBottomGroupBox, 90)
        self.memberRightLayout.addLayout(self.memberRightBottomLayout)

        ############Tab 2 Main Layouts##############
        self.memberMainLayout.addLayout(self.memberLeftLayout, 75)
        self.memberMainLayout.addLayout(self.memberRightLayout, 25)
        self.tab2.setLayout(self.memberMainLayout)

        ############Tab3 Layout##############
        self.historyMainLayout = QHBoxLayout()
        self.historyLeftLayout = QVBoxLayout()
        self.historyRightLayout = QVBoxLayout()
        self.historyRightTopLayout = QHBoxLayout()
        self.historyRightBottomLayout = QVBoxLayout()

        ############Right Layouts##############
        self.historyRightTopGroupBox = QGroupBox("Search for Records")
        self.historyRightTopGroupBox.setStyleSheet("QLabel {font-size: 15px}")
        self.historyRightBottomGroupBox = QGroupBox()

        ############Add Widgets##############
        ############Left Main Layout Widgets##############
        self.historyLeftLayout.addWidget(self.sellingTable)

        ############Right Top Layout Widgets##############
        self.historyRightTopGroupBox.setContentsMargins(10, 10, 10, 580)
        self.historyRightTopLayout.addWidget(self.historySearchText)
        self.historyRightTopLayout.addWidget(self.historySearchEntry)
        self.historyRightTopLayout.addWidget(self.historySearchButton)
        self.historyRightTopGroupBox.setLayout(self.historyRightTopLayout)
        self.historyRightLayout.addWidget(self.historyRightTopGroupBox, 10)

        ############Right Bottom Layout Widgets##############
        self.historyRightBottomLayout.addWidget(self.historyShow)
        self.historyRightBottomLayout.addWidget(self.printReceiptButton)
        self.historyRightBottomLayout.addWidget(self.deleteRecordBtn)
        self.historyRightBottomLayout.addWidget(self.deleteAllRecordsBtn)
        self.historyRightBottomGroupBox.setLayout(self.historyRightBottomLayout)
        self.historyRightLayout.addWidget(self.historyRightBottomGroupBox, 90)

        ############Main Layout for tab 3##############
        self.historyMainLayout.addLayout(self.historyLeftLayout, 75)
        self.historyMainLayout.addLayout(self.historyRightLayout, 25)

        self.tab3.setLayout(self.historyMainLayout)

        ############Tab4 Layout##############
        self.statMainLayout = QHBoxLayout()
        self.statLeftLayout = QVBoxLayout()
        self.statRightLayout = QVBoxLayout()

        self.statLayout = QFormLayout()
        self.statGroupBox = QGroupBox()
        self.statLayout.addRow("Total Products: ", self.totalProductLabel)
        self.statLayout.addRow("Total Members: ", self.totalMemberLabel)
        self.statLayout.addRow("Total In Stock: ", self.totalInStockLabel)
        self.statLayout.addRow("Total Sold: ", self.soldItemLabel)
        self.statLayout.addRow("Total Amount: ", self.totalAmountLabel)
        self.statLayout.addRow("Amount Earned: ", self.totalAmountEarnedLabel)

        ###########Add Pie Chart#################
        ##############Products Sold Pie Chart###################
        self.getStat()
        global productInstock, soldItems, totalAmount, amountEarned
        self.series = QPieSeries()
        self.series.append("Product Instock", productInstock)
        self.series.append("Sold Items", soldItems)

        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeBlueCerulean)
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Products Sold Pie Chart")

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chartview = QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.Antialiasing)

        self.statRightLayout.addWidget(self.chartview)

        ##############Cash Flow Pie Chart###################
        self.series1 = QPieSeries()
        self.series1.append("Total Amount", (totalAmount + amountEarned))
        self.series1.append("Amount Earned", amountEarned)

        self.chart1 = QChart()
        self.chart1.setTheme(QChart.ChartThemeBlueCerulean)
        self.chart1.legend().hide()
        self.chart1.addSeries(self.series1)
        self.chart1.createDefaultAxes()
        self.chart1.setAnimationOptions(QChart.SeriesAnimations)
        self.chart1.setTitle("Cash Flow Pie Chart")

        self.chart1.legend().setVisible(True)
        self.chart1.legend().setAlignment(Qt.AlignBottom)

        self.chartview1 = QChartView(self.chart1)
        self.chartview1.setRenderHint(QPainter.Antialiasing)

        self.statRightLayout.addWidget(self.chartview1)

        self.statGroupBox.setLayout(self.statLayout)
        self.statGroupBox.setStyleSheet("QLabel {font-size: 30px}")
        self.statLeftLayout.addWidget(self.statGroupBox)
        self.statMainLayout.addLayout(self.statLeftLayout, 40)
        self.statMainLayout.addLayout(self.statRightLayout, 60)
        self.statMainLayout.setAlignment(Qt.AlignCenter)
        self.tab4.setLayout(self.statMainLayout)

        # block signal for tabs
        self.tabs.blockSignals(False)

    def createMenu(self):
        ########Main Menu########
        menuBar = self.menuBar()
        file = menuBar.addMenu("File")
        product = menuBar.addMenu("Product")
        setting = menuBar.addMenu("Setting")
        ########Sub Menu########
        addProductMenu = QAction("Add Product", self)
        addProductMenu.setIcon(QIcon("icons/add.svg"))
        addProductMenu.setShortcut("Ctrl+A")
        addProductMenu.triggered.connect(self.funcAddProduct)

        addMemberMenu = QAction("Add Membership", self)
        addMemberMenu.setIcon(QIcon('icons/users.svg'))
        addMemberMenu.setShortcut("Ctrl+M")
        addMemberMenu.triggered.connect(self.funcAddMember)

        printMenu = QAction("Print", self)
        printMenu.setIcon(QIcon('icons/printer.svg'))
        printMenu.setShortcut("Ctrl+P")
        printMenu.triggered.connect(self.funcPrintPreview)

        exportPDF = QAction("ExportPDF", self)
        exportPDF.setShortcut("Ctrl+S")
        exportPDF.setIcon(QIcon('icons/pdf.svg'))
        exportPDF.triggered.connect(self.funcExportPdf)

        sellProductMenu = QAction("Sell Product", self)
        sellProductMenu.setIcon(QIcon('icons/sell.svg'))
        sellProductMenu.setShortcut("Ctrl+E")
        sellProductMenu.triggered.connect(self.funcSellProduct)

        refreshMenu = QAction("Refresh", self)
        refreshMenu.setIcon(QIcon('icons/refresh.svg'))
        refreshMenu.setShortcut("Ctrl+R")
        refreshMenu.triggered.connect(self.funcRefresh)

        changePasswordMenu = QAction("Change Password", self)
        changePasswordMenu.triggered.connect(self.funcChangePassword)

        infoMenu = QAction("About", self)
        infoMenu.setIcon(QIcon('icons/info.svg'))
        infoMenu.triggered.connect(self.funcInfo)

        helpMenu = QAction("Help", self)
        helpMenu.triggered.connect(self.funcHelp)

        logoutMenu = QAction("Logout", self)
        logoutMenu.setShortcut("Ctrl+O")
        logoutMenu.setIcon(QIcon('icons/logout.svg'))
        logoutMenu.triggered.connect(self.funcLogout)

        #add submenu to main menu
        file.addAction(addProductMenu)
        file.addAction(addMemberMenu)
        file.addAction(printMenu)
        file.addAction(exportPDF)
        product.addAction(sellProductMenu)
        setting.addAction(refreshMenu)
        setting.addAction(changePasswordMenu)
        setting.addAction(infoMenu)
        setting.addAction(helpMenu)
        setting.addAction(logoutMenu)

    def funcAddProduct(self):
        self.newProduct = add_product.AddProduct()

    def funcAddMember(self):
        self.newMember = add_member.AddMember()

    def funcSellProduct(self):
        self.sell = selling.SellProduct()

    def funcExportPdf(self):
        self.export = export_pdf.ExportPDF()

    def funcPrintPreview(self):
        self.printDiaglog = print_widget.Print()

    def funcCalendar(self):
        self.calendarDialog = calendar_class.Calendar()

    def funcInfo(self):
        self.info = info.Info()

    def funcHelp(self):
        self.help = help_class.Help()
        self.help.show()

    def funcLogout(self):
        self.logoutWindow = login_class.Login()
        self.logoutWindow.show()
        self.close()

    def funcChangePassword(self):
        self.changePassword = ChangePassword()
        self.changePassword.show()

    def funcRefresh(self):
        self.displayProduct()
        self.displayMember()
        self.displaySellingRecord()
        self.getStat()
        self.historyShow.setText("")

        # Update pie charts
        self.series.clear()
        self.series.append("Product Instock", productInstock)
        self.series.append("Sold Items", soldItems)
        self.slice = self.series.slices()[1]
        self.slice.setExploded(True)
        self.slice.setPen(QPen(Qt.darkGreen, 2))
        self.slice.setBrush(Qt.green)

        self.series1.clear()
        self.series1.append("Total Amount", totalAmount)
        self.series1.append("Amount Earned", amountEarned)

        self.slice1 = self.series1.slices()[1]
        self.slice1.setExploded(True)
        self.slice1.setPen(QPen(Qt.darkYellow, 2))
        self.slice1.setBrush(Qt.yellow)

        self.slice2 = QPieSlice()
        self.slice2 = self.series1.slices()[0]
        self.slice2.setPen(QPen(Qt.darkRed))
        self.slice2.setBrush(Qt.red)

    def getStat(self):
        global productInstock, soldItems, totalAmount, amountEarned

        try:

            countProducts = cur.execute("SELECT count(product_id) FROM products").fetchall()
            countProducts = countProducts[0][0]

            countMember = cur.execute("SELECT count(member_id) FROM members").fetchall()
            countMember = countMember[0][0]

            productInstock = cur.execute("SELECT sum(product_quota) FROM products").fetchall()
            productInstock = productInstock[0][0]

            soldItems = cur.execute("SELECT sum(selling_quantity) FROM sellings").fetchall()
            soldItems = soldItems[0][0]

            sumOfProductPrice = cur.execute("SELECT sum(product_price) FROM products").fetchall()
            sumOfProductPrice = sumOfProductPrice[0][0]

            sumOfProductQuota = cur.execute("SELECT sum(product_quota) FROM products").fetchall()
            sumOfProductQuota = sumOfProductQuota[0][0]

            amountEarned = cur.execute("SELECT sum(selling_amount) FROM sellings").fetchall()
            amountEarned = amountEarned[0][0]

        except:
            QMessageBox.information(self, "Information", "Database is empty")

        if countProducts is None:
            countProducts = 0
        if countMember is None:
            countMember = 0
        if productInstock is None:
            productInstock = 0
        if soldItems is None:
            soldItems = 0
        if sumOfProductPrice is None:
            sumOfProductPrice = 0
        if sumOfProductQuota is None:
            sumOfProductQuota = 0
        if amountEarned is None:
            amountEarned = 0


        totalAmount = sumOfProductPrice * sumOfProductQuota

        self.totalProductLabel.setText(str(countProducts) + " items")
        self.totalMemberLabel.setText(str(countMember) + " members")
        self.totalInStockLabel.setText(str(productInstock) + " units")
        self.soldItemLabel.setText(str(soldItems) + " units")
        self.totalAmountLabel.setText("$" + str(totalAmount + amountEarned))
        self.totalAmountEarnedLabel.setText("$" + str(amountEarned))

    def updateProduct(self):
        if not self.productTable.selectedItems():
            QMessageBox.information(self, "Information", "Please select a product")
        else:
            self.selectedProduct()

    def updateMember(self):
        if not self.memberTable.selectedItems():
            QMessageBox.information(self, "Information", "Please select a member")
        else:
            self.selectedMember()

    def printReceipt(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()

    def printPreview(self, printer):
        self.historyShow.document().print_(printer)

    def deleteOneRecord(self):
        listSelling = []

        if not self.sellingTable.selectedItems():
            QMessageBox.information(self, "Information", "No row has been selected")
        else:
            for i in range(0, 8):
                listSelling.append(self.sellingTable.item(self.sellingTable.currentRow(), i).text())
            mbox = QMessageBox.question(self, "Wanrning", "Are you sure to delete all records?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if (mbox == QMessageBox.Yes):
                try:
                    sellingId = listSelling[0]
                    query = "DELETE FROM sellings WHERE selling_id = ?"
                    cur.execute(query, (sellingId,))
                    sqlConnect.commit()
                    QMessageBox.information(self, "Information", "Selected receipt has been deleted. Please Refresh")
                except:
                    QMessageBox.information(self, "Information", "Selected receipt has been not deleted")


    def deleteHistory(self):
        mbox = QMessageBox.question(self, "Wanrning", "Are you sure to delete all records?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (mbox == QMessageBox.Yes):
            try:
                cur.execute("DELETE FROM sellings")
                sqlConnect.commit()
                QMessageBox.information(self, "Information", "All Records have been deleted")
            except:
                QMessageBox.information(self, "Information", "All records have not been deleted")

    def viewProductItem(self):
        productId = self.getProductIdFromCurrentRow()

        query = "SELECT * FROM products WHERE product_id=?"
        product = cur.execute(query, (productId,)).fetchone()  # single item tuple = (1,)
        productName = product[1]
        productManufacturer = product[2]
        productPrice = product[3]
        productQuota = product[4]
        productImg = product[5]
        productDate = product[6]
        productStatus = product[7]

        self.product_name.setText("Name: " + productName)
        self.product_manu.setText("Manufacturer: " + str(productManufacturer))
        self.product_price.setText("Price: $" + str(productPrice))
        self.product_quantity.setText("Quota: " + str(productQuota))
        self.product_date.setText("Date Added: " + str(productDate))
        self.product_status.setText("Status: " + productStatus)
        self.img = QPixmap('img/{}'.format(productImg))
        self.product_Img.setPixmap(self.img)

    def viewSelectedMember(self):
        memberId = self.getMemberIdFromCurrentRow()

        query = "SELECT * FROM members WHERE member_id=?"
        member = cur.execute(query, (memberId,)).fetchone()  # single item tuple = (1,)
        memberFName = member[1]
        memberLName = member[2]
        memberPhone = member[3]
        memberAddr = member[4]

        self.member_fname.setText("First name: " + memberFName)
        self.member_lname.setText("Last name: " + str(memberLName))
        self.member_phone.setText("Phone Number: " + str(memberPhone))
        self.member_address.setText("Full Address: " + str(memberAddr))

    def viewSelectedRecord(self):
        listSelling = []
        for i in range(0, 9):
            listSelling.append(self.sellingTable.item(self.sellingTable.currentRow(), i).text())

        sellingId = listSelling[0]
        product_name = listSelling[1]
        product_manu = listSelling[2]
        product_price = listSelling[3]
        member_name = listSelling[4]
        selling_quantity = listSelling[5]
        discount_rate = listSelling[6]
        selling_amount = listSelling[7]
        selling_date = listSelling[8]
        self.historyShow.clear()
        self.historyShow.append("###########Reciept###########")
        self.historyShow.append("Receipt number: " + str(sellingId))
        self.historyShow.append("Product Name: " + str(product_name))
        self.historyShow.append("Manufacturer: " + str(product_manu))
        self.historyShow.append("Product Price: $" + str(product_price))
        self.historyShow.append("Selling to: " + str(member_name))
        self.historyShow.append("Quantity: " + str(selling_quantity))
        self.historyShow.append("Discount Rate: " + str(discount_rate) + "%")
        self.historyShow.append("Amount: $" + str(selling_amount))
        self.historyShow.append("Date Sold: " + str(selling_date))

    def displayProduct(self):
        for i in reversed(range(self.productTable.rowCount())):
            self.productTable.removeRow(i)

        query = cur.execute(
            "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_date, product_availability FROM products")
        for row_data in query:
            row_number = self.productTable.rowCount()
            self.productTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.productTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def displayMember(self):
        for i in reversed(range(self.memberTable.rowCount())):
            self.memberTable.removeRow(i)

        members = cur.execute("SELECT * FROM members")
        for row_data in members:
            row_number = self.memberTable.rowCount()
            self.memberTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.memberTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.memberTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def displaySellingRecord(self):
        for i in reversed(range(self.sellingTable.rowCount())):
            self.sellingTable.removeRow(i)

        query = "SELECT sellings.selling_id, products.product_name, products.product_manufacturer, products.product_price, members.member_fname, sellings.selling_quantity, sellings.discount_rate, sellings.selling_amount, sellings.selling_date " \
                "FROM products, members, sellings " \
                "WHERE products.product_id = sellings.selling_product_id AND members.member_id = sellings.selling_member_id"
        records = cur.execute(query)
        for row_data in records:
            row_number = self.sellingTable.rowCount()
            self.sellingTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.sellingTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.sellingTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def getProductIdFromCurrentRow(self):
        listProduct = []
        for i in range(0, 7):
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
            query = "SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_date, product_availability " \
                    "FROM products WHERE product_name LIKE ? or product_manufacturer LIKE ? "
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
            results = cur.execute(query, (
                '%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()
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

    def searchRecord(self):
        value = self.historySearchEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search query cannot be empty")
        else:
            self.historySearchEntry.setText("")
            query = "SELECT sellings.selling_id, products.product_name, products.product_manufacturer, products.product_price, " \
                    "members.member_fname, sellings.selling_quantity, sellings.discount_rate, sellings.selling_amount, sellings.selling_date " \
                    "FROM ((products INNER JOIN sellings ON products.product_id = sellings.selling_product_id) " \
                    "INNER JOIN members ON members.member_id = sellings.selling_member_id)" \
                    "WHERE products.product_name LIKE ? or products.product_manufacturer LIKE ? or members.member_fname LIKE ? or sellings.selling_date LIKE ?"
            results = cur.execute(query, (
                '%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()
            if results == []:
                QMessageBox.information(self, "Warning", "There is no such a record")
            else:
                for i in reversed(range(self.sellingTable.rowCount())):
                    self.sellingTable.removeRow(i)

                for row_data in results:
                    row_number = self.sellingTable.rowCount()
                    self.sellingTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.sellingTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def tabsChanged(self):
        self.getStat()
        self.displayProduct()
        self.displayMember()
        self.displaySellingRecord()


        # Update pie charts
        self.series.clear()
        self.series.append("Product Instock", productInstock)
        self.series.append("Sold Items", soldItems)
        self.slice = self.series.slices()[1]
        self.slice.setExploded(True)
        self.slice.setPen(QPen(Qt.darkGreen, 2))
        self.slice.setBrush(Qt.green)

        self.series1.clear()
        self.series1.append("Total Amount", totalAmount)
        self.series1.append("Amount Earned", amountEarned)

        self.slice1 = self.series1.slices()[1]
        self.slice1.setExploded(True)
        self.slice1.setPen(QPen(Qt.darkYellow, 2))
        self.slice1.setBrush(Qt.yellow)

        self.slice2 = QPieSlice()
        self.slice2 = self.series1.slices()[0]
        self.slice2.setPen(QPen(Qt.darkRed))
        self.slice2.setBrush(Qt.red)

def main():
    App = QApplication(sys.argv)
    window = Main()
    window.show()
    App.setStyleSheet(qdarkstyle.load_stylesheet())
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()