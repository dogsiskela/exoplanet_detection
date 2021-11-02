import threading
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from os import walk

from data import get_last_downloaded_kepid_index, threadingTest

###SHOW STAR FLUX_TIME
star_time = []
star_flux = []

f = []


threadingTest()
# print(get_last_downloaded_kepid_index())
# threadingTest()

# plt.rcParams['axes.facecolor'] = 'black'
# plt.rcParams['figure.facecolor'] = 'gray'
# fig = plt.figure(figsize=(13, 6))

# def find_nearest(array, value):
#     array = np.asarray(array)
#     idx = (np.abs(array - value)).argmin()
#     return array[idx]

# for (dirpath, dirnames, filenames) in walk("./download_data/"+current_kic_id):
#     for index,file in enumerate(filenames):
#         lightcurve_file = fits.open("./download_data/"+current_kic_id + "/" +filenames[0])
#         lightcurve_data = lightcurve_file["LIGHTCURVE"].data

#         star_time = lightcurve_data["TIME"]
#         star_flux = lightcurve_data["PDCSAP_FLUX"]

#         a = np.array(star_time)
#         # print(np.where(np.isclose(a,140.49087)))
#         nearest = find_nearest(a,123.6);
#         index_transit = list(a).index(nearest)

#         star_time_transit = star_time[index_transit-60: index_transit + 60]
#         star_flux_transit = star_flux[index_transit-60: index_transit + 60]



        
#         star_flux -= np.nanmedian(star_flux)

#         plt.subplot(2,2,1)
#         plt.plot(star_time_transit, star_flux_transit, ".", markersize="3", color="orange")

# plt.show()


# for (dirpath, dirnames, filenames) in walk("./download_data/"+current_kic_id):
#     for index,file in enumerate(filenames):
#         lightcurve_file = fits.open("./download_data/"+current_kic_id + "/" +filenames[0])
#         lightcurve_data = lightcurve_file["LIGHTCURVE"].data

#         star_time = lightcurve_data["TIME"]
#         x_centroid = lightcurve_data["MOM_CENTR1"]
#         y_centroid = lightcurve_data["MOM_CENTR2"]
#         comb_centroid =[]

#         x_centroid -= np.nanmedian(x_centroid)
#         y_centroid -= np.nanmedian(y_centroid)

#         for i,val in enumerate(y_centroid):
#             calc = math.sqrt((x_centroid[i]*x_centroid[i]) + (y_centroid[i]*y_centroid[i]))
#             comb_centroid.append(calc)

#         x_centroid -= np.nanmedian(x_centroid)
#         plt.subplot(2,2,2)
#         plt.title("x_cent")
#         plt.plot(star_time, x_centroid, ".", markersize="3", color="orange")
        
#         y_centroid -= np.nanmedian(y_centroid)
#         plt.subplot(2,2,3)
#         plt.title("y_cent")
#         plt.plot(star_time, y_centroid, ".",  markersize="3", color="orange")
        
#         comb_centroid -= np.nanmedian(comb_centroid)
#         comb_centroid /=  10
#         plt.subplot(2,2,4)
#         plt.title("comb_cent")
#         plt.plot(star_time, comb_centroid, ".", markersize="3", color="orange")


# plt.grid()
# plt.show()

