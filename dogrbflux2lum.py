"""

    Author: G. Stratta

    Purpose: load data of short GRB afterglow from mysql data base on gravitwon
    and compute luminosity.

    This program creates a number of functions that are executed in plot_grb_kn_mag.py

            password: WG_p@ss17'
"""

import os
import numpy as np
import pandas as pd
import andNEDredshift

# path where there are the Instrumental Effective Frequency table
#path1='./kilonovatools/aux/'
path1='./aux/'

def read_db():
#   read data from sgrb DB on gravitown saved on table.txt created with load_data()

#   (If table already exists, this line can be commented)
#    os.system("ssh gwbologna@gravitown.oaroma.inaf.it \"mysql MisceCats -e \'select GRB,z,dhour,Flux,Fluxerr,filter from sgrb;\' \" > tablegrb.txt")

    data=pd.read_csv('tablegrb.txt',sep='\t', header='infer',skiprows=None,skip_blank_lines=True)
    data_array=data.values
    filt_w=data_array[:,5]
    GRB_w=data_array[:,0]
    z_w=data_array[:,1]
    dhour_w=data_array[:,2]
    flux_w=data_array[:,3]
    fluxerr_w=data_array[:,4]
    #flux_w=data_array[:,3]*1
    #fluxerr_w=data_array[:,4]*1

    # Does not read GRB data in white filter
    white_str='uvwhite'
    GRB=GRB_w[np.where(filt_w != white_str)]
    filt_old=filt_w[np.where(filt_w != white_str)]
    z=z_w[np.where(filt_w != white_str)]
    dhour=dhour_w[np.where(filt_w != white_str)]
    flux=flux_w[np.where(filt_w != white_str)]
    fluxerr=fluxerr_w[np.where(filt_w != white_str)]

    filt=[]
    # Rename similar filters (e.g. Rc = R )
    for i in range(len(filt_old)):
        filt.append(filt_old[i])

    for i in range(len(filt)):
        if 'Rc' in filt[i]:
            filt[i] = filt[i].replace ('Rc','R')
        if 'F160W' in filt[i]:
            filt[i] = filt[i].replace ('F160W','H')
        if 'F125W' in filt[i]:
            filt[i] = filt[i].replace ('F125W','J')
        if 'F110W' in filt[i]:
            filt[i] = filt[i].replace ('F110W','J')
        if 'F606W' in filt[i]:
            filt[i] = filt[i].replace ('F606W','r*')
        if 'uvb' in filt[i]:
            filt[i] = filt[i].replace ('uvb','B')
        if 'uvv' in filt[i]:
            filt[i] = filt[i].replace ('uvv','V')
        #if 'uvu' in filt[i]:
        #    filt[i] = filt[i].replace ('uvu','U')
        if 'Zg' in filt[i]:
            filt[i] = filt[i].replace ('Zg','z*')
        if 'Ks' in filt[i]:
            filt[i] = filt[i].replace ('Ks','K')


# Read filter's table and associated frequencies
    datafr=pd.read_csv(path1+'FrequenzeEfficaciStrumenti.txt',sep='\t', header='infer',skiprows=None,skip_blank_lines=True)
    datafr_array=datafr.values
    filt_from_tab=datafr_array[:,2]
    nueff=datafr_array[:,3]

# Associate a frequency to each GRB filter
    nueffgrblist=[]
    for i in range(0,len(GRB)):
        k=0
        # Quando filt[i]=filt_from_tab[j] (dove i=k) allora scrive
        # alla riga i-esima di nueffgrblist il valore in Hz

        for j in range(0,len(filt_from_tab)):
            if filt[i] != filt_from_tab[j]:
                k=k+1
            else:
                nueffgrblist.append(nueff[k])
                #print GRB[i],filt[i],filt_from_tab[j],nueff[k]
                break



# clean the list from last 3 elements "",00" and put it into a vector
    nueffgrblistnew=[]
    for i in nueffgrblist:
        nueffgrblistnew.append(float(i.rstrip(",00")))
    nueffgrb=np.asarray(nueffgrblistnew)

    return GRB,z,filt,filt_old,nueffgrb,flux,fluxerr,dhour


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
    return lum,lumerr,dhour_rf,nueffgrbz,DL

def printoutput(GRB,filt,nueffgrbz,dhour_rf,lum,lumerr,flux,fluxerr,DL):
    print'GRB,filt,nueffgrbz,dhour_rf,lum,lumerr,flux,fluxerr,DL'
    for i in range(0,len(GRB)):
        print GRB[i],filt[i],nueffgrbz[i],dhour_rf[i],lum[i],lumerr[i],flux[i],fluxerr[i],DL[i]
    return


#data_grb=data_array[np.where(data_array[:,0]=='130603B'),:]
