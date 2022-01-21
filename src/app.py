import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QListWidget, QPushButton, QLabel,QWidget
from data.fetch_data import download_single_fits, download_single_fits_tess, get_full_kepid_string
from data.kep_id_data import get_all_star_kic, get_data_for_kic

from visualization.visualize_data import visualize_star
from data.process_data import get_centroid_local, get_global_lightcurves, get_local_lightcurves

OPEN_PARAGRAPH = "<p>"
CLOSE_PARAGRAPH = "</p>"
OPEN_HEADER = "<h4>"
CLOSE_HEADER= "</h4>"

KEPLER_TYPES = ["PC", "AFP", "NTP"]
TESS_TYPES = ["PC", "KP", "FP","CP"]

class exoplanetFilter(QWidget):
    def __init__(self, parent = None):
        super(exoplanetFilter, self).__init__(parent)

        layout = QGridLayout()

        self.labMission = QLabel('<h4>Mission:</h4>')

        # TCE Type container
        self.labStarType = QLabel(OPEN_PARAGRAPH + 'TCE type:' + CLOSE_PARAGRAPH)
        self.typeCb = QComboBox()
        self.typeCb.addItems(KEPLER_TYPES)
        self.typeCb.currentIndexChanged.connect(self.typeChangeHandler)

        # Mission container
        self.missionCb = QComboBox()
        self.missionCb.addItems(["kepler","tess"])
        self.missionCb.currentIndexChanged.connect(self.selectionchange)
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.clickOnItemFromListHandler)

        # Get inital star data
        data = get_all_star_kic("PC","kepler")
        self.listWidget.addItems(data)

        # Visualization buttons 
        self.visualizeFluxButton = QPushButton("Visualize Flux")
        self.visualizeFluxButton.clicked.connect(self.visualizeStarFlux)
        self.visualizeCentroidButton = QPushButton("Visualize Centroid")
        self.visualizeCentroidButton.clicked.connect(self.visualizeStarCentroid)
        self.visualizeLocalButton = QPushButton("Visualize Local")
        self.visualizeLocalButton.clicked.connect(self.visualizeStarLocal)
        self.visualizeGlobalButton = QPushButton("Visualize Global")
        self.visualizeGlobalButton.clicked.connect(self.visualizeStarGlobal)

        # Unique TCE index for the current star picker
        self.starId = QLabel(OPEN_HEADER + "Star id:" + CLOSE_HEADER + OPEN_PARAGRAPH + "/" + CLOSE_PARAGRAPH)
        self.tceIndxComboBox = QComboBox()

        #S tar metadata
        self.tceIndx = QLabel(OPEN_HEADER + "TCE id:" + CLOSE_HEADER + OPEN_PARAGRAPH +"/" + CLOSE_PARAGRAPH)
        self.transitPeriod = QLabel(OPEN_HEADER + "Transit period:" + CLOSE_HEADER + OPEN_PARAGRAPH +"/" + CLOSE_PARAGRAPH)
        self.firstDayOfTransit = QLabel(OPEN_HEADER + "First day of transit:" + CLOSE_HEADER + OPEN_PARAGRAPH +"/" + CLOSE_PARAGRAPH)
        self.trainingSet = QLabel(OPEN_HEADER + "Training set type:" + CLOSE_HEADER + OPEN_PARAGRAPH +"/" + CLOSE_PARAGRAPH)

        # Build widget layout
        layout.addWidget(self.labMission,0,0)
        layout.addWidget(self.missionCb,0,1)
        layout.addWidget(self.labStarType,0,2)
        layout.addWidget(self.typeCb,0,3)
        layout.addWidget(self.listWidget,1,0,1,3)
        layout.addWidget(self.tceIndxComboBox,2,0)
        layout.addWidget(self.starId,2,1)
        layout.addWidget(self.transitPeriod,2,2)
        layout.addWidget(self.firstDayOfTransit,2,3)
        layout.addWidget(self.trainingSet,2,4)
        layout.addWidget(self.tceIndx,2,5)
        layout.addWidget(self.visualizeFluxButton,3,0)
        layout.addWidget(self.visualizeCentroidButton,3,1)
        layout.addWidget(self.visualizeLocalButton,3,2)
        layout.addWidget(self.visualizeGlobalButton,3,3)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle("Exoplanet visualization")
   
    def resetStarsData(self,_):
        self.listWidget.clear()

        data = get_all_star_kic(self.typeCb.currentText(),self.missionCb.currentText())
        self.listWidget.addItems(data)

   # Get the list of all the TCPs that satisfy the filters
    def selectionchange(self,i):
        self.typeCb.clear()
        try: self.typeCb.currentIndexChanged.disconnect() 
        except Exception: pass
        
        if self.missionCb.currentText() == "tess":
            self.typeCb.addItems(TESS_TYPES)
        elif self.missionCb.currentText() == "kepler":
            self.typeCb.addItems(KEPLER_TYPES)

        self.typeCb.currentIndexChanged.connect(self.typeChangeHandler)
        
        self.resetStarsData(self)

    def typeChangeHandler(self,i):
        self.resetStarsData(self)

    # Show star metadata when it is selected from the list
    #############################################################
    # single_kep_data: data for the currently selected star
    # tcpIndx: Index of the currently selected TCP index 
    def updateKicData(self,single_kep_data,tcpIndx):
        starId = ""
        transitPeriod = ""
        firstDayOfTransit = ""
        trainingSetType = ""
        tceId = ""
        if self.missionCb.currentText() == "kepler":
            starId = str(single_kep_data.iloc[tcpIndx].kepid)
            transitPeriod = str(single_kep_data.iloc[tcpIndx].tce_period)
            firstDayOfTransit = str(single_kep_data.iloc[tcpIndx].tce_time0bk)
            trainingSetType = str(single_kep_data.iloc[tcpIndx].av_training_set)
            tceId = str(single_kep_data.iloc[tcpIndx].tce_plnt_num)
        elif self.missionCb.currentText() == "tess":
            starId = str(single_kep_data.iloc[tcpIndx].tid)
            transitPeriod = str(single_kep_data.iloc[tcpIndx].pl_orbper)
            firstDayOfTransit = str(single_kep_data.iloc[tcpIndx].pl_tranmid)
            trainingSetType = str(single_kep_data.iloc[tcpIndx].tfopwg_disp)
            tceId = str(single_kep_data.iloc[tcpIndx].toi)

        self.starId.setText(OPEN_HEADER + "Star id:" + CLOSE_HEADER + OPEN_PARAGRAPH +starId + CLOSE_PARAGRAPH)
        self.transitPeriod.setText(OPEN_HEADER + "Transit period:" + CLOSE_HEADER + OPEN_PARAGRAPH  + transitPeriod + CLOSE_PARAGRAPH)
        self.firstDayOfTransit.setText(OPEN_HEADER + "First day of transit:" + CLOSE_HEADER + OPEN_PARAGRAPH  + firstDayOfTransit + CLOSE_PARAGRAPH)
        self.trainingSet.setText(OPEN_HEADER + "Training set type:" + CLOSE_HEADER + OPEN_PARAGRAPH  + trainingSetType + CLOSE_PARAGRAPH)
        self.tceIndx.setText(OPEN_HEADER + "TCE id:" + CLOSE_HEADER + OPEN_PARAGRAPH  + tceId + CLOSE_PARAGRAPH)

    # TCP list click handler
    def clickOnItemFromListHandler(self,item):
        single_kep_data = get_data_for_kic(item.text(),self.missionCb.currentText())
        transit_phen_indexes = [*range(0,len(single_kep_data))]
        transit_phen_indexes = [str(int) for int in transit_phen_indexes] 

        self.tceIndxComboBox.clear()
        try: self.tceIndxComboBox.currentIndexChanged.disconnect() 
        except Exception: pass

        self.tceIndxComboBox.addItems(transit_phen_indexes)
        self.tceIndxComboBox.currentIndexChanged.connect(self.tcpSelect)
        self.updateKicData(single_kep_data,0)
      
    # Handler for TCP onIndexChange
    def tcpSelect(self,indx):
        single_kep_data = get_data_for_kic(self.listWidget.currentItem().text(),self.missionCb.currentText())
        if(indx>=0):
            self.updateKicData(single_kep_data,indx)
       

    def visualizeStarFlux(self):
        current_kic = self.listWidget.currentItem().text()
        download_single_fits(current_kic)
        visualize_star(current_kic,self.missionCb.currentText())

    def visualizeStarCentroid(self):
        current_kic = self.listWidget.currentItem().text()
        download_single_fits(current_kic)
        get_centroid_local(current_kic,self.typeCb.currentText(),self.missionCb.currentText())

    def visualizeStarLocal(self):
        current_kic = self.listWidget.currentItem().text()
        download_single_fits(current_kic)
        get_local_lightcurves(get_full_kepid_string(current_kic),self.typeCb.currentText(),self.missionCb.currentText())
        
    def visualizeStarGlobal(self):
        current_kic = self.listWidget.currentItem().text()
        download_single_fits(current_kic)
        get_global_lightcurves(get_full_kepid_string(current_kic),self.typeCb.currentText(),self.missionCb.currentText())
        
    


def start_app():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./icon.png'))
    ex = exoplanetFilter()
    ex.show()
    sys.exit(app.exec_())

start_app()