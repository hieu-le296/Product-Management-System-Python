# Product Management System
This Product Management System is COMP 371 Project

## Features:
This application has some basic features:
* Exceptional Theme
* Add Product
* Add Membership
* Sell Product with the option to print receipt 
* Display simple statistics with Pie Charts
* Search for products/membership/records
* Save As CSV or PDF file
* Print option
* Show information on the right panel by clicking any cell of table
* Update item/membership by double clicking any cell of table
* Change admin password
* Some shortcuts to quickly open windows

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on any platform.

If you run this project in Virtual Environment, please delete the previous virtual environment (venv) and create the new one whenever you run it on the different Operating System.

## Prerequisites

What things you need to install the software and how to install them

```
Python 3.6 and later
Windows 10
MacOS 10.13 or later 
Linux OS such as CentOS, Ubuntu, Linux Mint
Visual Studio Code (optional for editor)
```

## Installing

Open terminal (Command Prompt on Windows 10) and type:

```
pip install -r requirements.txt
```

*Note: You can create python virtual environment to install python dependencies.

## Running the program

In order to run this program:

### Direct run
Double click the file main.py

### By terminal/Command Prompt:
##### On Mac/Linux:

```
python3 main.py
```
##### On Windows:
```
python main.py
```
## Login to program
```
username: admin
password: password
```

## Distribution - Windows 10
```
pip install cx_freeze
```
```
python3 setup.py build
```
The executable file (main_window.exe) will be located in build folder

You can deploy on the different OS, but setup.py must be modified


## Built With

* [Python 3](https://www.python.org/) - The programming language
* [PIP](https://pypi.org/project/pip/) - Dependency ManagementT
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) - Qt application framework 

## Planned Technology

* PyQt5 Core
* PyQt5 QWidgets
* PyQt5 QtGui
* PyQt5 QtChart
* PyQt5 QtPrintSupport
* PIL 
* Database: sqlite3
* Hashing 

## Version

* Version 1.0

## Author

* **Hieu Le**

## License

This project is the initial work for academic work at the University of the Fraser Valley. All Rights Reserved.