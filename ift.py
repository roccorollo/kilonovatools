#!/usr/bin/env python


'''
Convolves input model in fluxes with a given filter transmission  
USAGE: ifultra.py MODEL_FILE TRANSMISSION_FILE [--output]
'''

__Version__ = "1.0"
__Author__ = "Andrea Rossi "
__Usage__ = "ifultra.py MODEL_FILE TRANSMISSION_FILE [--output]"

import sys
def usage():
    print __Usage__

def main(lamm,flum,lamt,flut):
 	
 ##---------------------------------------------------------
 #Import packages
 import os
 #from scipy.interpolate import splprep, splev
 from scipy.interpolate import interp1d
 from scipy.integrate import trapz as  integ
 from numpy import loadtxt, arange #,pi, log, linspace, convolve
 
 ##---------------------------------------------------------

 ## define lambda vector = the same as transmission lambda
 ln=len(lamt)
 #-----------------------------------------------------------
 ## interpolate transmisison to cover same lambda intervals
 ## interpolate model to cover same lambda intervals
 ## Create interpolating function 
 tti=interp1d(lamt,flut)
 mmi=interp1d(lamm,flum)
 
 moint=[]
 trint=[]
 for i in lamt:
 	moint.append(float(mmi(i))) 
 		
 ## length must be the same
 print 'length of interpolated model is ', len(moint)
 print 'length of transmission file is', len(lamt)
 
 print '------------------ COMPUTE INTEGRAL -----------------'
 
 # filter characteristics:
 ltr=flut*lamt
 tint = integ(flut,lamt) # surface
 lef = integ(ltr,lamt) /tint # effective wavelength
 delta=flut*((lamt-lef)**2)
 dint = 2*(integ(delta,lamt) /tint)**(0.5)  # whole bandpass
 
 # Compute flux averaged in the transmission :
 ymt=moint*flut       
 imt = integ(ymt,lamt)  
 #flav=1
 flav=imt/tint# averaged flux
 
 
 # result
 res=[0*x for x in range (0,3)]
 res[0]=lef
 res[1]=dint
 res[2]=flav
 
 return res

#if __name__ == "__main__":
#    main()
