from data.fetch_data import download_single_fits_tess
from data.process_data import get_local_lightcurves, get_global_lightcurves
from visualization.visualize_data import visualize_star

# download_single_fits_tess("370133522")
visualize_star("370133522","tess")
get_local_lightcurves("370133522",mission_id="tess",p_type = "CP")


