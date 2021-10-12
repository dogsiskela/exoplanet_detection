from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from os import walk
from numpy.lib.arraysetops import unique
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os



LIGHTCURVES_URL = "https://archive.stsci.edu/pub/kepler/lightcurves";

if not os.path.exists('download_data'):    
        os.mkdir('download_data')

tce_data =pd.read_csv('tce_data.csv',comment="#")
kic_list_data = tce_data.kepid
kic_unique = unique(kic_list_data)

def kepid_string(id):
    id_string = str(id)
    id_length = len(id_string)
    remaining_zeroes = 9-id_length
    return "0" * remaining_zeroes + id_string

# current_kic_id = kepid_string(kic_unique[0]);
#kep-90
current_kic_id = kepid_string("011442793")

kic_id_link = LIGHTCURVES_URL+"/"+current_kic_id[0:4]+"/"+current_kic_id

response = requests.get(kic_id_link)
body = response.text


soup = BeautifulSoup(body, 'html.parser')
all_links_kic = soup.find_all('a');

if not os.path.exists('download_data/' + current_kic_id):
    for link in all_links_kic:
        # display the actual urls
        if not os.path.exists('download_data/' + current_kic_id):    
            os.mkdir('download_data/'+current_kic_id)


        fits_filename = link.get('href')
        if "_llc" in fits_filename:
            print("downloading: " + link.get('href'))       
            r = requests.get(kic_id_link+"/"+fits_filename)
            open('download_data/' + current_kic_id+"/"+ fits_filename, 'wb').write(r.content)


###SHOW STAR FLUX_TIME
star_time = []
star_flux = []

f = []


plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['figure.facecolor'] = 'gray'
fig = plt.figure(figsize=(13, 6))

for (dirpath, dirnames, filenames) in walk("./download_data/"+current_kic_id):
    for index,file in enumerate(filenames):
        lightcurve_file = fits.open("./download_data/"+current_kic_id + "/" +filenames[index])
        lightcurve_data = lightcurve_file["LIGHTCURVE"].data

        star_time = lightcurve_data["TIME"]
        star_flux = lightcurve_data["PDCSAP_FLUX"]
        star_flux -= np.nanmedian(star_flux)

        plt.plot(star_time, star_flux, ".", markersize="3", color="orange")


plt.grid()
plt.show()

