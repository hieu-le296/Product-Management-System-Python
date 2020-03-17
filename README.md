# Product-Manager-Python
This Product Manager Application is COMP 371 Project

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on any platform.

If you run this project in Virtual Environment, please delete the previous virtual environment (venv) and create the new one whenever you run it on the different Operating System.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.6 and later
Windows 10
MacOS 10.13 or later 
Linux OS such as CentOS, Ubuntu, Linux Mint
Visual Studio Code (optional for editor)
```

### Installing

Open terminal (Command Prompt on Windows 10) and type:

```
#pip3 install -r requirements.txt
```

#Note: You can create python virtual environment to install python dependencies.

## Running the tests

There is no need to run database migration again. In order to run this program:

```
python3 main_window.py
```

## Login to program
```
username: admin
password: password
```

## Deployment - Windows 10
```
pip3 install cx_freeze
```
```
python3 setup.py build
```
The executable file (main_window.exe) will be located in build folder

#You can deploy on the different OS, but setup.py must be modified


## Built With

* [Python 3](https://www.python.org/) - The programming language
* [PIP](https://pypi.org/project/pip/) - Dependency ManagementT
* [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) - Qt application framework 

## Planned Technology

* PyQt5 Core
* PyQt5 QWidgets
* PyQt5 QtGui
* PyQt5 QtChart
* Database: SQLlite
* Hashing 

## Version

* Version 1.0

## Author

* **Hieu Le**

## License

This project is licensed under the GNUv3 License - see the [LICENSE.md](LICENSE.md) file for details