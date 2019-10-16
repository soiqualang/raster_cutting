import subprocess
from osgeo import gdal, ogr, osr
import os

fbin='C:/Program Files/QGIS 2.18/bin/gdalwarp'
fout='C:/Users/soiqu/Desktop/raster_cutting/output/'
dbName='dbscl.sqlite'
tblName='dbscl'
dkCol='ten_eng'

def GetSQLiteLayer(lyr_name):
    conn = ogr.Open(dbName)
	# for i in range(conn.GetLayerCount()):
		# print(conn.GetLayerByIndex(i).GetName())

    lyr = conn.GetLayer(lyr_name)
    if lyr is None:
        print >> sys.stderr, '[ ERROR ]: layer name = "%s" could not be found in database "%s"' % ( lyr_name, dbName )
        sys.exit( 1 )

    featureCount = lyr.GetFeatureCount()

    print("Number of features in %s: %d" % (lyr_name,featureCount))
    #return (lyr_name,featureCount)

    #Get province code
    code_arr=[]
    for f in lyr:
        # geom = f.GetGeometryRef()        
        # print(geom.Centroid().ExportToWkt())
        val=f.GetField(dkCol)
        code_arr.append(val)
    return code_arr
    conn = None

code_arr=GetSQLiteLayer(tblName)


for code in code_arr:
    cmd='"'+fbin+'" -cutline "'+dbName+'" -csql "select * from '+tblName+' where "'+dkCol+'"=\''+str(code)+'\'" -crop_to_cutline -of GTiff -dstnodata -9999.0 -overwrite "input/DBSCL_20180611_NSS.tif" "'+fout+'out_'+str(code)+'.tif"'
    # print(cmd)
    subprocess.Popen(cmd,shell=True)