# raster_cutting
Cut raster for each features in a vector layer

## SQlite version (Easier to config)
> t1_sqlite.py

**Config**

```python
fbin='C:/Program Files/QGIS 2.18/bin/gdalwarp'
rasterFile='C:/Users/soiqu/Desktop/raster_cutting/input/DBSCL_20180611_NSS.tif'
fout='C:/Users/soiqu/Desktop/raster_cutting/output/'
dbName='dbscl.sqlite'
#Vector table (layer) name
tblName='dbscl'
#Column name which used as condition to define each feature (ex. each province in dbscl layer)
dkCol='ten_eng'
```


## PostgreSQL version



# Config
* Python with GDAL installed
* Path to `bin folder` of QGIS. Ex `C:/Program Files/QGIS 2.18/bin/gdalwarp`
* Path to `output folder`

## Preferences

> gdalwarp
`"C:/Program Files/QGIS 2.18/bin/gdalwarp" -cutline dbscl.sqlite -csql "select * from dbscl where ten_eng='Tra Vinh'" -crop_to_cutline -of GTiff -dstnodata -9999.0 -overwrite "DBSCL_20180611_NSS.tif" "C:/Users/soiqu/Desktop/raster_cutting/output/out_Tra Vinh.tif"`

> Subprocess
http://queirozf.com/entries/python-3-subprocess-examples

