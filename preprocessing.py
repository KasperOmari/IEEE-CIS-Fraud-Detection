#!/usr/bin/python
import numpy as np
import pandas as pd
import json

DATA_DIR='data/'

def read(mode='train'):
	df = pd.read_csv(f'{DATA_DIR}{mode}_transaction.csv')
	# (590540, 434)
	dfi = pd.read_csv(f'{DATA_DIR}{mode}_identity.csv')
	df =  pd.merge(df, dfi, how='left', on='TransactionID')
	return df


def readtmp(mode='train'):
	df = pd.read_csv(f'{DATA_DIR}tmp.csv')
	# (590540, 434)
	dfi = pd.read_csv(f'{DATA_DIR}tmpI.csv')
	df =  pd.merge(df, dfi, how='left', on='TransactionID')
	return df


def readAll():
	df = pd.read_csv(f'{DATA_DIR}dftmp.csv')
	return df


def readready():
	df = pd.read_csv(f'{DATA_DIR}numiricTmp.csv')
	return df


def testing(data):#TESTING
	R_emaildomain = data['R_emaildomain'].values
	for i in range(len(R_emaildomain)):
		if not pd.isna(R_emaildomain[i]) and not pd.isna(P_emaildomain[i]) and R_emaildomain[i] != P_emaildomain[i]:
			print(P_emaildomain[i],' ======> ',R_emaildomain[i])


def fraud_data(data):#TESTING
	cols = list(data.columns)
	dec = {}
	isFraud = data['isFraud'].values
	for i in range(len(isFraud)):
		if isFraud[i] == 1:
			for x in cols:
				if x not in dec:
					dec[x]=[]
				if not pd.isna(data[x].values[i]):
					dec[x].append(data[x].values[i])
	return dec


def fill_nulls(data):
	'''
		This functions fills the nulls with -1
	'''
	cols = list(data.columns)
	for col in cols:
		data[col] = data[col].fillna('-1')


def getLables(col, string):
	col = np.sort(col)
	items = {}
	c = 0
	for i in col:
		if i not in items:
			if i != -1 and i != '-1':
				items[i] = c
				c+=1
	return items


def Values2IDs(data, string):
	newcol = []
	col = data[string].values
	items = getLables(col, string)
	for i in col:
		if i not in items:
			if i not in [-1, '-1']:#!= -1 and i != '-1':
				newcol.append(items[i])
			else:
				newcol.append('-1')
		else:
			newcol.append(items[i])
	
	#Make values with more that 10 keys starts with 10 
	if len(items.keys()) > 10:
		for i in items:
			items[i] +=10

	return items, np.array(newcol)
	#return items


def make_numiric(data):
	'''
		This function converts all non-numiric columns to numiric 
	'''
	#All non-numiric columns
	cols = ['ProductCD','card4','card6','P_emaildomain','R_emaildomain','id_12','id_15','id_16','DeviceType','DeviceInfo']+['id_'+str(i) for i in range(28,39) if i != 32]+['M'+str(i) for i in range(1,10)]
	for col in cols:
		dic, arr = Values2IDs(data, col)
		#if len(dic.keys()) < 10:
		#print(col,': ',dic)
		data[col] = arr

def isThereNigative1(data):#TESTING
	cols = list(data.columns)
	for col in cols:
		for i in col:
			if i in [-1,'-1']:
				return 'YES'
	return 'NO'



if __name__ == '__main__':
	if False:#Run this just once 
		df = readtmp()
		#print(isThereNigative1(df)) #to make sure -1 is the right number to present null values
		fill_nulls(df)
		make_numiric(df)
		print(df.head())
		df.to_csv(f'{DATA_DIR}numiricTmp.csv', index=False)
	
	if True:
		df = readready()

#######################################
#df = readAll()
#print(df.head())
#print('='*50)
#make_numiric(df)
#print(df.head())

#df.to_csv(f'{DATA_DIR}numiricTmp.csv', index=False)
#######################################

#######################################
#df = readtmp()
#fill_nulls(df)
#df.to_csv(f'{DATA_DIR}dftmp.csv',index=False)
#######################################

'''
==================> All Features:

TransactionID	#Train: min = 86400 max = 15811131
				#Test: min = 18403224 max = 34214345

isFraud 		#The labels

TransactionDT	#Timedelta from a given reference datetime (not an actual timestamp)

TransactionAmt	#transaction payment amount in USD 

addr1, addr2	#Address

dist1, dist2	#Distance between (not limited) billing address, mailing address, zip code, IP address, phone area, etc.

C1 - C14		#Counting, such as how many addresses are found to be associated with the payment card, etc. The actual meaning is masked. 

D1 - D15		#Timedelta, such as days between previous transaction, etc. 

V1 - V339 		#Vesta engineered rich features, including ranking, counting, and other entity relations.
		  		#Groups according to data
		 		#{V1 - V11}, {V12 - V34}, {V35 - V52}, {V53 - V94}, {V95 - V125},
		  		#{V126 - V137}, {V138 - V166}, {V167 - V201}, {V202 - V216}, {V217 - V262},
		  		#{V263 - 278}, {V279 - V305}, {V306 - V321}, {V322 - V339}

==================> Categorical Features:

ProductCD

P_emaildomain

R_emaildomain	#Most of them are null

card1 - card6	#{[card1 - card3] + card5 = int}, {}

id_01 - id_38	#id_33: Screen dimensions
				#(id_01, id_06 & id_14 has nigative values, but there's no -1s){id_22 - id_27}

M1 - M9 		#Match, such as names on card and address, etc.

DeviceType

DeviceInfo

'''