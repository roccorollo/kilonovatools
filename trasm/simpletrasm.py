#!/usr/bin/env python
'''
Computes total transmission and create a smaller output
USAGE: 250tr.py FILE WAVELENGTH [--output ]
'''

__version__ = "1.0"
__author__ = "Andrea Rossi "

    
##---------------------------------------------------------
#Import packages
import sys
import os
from scipy import  *
from numpy import loadtxt
#from scipy import numpy
from pylab import *
##import scipy.io.array_import
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--output',dest='output',help='Sets the output filename [output.dat]',default="output.dat")
(options, args) = parser.parse_args()
file = args

if not args:
    sys.exit("ERROR: Not enough arguments specified")

##---------------------------------------------------------
print '------------------ READ FILE -----------------'
##Read the data

filename = sys.argv[1]
wave = sys.argv[2]
fact = float(sys.argv[3])

if not os.path.isfile(filename):
      sys.exit("ERROR: Specified file not found: %s" % filename)

##lamb=[]
##trasb=[]
##with open(filename,'r') as tcb:
## for _ in xrange(6):
##    next(tcb)
## for line in tcb:
##    i1, i2, = map(float, line.split())
##    lamb.append(i1)
##    trasb.append(i2)

tcb=loadtxt(filename)
ghz=tcb[:,0] ## lambda is in microns
trasb=tcb[:,1] 


ccc=299792458 ## m/s
ckm=299792.458 ## km/s

#print lamb
##loop
ln=len(ghz)
n=int(ln/3)

print 'FILE LENGTH ',ln
print 'SHORT VERSION will have ',n,'rows'

#print lb, len(lb),n

print '------------------ CREATE MICRON VERSION -----------------'

lb=[0*x for x in range (0,int(ln))]
tb=[0*x for x in range (0,int(ln))]

fileout=(wave+'.dat')
nn=int(ln)
#outf=open(fileout,'w')
smic=[]
j=nn-1
while j>=0:
	
	lb[j]=ghz[j]/fact 
	#lb[j]=ghz[j] 
	tb[j]=trasb[j]
	#outf.write('%4.6f\t%2.8f\n' %(lb[j],tb[j]))
	#print lb[j],tb[j],j
	smic.append((lb[j],tb[j]))
	j=j-1
	
#outf.close

micro=sorted(smic,key=lambda trasm: trasm[0])
#
#print '------------------ LOAD MICRON VERSION -----------------'
#
lamb=lb ## lambda is in microns
trasb=tb
#
#print '------------------ CREATE shorter version -----------------'
#
#lb=[0*x for x in range (0,int(ln/3+3))]
#tb=[0*x for x in range (0,int(ln/3+3))]
#
#fileshort=(wave+'short.dat')
#j= n-1
#outs=open(fileshort,'w')
#
#while j>=0:
#
#	lb[j]=(lamb[j*3]+lamb[j*3+1]+lamb[j*3+2])/3 #(lamb[j*10]+lamb[j*10+2]+lamb[j*10+4]+lamb[j*10+6]+lamb[j*10+8])/5
#	tb[j]=(trasb[j*3]  +trasb[j*3+1]  +trasb[j*3+2])/3 #(trasb[j*10]  +trasb[j*10+2]  +trasb[j*10+4]  +trasb[j*10+6]  +trasb[j*10+8])/(5*smax)
#	outs.write('%4.4f\t%2.7f\n' %(lb[j],tb[j]))
#	#print lb[j],tb[j],j
#	j=j-1
#
##outf.write(lb,tb)
#outs.close


##---------------------------------------------------------
##simpsons_rule=integration

def simpsons_rule(f,a,b):
    c = (a+b) / 2.0
    h3 = abs(b-a) / 6.0
    return h3*(f(a) + 4.0*f(c) + f(b))

##---------------------------------------------------------

def recursive_asr(f,a,b,eps,sum):
    "Recursive implementation of adaptive Simpson's rule."
    c = (a+b) / 2.0
    left = simpsons_rule(f,a,c)
    right = simpsons_rule(f,c,b)
    if abs(left + right - sum) <= 15*eps:
        return left + right + (left + right - sum)/15
    return recursive_asr(f,a,c,eps/2,left) + recursive_asr(f,c,b,eps/2,right)

def ads_rule(f,a,b,eps):
    "Calculate integral of f from a to b with max error of eps."
    return recursive_asr(f,a,b,eps,simpsons_rule(f,a,b))
##---------------------------------------------------------

def simp1(f,a,b,N):
    h=abs(b-a)/float(N)##stepsize
    x = arange(a,b+h,h)##points of the step
    Integral = 0
    term2 = 0
    term3 = 0
    for i in xrange(1,N-1):
        term2 = term2 + f(x[i])
    for i in xrange(1,N):
        term3 = term3 + f((x[i]+x[i-1])/2)
    Integral = h/3 * (1/2*(f(x[0])+f(x[N]))+2*term3+term2)
    return Integral;

##---------------------------------------------------------

print '------------------ COMPUTE INTEGRAL -----------------'
print '------------------ WAVELENGTH',wave,'----------------'

##loop
smax=max(trasb)

##function for the integration

def trasm(ll):
    return ss/smax+ll*0
    
def delta(ll):
    return (ss/smax)*((ll-lef)**2)
    
def lambef(ll):
    return ll*ss/smax
    
    

##First Surface
i=1
sint=0
eps=0.001
while i<ln:
    ss=(trasb[i]+trasb[i-1])/2
    sint=sint+ads_rule(trasm,lamb[i-1],lamb[i],eps)
    #sint=sint+simpsons_rule(trasm,lamb[i-1],lamb[i])
    i=i+1
print 'Surface             ',sint

#---------
i=1
lint=0

while i<ln:
    ss=(trasb[i]+trasb[i-1])/2
    lint=lint+simpsons_rule(lambef,lamb[i-1],lamb[i])
    i=i+1

lef=lint/sint

print 'effective wavelength',lef,'original wavelength unit'

#---------
i=1
dint=0
while i<ln:
    ss=(trasb[i]+trasb[i-1])/2
    dint=dint+simpsons_rule(delta,lamb[i-1],lamb[i])
    i=i+1

deltal=2*(dint/sint)**(0.5)

print 'Bandpass            ',deltal,'original wavelength unit'


print ' '
print 'END'
