#!/usr/bin/env python


'''
transforms fluxes to luminosities and viceversa
USAGE: lumflux.py spetra_file redshift distance
'''

__Version__ = "0.1"
__Author__ = "Andrea Rossi"
__Usage__ = "USAGE: lumflux.py spetra_file redshift distance"

import sys
def usage():
    print __Usage__


##---------------------------------------------------------
#Import packages
import os
#from scipy.interpolate import splprep, splev
from scipy.interpolate import interp1d
from scipy.constants import speed_of_light
from numpy import loadtxt, arange ,pi, log10, log, exp #, linspace, convolve

##---------------------------------------------------------
## constants
cc=speed_of_light
ckm=cc/1000 ## km/s
ccm=cc*100 ## cm/s
cca=cc*10**10 ##angstrom /s
zpab=8.926    ## zp for flux in Jy
##---------------------------------------------------------
## constants
def luma2lumh(ang,luma):
	lumh=luma*(ang**2)/cca 
	return lumh
 
def luma2fjy(ang,luma,mpc,z):
    lumh=luma*(ang**2)/cca
    fjy=10**23* lumh / ( 4 * pi * ( mpc * 3.08568 * 10**24 ) **2 ) * (1+z)
    return fjy
 
def fjy2mab(fjy):
     mab=-2.5 * ( log10(fjy)) + zpab 
     return mab
     
def l2fergc2sA(luma,mpc,z):
     fergc2sA=luma / ( 4 * pi * ( mpc * 3.08568 * 10**24 ) **2 ) / (1+z)
     return fergc2sA
     
def fergc2sA2fjy(fergc2sA,ang):
    fjy=10**23* fergc2sA *(ang**2)/cca
    return fjy
    
    
def lumh2fjy(lumh,mpc,z):
    fjy=10**23* lumh / ( 4 * pi * ( mpc * 3.08568 * 10**24 ) **2 ) * (1+z)
    return fjy
   
     
#------------reverse

def lumh2luma(ang,lumh):
	luma=lumh/(ang**2)*cca 
	return luma

def fjy2luma(ang,fjy,mpc,z):
     #lumh=fjy*10**(-23) * ( 4 * pi * ( mpc * 3.08568 * 10**24 ) **2 ) / (1+z)
     #ang_rest=ang/(1+z)
     #luma=lumh*cca/(ang_rest**2)
     luma= fjy* 10**(-23)*cca/(ang**2)  * ( 4 * pi * ( mpc * 3.08568 * 10**24 ) **2 ) * (1+z)
     return luma
     
def mab2fjy(mab):
     fjy=10**((mab-zpab)/(-2.5))
     return fjy

def fergc2sA2luma(fergc2sA,mpc,z):
     luma= fergc2sA * ( 4 * pi * ( mpc * 3.08568 * 10**24 ) **2 ) * (1+z)
     return luma

def fjy2fergc2sA(fjy,ang):
    fergc2sA =fjy* 10**(-23)*cca/(ang**2)
    return fergc2sA
     
     
def fjy2lumh(fjy,mpc,z):
     lumh= fjy* 10**(-23) * ( 4 * pi * ( mpc * 3.08568 * 10**24 ) **2 ) / (1+z)
     return lumh
   


#
#if __name__ == "__main__":
#    main()
