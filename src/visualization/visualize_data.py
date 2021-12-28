import os
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from os import walk

from data.data_constants import LIGHTCURVES_FOLDER, LIGHTCURVES_FOLDER_TESS
from data.fetch_data import get_full_kepid_string


def visualize_star(kic_id,mission_id):
    kic_id = get_full_kepid_string(kic_id)
    CURRENT_LIGHTCURVES_FOLDER = "" 
    if mission_id == "tess":
        CURRENT_LIGHTCURVES_FOLDER = LIGHTCURVES_FOLDER_TESS
    else:
        CURRENT_LIGHTCURVES_FOLDER = LIGHTCURVES_FOLDER 

    if not os.path.exists(CURRENT_LIGHTCURVES_FOLDER + '/' + str(kic_id)):
        return;
    print("exists")
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['figure.facecolor'] = 'gray'

    for (dirpath, dirnames, filenames) in walk("./"+CURRENT_LIGHTCURVES_FOLDER+"/"+kic_id):
        for index,file in enumerate(filenames):
            lightcurve_file = fits.open("./"+CURRENT_LIGHTCURVES_FOLDER+"/"+kic_id + "/" +filenames[index])
            lightcurve_data = lightcurve_file["LIGHTCURVE"].data

            star_time = lightcurve_data["TIME"]
            star_flux = lightcurve_data["PDCSAP_FLUX"]

            star_flux -= np.nanmedian(star_flux)

            plt.plot(star_time, star_flux, ".", markersize="3", color="orange")

    plt.show()
