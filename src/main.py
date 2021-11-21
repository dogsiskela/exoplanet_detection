from data.fetch_data import download_single_fits_tess
from visualization.visualize_data import visualize_star

download_single_fits_tess("290131778")
visualize_star("290131778","TESS")
# visualize_star("001161345")
# get_local_lightcurves("001161345")


