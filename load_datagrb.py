import os
import numpy as np
import pandas as pd

#password: WG_p@ss17

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
flux=data_array[:,3]
fluxerr=data_array[:,4]
filter=data_array[:,5]

data_grb=data_array[np.where(data_array[:,0]=='130603B'),:]



150423AS
150424AS
160410AS
160624AS
160821BS
170428AS


