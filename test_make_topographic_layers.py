# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore")
#from whitebox import WhiteboxTools
#wbt = WhiteboxTools()
#from whitebox import WhiteboxTools
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

#archivo_veris = 'capas/AGD-UNAGRO_Ponte_1_veris_16.shp'
#archivo_puntos_regulares = str((os.path.join(rootFile, 'temp/puntos_regulares.geojson')))



def create_soil_topographic_layers(archivo_veris, atributo_ec30, 
                                   atributo_ec90,atributo_elev):
        
    #========== interpolacion EC30
    try:
        outfile_EC30 = str((os.path.join(rootFile, 'temp/EC30.tif')))
        wbt.idw_interpolation(str((os.path.join(rootFile, archivo_veris))), 
                              atributo_ec30, 
                              outfile_EC30,
                              weight=2.0, 
                              radius=30, 
                              min_points=20, 
                              cell_size=10,
                              base=None,
                              
                              callback = my_callback)
        
        outfile_EC90 = str((os.path.join(rootFile, 'temp/EC90.tif')))
        wbt.idw_interpolation(str((os.path.join(rootFile, archivo_veris))), 
                              atributo_ec90, 
                              outfile_EC90,
                              weight=2.0, 
                              radius=30, 
                              min_points=20, 
                              cell_size=10,
                              base=None,
                              
                              callback = my_callback)
        
    
    except:
        print("Ocurrio un problema cuando se estaba realizando la interpolacion del archivo EC30")  
    
    
    
    try:
        outfile_interpolation = str((os.path.join(rootFile, 'temp/Elev_V1.tif'))) #str(rootFile + 'capas/mapa_rinde_V1.tif')
        wbt.idw_interpolation(str((os.path.join(rootFile, archivo_veris))), 
                              atributo_elev, 
                              outfile_interpolation,
                              weight=2.0, 
                              radius=30, 
                              min_points=20, 
                              cell_size=10,
                              #epsg=32720,
                              base=None,
                              
                              callback = my_callback)
    
    except:
        print("Ocurrio un problema cuando se estaba realizando la interpolacion")
    

    
    outfile_smoothing = outfile_interpolation.replace('_V1','')
    wbt.gaussian_filter(outfile_interpolation, outfile_smoothing ,sigma=3)
    
    outfile_SCA = outfile_smoothing.replace('Elev','SCA')
    wbt.d_inf_flow_accumulation(outfile_smoothing, outfile_SCA)
    
    outfile_SLP = outfile_smoothing.replace('Elev','SLP')
    wbt.slope(outfile_smoothing, outfile_SLP)
    
    outfile_CTI = outfile_smoothing.replace('Elev','CTI')
    wbt.wetness_index(outfile_SCA, outfile_SLP,outfile_CTI)
    
    """
    outfile_PlanCurv = outfile_smoothing.replace('Elev','PlanCurv')
    wbt.plan_curvature(outfile_smoothing, outfile_PlanCurv,zfactor=None)
    
    outfile_RugInd = outfile_smoothing.replace('Elev','RugInd')
    wbt.ruggedness_index(outfile_smoothing, outfile_RugInd, zfactor=None)
    
    outfile_ProfCurv = outfile_smoothing.replace('Elev','ProfCurv')
    wbt.profile_curvature(outfile_smoothing, outfile_ProfCurv, zfactor=None)
    """
    
    outfile_RelTopoPos = outfile_smoothing.replace('Elev','RELTOPOPOS')
    wbt.relative_topographic_position(outfile_smoothing, outfile_RelTopoPos, 
                                      filterx=11, filtery=11)   
    
    outfile_TotCurv = outfile_smoothing.replace('Elev','TOTCURV')
    wbt.total_curvature(outfile_smoothing, outfile_TotCurv)
    
    outfile_STI = outfile_smoothing.replace('Elev','STI')
    wbt.sediment_transport_index(outfile_SCA, outfile_SLP, outfile_STI, 
                                 sca_exponent=0.4, slope_exponent=1.3)
    

    os.remove(outfile_interpolation)
    
    
    
    
    """
    inputs = [outfile_smoothing, outfile_EC30, outfile_EC90, 
              outfile_SLP, outfile_SCA, outfile_CTI]
    
    outfile = str((os.path.join(rootFile, 'temp/outfile_topo_layers.geojson'))) 
    extract_point_data_from_rasters(archivo_puntos_regulares,inputs,outfile)
    """


