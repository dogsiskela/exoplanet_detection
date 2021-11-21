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

from data.data_constants import LIGHTCURVES_FOLDER,LIGHTCURVES_FOLDER_TESS,TESS_CSV_DATA,KEPLER_CSV_DATA

def get_kic_metadata_tess(kic_id,tcp_type):
    kic_metadata = []
    tce_data =pd.read_csv(TESS_CSV_DATA,comment="#")
    kic_id_metadata = tce_data[tce_data.tid==int(kic_id)]
    print(kic_id_metadata)
    kic_id_metadata = kic_id_metadata[tce_data.tfopwg_disp==tcp_type]
    for i in range(0,len(kic_id_metadata)):
        kic_metadata.append([kic_id_metadata.iloc[i].pl_tranmid-2457000,kic_id_metadata.iloc[i].pl_orbper])
    return kic_metadata

def get_kic_metadata_kepler(kic_id,tcp_type):
    kic_metadata = []
    tce_data =pd.read_csv(KEPLER_CSV_DATA,comment="#")
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

def get_all_flux_kic(kic_id,mission_id):
    FOLDER = ""
    if mission_id == "kepler":
        FOLDER = LIGHTCURVES_FOLDER
    elif mission_id == "tess":
        FOLDER = LIGHTCURVES_FOLDER_TESS

    if not os.path.exists(FOLDER + '/' + str(kic_id)):
        return;
        
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['figure.facecolor'] = 'gray'

    time=[]
    lightcurves=[]

    for (dirpath, dirnames, filenames) in walk(FOLDER+"/"+kic_id):
        for index,file in enumerate(filenames):
            lightcurve_file = fits.open(FOLDER+"/"+kic_id + "/" +filenames[index])
            lightcurve_data = lightcurve_file["LIGHTCURVE"].data

            star_time = lightcurve_data["TIME"]
            star_flux = lightcurve_data["PDCSAP_FLUX"]
            star_flux -= np.nanmedian(np.array(star_flux))
            time.extend(star_time)
            lightcurves.extend(star_flux)

    return time,lightcurves
    

def get_local_lightcurves(kic_id,p_type="PC",mission_id="kepler"):
   
    time,lightcurves = get_all_flux_kic(kic_id,mission_id=mission_id) 

    kic_metadata = ""
    if mission_id == "kepler":
        kic_metadata = get_kic_metadata_kepler(kic_id,p_type)
    elif mission_id == "tess":
        kic_metadata = get_kic_metadata_tess(kic_id,p_type)

    star_time_array = np.array(time)
    
    print(kic_metadata)
    # for i in range(0,len(kic_metadata)):
    kic_first_tce_day = kic_metadata[0][0]
    kic_orbital_period = kic_metadata[0][1]

    # orbits_skip = round((600-kic_first_tce_day)/kic_orbital_period)
    # print(orbits_skip)
    orbits_skip=4
    nearest_day_indx = find_nearest(star_time_array, kic_first_tce_day + (kic_orbital_period *  orbits_skip));
    star_time_transit = time[nearest_day_indx-100: nearest_day_indx + 100]
    star_flux_transit = lightcurves[nearest_day_indx-100: nearest_day_indx + 100]

    plt.subplot(1,2,1)
    plt.plot(star_time_transit, star_flux_transit, ".", markersize="3", color="orange")
    plt.show()
        # return fig
        

def get_global_lightcurves(kic_id,p_type="PC",mission_id="kepler"):
   
    time,lightcurves = get_all_flux_kic(kic_id,mission_id=mission_id) 

    kic_metadata = ""
    if mission_id == "kepler":
        kic_metadata = get_kic_metadata_kepler(kic_id,p_type)
    elif mission_id == "tess":
        kic_metadata = get_kic_metadata_tess(kic_id,p_type)

    star_time_array = np.array(time)
    print(kic_metadata)    
    # for i in range(0,len(kic_metadata)):
    kic_first_tce_day = kic_metadata[0][0]
    kic_orbital_period = kic_metadata[0][1]

    # orbits_skip = round((600-kic_first_tce_day)/kic_orbital_period)
    # print(orbits_skip)
    orbits_skip=10
    nearest_day_indx = find_nearest(star_time_array, kic_first_tce_day + (kic_orbital_period *  orbits_skip));
    star_time_transit = time[nearest_day_indx-1000: nearest_day_indx + 1000]
    star_flux_transit = lightcurves[nearest_day_indx-1000: nearest_day_indx + 1000]

    plt.plot(star_time_transit, star_flux_transit, ".", markersize="3", color="orange")
    plt.show()
        # return fig


    