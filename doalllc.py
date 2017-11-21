import os
import numpy as np
import pandas as pd
from numpy import loadtxt

# import local module
import dolc_fromlum

# function to search for filter transmission
def searchtrasm(filters):
	#read transmisison name conversion between database and trasm folder
	tabfilt='nametrasm.dat'
	dbfilters=[]
	trasmfromarchive=[]  
	with open(tabfilt,'r') as tf:
		for line in tf:
			l1=line.strip()
			if not l1.startswith("#"):
				dbfilters.append(str(l1.split()[0]))
				trasmfromarchive.append(str(l1.split()[1]))
	#search
	ftrasm=[]
	for f in filters:
		if f in dbfilters:
			idb=dbfilters.index(f)
			ftrasm.append(trasmfromarchive[idb])
	return ftrasm

# function to read GRB data table
def read_data(file):
    return pd.read_csv(file,sep='\t', header='infer',skiprows=None,skip_blank_lines=True)

data=read_data('table.txt')
data_array=data.values

GRB=data_array[:,0]

# compute lightcurves for each GRB
GRBset=set(GRB)   # unique list of GRBs
for g in GRBset:
	data_grb=data_array[np.where(data_array[:,0]==g),:][0]
	grb=g
	print ' ----------------------------- GRB %s' % grb + '------------------------------'
	redshift=data_grb[0][1]
	filters=set([x[5] for x in data_grb])               #(comma separated list of unique filters)
	ftrasm=searchtrasm(filters)                               
	dolc_fromlum.main(grb,redshift,ftrasm)                   



