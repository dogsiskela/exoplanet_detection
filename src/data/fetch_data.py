from numpy.lib.arraysetops import unique
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import threading

from data.data_constants import LIGHTCURVES_FOLDER_TESS, LIGHTCURVES_FOLDER, LIGHTCURVES_URL, LIGHTCURVES_URL_TESS


#############################################################
####################### DOWNLOAD DATA #######################
#############################################################


#Add leading zeroes to kepler star ids
#############################################################
def get_full_kepid_string(id):
    id_string = str(id)
    id_length = len(id_string)
    remaining_zeroes = 9-id_length
    return "0" * remaining_zeroes + id_string

#Returns all unique star IDs from the TCE collection dataset
#############################################################
def get_all_star_kic():
    tce_data =pd.read_csv('tce_data.csv',comment="#")
    kic_list_data = tce_data.kepid
    kic_unique = unique(kic_list_data)
    return kic_unique

#Downloads and writes a .fits file from a star to the corresponding star folder
#############################################################
#current_kic_id : id of the current star
#file_name : name of the file on the webiste
#kic_id_link : link to the page containing all the .llc and .slc files for the current star

def fetch_fits_file(current_kic_id,file_name,kic_id_link,mission_id):
        DOWNLOAD_FOLDER = "" 
        if mission_id == "kepler":
            DOWNLOAD_FOLDER = LIGHTCURVES_FOLDER
        elif mission_id == "tess":
            DOWNLOAD_FOLDER = LIGHTCURVES_FOLDER_TESS
            

        if not os.path.exists(DOWNLOAD_FOLDER + '/' + current_kic_id):    
            os.mkdir(DOWNLOAD_FOLDER + '/'+current_kic_id)
        
        
        print("Downloading: " + file_name)       
        r = requests.get(kic_id_link + "/" + file_name)
        open(DOWNLOAD_FOLDER  + '/' + current_kic_id+"/" + file_name, 'wb').write(r.content) 


#Get the ked_id of the last downloaded star
#############################################################
def get_last_downloaded_kepid_index():
    path, dirs, files = next(os.walk(LIGHTCURVES_FOLDER))
    dirs_count = len(dirs)
    return dirs_count-1

#Link to the page containing the .fits files for star
#Link format -> https://archive.stsci.edu/pub/kepler/lightcurves/kic_id[:4]/kic_id
#############################################################
#current_kic_id : id of the star
def get_kic_id_link(current_kic_id):
    return  LIGHTCURVES_URL+"/"+current_kic_id[0:4]+"/"+current_kic_id;


#Link to the page containing the .fits files for star
#Link format -> https://archive.stsci.edu/pub/kepler/lightcurves/kic_id[:4]/kic_id
#############################################################
#current_kic_id : id of the star
def get_kic_id_link_tess(current_kic_id,season=1):
    season_str = str(season)
    leading_zeroes = 4-len(season_str)
    season_str = "0"*leading_zeroes + season_str
    print( LIGHTCURVES_URL_TESS+season_str+"/0000/000"+current_kic_id[0]+"/"+current_kic_id[1:5]+"/"+current_kic_id[5:9])

    return  LIGHTCURVES_URL_TESS+season_str+"/0000/000"+current_kic_id[0]+"/"+current_kic_id[1:5]+"/"+current_kic_id[5:9];

#Get all llc (Long cadence light curves) download links for a star
#############################################################
#current_kic_id : pafe link with .fits files
def get_llc_links_kic(current_kic_link):
    response = requests.get(current_kic_link)
    body = response.text
    soup = BeautifulSoup(body, 'html.parser')
    all_links_on_site_kic = soup.find_all('a');
    all_links_kic = []
    for link in all_links_on_site_kic:
        if "_llc" in link["href"]:
            all_links_kic.append(link["href"])
    return all_links_kic

#Get all llc (Long cadence light curves) download links for a star
#############################################################
#current_kic_id : pafe link with .fits files
def get_llc_links_kic_fits(current_kic_link):
    response = requests.get(current_kic_link)
    body = response.text
    soup = BeautifulSoup(body, 'html.parser')
    all_links_on_site_kic = soup.find_all('a');
    all_links_kic = []
    for link in all_links_on_site_kic:
        if "s_lc.fits" in link["href"]:
            all_links_kic.append(link["href"])
    return all_links_kic

#Download single star .fits data for Kepler
#############################################################
def download_single_fits(kic_id):
    if not os.path.exists(LIGHTCURVES_FOLDER):    
        os.mkdir(LIGHTCURVES_FOLDER)
    
    #Get full KIC id
    current_kic_id = get_full_kepid_string(kic_id)

    if os.path.exists(LIGHTCURVES_FOLDER + '/' + current_kic_id):    
        return

    #Get the link to the page containing the files for the star
    kic_id_link = get_kic_id_link(current_kic_id)

    #Get the download links for the llc .fits files
    llc_links_current_kic = get_llc_links_kic(kic_id_link)

    llc_links_length = len(llc_links_current_kic)
    print("Length of fits files:" + str(llc_links_length))
    
    threads = []
    for i in range(0,llc_links_length):
        thread = threading.Thread(target = fetch_fits_file, args=(current_kic_id,llc_links_current_kic[i],kic_id_link,"kepler"))
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


#Download single star .fits data for Tess
#############################################################
def download_single_fits_tess(kic_id,seasons = 43):
    if not os.path.exists(LIGHTCURVES_FOLDER_TESS):    
        os.mkdir(LIGHTCURVES_FOLDER_TESS)
    
    #Get full KIC id
    current_kic_id = get_full_kepid_string(kic_id)

    for i in range(1,seasons+1): 
        print("======= TESS SEASON "+str(i)+" =======")
        #Get the link to the page containing the files for the star
        kic_id_link = get_kic_id_link_tess(current_kic_id,season=i)

        #Get the download links for the llc .fits files
        llc_links_current_kic = get_llc_links_kic_fits(kic_id_link)

        llc_links_length = len(llc_links_current_kic)
        print("Length of fits files:" + str(llc_links_length))
        
        threads = []
        for i in range(0,llc_links_length):
            thread = threading.Thread(target = fetch_fits_file, args=(current_kic_id,llc_links_current_kic[i],kic_id_link,"tess"))
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


#Download the whole dataset from the LIGHTCURVES_URL corresponding to
#the ids of the NASA DR24 exoplanet dataset
#############################################################
def download_fits_dataset():
    initial_kic_index = 0
    
    if not os.path.exists(LIGHTCURVES_FOLDER):    
        os.mkdir(LIGHTCURVES_FOLDER)
    else:
        initial_kic_index = get_last_downloaded_kepid_index()

    all_kics = get_all_star_kic()

    for i in range(initial_kic_index,len(all_kics)):
        print(all_kics[i])

        download_single_fits(all_kics[i])
