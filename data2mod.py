
'''
Take spectra template and trasmission, and computes observed mag at given distance
'''

__Version__ = "0.1"
__Author__ = "Andrea Rossi "
__Usage__ = "dosimphot.py data modelname redshift"

import sys
def usage():
    print __Usage__

def main():
 	
 ##---------------------------------------------------------
 #Import packages
 import os
 import platform
 import subprocess

 #from scipy.interpolate import splprep, splev
 #from scipy.interpolate import interp1d
 from scipy.constants import speed_of_light
 from numpy import loadtxt, arange #, pi, log, linspace, convolve
 ##import scipy.io.array_import
 ##from optparse import OptionParser
 
 # import other prog
 import lumflux
 import andNEDredshift
 
 #  input data 
 datafile = sys.argv[1]
 #  model name
 modelfile = sys.argv[2]    
 # '------------------ get redshift -----------------'
 redshift = float(sys.argv[3])
 
 #############  Constants
 cc=speed_of_light
 ckm=cc/1000 ## km/s
 ccm=cc*100 ## cm/s
 cca=cc*10**10 ##angstrom /s
 zpab=8.926    ## zp for flux in Jy
  
 def angtomic(lamm,sameunit):
      if sameunit in ("y"):
         lamm=lamm/1.
      else :
         lamm=lamm/1e4        
      return lamm
     
 def trasmpos(flum):
    flum=(flum**2)**0.5
    return flum
 
  
 print '------------------ READ FILE -----------------'
 ##Read the data
 

 if not os.path.isfile(datafile):
       sys.exit("ERROR: Specified file not found: %s" % datafile)
       
 mar=loadtxt(datafile)
 lamz=mar[:,0]
 flum=mar[:,1] 
 flum=trasmpos(flum)

# get redshift and give luminosity distance 
# redshift=0.01
 distlum=andNEDredshift.distlum(redshift)
 print 'luminosity distance is: %.2f ' % distlum + 'Mpc'
 #print 'The luminosity distance D_L is ' + '%1.2f' %  distlum
   
 
# from data to luminosity in erg/s/A
 lummod=lumflux.fergc2sA2luma(flum,distlum)*(1+redshift)
 lamm=lamz/(1+redshift) ## be sure that lambda unit is the same

 #print 'lum distance is ' + '%1.3f' %  distlum
 #flum
 
 
 print '------------------ save model -----------------'
 ln=len(lamm)
 n=int(ln)
 j=0
 out=open(modelfile,'w')
 #lb=[0*x for x in range (0,int(ln))]
 #mb=[0*x for x in range (0,int(ln))]

 
 while j<=n-1:
         out.write('%4.4f\t%2.7e\n' %(lamm[j],lummod[j]))
         #print lamm[j],lummod[j],j
         j=j+1
 
 out.close


if __name__ == "__main__":
    main()
    
    
    


  



 