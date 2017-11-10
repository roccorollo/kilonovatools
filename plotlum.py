import matplotlib.pyplot as plt
import grbflux2lum
import numpy as np

GRB,z,filt,nueffgrb,flux,fluxerr,dhour=grbflux2lum.read_db()
lum,lumerr,dhour_rf,nueffgrbz=grbflux2lum.lumlcgrb(flux,fluxerr,z,dhour,nueffgrb)
grbflux2lum.printoutput(GRB,filt,nueffgrbz,dhour_rf,lum,lumerr)

id=raw_input(' Which GRB do you want to plot? [e.g. 130603B]:') or '130603B'
fil=raw_input(' in which filter? [e.g. r*]:') or 'r*'

plt.loglog(dhour_rf[np.where((GRB == id) & (filt == fil))],lum[np.where((GRB == id) & (filt == fil))],'*')
plt.xlabel('rest frame time [hrs]')
plt.ylabel('Lnu [erg/s Hz]')
plt.title('GRB'+id+' observed in the filter '+fil)
plt.show()
