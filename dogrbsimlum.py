#!/usr/bin/env python

'''
Take spectra template and trasmission, and computes luminosity at shifted trasmission in restframe
Usage "dogrbsimlum.py model path_trasmission angstrom_or_mic redshift"
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

def main( modelfile,mytrasm, sameunit, redshift, filters):
 	
 ##---------------------------------------------------------
 #Import packages
 import os
 from os import walk, sys, path
 from os.path import join
 import fnmatch
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
 
 #filters = str(filters)     # filter
 #print filters
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
 #if os.path.isfile(modelfile):
 #	(dirmod, modname)=os.path.split(modelfile)
 #else:	 
 #      sys.exit("ERROR: Specified file not found: %s" % modelfile)
 		
 if os.path.isfile(mytrasm):
    (dirpath, file) = os.path.split(mytrasm)
    trasmnames=[file]
 elif os.path.isdir(mytrasm):
	(dirpath, dirnames, trasmnames) = walk(mytrasm).next()
 else:
      sys.exit("ERROR: Specified file/directory not found: %s" % mytrasm)

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
	if 'PHASE' in  line:	
		phasemod=line.split()[3]  # phase date from specfile 	   
	if 'MJD' in  line:	 
		mjdmod=line.split()[4]  # mjd observed! date from specfile 
	if 'UT' in  line:
		utmod=line.split()[4]  # ut observed! date from specfile 
      
 # initialize output data
 #testfile='test'         #modname+'z'+str(redshift)+'_phot.dat'
 #out=open(testfile,'w')
 #out.write('%s\n' %header) 
 
 #---------------------------------------------------------
 # get trasmission files
 
 #get only names in a list: get only filternames which file extension is .dat!!!
 archivedfilternames=[]
 extension='.dat'
 for f in trasmnames:
	if fnmatch.fnmatch(f,'*'+extension):
		archivedfilternames.append(os.path.splitext(f)[0])
	 
 #print "archived filter names", archivedfilternames
 
 # compare two lists and get only matching filters
 usedfilters=[]
 for f in filters:
	 #print f
	 if f in archivedfilternames:
		 print 'filter exists: %s' % f
		 usedfilters.append(f)                                   
	 else:
		 sys.exit("ERROR: Specified filter not found: %s" % f)
  
 # cycle over transmissions and give photometry
 print '--CYCLE over filters used by GRB and give photometry--'
 
 # take element for sort
 #def takeelem(elem):
 #	return lambda x: elem 
	
 
 photarr=[]
 nd=int(-99)                    # in case is not defined
 for tr in usedfilters: 
     trasm=join(dirpath,tr+extension)
     #print '------------------ READ FILE -----------------'
     tar=loadtxt(trasm)
     tar=tar[tar[:,0].argsort()]    # ascending order
     tar=tar[tar[:,1]>1e-2]         # only lambda for >1% transmission
     lamt=tar[:,0] ## be sure that lambda unit is the same
     lamt=angtomic(lamt,sameunit)  # in angstrom !!!
     # shift transm to redshift
     lamt=lamt/(1+redshift)
     flut=tar[:,1]              
     # check if shifted trnasmisison is within data
     if max(lamt) <= max(lamm) and min(lamt) >= min(lamm) :
        print '-- FILTER %s' % trasm 
        # integrate over trasmission
        phot=ift.main(lamm,lum,lamt,flut)
        leff=phot[0]   # ANGSTROM  !!!  HAI TRASFORMATO LAMT IN ANGSTROM SOPRA
	#aleff=angtomic(leff,sameunit)
	bpass=phot[1]
	luma=phot[2]   # l in erg/s/A
	lumh=lumflux.luma2lumh(leff,luma)  # l in erg/s/Hz  lumh=luma*(ang**2)/cca
        photarr.append((leff,lumh,tr,mjdmod,phasemod))
	print 'FILTER PROPERTIES AND LUMINOSITY'
	print '%1.2f' %  leff + ' effective wavelength in model spectral unit'
        print '%1.2e' %  lumh + ' Lum in erg/s/Hz'
        #out.write('%4.4f\t%2.7e\t%s\t%s\t%s\n' %(leff,lumh,tr,mjdmod,phasemod))
     #if max(lamt) >= min(lamm) and min(lamm) >= min(lamt) :
	## PUT transmission leff here. need to be computed outside from ift.main 
	#filter=ift.trasm(lamt,flut)
     #leff=filter[0]   # ANGSTROM  !!!  HAI TRASFORMATO LAMT IN ANGSTROM SOPRA    
	#bpass=filter[1]
	#print "TBD"	
     else:
	print 'warning: %.2f' % max(lamt) +'> %.2f' % max(lamm) +' or %.2f' % min(lamm) +'< %.2f' % min(lamm)     
        print '--' + trasm+' outside filter range'
	photarr.append((nd,nd,tr,mjdmod,phasemod))
        #out.write('%2.0f\t%2.0f\t%s\t%s\t%s\n' %(-99,-99,tr,mjdmod,phasemod))
	
 #out.close
 
 #print photarr	
 #photarr=sorted(photarr, key=takeelem(4)) 
 return photarr	 
 
 
if __name__ == "__main__":
   #usage()
   main()


