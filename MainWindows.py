import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from NewpassVault import PasswordVault_newAccount
from PasswordVault import PasswordVault
from CryptopyFiles import CryptoFiles
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()

class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab2 = PasswordVault(500,400,"Decryotion file")
        self.tab1 = PasswordVault_newAccount()
        self.tab3 = CryptoFiles()
       # self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"New password vault")
        self.tabs.addTab(self.tab2,"Open password vault")
        self.tabs.addTab(self.tab3,'Files/Image cryptophy')

        # Create first tab


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    try:
        sys.exit(app.exec_())
    except:
        pass
