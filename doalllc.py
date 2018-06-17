
'''
Take entry table table.txt and for each GRB gives LCs from models. Put then lightcurves in folder ./lc
'''

__Version__ = "0.1"
__Author__ = "Andrea Rossi "



import os
import sys
import numpy as np
import pandas as pd
from numpy import loadtxt

# import local module
import dolc_fromlum
#import write_newtablegrb.py

# import tabel from mysql db:
os.system("mysql -u rossi -p981424r MisceCats -e \'select GRB,z,dhour,Flux,Fluxerr,filter from sgrb ORDER BY GRB,filter;\' > tablegrb.txt")
os.system("python write_newtablegrb.py")
os.system("date=$(date '+%Y-%m-%d');rm table.txt; cp tablegrb.txt table${date}.txt;  ln -s table${date}.txt table.txt ")


# function to search for filter transmission
def searchtrasm(filters):
	#read transmisison name conversion between database and trasm folder
	tabfilt='trasm/nametrasm.txt'
	#tabfilt='trasm/nametrasm.txt.old
	dbfilters=[]
	trasmfromarchive=[]  
	with open(tabfilt,'r') as tf:
		for line in tf:
			l1=line.strip()
			if not l1.startswith("#"):
				#print l1
				dbfilters.append(str(l1.split()[0]))
				trasmfromarchive.append(str(l1.split()[1]))
				#print str(l1.split()[0]),str(l1.split()[1])
	#search
	ftrasm=[]
	for f in filters:
		if f in dbfilters:
			idb=dbfilters.index(f)
			ftrasm.append(trasmfromarchive[idb])
	return ftrasm

# function to read GRB data table
def read_data(file,skiprows):
    return pd.read_csv(file,sep='\t', header='infer',skiprows=skiprows,skip_blank_lines=True)

#data=read_data('test.txt')
#
if len(sys.argv)>1:
	print "TEST"
	os.system("cat test.txt >table+gw.txt")
else:
	os.system("grep -v '#' trasm/nametrasm.txt |awk '{print \"170817A\t0.00980\t0.0001\t0.0000001\t0.0001\t\"$1\"\t\"$1}' > GRB170817A.txt ")
	os.system("grep -v '#' trasm/nametrasm.txt |awk '{print    \"GRB0\t0.00000\t0.0001\t0.0000001\t0.0001\t\"$1\"\t\"$1}' > defaultz0.txt ")
	os.system("cat table.txt GRB170817A.txt defaultz0.txt>table+gw.txt")
	#os.system("echo # >table+gw.txt; cat GRB170817A.txt defaultz0.txt>table+gw.txt")
	
data=read_data('table+gw.txt',1)
data_array=data.values

GRB=data_array[:,0]

# compute lightcurves for each GRB
GRBset=set(GRB)   # unique list of GRBs
for g in GRBset:
	data_grb=data_array[ np.where(data_array[:,0]==g ),:][0]
	grb=g
	print ' ----------------------------- GRB %s' % grb + '------------------------------'
	redshift=data_grb[0][1]
	filters=set([x[6] for x in data_grb])               #(comma separated list of unique filters)
	ftrasm=searchtrasm(filters)  
	dolc_fromlum.main(grb,redshift,ftrasm)                   

os.system("if [ -d  lc ]; then sleep 0.1; else mkdir lc; fi ")
os.system("mv *lc.dat lc")


