#!/usr/bin/python
import numpy as np
import pandas as pd
import json
import datetime

DATA_DIR='data/'

#####################
def read(mode='train'):
	df = pd.read_csv(f'{DATA_DIR}{mode}_transaction.csv')
	# (590540, 434)
	dfi = pd.read_csv(f'{DATA_DIR}{mode}_identity.csv')
	df =  pd.merge(df, dfi, how='left', on='TransactionID')
	return df

#####################
def readtmp(mode='train'):
	df = pd.read_csv(f'{DATA_DIR}firstof_{mode}_transaction.csv')
	# (10000, 434)
	dfi = pd.read_csv(f'{DATA_DIR}firstof_{mode}_identity.csv')
	df =  pd.merge(df, dfi, how='left', on='TransactionID')
	return df

#####################
def readready():
	df = pd.read_csv(f'{DATA_DIR}numiricData.csv')
	return df

#####################
def fill_nulls(data):
	'''
		This functions fills the nulls with -1
	'''
	cols = list(data.columns)
	for col in cols:
		data[col] = data[col].fillna('-1')

#####################
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

#####################
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

#####################
def pre_Emaildomain(data):
	P = data['P_emaildomain'].values
	R = data['R_emaildomain'].values
	companies = {'Yahoo': ['yahoo','ymail','frontier','rocketmail'], 'Microsoft': ['hotmail', 'outlook', 'live', 'msn'],
	'Appe': ['icloud', 'mac', 'me'], 'AT&T': ['prodigy', 'att', 'sbcglobal', 'bellsouth'], 'Centurylink': ['centurylink', 'embarqmail','q'],
	'AOL': ['aim', 'aol'], 'Spectrum': ['twc', 'charter','cfl'], 'Xfinity': ['comcast'], 'Verizon': ['verizon'], 'Google':['gmail'], 'Mail': ['mail'],
	'Earthlink':['earthlink'], 'Anonymous': ['anonymous'], 'Cox':['cox'], 'Roadrunner': ['roadrunner'], 'Juno':['juno'], 'Optonline': ['optonline'],
	'Suddenlink': ['suddenlink'], 'Netzero': ['netzero'], 'WebDe': ['web.de'], 'Windstream': ['windstream'],'Cableone': ['cableone'], 'Gmx':['gmx'],'Servicios': ['servicios']}
	for i in range(len(P)):
		if P[i] == '-1':
			continue
		for CName in companies:
			for domain in companies[CName]:
				if domain in P[i]:
					P[i] = CName
				
	for i in range(len(R)):
		if R[i] == '-1':
			continue
		for CName in companies:
			for domain in companies[CName]:
				if domain in R[i]:
					R[i] = CName
					
#####################
def make_numiric(data):
	'''
		This function converts all non-numiric columns to numiric 
	'''
	pre_Emaildomain(df)

	#All non-numiric columns
	cols = ['ProductCD','card4','card6','P_emaildomain','R_emaildomain','id_12','id_15','id_16','id_23','DeviceType','DeviceInfo']+['id_'+str(i) for i in range(27,39) if i != 32]+['M'+str(i) for i in range(1,10)]
	for col in cols:
		dic, arr = Values2IDs(data, col)
		#if len(dic.keys()) < 10:
		#print(col,': ',dic)
		data[col] = arr


#####################
def get_prepare_data(data):
	X = data
	Y = data['isFraud'].values
	X.drop(['isFraud'], axis=1)
	X.drop(['TransactionID'], axis=1)
	return X, Y

#####################--------------------------------
def isThereNigative1(data):#TESTING
	'''
		Making sure that there's no -1 values (to present it as null) "Prints NO"
	'''
	cols = list(data.columns)
	for col in cols:
		for i in col:
			if i in [-1,'-1']:
				return 'YES'
	return 'NO'

#####################
def testing(data):#TESTING
	'''
		Checking if all P_emaildomain are the same as R_emaildomain or not 
	'''
	R_emaildomain = data['R_emaildomain'].values
	for i in range(len(R_emaildomain)):
		if not pd.isna(R_emaildomain[i]) and not pd.isna(P_emaildomain[i]) and R_emaildomain[i] != P_emaildomain[i]:
			print(P_emaildomain[i],' ======> ',R_emaildomain[i])

#####################
def fraud_data(data):#TESTING
	isFraud = data['isFraud'].values
	R = data['R_emaildomain'].values
	for i in range(len(isFraud)):
		if isFraud[i] == 1:
			print(R[i])

#####################
def show_TransactionDT(data):#TESTING
	START_DATE = '2017-12-01'
	startdate = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
	TransactionDT = data['TransactionDT'].apply(lambda x: (startdate + datetime.timedelta(seconds = x)))

	print(TransactionDT.head())
	print(TransactionDT.tail())

#####################
if __name__ == '__main__':
	if 1:#Run this just once 
		df = readtmp()
		#print(isThereNigative1(df)) #to make sure -1 is the right number to present null values
		fill_nulls(df)
		show_TransactionDT(df)
		make_numiric(df)
		print(df.head())
		df.to_csv(f'{DATA_DIR}numiricData.csv', index=False)
