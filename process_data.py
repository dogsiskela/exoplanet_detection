from numpy.lib.arraysetops import unique
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import threading
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from os import walk

from data_constants import LIGHTCURVES_FOLDER,LOCAL_LIGHTCURVES_FOLDER


def find_nearest(array, value):
    array = np.asarray(array)
    array[np.isnan(array)] = 999999
    idx = (np.abs(array - value)).argmin()
    return idx

def get_local_lightcurves(kic_id):
    if not os.path.exists(LIGHTCURVES_FOLDER + '/' + str(kic_id)):
        return;
    
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['figure.facecolor'] = 'gray'

    time=[]
    lightcurves=[]

    for (dirpath, dirnames, filenames) in walk("./download_data/"+kic_id):
        for index,file in enumerate(filenames):
            lightcurve_file = fits.open("./download_data/"+kic_id + "/" +filenames[index])
            lightcurve_data = lightcurve_file["LIGHTCURVE"].data

            star_time = lightcurve_data["TIME"]
            star_flux = lightcurve_data["PDCSAP_FLUX"]
            star_flux -= np.nanmedian(np.array(star_flux))
            time.extend(star_time)
            lightcurves.extend(star_flux)

    star_time_array = np.array(time)
    nearest = find_nearest(star_time_array,134.45 + (8.88 * 10));
    star_time_transit = time[nearest-60: nearest + 60]
    star_flux_transit = lightcurves[nearest-60: nearest + 60]
    

    plt.plot(star_time_transit, star_flux_transit, ".", markersize="3", color="orange")
    plt.show()
