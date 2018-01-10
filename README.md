

# AIM
Contains several tools useful for conversions from spectra to photometry, luminosity to fluxes and viceversa.
The goal is to obtain luminosity lightcurves from a kilonova spectral model using the filters used to observe a given GRB.
Cosmological redshift modify the filters, so that what we observe is not in the rest-frame filter.
running 'python doalllc.py', it reads the list of GRBs in file 'table.txt', and for each GRB creates a file in
folder 'lc'. This contains the lightcurve of the model kilonova all the virtual (i.e. redshifted) filters used to observe that GRB.
Example of file in folder 'lc': 

#lambda[A]  L[erg/s/Hz]         filter       MJD

-99.00  -9.9000000e+01  micGeneric_Bessell.B    57983.97

6580.61 5.2850007e+26   micSLOAN_SDSS.z 57983.97

lines with -99.00 are filters that are not covered by the KN model (usually due to redshift effect)
and should not be considered

# kilonovatools
tools useful for conversions from spectra to photometry, luminosity to fluxes and viceversa

### andNEDredshift.py
adjusted from NED: used to compute distANCE LUMINOSITIES IN Mpc

### lumflux.pyd
several functions to ttransform between luminosity, flux desities and magnitudes

### ift.py  
used to integrate filter over model

### data2mod.py  
used to trasfrom data to model (e.g. an observed spectra in flux density to luminosity )

### dosimphot.py  
used to simulate photmetry from spectral models

### dospectophot.py
tool to convolve spectral data with filters in obs frame

### folder  trasm
transmission of sevral filters from hyperz ad svo (microns)

