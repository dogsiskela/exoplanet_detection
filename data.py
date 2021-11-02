from numpy.lib.arraysetops import unique
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import threading
import time

#Store all individual lightcurve datas inside ./download_data/kep_star_id
LIGHTCURVES_FOLDER = "download_data";
LIGHTCURVES_URL = "https://archive.stsci.edu/pub/kepler/lightcurves";

def get_full_kepid_string(id):
    id_string = str(id)
    id_length = len(id_string)
    remaining_zeroes = 9-id_length
    return "0" * remaining_zeroes + id_string

def get_all_star_kic():
    tce_data =pd.read_csv('tce_data.csv',comment="#")
    kic_list_data = tce_data.kepid
    kic_unique = unique(kic_list_data)
    return kic_unique

def func(current_kic_id,file_name,kic_id_link):
        if not os.path.exists(LIGHTCURVES_FOLDER + '/' + current_kic_id):    
            os.mkdir(LIGHTCURVES_FOLDER + '/'+current_kic_id)
        
        print("Downloading: " + file_name)       
        r = requests.get(kic_id_link + "/" + file_name)
        open(LIGHTCURVES_FOLDER  + '/' + current_kic_id+"/" + file_name, 'wb').write(r.content) 
            

def get_last_downloaded_kepid_index():
    path, dirs, files = next(os.walk(LIGHTCURVES_FOLDER))
    dirs_count = len(dirs)
    return dirs_count-1


def download_fits_dataset():
    initial_kic_index = 0

    if not os.path.exists(LIGHTCURVES_FOLDER):    
        os.mkdir(LIGHTCURVES_FOLDER)
    else:
        initial_kic_index = get_last_downloaded_kepid_index()

    all_kics = get_all_star_kic()

    for i in range(initial_kic_index,len(all_kics)):
        print(all_kics[i])
        current_kic_id = get_full_kepid_string(all_kics[i])
        kic_id_link = LIGHTCURVES_URL+"/"+current_kic_id[0:4]+"/"+current_kic_id

        response = requests.get(kic_id_link)
        body = response.text
        soup = BeautifulSoup(body, 'html.parser')
        all_links_on_site_kic = soup.find_all('a');
        all_links_kic = []
        for link in all_links_on_site_kic:
            if "_llc" in link["href"]:
                all_links_kic.append(link["href"])

        print("Length of fits files:" + str(len(all_links_kic)))
            
        threads = []
        for i in range(0,len(all_links_kic)):
            thread = threading.Thread(target = func, args=(current_kic_id,all_links_kic[i],kic_id_link,))
            thread.daemon = True
            threads.append(thread)
            print ("Added thread " + str(i))
        
        for thread in threads:
            thread.start()
            print("Thread started")

        for thread in threads:
            thread.join()
            print("Finished")

        print("=== DONE ===")
