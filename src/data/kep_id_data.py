from numpy.lib.arraysetops import unique
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import threading

from data.data_constants import KEPLER_CSV_DATA, TESS_CSV_DATA

def get_all_star_kic(kic_type,mission):

    if mission == "kepler":
        tce_data = pd.read_csv(KEPLER_CSV_DATA,comment="#")
        tce_data = tce_data[tce_data.av_training_set == kic_type] 
        kic_list_data = tce_data.kepid.astype(str)
        return kic_list_data
    else:
        tce_data = pd.read_csv(TESS_CSV_DATA,comment="#")
        tce_data = tce_data[tce_data.tfopwg_disp == kic_type] 
        kic_list_data = tce_data.tid.astype(str)
        return kic_list_data

    
   
    # kic_unique = unique(kic_list_data)
    

def get_data_for_kic(kic,mission):
    if mission == "kepler":
        tce_data = pd.read_csv(KEPLER_CSV_DATA,comment="#")
        kic_data = tce_data[tce_data.kepid == int(kic)]
        return kic_data
    elif mission == "tess":
        tce_data = pd.read_csv(TESS_CSV_DATA,comment="#")
        kic_data = tce_data[tce_data.tid == int(kic)]
        print(kic_data)
        return kic_data
        