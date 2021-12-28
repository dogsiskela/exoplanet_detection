import sys
from PyQt5.QtGui import QIcon

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QListWidget, QPushButton, QLabel,QWidget
from data.fetch_data import download_single_fits, download_single_fits_tess, get_full_kepid_string
from data.kep_id_data import get_all_star_kic, get_data_for_kic

from visualization.visualize_data import visualize_star
from data.process_data import get_centroid_local, get_global_lightcurves, get_local_lightcurves


class exoplanetFilter(QWidget):
    def __init__(self, parent = None):
        super(exoplanetFilter, self).__init__(parent)

        layout = QGridLayout()

        #Star filtering
        self.labMission = QLabel('<h4>Mission:</h4>')
        self.labStarType = QLabel('<p>TCE type:')
        self.missionCb = QComboBox()
        self.missionCb.addItems(["kepler","tess"])
        self.cb = QComboBox()
        self.cb.addItems(["PC", "AFP", "NTP"])
        self.cb.currentIndexChanged.connect(self.selectionchange)
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.itemClickedList)

        #get inital star data
        data = get_all_star_kic("PC","kepler")
        self.listWidget.addItems(data)

        #TCP visualization
        self.visualizeFluxButton = QPushButton("Visualize Flux")
        self.visualizeCentroidButton = QPushButton("Visualize Centroid")
        self.visualizeLocalButton = QPushButton("Visualize Local")
        self.visualizeGlobalButton = QPushButton("Visualize Global")
        self.visualizeFluxButton.clicked.connect(self.visualizeStarFlux)
        self.visualizeCentroidButton.clicked.connect(self.visualizeStarCentroid)
        self.visualizeLocalButton.clicked.connect(self.visualizeStarLocal)
        self.visualizeGlobalButton.clicked.connect(self.visualizeStarGlobal)

        self.starId = QLabel("<h4>Star id:</h4> <p>/</p>")
        self.tceIndxComboBox = QComboBox()
        self.tceIndx = QLabel("<h4>TCE id:</h4> <p>/</p>")
        self.transitPeriod = QLabel("<h4>Transit period:</h4> <p>/</p>")
        self.firstDayOfTransit = QLabel("<h4>First day of transit:</h4> <p>/</p>")
        self.trainingSet = QLabel("<h4>Training set type:</h4> <p>/</p>")

        #Add widgets
        layout.addWidget(self.labMission,0,0)
        layout.addWidget(self.missionCb,0,1)
        layout.addWidget(self.labStarType,0,2)
        layout.addWidget(self.cb,0,3)
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

        #Set the layout
        self.setLayout(layout)
        self.setWindowTitle("Exoplanet viewer")
   
    def updateKicData(self,single_kep_data,tcpIndx):
        self.starId.setText("<h4>Star id:</h4> <p>"+str(single_kep_data.iloc[tcpIndx].kepid)+"</p>")
        self.transitPeriod.setText("<h4>Transit period:</h4> <p>"+str(single_kep_data.iloc[tcpIndx].tce_period)+"</p>")
        self.firstDayOfTransit.setText("<h4>First day of transit:</h4> <p>"+str(single_kep_data.iloc[tcpIndx].tce_time0bk)+"</p>")
        self.trainingSet.setText("<h4>Training set type:</h4> <p>"+str(single_kep_data.iloc[tcpIndx].av_training_set)+"</p>")
        self.tceIndx.setText("<h4>TCE id:</h4> <p>"+str(single_kep_data.iloc[tcpIndx].tce_plnt_num)+"</p>")

    def itemClickedList(self,item):
        single_kep_data = get_data_for_kic(item.text())
        print(len(single_kep_data))
        transit_phen_indexes = [*range(0,len(single_kep_data))]
        transit_phen_indexes = [str(int) for int in transit_phen_indexes] 
        print(transit_phen_indexes)
        self.tceIndxComboBox.clear()
        try: self.tceIndxComboBox.currentIndexChanged.disconnect() 
        except Exception: pass
        self.tceIndxComboBox.addItems(transit_phen_indexes)
        self.tceIndxComboBox.currentIndexChanged.connect(self.tcpSelect)
        self.updateKicData(single_kep_data,0)
      

    def tcpSelect(self,indx):
        print("IND"+str(indx))
        single_kep_data = get_data_for_kic(self.listWidget.currentItem().text())
        print(len(single_kep_data))
        if(indx>=0):
            self.updateKicData(single_kep_data,indx)
       

    def visualizeStarFlux(self):
        current_kic = self.listWidget.currentItem().text()
        download_single_fits(current_kic)
        visualize_star(current_kic,self.missionCb.currentText())

    def visualizeStarCentroid(self):
        current_kic = self.listWidget.currentItem().text()
        download_single_fits(current_kic)
        get_centroid_local(current_kic,self.cb.currentText(),self.missionCb.currentText())

    def visualizeStarLocal(self):
        current_kic = self.listWidget.currentItem().text()
        download_single_fits(current_kic)
        get_local_lightcurves(get_full_kepid_string(current_kic),self.cb.currentText(),self.missionCb.currentText())
        
    def visualizeStarGlobal(self):
        current_kic = self.listWidget.currentItem().text()
        download_single_fits(current_kic)
        get_global_lightcurves(get_full_kepid_string(current_kic),self.cb.currentText(),self.missionCb.currentText())
        
    def selectionchange(self,i):
      self.listWidget.clear()
      data = get_all_star_kic(self.cb.currentText(),self.missionCb.currentText())
      self.listWidget.addItems(data)


def start_app():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./icon.png'))
    ex = exoplanetFilter()
    ex.show()
    sys.exit(app.exec_())

start_app()