#!/usr/bin/env python
  
"""
Cosmology calculator ala Ned Wright (www.astro.ucla.edu/~wright)

USE 
NEDredshift.py [-v] redshift [Ho Omega_m Omega_vac]
ouput values = age at z, distance in Mpc, kpc/arcsec, apparent to abs mag conversion

"""
from math import *
from scipy.constants import speed_of_light

def distlum(redshift):
  
# if no values, assume Benchmark Model, input is z from Planck collaboration 2016  (and Gompertz too)
  z=float(redshift)            # redshift
  H0 = 67.8                         # Hubble constant
  WM = 0.308                        # Omega(matter)
  WV = 1.0 - WM - 0.4165/(H0*H0)  # Omega(vacuum) or lambda

# initialize constants

  WR = 0.        # Omega(radiation)
  WK = 0.        # Omega curvaturve = 1-Omega(total)
  c =  speed_of_light/1000. # velocity of light in km/sec
  DTT = 0.5      # time from z to now in units of 1/H0
  DCMR = 0.0     # comoving radial distance in units of c/H0
  DA = 0.0       # angular size distance
  DL = 0.0       # luminosity distance
  a = 1.0        # 1/(1+z), the scale factor of the Universe
  az = 1.0/(1+1.0*z)   # 1/(1+z(object))

  h = H0/100.
  WR = 4.165E-5/(h*h)   # includes 3 massless neutrino species, T0 = 2.72528
  WK = 1-WM-WR-WV
  n=10000         # number of points in integrals

  print '------------------ COMPUTE DISTANCE -----------------'

  # do integral over a=1/(1+z) from az to 1 in n steps, midpoint rule
  for i in range(n):
    a = az+(1-az)*(i+0.5)/n
    adot = sqrt(WK+(WM/a)+(WR/(a*a))+(WV*a*a))
    DTT = DTT + 1./adot
    DCMR = DCMR + 1./(a*adot)

  DTT = (1.-az)*DTT/n
  DCMR = (1.-az)*DCMR/n

  # tangential comoving distance

  ratio = 1.00
  x = sqrt(abs(WK))*DCMR
  if x > 0.1:
    if WK > 0:
      ratio =  0.5*(exp(x)-exp(-x))/x 
    else:
      ratio = sin(x)/x
  else:
    y = x*x
    if WK < 0: y = -y
    ratio = 1. + y/6. + y*y/120.
  DCMT = ratio*DCMR
  DA = az*DCMT
  DL = DA/(az*az)
  DL_Mpc = (c/H0)*DL

# return distance
  return   DL_Mpc

# test
#redshift=0.01 
#DL_Mpc=distlum(redshift)

#print 'The luminosity distance D_L is ' + '%1.2f' %  DL_Mpc
   

 

