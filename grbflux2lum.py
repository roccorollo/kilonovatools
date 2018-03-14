"""

    Author: G. Stratta

    Purpose: load data of short GRB afterglow from mysql data base on gravitwon
    and compute luminosity

"""
print 'Commands:'
print ''
print 'run plotlum.py'
print 'GRB,z,filt,nueffgrb,flux,fluxerr,dhour=grbflux2lum.read_db()'
print '   password: WG_p@ss17'

print 'lum,lumerr,dhour_rf,nueffgrbz=grbflux2lum.lumlcgrb(flux,fluxerr,z,dhour,nueffgrb)'
print 'grbflux2lum.printoutput(GRB,filt,nueffgrbz,dhour_rf,lum,lumerr)'


import os
import numpy as np
import pandas as pd
import andNEDredshift

# path where there are the Instrumental Effective Frequency table
path1='/Users/giulia/Documents/DRAFT/GRAWITA/GW170817/KN_AFTERGLOW/DATA/AG_SGRBs/'
#path1='/home/rossi/work/kilonova/tools/aux/'

def read_db():

#   read data from sgrb DB on gravitown saved on table.txt created with load_data()
#   (If table already exists, than it can be commented)
#    os.system("ssh gwbologna@gravitown.oaroma.inaf.it \"mysql MisceCats -e \'select GRB,z,dhour,Flux,Fluxerr,filter from sgrb;\' \" > tablegrb.txt")
    data=pd.read_csv('table.txt',sep='\t', header='infer',skiprows=None,skip_blank_lines=True)
    data_array=data.values
    GRB=data_array[:,0]
    z=data_array[:,1]
    dhour=data_array[:,2]
    flux=data_array[:,3]*1.e-29
    fluxerr=data_array[:,4]*1.e-29
    filt=data_array[:,5]

# Read filter's table and associated frequencies
    datafr=pd.read_csv(path1+'FrequenzeEfficaciStrumenti.txt',sep='\t', header='infer',skiprows=None,skip_blank_lines=True)
    datafr_array=datafr.values
    filt_from_tab=datafr_array[:,2]
    nueff=datafr_array[:,3]

# Associate a frequency to each GRB filter
    nueffgrblist=[]
    for i in range(0,len(GRB)):
        k=0
        for j in range(0,len(filt_from_tab)):
            if filt[i] != filt_from_tab[j]:
                k=k+1
            else:
                nueffgrblist.append(nueff[k])
    #            print GRB[i],filt[i],filt_from_tab[j],nueff[k]
                break

# clean the list from last 3 elements "",00" and put it into a vector
    nueffgrblistnew=[]
    for i in nueffgrblist:
        nueffgrblistnew.append(float(i.rstrip(",00")))
    nueffgrb=np.asarray(nueffgrblistnew)

    return GRB,z,filt,nueffgrb,flux,fluxerr,dhour

def lumlcgrb(flux,fluxerr,z,dhour,nueffgrb):
#    """
#    Compute luminosity and rest frame time
#    """
    DLlistMpc=[]
    for line in z:
        DLlistMpc.append(andNEDredshift.distlum(line))
    DL=np.asarray(DLlistMpc)*3.08568*1.e24
    lum=flux*(1/(1+z))*4*np.pi*DL**2
    lumerr=fluxerr*(1/(1+z))*4*np.pi*DL**2
    dhour_rf=dhour/(1+z)
    nueffgrbz=nueffgrb*(1+z)
    return lum,lumerr,dhour_rf,nueffgrbz

def printoutput(GRB,filt,nueffgrbz,dhour_rf,lum,lumerr,flux,fluxerr):
    print'GRB,filt,nueffgrbz,dhour_rf,lum,lumerr,flux,fluxerr'
    for i in range(0,len(GRB)):
        print GRB[i],filt[i],nueffgrbz[i],dhour_rf[i],lum[i],lumerr[i],flux[i],fluxerr[i]
    return


#data_grb=data_array[np.where(data_array[:,0]=='130603B'),:]
