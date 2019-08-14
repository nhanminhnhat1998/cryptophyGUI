class Account():
	def __init__(self,service='', ID='',PASS=''):
		self.service=service
		self.ID=ID
		self.PASS=PASS

	def edit(self,newservice, newID,newPASS):
		self.service=newservice
		self.ID=newID
		self.PASS=newPASS
	def __str__(self):
		return f"{self.service}: {self.ID} - {self.PASS}"

