#!/usr/bin/env python

'''
Take spectra template and trasmission, and computes observed mag at given distance
'''

__Version__ = "0.1"
__Author__ = "Andrea Rossi "
__Usage__ = "dosimphot.py model path_trasmission y_for_angstrom_else_mic  redshift"

import sys
def usage():
    print __Usage__

def main():
 	
 ##---------------------------------------------------------
 #Import packages
 import os
 from os import walk, sys, path
 from os.path import join
 import fnmatch
 #from os import sys, walk
 import platform
 import subprocess

 #from scipy.interpolate import splprep, splev
 #from scipy.interpolate import interp1d
 from scipy.constants import speed_of_light
 from numpy import loadtxt, arange #, pi, log, linspace, convolve
 ##import scipy.io.array_import
 ##from optparse import OptionParser
 
 # import other prog
 import ift
 import lumflux
 import andNEDredshift
 
 ############ get input
 
 modelfile = sys.argv[1]
 mypath    = sys.argv[2]
 sameunit  = sys.argv[3]
 redshift  = sys.argv[4]
 sameunit  = str(sameunit)
 redshift  = float(redshift)
 
 
 if not os.path.isfile(modelfile):
       sys.exit("ERROR: Specified file not found: %s" % modelfile)
       
 if not os.path.isdir(mypath):
       sys.exit("ERROR: Specified directory not found: %s" % mypath)
 
 #############  Constants
 ##cc=speed_of_light
 ##ckm=cc/1000 ## km/s
 ##ccm=cc*100 ## cm/s
 ##cca=cc*10**10 ##angstrom /s
 ##zpab=8.926    ## zp for flux in Jy
 
 def full_path(filepath):
     if platform.system() == 'Windows':
         if filepath[1:3] == ':\\':
             return u'\\\\?\\' + os.path.normcase(filepath)
     return os.path.normcase(filepath)
    
 
#subprocess.call("python ifultra.py trasm/Generic_Cousins.R.dat trasm/Generic_Cousins.R.dat")

 def angtomic(lamm,sameunit):
      if sameunit in ("y"):
         lamm=lamm/1.
      else :
         lamm=lamm/1e4        
      return lamm                    
     
 def trasmpos(flum):
    flum=(flum**2)**0.5
    return flum        

 # compute distance lum
 distlum=andNEDredshift.distlum(redshift)
 
 #--------------------- Read model file
 mar=loadtxt(modelfile)
 mar=mar[mar[:,0].argsort()]
 lamm=mar[:,0] ## be sure that lambda unit is the same
 lum=mar[:,1] 
 lamm=angtomic(lamm,sameunit)  ## transform lambda model to angstrom if necessary
 lum=trasmpos(lum)
 # shift lambda to redshift
 lamz=lamm*(1+redshift)
 # shift model to redshift!!
 fmod=lumflux.l2fergc2sA(lum,distlum)

 #---------------------------------------------------------
 # get trasmission files
 # (_, _, filenames) = walk(mypath).next()                             # get files in path using walk
 # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))] # using listdir
 (dirpath, dirnames, filenames) = walk(mypath).next() 
 
 # get trasm files only
 trasmfiles=[]
 for f in filenames:
   if fnmatch.fnmatch(f, '*.dat'):
      trasmfiles.append(f)
 
 # cycle over transmissions and give photometry
 print '--CYCLE over transmissions and give photometry--'
 for tr in trasmfiles: 
	trasm=join(dirpath,tr)
        print trasm
	#print '------------------ READ FILE -----------------'
	tar=loadtxt(trasm)
        tar=tar[tar[:,0].argsort()]
	lamt=tar[:,0] ## be sure that lambda unit is the same
	flut=tar[:,1]              

	# integrate over trasmission
	integ=ift.main(lamz,fmod,lamt,flut) 
	#leff=integ[0]
	#bpass=integ[1]
	#flux=integ[2]
	#
	#print flux
	

 print '------------------ save data -----------------'
 ln=len(lamz)
 n=int(ln)
 j=0
 testfile='test.txt'
 out=open(testfile,'w')
 #lb=[0*x for x in range (0,int(ln))]
 #mb=[0*x for x in range (0,int(ln))]

 #while j<=n-1:
 #        out.write('%4.4f\t%2.7e\n' %(lamz[j],flux[j]))
 #        #print lamm[j],lummod[j],j
 #        j=j+1
 #
 out.close


#
if __name__ == "__main__":
    main()


