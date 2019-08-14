from Account import Account
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
import os
from stat import S_IREAD, S_IRGRP, S_IROTH,S_IWUSR

class Vault():
	
	_check=b'myVault'
	def __init__(self,key,fulldir):
		self.key=key
		self.inputfile=fulldir
		self._dir=fulldir[:fulldir.rfind('/')+1]
		self.filename=fulldir[fulldir.rfind('/')+1:]
		self.listAccount=[]


	def encrypt(self,inData=b''):
		# get the size of the file so  we can write the file better
			#filesize=str(os.path.getsize(self._dir)).zfill(16) 		
			IV=Fernet.generate_key()[:16] # get a random IV
			hasher=SHA256.new(str.encode(self.key)) # create the key base on the password
			key=hasher.digest()
			encryptor=AES.new(key,AES.MODE_CBC,IV) # crate a encrptor usig het key and IV			
			#outputfile=self.inputfile

			if inData==b'':
				with open(self.inputfile,'rb') as infile:
					inData=infile.read()
				#print(inData)
				with open(self.inputfile,'wb') as outfile:
					#outfile.write(str.encode(filesize))
					outfile.write(IV)
					outfile.write(self._check)
					while True:
						chuck = inData[:16]
						inData=inData[16:]
						if len(chuck)==0:
							break
						elif len(chuck) % 16 !=0 :
							chuck+=b' '*(16-len(chuck)%16) # this becasue the encrypt must be multiply of 16
						outfile.write(encryptor.encrypt(chuck))
			else :
				outData=IV
				outData+=self._check
				while True:
					chuck = inData[:16]
					inData=inData[16:]
					if len(chuck)==0:
						break
					elif len(chuck) % 16 !=0:
						chuck+=b' '* (16-len(chuck)%16)
					outData+=encryptor.encrypt(chuck)
				try:
					os.chmod(self.inputfile, S_IWUSR|S_IREAD)
					with open(self.inputfile,'wb') as outfile:
						outfile.write(outData)
					os.chmod(self.inputfile, S_IREAD)
				except:
					with open(self.inputfile,'wb') as outfile:
						outfile.write(outData)
					os.chmod(self.inputfile, S_IREAD)


	def decrypt(self):	
			
			with open(self.inputfile,'rb') as infile:
					IV=infile.read(16)
					check=infile.read(7)
					if check==self._check:
						hasher=SHA256.new(str.encode(self.key))
						key=hasher.digest()
						decryptor=AES.new(key,AES.MODE_CBC,IV)
						data=b'' # 
						while True:
							chuck=infile.read(16)
							#print(data)
							if len(chuck)==0:
								break
							data+=decryptor.decrypt(chuck)
						return True,data
					# outfile.truncate(int(filesize))
					else :
						return False, b''
		# else :

		# 	IV=inData[:16]
		# 	inData=inData[16:]

		# 	hasher=SHA256.new(str.encode(self.key))
		# 	key=hasher.digest()

		# 	decryptor=AES.new(key,AES.MODE_CBC,IV)
		# 	outData=b''

			# while True:
			# 	chuck = inData[:16]
			# 	inData=inData[16:]
			# 	if len(chuck)==0:
			# 		break
			# 	outData+=decryptor.decrypt(chuck)
				

			# return outData

	def __len__(self):
		return len(self.listAccount)


	def extractAccount(self):
		try:
			check,datafile=self.decrypt()
			#print(datafile)
			datafile=bytes.decode(datafile).rstrip().split(',')
			numAccount=int(len(datafile)/3)
			for idx in range(0,numAccount):
					idx*=3
					service=datafile[idx]
					ID=datafile[idx+1]
					passw=datafile[idx+2]
					a=Account(service,ID,passw)
					self.listAccount.append(a)
			#print(datafile)
			return numAccount, check, True
		except :
			return 0,False,False
		
			

class Cryptography():
	def __init__(self, key):
		#self.filename=filename 
		self.key=key
		pass

	def encrypt(self, filename, replace=False, data=b''):
		IV=Fernet.generate_key()[:16] # get a random IV
		hasher=SHA256.new(str.encode(self.key)) # create the key base on the password
		key=hasher.digest()
		encryptor=AES.new(key,AES.MODE_CBC,IV) # crate a encrptor usig het key and IV	
		filesize=str.encode(str(os.path.getsize(filename)).zfill(16) )		

		if filename=='': # encrypt the given data
			outData=IV
			while True:
				chuck = inData[:16]
				inData=inData[16:]
				if len(chuck)==0:
					break
				elif len(chuck) % 16 !=0:
					chuck+=b' '* (16-len(chuck)%16)
				outData+=encryptor.encrypt(chuck)
			return outData
		else :
		
		# replace the original file with encrypted file 
			with open(filename,'rb') as infile:
				inData=infile.read()
				if replace == False:
					filename=filename[:filename.rfind('/')+1]+"(encrypted)"+filename[filename.rfind('/')+1:]
					print(filename)
				with open (filename,'wb') as outfile:
					outfile.write(IV)
					outfile.write(filesize)
					while True:
						chuck = inData[:16]
						inData=inData[16:] # read 16 bytes of the file
						if len(chuck)==0:
							break
						elif len(chuck) % 16 !=0 :
							chuck+=b' '*(16-len(chuck)%16) # this becasue the encrypt must be multiply of 16
						outfile.write(encryptor.encrypt(chuck))

	def decrypt(self, filename,replace=False):
	
	
			with open(filename,'rb') as infile:
				IV=infile.read(16)
				filesize=infile.read(16)

				hasher=SHA256.new(str.encode(self.key)) # create the key base on the password
				key=hasher.digest()
				decryptor=AES.new(key,AES.MODE_CBC,IV) 

				ofile=filename[:filename.rfind('/')+1]+"(D)"+filename[filename.rfind('/')+1:]
				with open(ofile,'wb') as outfile:
					while True:
								chuck=infile.read(16)
								#print(data)
								if len(chuck)==0:
									break
								outfile.write(decryptor.decrypt(chuck))

					outfile.truncate(int(filesize))


# ==== testing class =====
# key='nhat'
# file='AccountTest.txt'
# #data=b'Hello word sakdksak dawi dsajkjd asd askdk asd\nHello word sakdksak dawi dsajkjd asd askdk asdHello word sakdksak dawi dsajkjd asd askdk asd'
# _dir=os.getcwd()+'/TestFolder/'+file
# _dir2=os.getcwd()+"/TestFolder/(encrpted)"+file
# # # _dir=_dir[:_dir.rfind('/')+1]
# # # filename=_dir[_dir.rfind('/')+1:]
# # # print(_dir)

# v=Vault(key,_dir)
# a,b = v.extractAccount()

# print(a[0])
# url=['/home/nhat/Documents/GUI/TestImg/ind2e1x.jpeg','/home/nhat/Documents/GUI/TestImg/index.jpeg','/home/nhat/Documents/GUI/TestImg/inde1x.jpeg']
# url2=['/home/nhat/Documents/GUI/TestImg/(encrypted)ind2e1x.jpeg','/home/nhat/Documents/GUI/TestImg/(encrypted)inde1x.jpeg','/home/nhat/Documents/GUI/TestImg/(encrypted)index.jpeg']
# url3='/home/nhat/Documents/GUI/TestImg/(D)ind2e1x.jpeg'
# c=Cryptophy('nhat')

# # c.encrypt('/home/nhat/Documents/GUI/TestImg/ind2e1x.jpeg')
# # c.decrypt('/home/nhat/Documents/GUI/TestImg/(encrypted)ind2e1x.jpeg')

# for file in url:

# 	c.encrypt(file)

# for file in url2:

# 	c.decrypt(file)