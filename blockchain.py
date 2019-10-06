
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from google.cloud import vision
import sys
import os
from sklearn.linear_model import LogisticRegression
import datetime as dt
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
import httplib,urllib,base64
import json


def detect_safe_search_uri(uri):
    """Detects unsafe features in the file located in Google Cloud Storage or
    on the Web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation
   

    return safe

#private_key = RSA.generate(2048,prng)
#public_key = private_key.publickey()
#generate return RSA key object


#dynamic updation of rewards after some criteria



class block:
	# chain.addblock(id,users['goofy'][0][1],users['goofy'][0][1],no,transaction,0,None,sign,hashed_value)
	def __init__(self,id,sender,receiver,amount,transaction,spentflag,parent_block_id,signature,hashed_value,coinbase_value,reward,type_of_trans,content,miner_id,miner_name):
		self.id = id
		self.dirty = 0
		self.amount = amount
		self.prev = None
		self.sender = sender
		self.receiver = receiver
		self.next = None
		self.parent_block_id = parent_block_id
		self.transaction = transaction
		self.spentflag = spentflag	 #0-not spent, 1-spent
		self.timestamp = dt.datetime.now().strftime("Created on %d %b,%y(%A) at %I:%M:%S %p")	#dt.date.today().weekday()
		self.signature = signature


		self.hash = hashed_value
		self.coinbase = coinbase_value
		self.type = type_of_trans #send/receive,return
		self.reward = reward
		self.content = content #until trans. type is return
		self.miner_name = miner_name

		if (id==-1 and sender == "" and receiver == "" and amount == -1 and transaction == '' and spentflag == -1 and parent_block_id == -1 and signature == '' and hashed_value == '' and coinbase_value == '' and reward == 50 and type_of_trans == '' and content == ''):
			self.miner_id = miner_id
			self.miner_name = miner_name
		else:
			self.miner_id = ''
			self.miner_name = ''



		#also add minted variable to keep diff between goofy to goofy...or check previous pointer whether it's None or not
		#and goofy to anyone splitted having also goofy to goofy


class blockchain:
	def __init__(self):
		self.head=None
		self.id=0

	def blockid(self):
		self.id+=1
		return self.id

	def ischainempty(self):#return true/false
		return self.head == None
	
			

	def addblock(self,block_id,sender,receiver,amount,transaction,spentflag,parent_block_id,signature,hashed_value,coinbase_value,reward,type_of_trans,content,miner_id,miner_name):
	

		


	#### if you have 0 bitcoin, you can't pay as you have spent all bitcoin ####		
	#	-_value
	#	self.civalue=False
	#	if coinbase_value.find(".jpg") or coinbase_value.find(".jpeg") or coinbase_value.find(".png") or coinbase_value.find(".bmp"):
	#		civalue = self.content_filter_image(coinbase_value)		
	#		if ciValue is True:
	#			print "Malicious Content"
	#			return	
	#	cfValue = self.content_filter_text(coinbase_value)
	#	if cfValue is True:
	#		print "Malicious Content"
	#		return		
	#	print miner_name
		if amount == 0:
			spentflag = 1
		temp=block(block_id,sender,receiver,amount,transaction,spentflag,parent_block_id,signature,hashed_value,coinbase_value,reward,type_of_trans,content,miner_id,miner_name)
		############################
		
		h=self.head
		if h == None:
			self.head = temp
		else:
			while h.next != None:
				h=h.next
			h.next=temp

	def getlatestblock(self):
		t = self.head
		while t.next != None:
			t = t.next
		return t

#traverse to vid
	def getblock_by_id(self,vid):
		t = self.head
		while t != None:
#			print 'current_block_id',t.id
			if t.id == vid:
				return t
			t = t.next

	def isvalid(self,vid):
		if self.getblock_by_id(vid).dirty:
			return False
		else:
			return True

	def calculate_hash(self,data):
		return SHA256.new(data).hexdigest()

	def printchain(self):
		print 'chain\n['
		t=self.head
		while t != None:# '!=' is equivalent to 'is not'
			#using SHA256 for shortening long public and private keys and signature also...
			try:
				pk = SHA256.new(t.sender.exportKey('PEM')).hexdigest()
				sk = SHA256.new(t.receiver.exportKey('PEM')).hexdigest()
			except:
				pk = ''
				sk = ''
			print '''
  {
     ID: ''',t.id,'''
     Is Valid: ''',self.isvalid(t.id),'''
     Sender(Public Key): ''',pk,'''
     Receiver(Public Key): ''',sk,'''
     Parent: ''',t.parent_block_id,'''
     Amount: ''',t.amount,'''
     Transaction: ''',t.transaction,'''
     Timestamp: ''',t.timestamp,'''
     Spent: ''',t.spentflag,'''
     Signature: ''',SHA256.new(str(t.signature)).hexdigest(),'''
     Hash: ''',t.hash,'''
     Coinbase: ''',t.coinbase,'''
     Type of trans. : ''',t.type,'''
     Content Value: ''',t.content,'''
     Miner ID: ''',t.miner_id,'''
     Miner Name: ''',t.miner_name,'''
     Reward: ''',t.reward,'''
  }
			'''
			t=t.next
		print ']'




def main():

	def getTokens(input):
		tokensBySlash = str(input.encode('utf-8')).split('/')
		allTokens = []
		for i in tokensBySlash:
			tokens = str(i).split('-')
			tokensByDot = []
			for j in range(0,len(tokens)):
				tempTokens = str(tokens[j]).split('.')
				tokensByDot = tokensByDot + tempTokens
			allTokens = allTokens + tokens + tokensByDot
		allTokens = list(set(allTokens))
		if 'com' in allTokens:
			allTokens.remove('com')
	#total_tokens = allTokens		
		
		return allTokens

	#allurls = 'my_data.csv'
	#allurlscsv = pd.read_csv(allurls,',',error_bad_lines = False)
	#allurlsdata = pd.DataFrame(allurlscsv)		
	#allurlsdata = np.array(allurlsdata)
	#random.shuffle(allurlsdata)
	#y = [d[1] for d in allurlsdata]
	#corpus = [d[0] for d in allurlsdata]
	vectorizer = TfidfVectorizer(tokenizer = getTokens)
	#X = vectorizer.fit_transform(corpus)
	#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
	#lgs = LogisticRegression()
	#lgs.fit(X_train, y_train)

#	def url_filtering(input):
#		print "Here"
		

	def getkeys():
		prng = Random.new().read
		key = RSA.generate(2048,prng)
		private_key = key#.exportKey('PEM')
		public_key = key.publickey()#.exportKey('PEM')
		keys=[private_key,public_key]
		return keys

	def add_user():
		###### local reference ######
		name = raw_input('Enter username: ').lower()
		if name in users:
			print 'User already exists !'
			return
		users[name] = [getkeys(),0]  #DOUBT
		#############################

	def show_users():
		###### local reference ######
		if not users:
			print 'No users are there in system !'
		else:
			for i in users:
				print i,' has ',users[i][1],' bitcoin in total'
				# print i,
			# print users.keys()
		#############################

	def transact():
		sender = raw_input('Enter Sender: ').lower()

		if sender not in users:
			print "User:",sender,"don't exist!"
			ch = raw_input('Add user(Y/N)?')
			if ch.lower() == 'y':
				add_user()
			return

		receiver = raw_input('Enter Receiver:').lower()

		if receiver not in users:
			print "User:",receiver,"don't exist!"
			ch = raw_input('Add user(Y/N)?')
			if ch.lower() == 'y':
				add_user()
			return

		amt = int(raw_input('Enter amount: '))

		#### precheck balance then only go forward ####
		if users[sender][1] == 0:
			print sender,"have 0 balance !"
			return

		######## work on cryptography

		############################

		t = chain.head
		while t != None:
			#comparing pulbic keys of the two nodes
			if t.receiver == users[sender][0][1] and t.spentflag == 0 and amt <= t.amount:
				current_amt = t.amount
				t.spentflag = 1
				parent_block_id = t.id
				###### local reference ######
				users[sender][1] = users[sender][1]-amt
				users[receiver][1] = users[receiver][1]+amt
				#############################
				break
			else:
				t = t.next

			if t == None:
				print sender,' is trying to spend more than what they have !'
				return
		#############################



		#### we can add block before verifying the transaction by meeting certain conditions or during the time of adding block...

		transaction1 = SHA256.new(sender+' paid '+str(amt)+' coins to '+receiver).hexdigest()   #DOUBT
		coinbase_value = raw_input('Enter the coinbase data here:')
		#print coinbase_value
		



		while(1):
			print '''
	Enter the type of transaction:
	1) Send/Receive
	2) Return
	'''
			try:
				type_of_trans = int(raw_input())
				if type_of_trans == 1 or type_of_trans == 2:
					break
			except:
				print 'Enter again correctly !'			

		if type_of_trans == 1:
			typees = 'send/receive'
		else:
			typees = 'return'
			content_value = raw_input('Enter the content value: ')
			url_filtering(content_value)
			print content_value





		transaction2 = SHA256.new(sender+' paid '+str(current_amt-amt)+' coins to '+sender).hexdigest()

		id1 = chain.blockid()
		id2 = chain.blockid()
		data_for_signature1 = str(id1)+str(users[sender][0][1])+transaction1+str(amt)
		data_for_signature2 = str(id2)+str(users[sender][0][1])+transaction2+str(current_amt-amt)

		sign1 = calculate_signature(users[sender][0][0],data_for_signature1)
		sign2 = calculate_signature(users[sender][0][0],data_for_signature2)

		hashed_value1 = chain.calculate_hash(data_for_signature1)
		hashed_value2 = chain.calculate_hash(data_for_signature2)


		miner = raw_input('Hello Miner Enter your name !')
		mid = SHA256.new(miner).hexdigest()[:10]


		chain.addblock(id1,users[sender][0][1],users[receiver][0][1],amt,transaction1,0,parent_block_id,sign1,hashed_value1,coinbase_value,50,type_of_trans,content_value,'','')
		chain.getlatestblock().prev = chain.getblock_by_id(parent_block_id)

		chain.addblock(id2,users[sender][0][1],users[sender][0][1],current_amt-amt,transaction2,0,parent_block_id,sign2,hashed_value2,coinbase_value,50,type_of_trans,content_value,'','')
		chain.getlatestblock().prev = chain.getblock_by_id(parent_block_id)

		chain.addblock(-1,'','',-1,'',-1,-1,'','','',-1,'','',mid,miner)
		chain.getlatestblock().prev = chain.getblock_by_id(parent_block_id)
		# if (id==-1 and sender == "" and receiver == "" and amount == -1 and transaction == '' and spentflag == -1 and parent_block_id == -1 and signature == '' and hashed_value == '' and coinbase_value == '' and reward == -1 and type_of_trans == '' and content == ''):


		# chain.add_miner_block(mid,miner,miner_reward)

	def display_chain():
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
		chain.printchain()
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

	def make_coin():
		no = int(raw_input('Enter no. of coins: '))
		
		######## local reference #######
		users['goofy'][1]=users['goofy'][1]+no
		################################

		transaction = SHA256.new('Goofy created '+str(no)+' more coins in the system!').hexdigest()

		#no need to add str(None) in data_for_signature here in make_coin
		id = chain.blockid()
		data_for_signature = str(id)+str(users['goofy'][0][1])+transaction+str(no)
		sign = calculate_signature(users['goofy'][0][0],data_for_signature)

		hashed_value = chain.calculate_hash(data_for_signature)
		coinbase_value = raw_input('Enter the coinbase data:')

		
		#print (lgs.score(X_test, y_test))
		safe=detect_safe_search_uri(coinbase_value)
		if(safe.adult>2 or safe.violence>2 or safe.racy>2):
    			print("CODE RED")

		print coinbase_value
		#X_predict = [coinbase_value]
		#X_predict = vectorizer.transform(X_predict)
		#y_predict = lgs.predict(X_predict)
		#print y_predict
		#if y_predict[0] == 'bad':
		#	print "Data found is spam...Sorry miner this block can't be mined !!! Please update ..!!"
		#	exit(1)



		while(1):
			print '''
	Enter the type of transaction:
	1) Send/Receive
	2) Return
	'''
			try:
				type_of_trans = int(raw_input())
				if type_of_trans == 1 or type_of_trans == 2:
					break
			except:
				print 'Enter again correctly !'			

		content_value = ''
		if type_of_trans == 1:
			typees = 'send/receive'
		else:
			typees = 'return'
			content_value = raw_input('Enter the content value: ')
					#print (lgs.score(X_test, y_test))
			print content_value
			X_predict = [content_value]
			X_predict = vectorizer.transform(X_predict)
			y_predict = lgs.predict(X_predict)
			print y_predict
			if y_predict[0] == 'bad':
				print "Data found is spam...Sorry miner this block can't be mined !!! Please update ..!!"
				exit(1)

	#	print "HI"
		chain.addblock(id,users['goofy'][0][1],users['goofy'][0][1],no,transaction,0,None,sign,hashed_value,coinbase_value,50,typees,content_value,'','')
	#	print "BYE"
		miner = raw_input('Hello Miner Enter your name !')
		mid = SHA256.new(miner).hexdigest()[:10]

		chain.addblock(-1,'','',-1,'',-1,-1,'','','',-1,'','',mid,miner)


		# chain.add_miner_block(mid,miner,miner_reward)




	def calculate_signature(sender_private_key,data):
		digest = SHA256.new(data).hexdigest()#digest or hash same thing
		signature = sender_private_key.sign(digest,'')
		return signature


	def match_signature(sender_public_key,data,signature):
		digest = SHA256.new(data).hexdigest()
		return sender_public_key.verify(digest,signature)


	def verify():
		vid = int(raw_input('Enter the block id(to verify): '))
		found = chain.getblock_by_id(vid)
		if found == None:
			print "Block don't exist !"
			return
		# if found.prev == None:
		# 	print 'Transaction is valid !'
		# else:

		current_signature = found.signature
		current_transaction = found.transaction
		current_amt = found.amount
		current_sender = found.sender
		current_id = found.id

		while found.prev != None:
			# ########### finding sender name to get its private key from the local data structure(dictionary) ###########
			# for i in users:
			# 	if users[i][0][1] == found.sender:
			# 		sender_name = i
			# 		break
			# ###########################################

			data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)
			# sign = calculate_signature(users[sender_name][0][0],data_for_signature)

			if match_signature(current_sender,data_for_signature,current_signature):
				found = found.prev
			else:
				print 'Transaction is NOT VALID !'
				return
			current_signature = found.signature
			current_transaction = found.transaction
			current_amt = found.amount
			current_sender = found.sender
			current_id = found.id

		data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)
		if match_signature(current_sender,data_for_signature,current_signature):
			print 'Transaction is VALID !'
		else:
			print 'Transaction is NOT VALID !'

	def change_block():
		cb = int(raw_input('Enter block id to change: '))
		bk = chain.getblock_by_id(cb)
		bk.amount = 5000
		bk.dirty = 1


	def ischain_valid():
		t = chain.head
		if t == None:
			print 'Chain is empty, do some transactions first !'
			return
		while t != None:
			# checking if block is dirty or not, if it is then not valid
			if not chain.isvalid(t.id):
				print 'Chain is NOT VALID !'
				return
			t = t.next
		print 'Chain is VALID !'

	#name vs [[private_key,public_key],amount]
	users={
	'goofy':[getkeys(),0]
	}
	chain = blockchain()


	while(True):
		print '''
	|------- MENU --------|
	| 1.Add user          |
	| 2.Make coin         |
	| 3.Do transaction    |
	| 4.Show blockchain   |
	| 5.Show users        |
	| 6.Verify transaction|
	| 7.Change a block    |
	| 8.Is chain valid?   |
	| 9.Exit              |
	|---------------------|'''
		try:
			ch=int(raw_input())
		except Exception:
			print 'Please enter choice no. !'
			continue
		myswitch={
		1:add_user,
		2:make_coin,
		3:transact,
		4:display_chain,
		5:show_users,
		6:verify,
		7:change_block,
		8:ischain_valid,
		9:exit
		}
		#handle wrong choice error
		try:
			myswitch.get(ch)()
		except Exception as e:
			print e



if __name__ == '__main__':
	main()
