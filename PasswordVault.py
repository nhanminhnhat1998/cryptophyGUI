import sys,os
from shutil import copyfile

from PyQt5.QtWidgets import (QMainWindow,QLineEdit,QPushButton,QTextEdit,QLabel,QCheckBox, QAbstractItemView,
QHBoxLayout,QVBoxLayout,QApplication,QRadioButton,QWidget, QTableWidget,QTableWidgetItem,QFileDialog,QMessageBox)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Vault import Vault
from Account import Account
from PV_Password import ChangePassword
#from PyQt5.QtWidgets import QWidget,QMainWindow

class PasswordVault(QWidget):
	
	#_listAccount=[]
	count=True
	_newFileCount=True
	_filename='' # this is a full path of the file
	_password=''
	_dirIcon=os.getcwd()+'/Icon/'
	_dirBackup=os.getcwd()+'/Backup/'
	
	countTable=[]
	countCheckbox=[]
	countCheckboxAll=False
	
	
	def __init__(self,x,y,title=""):
		super(PasswordVault,self).__init__()
		self.x=x
		self.y=y
		self._myVault=''
		self.changePass=ChangePassword()
		self.changePass.getPass.connect(self._getPass)
		# self.height=height
		# self.width=width
		self.saveflag=True
		self.title=title
		#self.move(self.x,self.y)
		self.setWindowTitle(self.title)
		self.vlayout=QVBoxLayout()



		self.draw()
		self.drawTable()
		self.events()

		self.show()
		#self.setGeometry(self.x,self.y,self.width,self.height)
		#self.statusBar().showMessage('Message in statusbar.')
	# This function is stored all the events of the app
	def events(self):
		#click events
		self.btn_unclock.clicked.connect(self._btnUnClockCick)
		self.btn_brownse.clicked.connect(self._btnBrowse)
		self.btn_showpass.clicked.connect(self._btnShowpass)
		self.btn_brownse.installEventFilter(self)
		#self.table.clicked.connect(self._tableClickpass)
		self.table.cellClicked.connect(self._cellCLicked)
		self.table.cellChanged.connect(self._cellChanged)
		# Table events
		self.tablebtnAdd.clicked.connect(self._tablebtnAdd)
		self.tablebtnDelete.clicked.connect(self._tablebtnDelete)
		self.tablebtnSave.clicked.connect(self._tablebtnSave)
		self.tablebtnChangePassword.clicked.connect(self._tableChangepass)

		#self.table.itemSelectionChanged.connect(self._tableEditTable)

	# Draw the inition GUI for the app
	def draw(self):
		font_lbl_errorMsg=QFont()
		font_lbl_errorMsg.setItalic(True)
		font_lbl_errorMsg.setUnderline(True)
		
		# Table
		self.table=QTableWidget()
		#self.table.setEditTriggers(QAbstractItemView.NoEditTriggers);
		self.table.setFocusPolicy(Qt.NoFocus);
		self.table.setSelectionMode(QAbstractItemView.NoSelection);

		# ============= LABEL ===============
		self.lbl_filename=QLabel("Filename:") 
		self.lbl_password=QLabel("Password:")
		self.lbl_errorMsg=QLabel("")

		self.lbl_errorMsg.setFont(font_lbl_errorMsg)
		#self.lbl_errorMsg.setText("<font color='blue'>Create new file</font>")
		#self.lbl_errorMsg.setOpenExternalLinks(True)
		#self.lbl_errorMsg.installEventFilter(self)
		# ============= BUTTON =====================
		
		self.btn_brownse=QPushButton()
		self.btn_brownse.setIcon(QIcon(self._dirIcon+'icons8-browse-page-filled-50.png'))
		sizeHint_height=self.btn_brownse.sizeHint().height()
		self.size=sizeHint_height# this is a hint size is used for the table
		#print(sizeHint_height)
		self.btn_brownse.setIconSize(QSize(sizeHint_height,sizeHint_height))
		#self.btn_brownse.setFixedWidth(sizeHint_height)
		#self.btn_brownse.setFixedHeight(self.size_of_btn)

		self.btn_showpass=QPushButton()
		self.btn_showpass.setIcon(QIcon(self._dirIcon+'icons8-eye-1.png'))
		self.btn_showpass.setIconSize(QSize(sizeHint_height,sizeHint_height))
		self.btn_unclock=QPushButton("Unclock")
		self.btn_unclock.setDisabled(True)
		#radio button
		# self.rbtn_textfile=QRadioButton("Text file")
		# self.rbtn_image=QRadioButton("Image file")

		# text box
		self.tbox_filename=QLineEdit("--- Select your file ---") 
		self.tbox_password=QLineEdit() 

		self.tbox_filename.setReadOnly(True)
		self.tbox_password.setEchoMode(2)


		hbox1=QHBoxLayout()	
		hbox1.addWidget(self.lbl_filename)
		hbox1.addWidget(self.tbox_filename)
		hbox1.addWidget(self.btn_brownse)
		#hbox1.addWidget(self.btn_hint)

		hbox2=QHBoxLayout()
		hbox2.addWidget(self.lbl_password)
		hbox2.addWidget(self.tbox_password)
		hbox2.addWidget(self.btn_showpass)
		hbox2.addWidget(self.btn_unclock)

		hbox3=QHBoxLayout()
		hbox3.addWidget(self.lbl_errorMsg)


		
		self.vlayout.addLayout(hbox1)
		self.vlayout.addLayout(hbox2)
		self.vlayout.addLayout(hbox3)


		
		#self.resize(580,120)
		self.setLayout(self.vlayout)
	# Create a data table
	def drawTable(self):		
	
		#check=True
			height=self.frameGeometry().height()
			width=self.table.frameGeometry().width()

			fontBold=QFont()
			fontBold.setBold(True)

			#=== Button of the table =====

			self.tablebtnSave=QPushButton("Save")
			self.tablebtnChangePassword=QPushButton("Change vault's password")
			self.tablebtnDelete=QPushButton('-')
			self.tablebtnAdd=QPushButton('+')
			## SET size for btn
			sizeHint_height=self.tablebtnAdd.sizeHint().height()
			self.tablebtnDelete.setFixedWidth(sizeHint_height)
			#self.tablebtnDelete.setFixedHeight(self.size_of_btn)
			self.tablebtnAdd.setFixedWidth(sizeHint_height)
			#self.tablebtnAdd.setFixedHeight(self.size_of_btn)

			## EVNET of the table
			

			self.tablebtnAdd.setDisabled(True)
			self.tablebtnSave.setDisabled(True)
			self.tablebtnDelete.setDisabled(True)
			self.tablebtnChangePassword.setDisabled(True)

			hboxTable=QHBoxLayout()
			
			hboxTable.addWidget(self.tablebtnChangePassword)
			hboxTable.addSpacing((width/height)*120)
			hboxTable.addWidget(self.tablebtnSave)
			#hboxTable.addSpacing((width/height)*20)
			hboxTable.addWidget(self.tablebtnDelete)
			hboxTable.addWidget(self.tablebtnAdd)
			
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
			
			print(width,height)
		#self.table.setFocusPolicy(Qt.NoFocus)
			self.resize(width,height)
	# Generate Item and Widget inside table cell
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
		# Item view pass
			ItemViewPass=QTableWidgetItem()
			ItemViewPass.setIcon(QIcon(self._dirIcon+'icons8-eye-1.png'))
			ItemViewPass.setFlags(Qt.ItemIsEnabled)
			self.table.setIconSize(QSize(self.size,self.size))

		# ====== Line Edit / Textbox ======
	
			
	
			return checkBox,ItemViewPass
	# pop-up a browse for choosing a file
	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text Files (*.txt)", options=options)
		if fileName:
			self.resetData()
			return fileName
	# Converting all the data on the created table into a desire format
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
	# A message from saving a file
	def popup_save_table(self):
			choice = QMessageBox.question(self,'Double check!',"Your original file will be move to a backup folder\n Your edited data will be save at the same location with the same name",QMessageBox.Close)
			if choice == QMessageBox.Close:
			#self._filename[sefl._filename.rfind('/')+1:]
					backupname=self._filename[self._filename.rfind(')')+1:]

					backupdir=self._dirBackup+'(BackupE)'+backupname
					copyfile(self._filename,backupdir)
					sys.exit()
			else:
					pass
	#confirm closing a working file
	def popup_exitingfile(self):
		op =QMessageBox.question(self,'Warning',"Do you want to save this file",(QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel))

		if op==QMessageBox.Save :
			self._tablebtnSave()
			return True
		elif op==QMessageBox.Discard:
			return True
		else : 
			return False
	# Getting the data from encrypted file then upload to the table base on the design format
	def assignData2Table(self):
			del self._myVault
			self._myVault=Vault(self._password,self._filename) # create the vault
			a,check,checkPass=self._myVault.extractAccount()
			if checkPass==False:
				#print("Plase enter diff password")
				self.lbl_errorMsg.setText("<font color='red'>Please try a diff password</font>")

			else:#print(len(self._myVault))
				if check==True:
					#Enbale some btn if the file is open successfully
					self.lbl_errorMsg.setText('')
					self.tablebtnAdd.setDisabled(False)
					self.tablebtnSave.setDisabled(False)
					self.tablebtnDelete.setDisabled(False)
					self.tablebtnChangePassword.setDisabled(False)
					self.btn_unclock.setDisabled(True)

					for idx,item in enumerate(self._myVault.listAccount):
						#print(idx)
						self.table.insertRow(self.table.rowCount())
						newRowidx=self.table.rowCount()-1
						checkBox,iViewPass=self.widgetInsideTable()
						self.table.setItem(newRowidx,0, QTableWidgetItem(item.service))
						self.table.setItem(newRowidx,1, QTableWidgetItem(item.ID))
						self.table.setCellWidget(newRowidx,2, QLineEdit(item.PASS))
						self.table.setItem(newRowidx,3, iViewPass)
						self.table.setItem(newRowidx,4, checkBox)

						

						self.countTable.append(True)
						self.countCheckbox.append(False)

						self.table.cellWidget(newRowidx,2).setEchoMode(2)
					#print(self.table.item(1,3).sizeHint().height())
				else :
					#print("Print a message box : error the invalid file")
					del self._myVault
					self._myVault=''
					self.lbl_errorMsg.setText("<font color='red'>the file which is invaild, is not the format of password vault app</font>")

				self.table.resizeColumnsToContents()
	# Reset all data and delete the table / ready for another open file or create new file
	def resetData(self):
		PasswordVault._filename='' # this is a full path of the file
		PasswordVault._password=''
		del PasswordVault.countTable
		del PasswordVault.countCheckbox
		del self._myVault
		PasswordVault.countTable=[]
		PasswordVault.countCheckbox=[]
		self._myVault=''
		for i in range(self.table.rowCount()-1,0,-1):
			self.table.removeRow(i)

		#self.setLayout(self.vlayout)
		#self.draw()
		
		#self.show()

	# overite Event
	def eventFilter(self,ob, event):
		if ob is self.btn_brownse and event.type()==129:
			for i in range(0,self.table.rowCount()-1):
				#print(self._myVault.listAccount[i].PASS,self.table.cellWidget(i+1,2).text())
				if self._myVault.listAccount[i].PASS!=self.table.cellWidget(i+1,2).text():
					self.saveflag=False

		return False
# this is the overwrite event of the lbl_errorMsg and can be for other widget
	# def eventFilter(self,ob,event):
	# 		#print(type(ob))
	# 		if ob is self.lbl_errorMsg and event.type()==2:
	# 			#print(event.type())
	# 			PasswordVault._newFileCount = not PasswordVault._newFileCount
	# 			#print(PasswordVault._new)
	# 			if PasswordVault._newFileCount==False: #new account
	# 				self.tbox_filename.setReadOnly(False)
	# 				self.btn_unclock.setDisabled(False)
	# 				self.btn_brownse.setDisabled(True)
	# 				self.btn_unclock.setText('Create')
	# 				self.tbox_filename.setText("--- Enter your file name ---")

	# 				self.lbl_errorMsg.setText("<font color='blue'>Already have a file</font>")
					
	# 			else: 
	# 				self.tbox_filename.setReadOnly(True)
	# 				self.btn_unclock.setDisabled(True)
	# 				self.btn_brownse.setDisabled(False)

	# 				self.btn_unclock.setText('Unclock')
	# 				self.tbox_filename.setText("--- Select your file ---")

	# 				self.lbl_errorMsg.setText("<font color='blue'>Create new file</font>")





	# 			return False
	# 		else :
	# 		  return False


# ======== events =========
	@pyqtSlot()
	# Event Browse btn
	def _btnBrowse(self):
			#self.resetData()
			#print(self._myVault)
			op=True
			if not self.saveflag : # currently openning a file
				op=self.popup_exitingfile()

			
			if op==True:
				self._filename=self.openFileNameDialog()
				if self._filename:
					self.tbox_password.setText('')
					self.tbox_filename.setText(self._filename)
					self.btn_unclock.setDisabled(False)
					#self.saveflag=False
			else : pass
	# event of Unclock btn or Create new file btn
	def _btnUnClockCick(self):
		self._password=self.tbox_password.text()
		#print(PasswordVault._newFileCount)
		if self._password:
			self.assignData2Table()
			self.saveflag=True

		else :
			self.lbl_errorMsg.setText("<font color='red'>password is empty</font>")
			#print("Pop up a error message: password is empty")
		#these for testing
		# self._filename="/home/nhat/Documents/GUI/Project_1_encryption/TestFolder/(encrpted)AccountTest.txt"
		# self._password='nhat'

		#self.show()

	def _btnShowpass(self):

		self.count= not self.count
		if self.count==False:
			self.tbox_password.setEchoMode(0)
			self.btn_showpass.setIcon(QIcon(self._dirIcon+'icons8-eye-0.png'))
			#print ("echo 0")
		else :
			self.tbox_password.setEchoMode(2)
			self.btn_showpass.setIcon(QIcon(self._dirIcon+'icons8-eye-1.png'))
	
	def _cellCLicked(self,row,column):
		## cellClicked for view password
		if column==3 and row>0:
			self.countTable[row-1]= not self.countTable[row-1]
			if self.countTable[row-1]==False:
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
	
	def _cellChanged(self,row,column):
		if row>0 and column is not 3 and column is not 4:
		#	print ("cell changed")
			self.saveflag=False

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
		self.countTable.append(True)
		self.countCheckbox.append(False)
		self.table.resizeColumnsToContents()
		self.saveflag=False

	def _tablebtnDelete(self):
		#print(self.countCheckbox)
		#print(len(self.countCheckbox))
		self.saveflag=False
		
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
		dataReady=self.convertData_2_bytes()
		#print(dataReady)
		self._myVault.encrypt(dataReady)
		print("Saved")
		self.saveflag=True
		#self.resetData()
		# print("reset adtributes")
		# for i in reversed(range(self.vlayout.count())): 
		# 		self.vlayout.removeItem(self.vlayout.takeAt(i))
		# self.drawTable()
		#print(self.countCheckbox)
		#self.save_PasVault()
	
	def _tableChangepass(self):
		self.changePass.currentPassword=self._password
		self.changePass.show()

	def _getPass(self, thepass):
		print('New pass:',thepass)
		tempList=self._myVault.listAccount
		dataReady=''
		for i,account in enumerate(tempList):
			dataReady+=f',{account.service},{account.ID},{account.PASS}'
		dataReady=str.encode(dataReady[1:])
		print(dataReady)
		del self._myVault
		self._myVault=Vault(thepass,self._filename)
		self._myVault.encrypt(dataReady)
		print("Password was changed successfully")


# if __name__ == "__main__":
		
# 		app = QApplication(sys.argv)	
# 		w=PasswordVault(500,400,"Decryotion file")
# 		try:
# 			sys.exit(app.exec_())
# 		except:
# 			pass



