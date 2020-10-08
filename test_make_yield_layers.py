# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 21:25:28 2020

@author: carli
"""

# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore")
#from whitebox import WhiteboxTools
#wbt = WhiteboxTools()
try:
    from whitebox_tools import WhiteboxTools
except:
    from whitebox import WhiteboxTools
wbt = WhiteboxTools()
import os 
from functions_V2 import *
from osgeo  import ogr,gdal
from functions import extract_point_data_from_rasters, CreateGridPointFromPolygon

def my_callback(value):
    if not "%" in value:
        print(value)
        
rootFile = "C:/Users/carli/Documents/Proyectos_Desarrollo_de_Software/prueba_raster_postgis/"
os.chdir(rootFile)

#========== interpolacion mapa rinde
def create_yield_layers(archivo_cosecha): 
    atributo_rto = 'RTO'
    atributo_rto_rel = 'RTOREL' 
    
    try:
        outfile_RTO = str((os.path.join(rootFile, 'temp/RTO.tif')))
        wbt.idw_interpolation(str((os.path.join(rootFile, archivo_cosecha))), 
                              atributo_rto, 
                              outfile_RTO,
                              weight=2.0, 
                              radius=30, 
                              min_points=20, 
                              cell_size=10,
                              base=None,
                              callback = my_callback)
        
        outfile_RTO_REL = str((os.path.join(rootFile, 'temp/RTO_REL.tif')))
        wbt.idw_interpolation(str((os.path.join(rootFile, archivo_cosecha))), 
                              atributo_rto_rel, 
                              outfile_RTO_REL,
                              weight=2.0, 
                              radius=30, 
                              min_points=20, 
                              cell_size=10,
                              base=None,
                              callback = my_callback)
    except:
        print("Ocurrio un problema cuando se estaba realizando la interpolacion del mapa de rinde")  