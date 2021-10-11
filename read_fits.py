from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from os import walk


star_time = []
star_flux = []

f = []


plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['figure.facecolor'] = 'gray'
fig = plt.figure(figsize=(13, 6))

for (dirpath, dirnames, filenames) in walk("./data"):
    for file in filenames:
        lightcurve_file = fits.open("./data/"+file)
        lightcurve_data = lightcurve_file["LIGHTCURVE"].data

        star_time = lightcurve_data["TIME"]
        star_flux = lightcurve_data["PDCSAP_FLUX"]
        star_flux -= np.nanmedian(star_flux)

        plt.plot(star_time, star_flux, ".", markersize="3", color="orange")


plt.grid()
plt.show()
