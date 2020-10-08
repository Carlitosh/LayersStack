# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore")
#from whitebox import WhiteboxTools
try:
    from whitebox_tools import WhiteboxTools
except:
    from whitebox import WhiteboxTools
wbt = WhiteboxTools()
import os 
#from functions_V2 import *
from osgeo  import ogr,gdal
from functions import Interpolation_Default

def my_callback(value):
    if not "%" in value:
        print(value)



rootFile = "C:/Users/carli/Documents/Proyectos_Desarrollo_de_Software/prueba_raster_postgis/"
os.chdir(rootFile)

archivo_muestreo = 'capas/AGD-UNAGRO_Ponte_1_muestreo_16.shp'
archivo_puntos_regulares = str((os.path.join(rootFile, 'temp/puntos_regulares.geojson')))

def create_soil_layers(archivo_muestreo):
    
    atributo_CIC = 'CIC_del_su'
    atributo_MO = 'MO_del_sue'
    atributo_P = 'P1_del_sue'
    atributo_K = 'K_del_suel'
    atributo_MG = 'MG_del_sue'
    atributo_CA = 'CA_del_sue'
    atributo_NA = 'NA_del_sue'
    atributo_pH = 'pH_del_sue'
    atributo_S = 'S_del_suel'
    atributo_Zn = 'ZN_del_sue'
    atributo_MN = 'MN_del_sue'
    atributo_FE = 'FE_del_sue'
    atributo_CU = 'CU_del_sue'
    atributo_B = 'B_del_suel'
    atributo_CO = 'Co_del_Sue'
    atributo_ARC = str("__Arcilla_")
    atributo_ARE =  str("__Arena__")
    atributo_LIM =  str("__Limo___")
    
    
    outfile_MO = str((os.path.join(rootFile, 'temp/MO_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_MO, outfile_MO, method='nearest', cellsize=10)
    
    outfile_P = str((os.path.join(rootFile, 'temp/P_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_P, outfile_P, method='nearest', cellsize=10)
    
    
    outfile_K = str((os.path.join(rootFile, 'temp/K_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_K, outfile_K, method='nearest', cellsize=10)
    
    
    outfile_MG = str((os.path.join(rootFile, 'temp/MG_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_MG, outfile_MG, method='nearest', cellsize=10)
    
    outfile_CA = str((os.path.join(rootFile, 'temp/CA_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_CA, outfile_CA, method='nearest', cellsize=10)
    
    outfile_NA = str((os.path.join(rootFile, 'temp/NA_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_NA, outfile_NA, method='nearest', cellsize=10)
    
    outfile_pH = str((os.path.join(rootFile, 'temp/pH_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_pH, outfile_pH, method='nearest', cellsize=10)
    
    
    outfile_Zn = str((os.path.join(rootFile, 'temp/Zn_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_Zn, outfile_Zn, method='nearest', cellsize=10)
    
    outfile_S = str((os.path.join(rootFile, 'temp/S_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_S, outfile_S, method='nearest', cellsize=10)
    
    
    outfile_MN = str((os.path.join(rootFile, 'temp/MN_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_MN, outfile_MN, method='nearest', cellsize=10)
    
    outfile_FE = str((os.path.join(rootFile, 'temp/FE_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_FE, outfile_FE, method='nearest', cellsize=10)
    
    
    outfile_CU = str((os.path.join(rootFile, 'temp/CU_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_CU, outfile_CU, method='nearest', cellsize=10)
    
    outfile_B = str((os.path.join(rootFile, 'temp/B_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_B, outfile_B, method='nearest', cellsize=10)
    
    outfile_CO = str((os.path.join(rootFile, 'temp/CO_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_CO, outfile_CO, method='nearest', cellsize=10)
    
    outfile_ARC = str((os.path.join(rootFile, 'temp/ARC_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_ARC, outfile_ARC, method='nearest', cellsize=10)
    """
    outfile_ARE = str((os.path.join(rootFile, 'temp/ARE_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_ARE, outfile_ARE, method='nearest', cellsize=10)
    
    """
    outfile_LIM = str((os.path.join(rootFile, 'temp/LIM_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_LIM, outfile_LIM, method='nearest', cellsize=10)
    
    
    outfile_CIC = str((os.path.join(rootFile, 'temp/CIC_V1.tif')))
    Interpolation_Default(str(os.path.join(rootFile, archivo_muestreo)), 
                              atributo_CIC, outfile_CIC, method='nearest', cellsize=10)
    
    try:
        
        outfile_smoothing_MO = outfile_MO.replace('MO_V1','MO')
        wbt.gaussian_filter(outfile_MO, outfile_smoothing_MO ,sigma=5)
    
        outfile_smoothing_CIC = outfile_CIC.replace('CIC_V1','CIC')
        wbt.gaussian_filter(outfile_CIC, outfile_smoothing_CIC ,sigma=5)
        
        outfile_smoothing_P = outfile_P.replace('P_V1','P')
        wbt.gaussian_filter(outfile_P, outfile_smoothing_P ,sigma=5)
        
        outfile_smoothing_K = outfile_K.replace('K_V1','K')
        wbt.gaussian_filter(outfile_K, outfile_smoothing_K ,sigma=5)
        
        
        outfile_smoothing_MG = outfile_MG.replace('MG_V1','MG')
        wbt.gaussian_filter(outfile_MG, outfile_smoothing_MG ,sigma=5)
        
        outfile_smoothing_CA = outfile_CA.replace('CA_V1','CA')
        wbt.gaussian_filter(outfile_CA, outfile_smoothing_CA ,sigma=5)
        
        outfile_smoothing_NA = outfile_NA.replace('NA_V1','NA')
        wbt.gaussian_filter(outfile_NA, outfile_smoothing_NA ,sigma=5)
        
        outfile_smoothing_pH = outfile_pH.replace('pH_V1','pH')
        wbt.gaussian_filter(outfile_pH, outfile_smoothing_pH ,sigma=5)
        
        outfile_smoothing_S = outfile_S.replace('S_V1','S')
        wbt.gaussian_filter(outfile_S, outfile_smoothing_S ,sigma=5)
    
        outfile_smoothing_Zn = outfile_Zn.replace('Zn_V1','Zn')
        wbt.gaussian_filter(outfile_Zn, outfile_smoothing_Zn ,sigma=5)
        
        outfile_smoothing_MN = outfile_MN.replace('MN_V1','MN')
        wbt.gaussian_filter(outfile_MN, outfile_smoothing_MN ,sigma=5)
        
        outfile_smoothing_FE = outfile_CIC.replace('FE_V1','FE')
        wbt.gaussian_filter(outfile_FE, outfile_smoothing_FE ,sigma=5)
        
        outfile_smoothing_CU = outfile_CIC.replace('CU_V1','CU')
        wbt.gaussian_filter(outfile_CU, outfile_smoothing_CU ,sigma=5)
        
        outfile_smoothing_B = outfile_CIC.replace('B_V1','B')
        wbt.gaussian_filter(outfile_B, outfile_smoothing_B ,sigma=5)
        
        outfile_smoothing_CIC = outfile_CIC.replace('CIC_V1','CIC')
        wbt.gaussian_filter(outfile_CIC, outfile_smoothing_CIC ,sigma=5)
        
        outfile_smoothing_CO = outfile_CO.replace('CO_V1','CO')
        wbt.gaussian_filter(outfile_CO, outfile_smoothing_CO ,sigma=5)
        
        outfile_smoothing_ARC = outfile_ARC.replace('ARC_V1','ARC')
        wbt.gaussian_filter(outfile_ARC, outfile_smoothing_ARC ,sigma=5)
        
        """
        outfile_smoothing_ARE = outfile_ARE.replace('ARE_V1','ARE')
        wbt.gaussian_filter(outfile_ARE, outfile_smoothing_ARE ,sigma=5)
        """
        outfile_smoothing_LIM = outfile_LIM.replace('LIM_V1','LIM')
        wbt.gaussian_filter(outfile_LIM, outfile_smoothing_LIM ,sigma=5)
        
        """
        P1_del_sue, K_del_suel, MG_del_sue, CA_del_sue, NA_del_sue, pH_del_sue
        S_del_suel, ZN_del_sue, MN_del_sue, FE_del_sue, CU_del_sue, B_del_suel
        Co_del_Sue , __Arcilla_ , __Arena__ , __Limo___ 
        
        """
        os.remove(outfile_MO)
        os.remove(outfile_CIC)        
        os.remove(outfile_P)
        os.remove(outfile_K)
        os.remove(outfile_MG)
        os.remove(outfile_CA)
        os.remove(outfile_NA)
        os.remove(outfile_pH)
        os.remove(outfile_S)
        os.remove(outfile_Zn)
        os.remove(outfile_MN)
        os.remove(outfile_FE)
        os.remove(outfile_CU)
        os.remove(outfile_B)
        os.remove(outfile_CO)
        os.remove(outfile_ARC)
        #os.remove(outfile_ARE)
        #os.remove(outfile_LIM)

    except:
        print("Ocurrio un problema cuando se estaba realizando el interpolado")
    
    """
    inputs = [outfile_smoothing_CIC, outfile_smoothing_MO]
    outfile = str((os.path.join(rootFile, ('temp/outfile_soil_layers.geojson').format()))) 
    extract_point_data_from_rasters(archivo_puntos_regulares,inputs,outfile)
    """

