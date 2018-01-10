#!/usr/bin/env python

'''
make seds fit and spline
'''

__Version__ = "0.1"
__Author__ = "Andrea Rossi "

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
 from scipy.constants import speed_of_light
 from scipy.optimize import curve_fit
 from scipy.interpolate import interp1d,  splrep, splev
 import numpy as np
 from numpy import loadtxt, argsort, exp, pi, log , linspace, concatenate, array #, convolve
 import matplotlib.pyplot as plt                                                               
 
 
 # some useful functions
 def trasmpos(flum):
    flum=(flum**2)**0.5
    return flum

 #-------  Constants
 #cc=speed_of_light
 #zpab=8.926    ## zp for flux in Jy
 t0=57982.528  ## Time= MJD  (T0 for GW trigger is MJD=57982.528)
 
 # get input
 
 if len(sys.argv) < 2:
	 sys.exit("please give one argument")
	 
 datafile = sys.argv[1]
 if os.path.isfile(datafile):
	(dirdata, dataname)=os.path.split(datafile)
 else:
	sys.exit("please give valid datafile name") 
 print dataname
 
 
 print '------------------ READ FILE -----------------'
 ##Read the data
 
 if not os.path.isfile(datafile):
       sys.exit("ERROR: Specified file not found: %s" % datafile)
       
 mar=loadtxt(datafile)
 lamm=mar[:,0]
 flum=mar[:,1] 
 flum=trasmpos(flum) 
 
 #------------- extract PARAMATER for datee
 head=[]
 with open(datafile, 'r') as sf: 
  for line in sf: 
	if line.startswith('#'):       
		head.append(line)         

 print head
 
 plt.plot(lamm, flum, 'o', label='data')
 #mint=min(lam)
 mint=2000.0   # !!! USER FIXED lamda 2000 A !!!
 maxt=max(lamm)
 maxm=max(flum*1.5)
 minm=min(flum/1.5)
 
 # grid
 x = linspace(mint, maxt, num=1000, endpoint=True)	

 #---------cubic spline
 
 #if len(lamm)>5 :
#	k=5
 #elif len(lamm)>2 :
#	k=3
 #else:
#	k=1
#	
 #s=1
 #k=1
 #spl  = splrep(lamm, flum, k=k, s=s)
 #print 'splrep done k=%.0f' %k+'; s=%.0f' %s
 #yspl = splev(x,spl ,der=0)
 #print 'splev done'
 #plt.plot(x, yspl , 'r-', label='cubic k=%.0f' %k +'; s=%.0f' %s +' spline')
 
 ##--- polynomial
 #k=9
 #z = np.polyfit(lamm, flum, k)
 #fpoly = np.poly1d(z)
 #ypoly=fpoly(x)
 #
 #plt.plot(x, ypoly , 'b-', label='poly fit k=%.0f' %k)
 
 # ---- Univariate spline
 from scipy.interpolate import UnivariateSpline
 
 if len(lamm)>5 :
	k=5
 elif len(lamm)>2 :
	k=3
 else:
	k=1
 
 s=100
 spl = UnivariateSpline(lamm, flum, k=k, s=s)
 print 'spl done'
 spl.set_smoothing_factor(0.5)
 yspl=spl(x) 
 
 plt.plot(x, yspl , 'g-', label='univariate spline')
 
 # bezier function
 # installed bezier via pip https://pypi.python.org/pypi/bezier
 import bezier
 bez = bezier.Curve(mar, degree=2)
 pbez = bez.plot(num_pts=256)
 #plt.plot(bez , 'g-', label='bezier')
 
 
 
 print '------------------ save model -----------------'
 ln=len(x)
 n=int(ln)
 j=0
 os.system("if [ -d  supermod ]; then sleep 0.1; else mkdir supermod; fi ")
 outfile='supermod/super'+dataname
 out=open(outfile,'w')
 
 for i in head:
	out.write('%s' %i) 
 #out.write('%s\n' %header) 
 
 while j<=n-1:
         out.write('%4.4f\t%2.7e\n' %(x[j],yspl[j]))
         #print lamm[j],lummod[j],j
         j=j+1
 
 out.close
 
 

 #--------- show plot
 #plt.figure()
 plt.ylim(minm,maxm)
 #plt.xlim(1800,2100)
 plt.xlabel('lambda')
 plt.ylabel('L[erg/s/A]')
 plt.legend()
 opl=outfile+'.png'
 plt.savefig(opl,bbox_inches='tight')
 plt.show()
 
if __name__ == "__main__":
   usage()
   main()


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 