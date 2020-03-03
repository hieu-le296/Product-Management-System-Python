import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import add_product

sqlConnect = sqlite3.connect("products.db")
cur = sqlConnect.cursor()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Manager")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 1350, 750)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()

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
        self.addMember = QAction(QIcon('icons/users.png'), "Add Memeber", self)
        self.tb.addAction(self.addMember)
        self.tb.addSeparator()
        ############Selling##############
        self.sellProduct = QAction(QIcon('icons/sell.png'), "Sell Product", self)
        self.tb.addAction(self.sellProduct)
        self.tb.addSeparator()

    def tabWidget(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Members")
        self.tabs.addTab(self.tab3, "Statistics")


    def widgets(self):
        ############Tab 1 Widgets##############
        ############Main Left Layout Widget##############
        self.prodcutTable = QTableWidget()
        self.prodcutTable.setColumnCount(6)
        # Hide the column product id
        self.prodcutTable.setColumnHidden(0, True)
        self.prodcutTable.setHorizontalHeaderItem(0, QTableWidgetItem("Product ID"))
        self.prodcutTable.setHorizontalHeaderItem(1, QTableWidgetItem("Product Name"))
        self.prodcutTable.setHorizontalHeaderItem(2, QTableWidgetItem("Manufacture"))
        self.prodcutTable.setHorizontalHeaderItem(3, QTableWidgetItem("Price"))
        self.prodcutTable.setHorizontalHeaderItem(4, QTableWidgetItem("Quota"))
        self.prodcutTable.setHorizontalHeaderItem(5, QTableWidgetItem("Availability"))
        ############Right Top Layout Widget##############
        self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search for products")
        self.searchButton = QPushButton("Search")
        ############Right Middle Layout Widget##############
        self.allProduct = QRadioButton("All Products")
        self.availableProduct = QRadioButton("Available")
        self.notAvailableProduct = QRadioButton("Not Available")
        self.listButton = QPushButton("List")

        ############Tab 2 Widgets##############
        self.memberTableWidget = QTableWidget()
        self.memberTableWidget.setColumnCount(5)
        self.memberTableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Member ID"))
        self.memberTableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("First Name"))
        self.memberTableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Last Name"))
        self.memberTableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Phone Number"))
        self.memberTableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Address"))
        self.memberSearchText = QLabel("Search Member")
        self.memberSearchEntry = QLineEdit()
        self.memberSearchButton = QPushButton("Search")




    def layouts(self):
        ############Tab1 Layout##############
        self.productMainLayout = QHBoxLayout()
        self.productLeftLayout = QVBoxLayout()
        self.productRightLayout = QVBoxLayout()
        self.productRightTopLayout = QHBoxLayout()
        self.productRightMiddleLayout = QHBoxLayout()
        #self.rightBottomLayout = QVBoxLayout()


        ############Add Widgets##############
        ############Left Main Layout Widgets##############
        self.productLeftLayout.addWidget(self.prodcutTable)

        ############Right Top Layout Widgets##############
        self.topGroupBox = QGroupBox("Search Box")
        self.middleGroupBox = QGroupBox("List Box")
        # self.bottomGroupBox = QGroupBox("Product Image")
        self.productRightTopLayout.addWidget(self.searchText)
        self.productRightTopLayout.addWidget(self.searchEntry)
        self.productRightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self.productRightTopLayout)
        self.productRightLayout.addWidget(self.topGroupBox)


        ############Right Middle Layout Widget##############
        self.productRightMiddleLayout.addWidget(self.allProduct)
        self.productRightMiddleLayout.addWidget(self.availableProduct)
        self.productRightMiddleLayout.addWidget(self.notAvailableProduct)
        self.productRightMiddleLayout.addWidget(self.listButton)
        self.middleGroupBox.setLayout(self.productRightMiddleLayout)
        self.productRightLayout.addWidget(self.middleGroupBox)


        ############Tab 1 Main Layouts##############
        self.productMainLayout.addLayout(self.productLeftLayout, 70)
        self.productMainLayout.addLayout(self.productRightLayout, 30)
        self.tab1.setLayout(self.productMainLayout)

        ############Tab2 Layout##############
        self.memberMainLayout = QHBoxLayout()
        self.memberLeftLayout = QVBoxLayout()
        self.memberRightLayout = QVBoxLayout()
        self.memberRightTopLayout = QHBoxLayout()


        ############Add Widgets##############
        ############Left Main Layout Widgets##############
        self.memberLeftLayout.addWidget(self.memberTableWidget)

        ############Right Top Layout Widgets##############
        self.memberRightGroupBox = QGroupBox("Search For Member")
        self.memberRightGroupBox.setContentsMargins(10, 10, 10, 580)
        self.memberRightTopLayout.addWidget(self.memberSearchText)
        self.memberRightTopLayout.addWidget(self.memberSearchEntry)
        self.memberRightTopLayout.addWidget(self.memberSearchButton)
        self.memberRightGroupBox.setLayout(self.memberRightTopLayout)
        self.memberRightLayout.addWidget(self.memberRightGroupBox)


        ############Tab 2 Main Layouts##############
        self.memberMainLayout.addLayout(self.memberLeftLayout, 70)
        self.memberMainLayout.addLayout(self.memberRightLayout, 30)
        self.tab2.setLayout(self.memberMainLayout)


    def funcAddProduct(self):
        self.newProduct = add_product.AddProduct()





def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()

