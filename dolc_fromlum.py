#!/usr/bin/env python

'''
Take GRB with redshift and observed filters, for each filter get LC from models in rest frame
Usage "dolc_fromlum.py grb redshift filters(comma separated)"
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
	filters = str(filters).split(',')     # filters as list
	
	models='gw170817fromXSdata'  # where models at different times are
	trasm='trasm'    #  where trasnmissions are
	trangmic='mic'   # USED MICRONS IN TRASMISSIONS (otehrwise write ~angstroms)
	
	
	if os.path.isfile(models):
		(dirpath, file) = os.path.split(models)
		modelnames=[file]
	elif os.path.isdir(models):
		(dirpath, dirnames, modelnames) = walk(models).next()
	else:
		sys.exit("ERROR: Specified file/directory not found: %s" % models)
	
	
	#initialize output data
	testfile='test'         
	out=open(testfile,'w')
	header='#lambda[A]  L[erg/s/Hz]         filter	     MJD'
	out.write('%s\n' %header) 
	
	# cycle over models at different times and get lc of KN model
	grblc=[]	
	modelsorted=sorted(modelnames, key=str.lower, reverse=False) # just for easier visualization
	for m in modelsorted:
		print '--------------------  MODEL IS %s' % m +'------------------------'
		modelfile=join(dirpath,m)
		grblum=dogrbsimlum.main(modelfile,trasm,trangmic,redshift,filters)
		grblc+=grblum
		
	print ' check output'	
	print grblc
		
	for item in grblc:
		out.write('%.2f\t%.7e\t%s\t%s\n' %(item[0],item[1],item[2],item[3]))


if __name__ == "__main__":
   usage()
   main()


