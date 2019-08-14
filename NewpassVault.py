import sys,os
from shutil import copyfile
from stat import S_IREAD, S_IRGRP, S_IROTH
from PyQt5.QtWidgets import (QMainWindow,QLineEdit,QPushButton,QTextEdit,QLabel,QCheckBox, QAbstractItemView,
QHBoxLayout,QVBoxLayout,QApplication,QRadioButton,QWidget, QTableWidget,QTableWidgetItem,QFileDialog,QMessageBox)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Vault import Vault
from Account import Account
from PV_Password import GetPassword

class PasswordVault_newAccount(QWidget):
		_dirIcon=os.getcwd()+'/Icon/'
		_dirBackup=os.getcwd()+'/Backup/'

		def __init__(self):
			super(PasswordVault_newAccount,self).__init__()
			self.myVault=''
			self.filename='' # a fill directory
			self.password=''
			self.viewpass=False
			self.countViewpassword=[]
			self.countCheckbox=[]
			self.countCheckboxAll=False
			self.table=QTableWidget()
			self.vlayout=QVBoxLayout()

			self.move(550,400)
			self.setWindowTitle("New account for password vault")

			self.drawTable()
			self.events()

			self.show()

		def events(self):
			# Table events
			self.tablebtnAdd.clicked.connect(self._tablebtnAdd)
			self.tablebtnDelete.clicked.connect(self._tablebtnDelete)
			self.tablebtnSave.clicked.connect(self._tablebtnSave)
			self.table.cellClicked.connect(self._cellCLicked)
			self.btn_viewpass.clicked.connect(self._viewPass)

			self.tablebtnSave.installEventFilter(self)
			self.tbox_pass.installEventFilter(self)
			#self.tablebtnChangePassword.clicked.connect(self._tableChangepass)
			#self.table.itemSelectionChanged.connect(self._tableEditTable)


		def drawTable(self):		
	
			#check=True
			height=self.frameGeometry().height()
			width=self.table.frameGeometry().width()



			fontBold=QFont()
			fontBold.setBold(True)

			self.tablebtnSave=QPushButton("Save")
			self.tablebtnDelete=QPushButton('-')
			self.tablebtnAdd=QPushButton('+')

			sizeHint_height=self.tablebtnAdd.sizeHint().height()
			self.size=sizeHint_height

			print(self.size)

			self.lbl_pass=QLabel("Password:")
			self.tbox_pass=QLineEdit('')
			self.tbox_pass.setEchoMode(2)
			self.btn_viewpass=QPushButton()
			self.btn_viewpass.setIcon(QIcon(self._dirIcon+'icons8-eye-1.png'))
			#self.btn_viewpass.setIconSize(QSize(self.size,self.size))
		
			#=== Button of the table =====

			


			## SET size for btn
			self.btn_viewpass.setFixedWidth(self.size)
			self.tablebtnDelete.setFixedWidth(sizeHint_height)
			self.tablebtnAdd.setFixedWidth(sizeHint_height)

			## EVNET of the table
			
			#self.tablebtnChangePassword.setDisabled(True)

			hboxTable=QHBoxLayout()
			hboxTable.addWidget(self.lbl_pass)
			hboxTable.addWidget(self.tbox_pass)
			hboxTable.addWidget(self.btn_viewpass)
			hboxTable.addWidget(self.tablebtnSave)

			hboxTable.addWidget(self.tablebtnDelete)
			hboxTable.addWidget(self.tablebtnAdd)
			hboxTable.setAlignment(Qt.AlignRight)
			# Data handle of the table
			#print(self.tbox_filename.text())
			#sefl._noAccount=int(self.tbox_filename.text())
			self.table.setRowCount(1)
			self.table.setColumnCount(5)
			self.table.setItem(0,0, QTableWidgetItem('Service'))
			self.table.setItem(0,1, QTableWidgetItem("ID"))
			self.table.setItem(0,2, QTableWidgetItem('Password'))
			self.table.setItem(0,3, QTableWidgetItem(''))
			self.table.setItem(0,4, QTableWidgetItem(''))
			for i in range(0,5):
				#print(i)
				self.table.item(0,i).setFont(fontBold)
				self.table.item(0,i).setFlags(Qt.ItemIsEnabled)

			# import data to the table

			#==== UPDATA the PasswordVault Layout
			self.table.resizeColumnsToContents()
			self.vlayout.addWidget(self.table)		
			self.vlayout.addLayout(hboxTable)
			self.setLayout(self.vlayout)
			
			#rint(width,height)
			#self.table.setFocusPolicy(Qt.NoFocus)
			self._tablebtnAdd()
			self.resize(width-(width*0.2),height-(height*0.3))

		def widgetInsideTable(self):
			# ===== Button view pass inside table =====
			# viewPassbtn=QPushButton()
			# viewPassbtn.setFixedHeight(self.size_of_btn)
			# viewPassbtn.setFixedWidth(self.size_of_btn)
			# viewPassbtn.setIcon(QIcon(self._dirIcon+'icons8-eye-1.png'))
			# ====== CheckBox ======
			checkBox=QTableWidgetItem()
			checkBox.setIcon(QIcon(self._dirIcon+'icons8-checkbox-0.png'))
			checkBox.setFlags(Qt.ItemIsEnabled)
		






			ItemViewPass=QTableWidgetItem()
			ItemViewPass.setIcon(QIcon(self._dirIcon+'icons8-eye-1.png'))
			ItemViewPass.setFlags(Qt.ItemIsEnabled)
			self.table.setIconSize(QSize(self.size,self.size))

			return checkBox,ItemViewPass

		def eventFilter(self,ob,event):
			#print(event.type())
			if ob is self.tablebtnSave and event.type()==129:
				#print (ob, event.type())

				if self.tbox_pass.text()=='':
					self.tbox_pass.setText("Enter your pass word")
					self.tbox_pass.setStyleSheet("color: red")
					self.tbox_pass.setEchoMode(0)
					self.viewpass=True
					self.btn_viewpass.setIcon(QIcon(self._dirIcon+'icons8-eye-0.png'))
					self.tablebtnSave.setDisabled(True)
			elif ob is self.tbox_pass and event.type()==2:
				self.tbox_pass.setText('')
				self.tbox_pass.setEchoMode(2)
				self.viewpass=False
				self.btn_viewpass.setIcon(QIcon(self._dirIcon+'icons8-eye-1.png'))
				self.tablebtnSave.setDisabled(False)
				self.tbox_pass.setStyleSheet("color: black")

				


			return False

		def saveFileDialog(self):    
		  options = QFileDialog.Options()
		  options |= QFileDialog.DontUseNativeDialog
		  fileName, a = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Text Files (*.txt)", options=options)
		  #print(a)
		  if fileName:
		      return fileName

		def convertData_2_bytes(self): # this function is user before encrypt data
			noRow=self.table.rowCount()
			data=''
			for i in range(1,noRow):
				#print(len(self._listAccount))			
				Service=self.table.item(i,0).text()
				ID=self.table.item(i,1).text()
				PASS=self.table.cellWidget(i,2).text()
				
				data+=f',{Service},{ID},{PASS}'

			data=str.encode(data[1:])
			return data

		@pyqtSlot()

		def _viewPass(self):
			self.viewpass= not self.viewpass
			if self.viewpass==True:
				self.tbox_pass.setEchoMode(0)
				self.btn_viewpass.setIcon(QIcon(self._dirIcon+'icons8-eye-0.png'))
				#print ("echo 0")
			else :
				self.tbox_pass.setEchoMode(2)
				self.btn_viewpass.setIcon(QIcon(self._dirIcon+'icons8-eye-1.png'))

		def _tablebtnAdd(self): # when a new row added a new account created coreponding to the row nomber
			#print(self.table.rowCount())
			checkBox,iViewPass=self.widgetInsideTable()
			self.table.insertRow(self.table.rowCount())
			newRowidx=self.table.rowCount()-1

			# setup new row
			
			self.table.setItem(newRowidx,0, QTableWidgetItem(' new service'))
			self.table.setItem(newRowidx,1, QTableWidgetItem(' new ID '))
			self.table.setCellWidget(newRowidx,2, QLineEdit('type pass'))
			self.table.setItem(newRowidx,3, iViewPass)
			self.table.setItem(newRowidx,4, checkBox)
			#self.table.item(newRowidx,3).setIcon(QIcon(self._dirIcon+'icons8-eye-0.png'))

			self.table.cellWidget(newRowidx,2).setEchoMode(2)
			self.countViewpassword.append(True)
			self.countCheckbox.append(False)
			self.table.resizeColumnsToContents()

		def _tablebtnDelete(self):
			#print(self.countCheckbox)
			#print(len(self.countCheckbox))
			
			idx=0
			out = True
			while idx<len(self.countCheckbox):
				checkBox=self.countCheckbox[idx]
				if checkBox == True:
					self.table.removeRow(idx+1)
					self.countCheckbox.remove(self.countCheckbox[idx])
					idx=-1
				idx+=1
			
			#.statusBar.showMessage(f'A row at {self.currentRow-2} was delete')
			#print(self.countCheckbox)
		
		def _tablebtnSave(self):
			self.filename=self.saveFileDialog()+'.txt'
			self.password=self.tbox_pass.text()
			self.myVault=Vault(self.password,self.filename)
			dataReady=self.convertData_2_bytes()
			self.myVault.encrypt(dataReady)
			os.chmod(self.filename, S_IREAD)


		def _cellCLicked(self,row,column):
			## cellClicked for view password
			if column==3 and row>0:
				self.countViewpassword[row-1]= not self.countViewpassword[row-1]
				if self.countViewpassword[row-1]==False:
					self.table.cellWidget(row,2).setEchoMode(0)
					self.table.item(row,column).setIcon(QIcon(self._dirIcon+'icons8-eye-0.png'))
				else :
					self.table.cellWidget(row,2).setEchoMode(2)
					self.table.item(row,column).setIcon(QIcon(self._dirIcon+'icons8-eye-1.png'))
			## cellClicked for cehckbox
			elif column==4 and row>0:
				#print (self.countCheckbox[row-1])
				self.countCheckbox[row-1]= not self.countCheckbox[row-1]
				#	print('clicked',row, column,self.countCheckbox[row-1])
				if self.countCheckbox[row-1]==True:
					self.table.item(row,column).setIcon(QIcon(self._dirIcon+'icons8-checkbox-1.png'))
				else :
					self.table.item(row,column).setIcon(QIcon(self._dirIcon+'icons8-checkbox-0.png'))
				#print(self.countCheckbox)
			elif row==0 and column==4:
				self.countCheckboxAll= not self.countCheckboxAll
				for i in range(1,self.table.rowCount()):
					if self.countCheckboxAll==True:
						self.countCheckbox[i-1]=True
						self.table.item(i,4).setIcon(QIcon(self._dirIcon+'icons8-checkbox-1.png'))
					else :
						self.countCheckbox[i-1]=False
						self.table.item(i,4).setIcon(QIcon(self._dirIcon+'icons8-checkbox-0.png'))
			self.table.resizeColumnsToContents()

# if __name__ == "__main__":
		
# 		app = QApplication(sys.argv)	
# 		w=PasswordVault_newAccount()
# 		try:
# 			sys.exit(app.exec_())
# 		except:
# 			pass