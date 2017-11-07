import os
import numpy as np
import pandas as pd

#password: BOgw_2017

def load_data():
    return os.system("ssh gwbologna@gravitown.oaroma.inaf.it \"mysql MisceCats -e \'select GRB,z,dhour,Flux,Fluxerr,filter from sgrb;\' \" > table.txt")


def read_data():
    return pd.read_csv('table.txt',sep='\t', header='infer',skiprows=None,skip_blank_lines=True)

load_data()
data=read_data()
data_array=data.values

GRB=data_array[:,0]
z=data_array[:,1]
dhour=data_array[:,2]
filt=data_array[:,3]

data_grb=data_array[np.where(data_array[:,0]=='130603B'),:]
