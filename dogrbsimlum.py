#!/usr/bin/env python

'''
Take spectra template and trasmission, and computes luminosity at shifted trasmission in restframe
Usage "dogrbsimlum.py model path_trasmission y_for_angstrom_else_mic redshift"
'''

__Version__ = "0.1"
__Author__ = "Andrea Rossi "
__Usage__ = "dogrbsimlum.py model path_trasmission angstrom_else_mic redshift"
__Notes__ = "if transmission is out of interval is not used"

import sys
def usage():
    print __doc__
    #print __Usage__
    #print __Notes__

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
 from scipy.constants import speed_of_light
 from numpy import loadtxt, arange #, pi, log, linspace, convolve
 
 # import other prog
 import ift
 import lumflux
 import andNEDredshift
  
 #############  Constants
 cc=speed_of_light
 ckm=cc/1000 ## km/s
 ccm=cc*100 ## cm/s
 cca=cc*10**10 ##angstrom /s
 ##zpab=8.926    ## zp for flux in Jy
 
 # get input
 
 modelfile = sys.argv[1]
 mypath    = sys.argv[2]
 sameunit  = sys.argv[3]
 redshift  = sys.argv[4]
 sameunit  = str(sameunit)
 redshift  = float(redshift)
 
 # define special functions    
 def angtomic(lamm,sameunit):
      if sameunit in ("angstrom"):
         lamm=lamm/1.
      elif sameunit in ("microns"):
         lamm=lamm*1e4
      else:
         sys.exit("Please specify ang or mic as unit for transmission file")
      return lamm                    
     
 def trasmpos(flum):
    flum=(flum**2)**0.5
    return flum        
 #check unit is correct
 checkunit=angtomic(1,sameunit)

 # handle paths
 if os.path.isfile(modelfile):
	(dirmod, modname)=os.path.split(modelfile)
 else:	 
       sys.exit("ERROR: Specified file not found: %s" % modelfile)
 		
 if os.path.isfile(mypath):
    (dirpath, file) = os.path.split(mypath)
    filenames=[file]    
 elif os.path.isdir(mypath):
	(dirpath, dirnames, filenames) = walk(mypath).next()
 else:
      sys.exit("ERROR: Specified file/directory not found: %s" % mypath)
   
 def full_path(filepath):
     if platform.system() == 'Windows':
         if filepath[1:3] == ':\\':
             return u'\\\\?\\' + os.path.normcase(filepath)
     return os.path.normcase(filepath)
 
 # compute distance lum
 distlum=andNEDredshift.distlum(redshift)
 
 #--------------------- Read model file
 mar=loadtxt(modelfile)
 mar=mar[mar[:,0].argsort()]   # ascending order
 lamm=mar[:,0] ## be sure that lambda unit is the same
 lum=mar[:,1] 
 #lamm=angtomic(lamm,sameunit)  ## transform lambda model to angstrom if necessary
 lum=trasmpos(lum)
  
 #------------- extract PARAMATER for date
 headsf=[]
 with open(modelfile, 'r') as sf:
  for line in sf:
    if line.startswith('#'):
      headsf.append(line)         
      
 mjd=headsf[1].split()[3]  # mjd date from specfile
  
 # initialize output data
 testfile=modname+'z'+str(redshift)+'_phot.dat'
 out=open(testfile,'w')
 header='#lambda[A]      f[Jy]      mag[AB]     name'
 out.write('%s\n' %header) 
 
 #---------------------------------------------------------
 # get trasmission files
 
 # cycle over transmissions and give photometry
 print '--CYCLE over transmissions and give photometry--'
 #for tr in trasmfiles: 
 photarr=[]
 nd=int(-99) 
 for tr in filenames: 
   # get trasm files only (dat extension only)
   if fnmatch.fnmatch(tr, '*.dat'):
     trasm=join(dirpath,tr)
     #print '------------------ READ FILE -----------------'
     tar=loadtxt(trasm)
     tar=tar[tar[:,0].argsort()]    # ascending order
     tar=tar[tar[:,1]>1e-2]         # only lambda for >1% transmission
     lamt=tar[:,0] ## be sure that lambda unit is the same
     lamt=angtomic(lamt,sameunit)
     # shit transm to redshift
     lamt=lamt/(1+redshift)
     # check if shifted trnasmisison is within data
     if max(lamt) < max(lamm) and min(lamm) > min(lamm) :
        print trasm
        flut=tar[:,1]              
        # integrate over trasmission
        phot=ift.main(lamm,fmod,lamt,flut)
        leff=phot[0]   # micron
	#aleff=angtomic(leff,sameunit)
	bpass=phot[1]
	luma=phot[2]   # l in erg/s/A
	lumh=luma*((leff*1e4)**2)/cca   # l in erg/s/Hz  lumh=luma*(ang**2)/cca
        photarr.append((leff,lumh,tr,mjd))
	print '%1.2f' %  leff + ' effective wavelength in model spectral unit'
        print '%1.2e' %  lumh + ' Lum in erg/s/Hz'
        out.write('%4.4f\t%2.7e\t%s\t%s\n' %(leff,lumh,tr,mjd))
     else:
        print '--' + trasm+' outside filter range'
	photarr.append((nd,nd,tr,mjd))
        out.write('%2.0f\t%2.0f\t%s\t%s\n' %(-99,-99,tr,mjd))
	
 out.close
 
 print photarr	 

#print '------------------ save data -----------------'
#testfile='test.txt'
#out=open(testfile,'w')
##lb=[0*x for x in range (0,int(ln))]
##mb=[0*x for x in range (0,int(ln))]
#
#j=0
#nf=len(filenames)
# while j<=nf-1:
#       #print j
#	out.write('%4.4f\t%2.7e\t%s\n' %(photarr[j][0],photarr[j][1],photarr[j][2]))
#	j=j+1
#
#out.close
#
#

if __name__ == "__main__":
   usage()
   main()


