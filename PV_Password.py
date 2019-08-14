import sys,os


from PyQt5.QtWidgets import (QLineEdit,QPushButton,QLabel,
QHBoxLayout,QVBoxLayout,QApplication,QWidget)
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ChangePassword(QWidget):

		getPass=pyqtSignal(str)
		def __init__(self,currentPassword=''):
			super().__init__()
			self.move(500,500)
			self.currentPassword=currentPassword
			#self.newPass=''
			self.setWindowTitle("Change password")
			#self.app=app
			


			self.draw()
			self.btn_change.clicked.connect(self._btnChange)
			self.btn_cancel.clicked.connect(self.close)

			#self.show()

		def draw(self):
			self.lbl_currentPass=QLabel("Current password: ")
			self.lbl_newPass=QLabel("New password")
			self.lbl_confirmPass=QLabel("Confirm new password:")

			self.tbox_currentPass=QLineEdit("")
			self.tbox_newPass=QLineEdit("")
			self.tbox_confirmPass=QLineEdit("")

			self.btn_change=QPushButton("Change")
			self.btn_cancel=QPushButton("Cancel")


			self.tbox_currentPass.setEchoMode(2)
			self.tbox_newPass.setEchoMode(2)
			self.tbox_confirmPass.setEchoMode(2)

			self.tbox_newPass.installEventFilter(self)
			self.tbox_confirmPass.installEventFilter(self)
			self.btn_change.installEventFilter(self)

			self.lbl_error=QLabel('')
			self.lbl_error1=QLabel('')
			# self.vlayoutL=QVBoxLayout()
			# self.vlayoutL.addWidget(self.lbl_currentPass)
			# self.vlayoutL.addWidget(self.lbl_newPass)
			# self.vlayoutL.addWidget(self.lbl_confirmPass)
			# self.vlayoutL.addWidget(self.btn_change)

			# self.vlayoutR=QVBoxLayout()
			# self.vlayoutR.addWidget(self.tbox_currentPass)
			# self.vlayoutR.addWidget(self.tbox_newPass)
			# self.vlayoutR.addWidget(self.tbox_confirmPass)
			# self.vlayoutR.addWidget(self.btn_cancel)
			l1=len(self.lbl_currentPass.text())
			l2=len(self.lbl_newPass.text())
			l3=len(self.lbl_confirmPass.text())

			# self.hlayout=QHBoxLayout()
			# self.hlayout.addLayout(self.vlayoutL)
			# self.hlayout.addLayout(self.vlayoutR)
			# 
			self.h1=QHBoxLayout()
			self.h1.addWidget(self.lbl_currentPass)
			self.h1.addWidget(self.tbox_currentPass)

			self.h2=QHBoxLayout()
			self.h2.addWidget(self.lbl_newPass)
			self.h2.addWidget(self.tbox_newPass)

			self.h3=QHBoxLayout()
			self.h3.addWidget(self.lbl_confirmPass)
			self.h3.addWidget(self.tbox_confirmPass)

			self.h4=QHBoxLayout()
			self.h4.addWidget(self.btn_change)
			self.h4.addWidget(self.btn_cancel)

			self.vlayout=QVBoxLayout()
			self.vlayout.addLayout(self.h1)
			self.vlayout.addWidget(self.lbl_error)
			self.vlayout.addLayout(self.h2)
			self.vlayout.addLayout(self.h3)
			self.vlayout.addWidget(self.lbl_error1)
			self.vlayout.addLayout(self.h4)

			self.setLayout(self.vlayout)

		def eventFilter(self,ob,event):
			#print(event.type())
			if ( ob is self.tbox_newPass) and event.type() ==2:
				print(self.currentPassword,self.tbox_currentPass.text())
				if self.currentPassword!=self.tbox_currentPass.text() and self.tbox_currentPass.text() is not '':
					self.lbl_error.setText("<font size=3 color='red'><i><u>Your current password doesn't match</u></i></font>")
				else :
					self.lbl_error.setText("")

			elif ob is self.btn_change and event.type() ==129:
				print(self.tbox_confirmPass.text(),self.tbox_newPass.text())
				if self.tbox_confirmPass.text()!=self.tbox_newPass.text() :
					self.lbl_error1.setText("<font size=3 color='red'><i><u>Password doesn't match</u></i></font>")
					self.btn_change.setDisabled(True)
				else :
					self.lbl_error1.setText("")
			elif ( ob is self.tbox_newPass or ob is self.tbox_confirmPass) and event.type() ==5:
					self.btn_change.setDisabled(False)

			return False

		def emptyTbox(self):
			self.tbox_newPass.setText('')
			self.tbox_currentPass.setText('')
			self.tbox_confirmPass.setText('')

		@pyqtSlot()

		def _btnChange(self):
			print("Changed")
			self.getPass.emit(self.tbox_newPass.text())
			self.emptyTbox()
			self.close()

		


		
		# app = QApplication(sys.argv)	
		# w=ChangePassword('nhat',app)
		# w.show()
		# sys.exit(app.exec_())
		# 
		# 

class GetPassword(QWidget):
		getPass=pyqtSignal(str)
		def __init__(self,currentPassword=''):
			super().__init__()
			self.move(500,500)
			self.currentPassword=currentPassword
			#self.newPass=''
			self.setWindowTitle("Change password")
			#self.app=app
			


			self.draw()
			self.btn_change.clicked.connect(self._btnSave)
			self.btn_cancel.clicked.connect(self.close)

		def draw(self):
			self.lbl_newPass=QLabel("New password")
			self.lbl_confirmPass=QLabel("Confirm new password:")

			self.tbox_newPass=QLineEdit("")
			self.tbox_confirmPass=QLineEdit("")

			self.btn_change=QPushButton("Save")
			self.btn_cancel=QPushButton("Cancel")


			#self.tbox_currentPass.setEchoMode(2)
			self.tbox_newPass.setEchoMode(2)
			self.tbox_confirmPass.setEchoMode(2)

			self.tbox_newPass.installEventFilter(self)
			self.tbox_confirmPass.installEventFilter(self)
			self.btn_change.installEventFilter(self)

			
			self.lbl_error1=QLabel('')

			# 
		

			self.h2=QHBoxLayout()
			self.h2.addWidget(self.lbl_newPass)
			self.h2.addWidget(self.tbox_newPass)

			self.h3=QHBoxLayout()
			self.h3.addWidget(self.lbl_confirmPass)
			self.h3.addWidget(self.tbox_confirmPass)

			self.h4=QHBoxLayout()
			self.h4.addWidget(self.btn_change)
			self.h4.addWidget(self.btn_cancel)

			self.vlayout=QVBoxLayout()
			self.vlayout.addLayout(self.h2)
			self.vlayout.addLayout(self.h3)
			self.vlayout.addWidget(self.lbl_error1)
			self.vlayout.addLayout(self.h4)

			self.setLayout(self.vlayout)

		def emptyTbox(self):
			self.tbox_newPass.setText('')
			self.tbox_confirmPass.setText('')

		def eventFilter(self,ob,event):
			#print(event.type())
			
			if ob is self.btn_change and event.type() ==129:
				print(self.tbox_confirmPass.text(),self.tbox_newPass.text())
				if self.tbox_confirmPass.text()!=self.tbox_newPass.text() :
					self.lbl_error1.setText("<font size=3 color='red'><i><u>Password doesn't match</u></i></font>")
					self.btn_change.setDisabled(True)
				else :
					self.lbl_error1.setText("")
			elif ( ob is self.tbox_newPass or ob is self.tbox_confirmPass) and event.type() ==5:
					self.btn_change.setDisabled(False)

			return False

		@pyqtSlot()
		def _btnSave(self):
			#print("Changed")
			self.getPass.emit(self.tbox_newPass.text())
			self.emptyTbox()
			self.close()


# app = QApplication(sys.argv)	
# w=GetPassword()
# w.show()
# try:
# 	sys.exit(app.exec_())
# except:
# 	pass