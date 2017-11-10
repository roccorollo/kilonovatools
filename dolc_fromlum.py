#!/usr/bin/env python

'''
Take GRB with redshift and observed filters, for each filter get LC from models in rest frame
Usage "dolc_fromlum.py grb redshift filters(comma separated"
'''

__Version__ = "0.1"
__Author__ = "Andrea Rossi "

def usage():
    print __doc__
    #print __Usage__
    #print __Notes__

def main():
	
	#import sys
	import os
	from os import walk, sys, path
	from os.path import join
	
	# import other prog
	import dogrbsimlum
	
	# input
	grb = sys.argv[1]
	redshift = sys.argv[2]
	filters = sys.argv[3]
	redshift  = float(redshift)
	filters = str(filters).split(',')     # filters
	
	models='gw170817fromXSdata/'
	trasm='trasm/R_Cousins.dat'
	trangmic='mic'
	
	
	if os.path.isfile(models):
		(dirpath, file) = os.path.split(models)
		modelnames=[file]
	elif os.path.isdir(models):
		(dirpath, dirnames, modelnames) = walk(models).next()
	else:
		sys.exit("ERROR: Specified file/directory not found: %s" % models)
	
	grblc=[]		
	for f in filters:
		for m in modelnames:
			modelfile=join(dirpath,m)
			grblum=dogrbsimlum.main(modelfile,trasm,trangmic,redshift,f)
			grblc.append(grblum)

	print grblc
		
	
if __name__ == "__main__":
   usage()
   main()


