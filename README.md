<h3 align="center"> Tess + Kepler Data Fetch and Preprocessing</h3>

---

<p align="center"> Interface for exoplanet data visualisation and preprocessing.
    <br> 
</p>

## About <a name = "about"></a>
The goal of this project is to combine data from both exoplanet missions, TESS and Kepler, in a common interface for visualisation and data preprocessing.

## Getting Started <a name = "getting_started"></a>
- Download the requirements from "requirements.txt"
- Run app.py

## Usage <a name="usage"></a>
The interface gives access to the TCE (Treshold Crossing Events) dataset list from Kepler and TESS mission.
![Annotation 2022-01-21 040922](https://user-images.githubusercontent.com/45862325/150458960-7097d648-73c4-4489-a532-4e11ee9d0edb.png)

  **Mission:** Kepler or TESS\
  **TCE Type:** PC - Planet Candidate, AFP - Astrophysical False Positive, NTP - Non Transiting Phenomenon\
  **Star Id:** Selected TCE's star ID\
  **Transit Period:** Time of one transit in days\
  **First day of transit:** First day of transit in BJD\
  **TCE Id:** The ID of the unique TCE (object) for that star

- Kepler TCA dataset -> https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=q1_q17_dr24_tce
- TESS TCA dataset -> https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=TOI

## Project goals
- [x] Automatic fetch of Kepler data or a single star (.fits files based on the TCA dataset)
- [x] Automatic fetch of TESS data or a single star (.fits files based on the TCA dataset)
- [x] Local and global star fluxes and centroids
- [x] Star flux and centroid visuelization 
- [x] User Interface for data visualization and dataset access
- [ ] Complete preprocessing of the star fluxes and centroids
- [ ] Functionality robusntess independent of the specific mission
- [ ] A functionality in the UI to retrieve ready processed star data for the pretrained ML model (global_flux,local_flux,global_centroid,local_centroid,metadata)  

## Acknowledgements <a name = "acknowledgement"></a>
- https://github.com/google-research/exoplanet-ml/tree/master/exoplanet-ml/astronet - Shallue, Christopher J. , Vanderburg, Andrew
