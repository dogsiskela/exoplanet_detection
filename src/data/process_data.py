import math
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
from data.fetch_data import get_full_kepid_string


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
    print(tcp_type)
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

def get_all_centroid(kic_id,mission_id):
    FOLDER = ""
    if mission_id == "kepler":
        FOLDER = LIGHTCURVES_FOLDER
    elif mission_id == "tess":
        FOLDER = LIGHTCURVES_FOLDER_TESS

    print(FOLDER)
    if not os.path.exists(FOLDER + '/' + str(kic_id)):
        return;
    
    
    time = []
    x_centroid = []
    y_centroid = []

    for (dirpath, dirnames, filenames) in walk(FOLDER+"/"+kic_id):
        for index,file in enumerate(filenames):
            lightcurve_file = fits.open(FOLDER+"/"+kic_id + "/" +filenames[1])
            lightcurve_data = lightcurve_file["LIGHTCURVE"].data

            star_time = lightcurve_data["TIME"]
            star_x_centr = lightcurve_data["MOM_CENTR1"]
            star_y_centr = lightcurve_data["MOM_CENTR2"]
            # star_x_centr -= np.nanmedian(np.array(star_x_centr))
            # star_y_centr -=np.nanmedian(np.array(star_y_centr))
            time.extend(star_time)
            x_centroid.extend(star_x_centr)
            y_centroid.extend(star_y_centr)

    return time,x_centroid,y_centroid
    

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
    orbits_skip=8
    nearest_day_indx = find_nearest(star_time_array, kic_first_tce_day + (kic_orbital_period *  orbits_skip));
    star_time_transit = time[nearest_day_indx-100: nearest_day_indx + 100]
    star_flux_transit = lightcurves[nearest_day_indx-100: nearest_day_indx + 100]

    plt.plot(star_time_transit, star_flux_transit, ".", markersize="3", color="orange")
    plt.show()
    return star_flux_transit,star_time_transit
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
    orbits_skip=1
    nearest_day_indx = find_nearest(star_time_array, kic_first_tce_day + (kic_orbital_period *  orbits_skip));
    star_time_transit = time[nearest_day_indx-300: nearest_day_indx + 300]
    star_flux_transit = lightcurves[nearest_day_indx-300: nearest_day_indx + 300]

    plt.plot(star_time_transit, star_flux_transit, ".", markersize="3", color="orange")
    plt.show()
    return star_flux_transit,star_time_transit

def get_centroid(kic_id,p_type="PC",mission_id="kepler"):
   
    time,x_centroid,y_centroid = get_all_centroid(kic_id,mission_id=mission_id) 
    x_avg = np.nansum(x_centroid)/(len(x_centroid))
    y_avg = np.nansum(y_centroid)/(len(y_centroid))
    y_new = []
    avg = math.sqrt((x_avg*x_avg)+(y_avg*y_avg))
    for i in range(0,len(time)):
        tempAvg = math.sqrt((x_centroid[i]*x_centroid[i])+(y_centroid[i]*y_centroid[i]))
        y_new.append(avg-tempAvg)

    kic_metadata = ""
    if mission_id == "kepler":
        kic_metadata = get_kic_metadata_kepler(kic_id,p_type)
    elif mission_id == "tess":
        kic_metadata = get_kic_metadata_tess(kic_id,p_type)
    plt.plot(time,y_new, ".", markersize="3", color="orange")
    plt.show()


    print(x_avg,y_avg)
    plt.scatter(x_centroid,y_centroid)
    plt.show()



def get_centroid_local(kic_id,p_type="PC",mission_id="kepler"):
    time,x_centroid,y_centroid = get_all_centroid(get_full_kepid_string(kic_id),mission_id=mission_id) 
    x_avg = np.nansum(x_centroid)/(len(x_centroid))
    y_avg = np.nansum(y_centroid)/(len(y_centroid))
    y_new = []
    avg = math.sqrt((x_avg*x_avg)+(y_avg*y_avg))
    for i in range(0,len(time)):
        tempAvg = math.sqrt((x_centroid[i]*x_centroid[i])+(y_centroid[i]*y_centroid[i]))
        y_new.append(tempAvg-avg)

    kic_metadata = ""
    if mission_id == "kepler":
        kic_metadata = get_kic_metadata_kepler(kic_id,p_type)
    elif mission_id == "tess":
        kic_metadata = get_kic_metadata_tess(kic_id,p_type)

    # for i in range(0,len(kic_metadata)):
    kic_first_tce_day = kic_metadata[0][0]
    kic_orbital_period = kic_metadata[0][1] 
    orbits_skip = 5
    print(kic_first_tce_day + (kic_orbital_period *  orbits_skip))
    nearest_day_indx = find_nearest(time, kic_first_tce_day + (kic_orbital_period *  orbits_skip));
    print(nearest_day_indx)
    # nearest_day_indx = 300
    star_time_transit = time[nearest_day_indx-100: nearest_day_indx + 100]
    star_flux_transit = y_new[nearest_day_indx-100: nearest_day_indx + 100]
    star_flux_transit_y = y_centroid[nearest_day_indx-100: nearest_day_indx + 100]
    star_flux_transit_x = x_centroid[nearest_day_indx-100: nearest_day_indx + 100]

    plt.subplot(1,3,1)
    plt.plot(star_time_transit,star_flux_transit, ".", markersize="3", color="orange")
    plt.title("centroid avg")

    plt.subplot(1,3,2)
    plt.plot(star_time_transit,star_flux_transit_y, ".", markersize="3", color="orange")
    plt.title("centroid y")

    plt.subplot(1,3,3)
    plt.plot(star_time_transit,star_flux_transit_x, ".", markersize="3", color="orange")
    plt.title("centroid x")
    plt.show()
    return star_flux_transit,star_time_transit


    