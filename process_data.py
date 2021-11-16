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

def get_kic_metadata(kic_id,tcp_type):
    kic_metadata = []
    tce_data =pd.read_csv('tce_data_new.csv',comment="#")
    kic_id_metadata = tce_data[tce_data.kepid==int(kic_id)]
    kic_id_metadata = kic_id_metadata[tce_data.av_training_set==tcp_type]
    for i in range(0,len(kic_id_metadata)):
        kic_metadata.append([kic_id_metadata.iloc[i].tce_time0bk,kic_id_metadata.iloc[i].tce_period])
    return kic_metadata

def find_nearest(array, value):
    array = np.asarray(array)
    array[np.isnan(array)] = 999999
    idx = (np.abs(array - value)).argmin()
    return idx

def get_all_flux_kic(kic_id):
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

    return time,lightcurves
    

def get_local_lightcurves(kic_id):
   
    time,lightcurves = get_all_flux_kic(kic_id) 
    
    kic_metadata = get_kic_metadata(kic_id,"PC")
    print(kic_metadata)
    
    star_time_array = np.array(time)
    
    # for i in range(0,len(kic_metadata)):
    kic_first_tce_day = kic_metadata[0][0]
    kic_orbital_period = kic_metadata[0][1]

    orbits_skip = round((600-kic_first_tce_day)/kic_orbital_period)
    print(orbits_skip)
    nearest_day_indx = find_nearest(star_time_array, kic_first_tce_day + (kic_orbital_period *  orbits_skip));
    star_time_transit = time[nearest_day_indx-100: nearest_day_indx + 100]
    star_flux_transit = lightcurves[nearest_day_indx-100: nearest_day_indx + 100]

    plt.subplot(1,2,1)
    plt.plot(star_time_transit, star_flux_transit, ".", markersize="3", color="orange")
        # return fig
        

def get_global_lightcurves(kic_id):
   
    time,lightcurves = get_all_flux_kic(kic_id) 
    
    kic_metadata = get_kic_metadata(kic_id,"PC")
    
    star_time_array = np.array(time)
    
    # for i in range(0,len(kic_metadata)):
    kic_first_tce_day = kic_metadata[0][0]
    kic_orbital_period = kic_metadata[0][1]
    orbits_skip = round((600-kic_first_tce_day)/kic_orbital_period)
    nearest_day_indx = find_nearest(star_time_array, kic_first_tce_day + (kic_orbital_period * orbits_skip));
    star_time_transit = time[nearest_day_indx-1000: nearest_day_indx + 1000]
    star_flux_transit = lightcurves[nearest_day_indx-1000: nearest_day_indx + 1000]
    plt.subplot(1,2,2)
    plt.plot(star_time_transit, star_flux_transit, ".", markersize="3", color="orange")
        # return fig


