#!/usr/bin/env python

'''
Take spectra template and trasmission, and computes observed mag at given distance
Usage "dosimphot.py model path_trasmission y_for_angstrom_else_mic redshift"
'''

__Version__ = "0.1"
__Author__ = "Andrea Rossi "
__Usage__ = "dosimphot.py spectra path_trasmission angstrom_else_mic"
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
 
 #############  Constants
 ##cc=speed_of_light
 ##ckm=cc/1000 ## km/s
 ##ccm=cc*100 ## cm/s
 ##cca=cc*10**10 ##angstrom /s
 ##zpab=8.926    ## zp for flux in Jy
 
 ############ get input
 
 specfile = sys.argv[1]
 mypath    = sys.argv[2]
 sameunit  = sys.argv[3]
 sameunit  = str(sameunit)
 
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
 if os.path.isfile(specfile):
	(dirspec, specname)=os.path.split(specfile)
 else:	 
       sys.exit("ERROR: Specified file not found: %s" % specfile)
       
 # (_, _, filenames) = walk(mypath).next()                             # get files in path using walk
 # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))] # using listdir
  
 		
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
  
 #--------------------- Read model file
 mar=loadtxt(specfile)
 mar=mar[mar[:,0].argsort()]   # ascending order
 lamm=mar[:,0] ## be sure that lambda unit is the same
 fmod=mar[:,1] 
 fmod=trasmpos(fmod)

 #---------------------------------------------------------
 
 # initialize output data
 testfile=specname+'_phot.dat'
 out=open(testfile,'w')
 header='#lambda[A]      f[Jy]      mag[AB]     name'
 out.write('%s\n' %header) 
 
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
     tar=tar[tar[:,1]>1e-2]         # only lambda for >1% transmisison
     lamt=tar[:,0] ## be sure that lambda unit is the same
     lamt=angtomic(lamt,sameunit)
     if max(lamt) < max(lamm) and min(lamt) > min(lamm) :
        print trasm
        flut=tar[:,1]              

        # integrate over trasmission
        phot=ift.main(lamm,fmod,lamt,flut)
        leff=phot[0]   # micron
	#aleff=angtomic(leff,sameunit)
	bpass=phot[1]
	flux=phot[2]   # fergc2sA
        fjy=lumflux.fergc2sA2fjy(flux,leff)
        magab=lumflux.fjy2mab(fjy)
        photarr.append((leff,fjy,magab,tr))
	print '%1.2f' %  leff + ' effective wavelength in spectral unit'
        #print '%1.2e' %  flux + ' flux in erg/cm^2/s/Ang'
        print '%2.1f' %  magab + ' mag in AB'
        out.write('%4.4f\t%2.7e\t%2.2f\t%s\n' %(leff,fjy,magab,tr))
     else:
        print '--' + trasm+' outside filter range'
	photarr.append((nd,nd,nd,tr))
        out.write('%2.0f\t%2.0f\t%2.0f\t%s\n' %(-99,-99,-99,tr))
 
 # close output file	 
 out.close
 
 print photarr	 # check result

if __name__ == "__main__":
   usage()
   main()


