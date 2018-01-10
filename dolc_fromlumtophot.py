#!/usr/bin/env python

'''
Take target with redshift and path to observed filters, for each filter get LC from models in OBSERVER frame
Usage "dolc_fromlumtophot.py target redshift filters(comma separated)"
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
	import dosimphot                                        
	
	## input
	target = sys.argv[1]
	redshift = sys.argv[2]
	mytrasm = sys.argv[3]     # path to transmission
	redshift  = float(redshift)
	models=sys.argv[4] #'Barnes2016_split'  # where models at different times are
	trangmic='mic'   # USED MICRONS IN TRASMISSIONS (otehrwise write ~angstroms)
	
	#target = 'KN200mpc' 
	#redshift = 0.0435 
	#ftrasm = 'micParanal_HAWKI.H' 
	#models='Barnes2016_split'
	#redshift  = float(redshift)
	#ftrasm = str(ftrasm).split(',')
	
	# handle path models
	
	if os.path.isfile(models):
		(dirpath, file) = os.path.split(models)
		modelnames=[file]
	elif os.path.isdir(models):
		(dirpath, dirnames, modelnames) = walk(models).next()
	else:
		sys.exit("ERROR: Specified file/directory not found: %s" % models)
	
	
	if os.path.isfile(mytrasm):
		(trasmpath, tfile) = os.path.split(mytrasm)
		trasmname=tfile
	else: 	
		sys.exit("ERROR: Specified file/directory not found: %s" % models)
	
	#initialize output data
	targetlcfile=target+'_'+dirpath+'_redshift'+str(redshift)+str(trasmname)+'_lcphot.dat'         
	out=open(targetlcfile,'w')
	header='#lambda[A]      F[Jy]           mag[AB] filter	       MJD'
	out.write('%s\n' %header) 
	
	# cycle over models at different times and get lc of KN model
	targetlc=[]	
	modelsorted=sorted(modelnames, key=str.lower, reverse=False) # just for easier visualization
	for m in modelsorted:
		print '--------------------  MODEL IS %s' % m 
		modelfile=join(dirpath,m)
		targetlum=dosimphot.main(modelfile,mytrasm,trangmic,redshift)
		targetlc+=targetlum
		
	#print ' check output'	
	#print targetlc
	
	# write output lc for each GRB	
	for item in targetlc:
		out.write('%.2f\t%.7e\t%.4f\t%s\t%.4f\n' %(item[0],item[1],item[2],item[3],item[4]))
	
	out.close


if __name__ == "__main__":
   usage()
   main()


