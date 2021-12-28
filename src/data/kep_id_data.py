from numpy.lib.arraysetops import unique
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import threading

from data.data_constants import KEPLER_CSV_DATA

def get_all_star_kic(kic_type,mission):
    print(mission)
    print(kic_type)
    tce_data =pd.read_csv(KEPLER_CSV_DATA,comment="#")
    tce_data = tce_data[tce_data.av_training_set == kic_type] 
    kic_list_data = tce_data.kepid.astype(str)
    # kic_unique = unique(kic_list_data)
    return kic_list_data

def get_data_for_kic(kic):
    print(kic)
    tce_data = pd.read_csv(KEPLER_CSV_DATA,comment="#")
    kic_data = tce_data[tce_data.kepid == int(kic)]
    return kic_data