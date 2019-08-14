import sys,os
from shutil import copyfile

from PyQt5.QtWidgets import (QMainWindow,QLineEdit,QPushButton,QTextEdit,QLabel,QCheckBox, QAbstractItemView,QPlainTextEdit,
QHBoxLayout,QVBoxLayout,QApplication,QRadioButton,QWidget, QTableWidget,QTableWidgetItem,QFileDialog,QMessageBox)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Vault import Cryptography
from Account import Account
from PV_Password import ChangePassword


class CryptoFiles(QWidget):
	def __init__(self):
		super(CryptoFiles,self).__init__()
		self.listFiles=[]
		self.password=''



		self.draw()
		self.events()
		self.show()

	def draw(self):
		height=self.frameGeometry().height()
		width=self.frameGeometry().width()
		print(width)
		self.Files=QPlainTextEdit()
		self.Files.setFixedHeight(height/2+150)
		self.Files.setFixedWidth(width)
		self.Files.setReadOnly(True)
		self.password=QLineEdit()

		self.btn=QPushButton("Encrypt")
		self.Browse=QPushButton('Select files')
		width_btn=self.btn.sizeHint().width()

		self.btn.setFixedWidth(width/4)
		self.Browse.setFixedWidth(width/4)
		self.password.setFixedWidth(width/4)
		#elf.Browse.setFixedWidth(width_btn/2)

		self.E=QRadioButton('Encrypt')
		self.D=QRadioButton('Decrypt')
		self.E.setChecked(True)

		self.vbox=QVBoxLayout()
		self.vbox.addWidget(self.Browse)
		self.vbox.addWidget(self.password)
		self.vbox.addWidget(self.E)
		self.vbox.addWidget(self.D)
		self.vbox.addWidget(self.btn)
		self.vbox.setAlignment(Qt.AlignTop)

		self.hbox=QHBoxLayout()
		self.hbox.addWidget(self.Files)
		self.hbox.addLayout(self.vbox)
		self.hbox.setAlignment(Qt.AlignTop)

		self.setLayout(self.hbox)
		print(height)

	def events(self):
		self.E.installEventFilter(self)
		self.D.installEventFilter(self)
		self.Browse.clicked.connect(self._btnBrowse)
		self.btn.clicked.connect(self._btn)
		self.btn.installEventFilter(self)
		self.password.installEventFilter(self)


	def openFileNamesDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py);;Text FIles (*.txt)", options=options)
		if files:
			print(type(files))
			return files

	def eventFilter(self,ob,event):
		if (ob is self.E or ob is self.D) and event.type()==2:
			self.btn.setText(ob.text())
		elif ob is self.btn and event.type()==129 and self.password.text()=='':
			self.password.setText("Enter your password")
			self.password.setStyleSheet("color: red")
			self.password.setEchoMode(0)
			self.btn.setDisabled(True)
		elif ob is self.password and event.type()==2:
			self.password.setText('')
			self.password.setStyleSheet("color: black")
			self.password.setEchoMode(2)
			self.btn.setDisabled(False)

		return False

	@pyqtSlot()

	def _btnBrowse(self):
		self.listFiles=self.openFileNamesDialog()
		string=''
		for i,url in enumerate(self.listFiles):
			string+=url+'\n'
		self.Files.setPlainText(string)
	def _btn(self):
		cryptophy=Cryptography(self.password.text())
		for file in self.listFiles:
			if self.btn.text()=='Encrypt':
				cryptophy.encrypt(file)
				print('Encrypt')
			else:
				print('Decrypt')
				cryptophy.decrypt(file)
		

		


# if __name__ == "__main__":
		
# 		app = QApplication(sys.argv)	
# 		w=CryptoFiles()
# 		try:
# 			sys.exit(app.exec_())
# 		except:
# 			pass