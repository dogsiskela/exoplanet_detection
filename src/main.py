from data.fetch_data import download_single_fits, download_single_fits_tess
from data.process_data import get_all_centroid, get_centroid, get_centroid_local, get_local_lightcurves, get_global_lightcurves
from visualization.visualize_data import visualize_star


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

from data.spline import fit_kepler_spline, split
# download_single_fits("007049486")
# visualize_star("000757450","kepler")
# get_global_lightcurves("000757450",mission_id="kepler",p_type = "PC")

# visualize_star("007049486","kepler")
# get_local_lightcurves("007049486",p_type="AFP")
# get_centroid_local("007049486",p_type="AFP")
# get_centroid("007049486")

# download_single_fits("007049486")
lightcurve, timeframe = get_centroid_local("007105574",p_type="AFP",mission_id="kepler")
timeframe, lightcurve = split(timeframe, lightcurve, gap_width=0.75)
mylist = [0 if pd.isna(x) else x for x in lightcurve[0]]
print(np.count_nonzero(np.isnan(mylist)))
print(mylist)
# print(lightcurve)
spline = fit_kepler_spline(all_time=np.array(timeframe),all_flux=np.array([mylist]),verbose=False)[0]
print(spline)
# print("SPLINE")
# # print(spline)
res = [i / j for i, j in zip(lightcurve, spline)]
# print(res)
# lightcurve = np.divide(lightcurve, 35)
plt.subplot(1,2,1)
plt.plot(timeframe, res, ".", markersize="3", color="orange")
plt.subplot(1,2,2)
plt.plot(timeframe, lightcurve, ".", markersize="3", color="orange")
plt.show()
print(lightcurve)
# get_centroid_local("000757450",mission_id="kepler")
# get_centroid_local("233681149",mission_id="tess",p_type="FP")