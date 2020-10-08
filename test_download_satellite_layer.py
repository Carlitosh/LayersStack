# -*- coding: utf-8 -*-

import urllib.request
import geojson
import ee 
import os
import zipfile

ee.Initialize()

rootFile = "C:/Users/carli/Documents/Proyectos_Desarrollo_de_Software/prueba_raster_postgis/"
os.chdir(rootFile)

archivo_geojson = str("capas/boundary.geojson")

def maskS2clouds(image):
    
    qa = image.select('QA60')
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask).divide(10000)

def NDVI(image):
    """A function to compute NDVI."""
    return image.expression('float(b("B8") - b("B4")) / (b("B8") + b("B4"))')

def NDRE (image):
    """A function to compute NDRE."""
    return image.expression('float(b("B8") - b("B5")) / (b("B8") + b("B5"))')

def SAVI(image):
    """A function to compute Soil Adjusted Vegetation Index."""
    return ee.Image(0).expression(
        '(1 + L) * float(nir - red)/ (nir + red + L)',
        {
            'nir': image.select('B8'),
            'red': image.select('B4'),
            'L': 0.2
        })

def EVI(image):
    """A function to compute Enhanced Vegetation index."""
    return ee.Image(0).expression(
        '(2.5 * float(nir - red)/ ((nir + 6*red - 7.5* azul) + 1))',
        {
            'nir': image.select('B8'),
            'red': image.select('B4'),
            'azul': image.select('B2')
        })


def GNDVI(image):
    """A function to compute NDVI."""
    return image.expression('float(b("B8") - b("B3")) / (b("B8") + b("B3"))')



def download_NDRE(archivo_geojson, anio):
    
    fecha_inicio = '{0}-2-1'.format(str(anio))
    fecha_fin = '{0}-4-10'.format(str(anio))  
    satelite = str("COPERNICUS/S2")
    src = '32720'
    with open(archivo_geojson) as f:
        gj = geojson.load(f)
    features = gj['features'][0]
    roi = ee.Geometry.Polygon(features.geometry.coordinates)
    copernicus_image = ee.ImageCollection(satelite)
    copernicus_image = copernicus_image.filterDate(fecha_inicio,fecha_fin)
    copernicus_image = copernicus_image.filterBounds(roi)
    copernicus_image = copernicus_image.filterMetadata('CLOUD_COVERAGE_ASSESSMENT', 'less_than', 5)
    copernicus_image = copernicus_image.map(maskS2clouds)
    copernicus_image = copernicus_image.map(NDRE)
    copernicus_image = ee.Image(copernicus_image.reduce(ee.Reducer.median())).clip(roi)
    name = str('NDRE'+'_Feb_CA_'+str(anio))
    path = copernicus_image.getDownloadUrl({
        'name': name,
        'scale': 10,
        'crs': str('EPSG:'+src)
        })
    sentencia = str(path)
    file = str('temp/NDRE'+'_Feb_CA_'+str(anio)+'.zip')
    urllib.request.urlretrieve(sentencia, file)
    
    with zipfile.ZipFile(str((os.path.join(rootFile, file))),"r") as zip_ref:
        zip_ref.extractall('temp/')
        zip_ref.close()
    
    old_name = str('temp/'+name+'.B8_median.tif')
    new_name = old_name.replace('.B8_median','')
    os.rename(old_name,new_name)

    
    os.remove(file)
    urllib.request.urlcleanup()
    print("Descarga exitosa de capa NDRE")
    


def download_CHIRPS(archivo_geojson, anio):
    
    fecha_inicio = '{0}-2-1'.format(str(anio))
    fecha_fin = '{0}-4-10'.format(str(anio))
    satelite = str("UCSB-CHG/CHIRPS/DAILY")
    src = '32720'
    with open(archivo_geojson) as f:
        gj = geojson.load(f)
    features = gj['features'][0]
    roi = ee.Geometry.Polygon(features.geometry.coordinates) 
    collection = ee.ImageCollection(satelite)
    collection = collection.filterDate(fecha_inicio,fecha_fin)
    collection = collection.filterBounds(roi)
    image = ee.Image(collection.sum()).clip(roi)
    name =  name = str('CHIRPS'+'_Feb_CA_'+str(anio))
    path = image.getDownloadUrl({
        'name': name,
        'scale': 10,
        'crs': str('EPSG:'+src)
        }) 
    sentencia = str(path)
    if not os.path.exists('temp'):
        os.makedirs('temp')
    file = str('temp/CHIRPS'+'_Feb_CA_'+str(anio)+'.zip')
    urllib.request.urlretrieve(sentencia, file)
    with zipfile.ZipFile(str((os.path.join(rootFile, file))),"r") as zip_ref:
        zip_ref.extractall('temp/')

    old_name = str('temp/'+name+'.precipitation.tif')
    new_name = old_name.replace('.precipitation','')
    os.rename(old_name,new_name)
    os.remove(file)
    urllib.request.urlcleanup()
    print("Descarga exitosa de capa CHIRPS")


def download_SMAP(archivo_geojson, anio):
    
    fecha_inicio = '{0}-2-1'.format(str(anio))
    fecha_fin = '{0}-4-10'.format(str(anio))
    satelite = str("NASA_USDA/HSL/SMAP_soil_moisture")
    src = '32720'
    with open(archivo_geojson) as f:
        gj = geojson.load(f)
    features = gj['features'][0]
    roi = ee.Geometry.Polygon(features.geometry.coordinates) 
    collection = ee.ImageCollection(satelite).select('ssm')
    collection = collection.filterDate(fecha_inicio,fecha_fin)
    collection = collection.filterBounds(roi)
    image = ee.Image(collection.sum()).clip(roi)
    name = name = str('SMAP'+'_Feb_CA_'+str(anio))
    path = image.getDownloadUrl({
        'name': name,
        'scale': 10,
        'crs': str('EPSG:'+src)
        }) 
    sentencia = str(path)
    if not os.path.exists('temp'):
        os.makedirs('temp')
    file = str('temp/SMAP'+'_Feb_CA_'+str(anio)+'.zip')
    urllib.request.urlretrieve(sentencia, file)
    with zipfile.ZipFile(str((os.path.join(rootFile, file))),"r") as zip_ref:
        zip_ref.extractall('temp/')
    old_name = str('temp/'+name+'.ssm.tif')
    new_name = old_name.replace('.ssm','')
    os.rename(old_name,new_name)
    os.remove(file)
    
    urllib.request.urlcleanup()
    print("Descarga exitosa de capa SMAP")

def download_SAVI(archivo_geojson, anio):
    
    fecha_inicio = '{0}-2-1'.format(str(anio))
    fecha_fin = '{0}-4-10'.format(str(anio))  
    satelite = str("COPERNICUS/S2")
    src = '32720'
    with open(archivo_geojson) as f:
        gj = geojson.load(f)
    features = gj['features'][0]
    roi = ee.Geometry.Polygon(features.geometry.coordinates)
    copernicus_image = ee.ImageCollection(satelite)
    copernicus_image = copernicus_image.filterDate(fecha_inicio,fecha_fin)
    copernicus_image = copernicus_image.filterBounds(roi)
    copernicus_image = copernicus_image.filterMetadata('CLOUD_COVERAGE_ASSESSMENT', 'less_than', 5)
    copernicus_image = copernicus_image.map(maskS2clouds)
    copernicus_image = copernicus_image.map(SAVI)
    copernicus_image = ee.Image(copernicus_image.reduce(ee.Reducer.median())).clip(roi)
    name = str('SAVI'+'_Feb_CA_'+str(anio))
    path = copernicus_image.getDownloadUrl({
        'name': name,
        'scale': 10,
        'crs': str('EPSG:'+src)}) 
    sentencia = str(path)
    if not os.path.exists('temp'):
        os.makedirs('temp')
    file = str('temp/SAVI'+'_Feb_CA_'+str(anio)+'.zip')
    urllib.request.urlretrieve(sentencia, file)
    with zipfile.ZipFile(str((os.path.join(rootFile, file))),"r") as zip_ref:
        zip_ref.extractall('temp/')
        
    old_name = str('temp/'+name+'.constant_median.tif')
    new_name = old_name.replace('.constant_median','')
    os.rename(old_name,new_name)  
    os.remove(file)
    urllib.request.urlcleanup()
    print("Descarga exitosa de capa SAVI")

def download_EVI(archivo_geojson, anio):
    
    fecha_inicio = '{0}-2-1'.format(str(anio))
    fecha_fin = '{0}-4-10'.format(str(anio))  
    satelite = str("COPERNICUS/S2")
    src = '32720'
    with open(archivo_geojson) as f:
        gj = geojson.load(f)
    features = gj['features'][0]
    roi = ee.Geometry.Polygon(features.geometry.coordinates)
    copernicus_image = ee.ImageCollection(satelite)
    copernicus_image = copernicus_image.filterDate(fecha_inicio,fecha_fin)
    copernicus_image = copernicus_image.filterBounds(roi)
    copernicus_image = copernicus_image.filterMetadata('CLOUD_COVERAGE_ASSESSMENT', 'less_than', 5)
    copernicus_image = copernicus_image.map(maskS2clouds)
    copernicus_image = copernicus_image.map(EVI)
    copernicus_image = ee.Image(copernicus_image.reduce(ee.Reducer.median())).clip(roi)
    name = str('EVI'+'_Feb_CA_'+str(anio))
    path = copernicus_image.getDownloadUrl({
        'name': name,
        'scale': 10,
        'crs': str('EPSG:'+src)
        })
    sentencia = str(path)
    if not os.path.exists('temp'):
        os.makedirs('temp')
    file = str('temp/EVI'+'_Feb_CA_'+str(anio)+'.zip')
    urllib.request.urlretrieve(sentencia, file)
    with zipfile.ZipFile(str((os.path.join(rootFile, file))),"r") as zip_ref:
        zip_ref.extractall('temp/')
        
    old_name = str('temp/'+name+'.constant_median.tif')
    new_name = old_name.replace('.constant_median','')
    os.rename(old_name,new_name)    
    os.remove(file)
    urllib.request.urlcleanup()
    print("Descarga exitosa de capa EVI")

def download_NDVI(archivo_geojson, anio):
    
    fecha_inicio = '{0}-2-1'.format(str(anio))
    fecha_fin = '{0}-4-10'.format(str(anio))  
    satelite = str("COPERNICUS/S2")
    src = '32720'
    with open(archivo_geojson) as f:
        gj = geojson.load(f)
    features = gj['features'][0]
    roi = ee.Geometry.Polygon(features.geometry.coordinates)  
    copernicus_image = ee.ImageCollection(satelite)
    copernicus_image = copernicus_image.filterDate(fecha_inicio,fecha_fin)
    copernicus_image = copernicus_image.filterBounds(roi)
    copernicus_image = copernicus_image.filterMetadata('CLOUD_COVERAGE_ASSESSMENT', 'less_than', 5)
    copernicus_image = copernicus_image.map(maskS2clouds)
    copernicus_image = copernicus_image.map(NDVI)
    copernicus_image = ee.Image(copernicus_image.reduce(ee.Reducer.median())).clip(roi)    
    name = str('NDVI'+'_Feb_CA_'+str(anio))
    path = copernicus_image.getDownloadUrl({
        'name': name,
        'scale': 10,
        'crs': str('EPSG:'+src)
        })
    sentencia = str(path)
    if not os.path.exists('temp'):
        os.makedirs('temp')
    file = str('temp/NDVI'+'_Feb_CA_'+str(anio)+'.zip')
    urllib.request.urlretrieve(sentencia, file)
    with zipfile.ZipFile(str((os.path.join(rootFile, file))),"r") as zip_ref:
        zip_ref.extractall('temp/')
    
    old_name = str('temp/'+name+'.B8_median.tif')
    new_name = old_name.replace('.B8_median','')
    os.rename(old_name,new_name)
    os.remove(file)
    urllib.request.urlcleanup()
    print("Descarga exitosa de capa NDVI")

def download_GNDVI(archivo_geojson, anio):
    
    fecha_inicio = '{0}-2-1'.format(str(anio))
    fecha_fin = '{0}-4-10'.format(str(anio))  
    satelite = str("COPERNICUS/S2")
    src = '32720'
    with open(archivo_geojson) as f:
        gj = geojson.load(f)
    features = gj['features'][0]    
    roi = ee.Geometry.Polygon(features.geometry.coordinates)    
    copernicus_image = ee.ImageCollection(satelite)
    copernicus_image = copernicus_image.filterDate(fecha_inicio,fecha_fin)
    copernicus_image = copernicus_image.filterBounds(roi)
    copernicus_image = copernicus_image.filterMetadata('CLOUD_COVERAGE_ASSESSMENT', 'less_than', 5)
    copernicus_image = copernicus_image.map(maskS2clouds)
    copernicus_image = copernicus_image.map(GNDVI)
    copernicus_image = ee.Image(copernicus_image.reduce(ee.Reducer.median())).clip(roi)
    name = str('GNDVI'+'_Feb_CA_'+str(anio))
    path = copernicus_image.getDownloadUrl({
        'name': name,
        'scale': 10,
        'crs': str('EPSG:'+src)
        })
    sentencia = str(path)
    if not os.path.exists('temp'):
        os.makedirs('temp')
    file = str('temp/GNDVI'+'_Feb_CA_'+str(anio)+'.zip')
    urllib.request.urlretrieve(sentencia, file)
    with zipfile.ZipFile(str((os.path.join(rootFile, file))),"r") as zip_ref:
        zip_ref.extractall('temp/')
    old_name = str('temp/'+name+'.B8_median.tif')
    new_name = old_name.replace('.B8_median','')
    os.rename(old_name,new_name)
    os.remove(file)
    urllib.request.urlcleanup()
    print("Descarga exitosa de capa GNDVI")