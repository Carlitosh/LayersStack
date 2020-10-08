# -*- coding: utf-8 -*-

from PyQt5 import uic, QtWidgets #Importamos módulo uic y Qtwidgets

import warnings
warnings.simplefilter('ignore')
import os 
import ogr 
import numpy as np
#os.chdir('C:/ambientaciones') 
from test_make_topographic_layers import create_soil_topographic_layers
from test_make_soil_layers import create_soil_layers
from test_make_yield_layers import create_yield_layers
from test_download_satellite_layer import *
from functions import extract_point_data_from_rasters, CreateGridPointFromPolygon

qtCreatorFile = "interfaz_agregar_capas.ui" # Nuestro archivo UI aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) #El modulo ui carga
rootFile = "C:/Users/carli/Documents/Proyectos_Desarrollo_de_Software/prueba_raster_postgis/"
os.chdir(rootFile)
if not os.path.exists('temp'):
        os.makedirs('temp')

class Aggregatelayers(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self): #Constructor de la clase
        QtWidgets.QMainWindow.__init__(self) #Constructor
        Ui_MainWindow.__init__(self) #Constructor
        self.setupUi(self) # Método Constructor de la ventana

        self.btn_abrir_capa_limites.clicked.connect(self.abrir_capa_limites)
        self.btn_abrir_capa_rindes.clicked.connect(self.abrir_mapa_rinde)
        self.btn_abrir_capa_veris.clicked.connect(self.abrir_mapa_veris) 
        self.btn_abrir_capa_muestreo.clicked.connect(self.abrir_mapa_muestreo) 
        self.btn_correr.clicked.connect(self.correr_funciones)
        self.btn_cerrar_ventana.clicked.connect(self.correr_funciones)
    
    def cerrar_ventana(self):
        pass
        
    def abrir_capa_limites(self):
        dir_capa_limites= QtWidgets.QFileDialog.getOpenFileName(self, "Abrir Mapa de limites",filter="GeoJSON (*.geojson)")
        self.lineEdit_capa_limites.setText(str(dir_capa_limites[0]))
    
    def abrir_mapa_rinde(self):
        dir_capa_rindes= QtWidgets.QFileDialog.getOpenFileName(self, "Abrir Mapa de rinde",filter="ESRI Shapefile (*.shp)")
        self.lineEdit_capa_rindes.setText(str(dir_capa_rindes[0]))    
        
    def abrir_mapa_veris(self):
        dir_capa_veris= QtWidgets.QFileDialog.getOpenFileName(self, "Abrir Mapa de veris",filter="ESRI Shapefile (*.shp)")
        self.lineEdit_capa_veris.setText(str(dir_capa_veris[0]))
        
        dirMapaVeris = str(self.lineEdit_capa_veris.text())
        dataSource = ogr.Open(dirMapaVeris)
        daLayer = dataSource.GetLayer(0)
        layerDefinition = daLayer.GetLayerDefn()
        Atributos = []
        for i in range(layerDefinition.GetFieldCount()):
            at = layerDefinition.GetFieldDefn(i).GetName()
            Atributos.append(at)
        lista_de_atributos = []
        for i in Atributos:
            lista_de_atributos.append(i)

        self.comboBox_EC30.addItems(lista_de_atributos)
        self.comboBox_EC90.addItems(lista_de_atributos)
        self.comboBox_Elev.addItems(lista_de_atributos)
        
        
        
    def abrir_mapa_muestreo(self):
        dir_capa_muestreo= QtWidgets.QFileDialog.getOpenFileName(self, "Abrir Mapa de muestreo",filter="ESRI Shapefile (*.shp)")
        self.lineEdit_capa_muestreo.setText(str(dir_capa_muestreo[0])) 


    def correr_funciones(self):
        archivo_muestreo = str(self.lineEdit_capa_muestreo.text())
        #create_soil_layers(archivo_muestreo)
        
        archivo_veris = str(self.lineEdit_capa_veris.text())
        

        
        atributo_ec30 = str(self.comboBox_EC30.currentText())
        atributo_ec90 = str(self.comboBox_EC90.currentText())
        atributo_elev = str(self.comboBox_Elev.currentText())
        #create_soil_topographic_layers(archivo_veris, atributo_ec30, 
        #                           atributo_ec90,atributo_elev)
        archivo_cosecha = str(self.lineEdit_capa_rindes.text())
        #create_yield_layers(archivo_cosecha)
        
        anio = str(self.comboBox_anio.currentText())
        archivo_geojson = str(self.lineEdit_capa_limites.text())
        #download_NDRE(archivo_geojson, anio)
        #download_CHIRPS(archivo_geojson, anio)
        #download_SMAP(archivo_geojson, anio)
        #download_SAVI(archivo_geojson, anio)
        #download_EVI(archivo_geojson, anio)
        #download_NDVI(archivo_geojson, anio)
        #download_GNDVI(archivo_geojson, anio)
        archivo_puntos_regulares = str(os.path.join(rootFile, 'temp/puntos_regulares.geojson'))
        CreateGridPointFromPolygon(archivo_geojson, archivo_puntos_regulares, cellsize = 10)
        "El archivo de limites debe estar en wgs84 para las imagenes pero en 32720 para la creacion del grid de puntos"
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    screen = Aggregatelayers()
    screen.show() 
    app.exec_()