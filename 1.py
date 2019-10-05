import httplib, urllib, base64
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import os
from sklearn.linear_model import LogisticRegression
import datetime as dt
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
import httplib,urllib,base64
import json

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
	#	print coinbase_value
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

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '{subscription key}',
}

params = urllib.urlencode({
    # Request parameters
    'CacheImage': '{boolean}',
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/contentmoderator/moderate/v1.0/ProcessImage/Evaluate?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

