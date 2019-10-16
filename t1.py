import subprocess
from osgeo import gdal, ogr, osr
import os

fbin='C:/Program Files/QGIS 2.18/bin/gdalwarp'
fout='C:/Users/soiqu/Desktop/raster_cutting/output/'
databaseServer = "localhost"
databaseName = "raster_cutting"
databaseUser = "postgres"
databasePW = "*****"
databasePort = "5433"
connString = "PG: host=%s dbname=%s user=%s password=%s port=%s" % (databaseServer,databaseName,databaseUser,databasePW,databasePort)

def GetPGLayer(lyr_name):
    conn = ogr.Open(connString)

    lyr = conn.GetLayer(lyr_name)
    if lyr is None:
        print >> sys.stderr, '[ ERROR ]: layer name = "%s" could not be found in database "%s"' % ( lyr_name, databaseName )
        sys.exit( 1 )

    featureCount = lyr.GetFeatureCount()

    print("Number of features in %s: %d" % (lyr_name,featureCount))
    #return (lyr_name,featureCount)

    #Get province code
    id_arr=[]
    for f in lyr:
        # geom = f.GetGeometryRef()        
        # print(geom.Centroid().ExportToWkt())
        val=f.GetField('ten_eng')
        # print(val)
        id_arr.append(val)

    #return (featureCount)
    return id_arr

    # Close connection
    conn = None

id_arr=GetPGLayer('dbscl')


for id in id_arr:
    cmd='"'+fbin+'" -cutline "PG:dbname=\'raster_cutting\' host=localhost port=5433 user=\'postgres\' password=\'2679191\'" -csql "select * from dbscl where ten_eng=\''+str(id)+'\'" -crop_to_cutline -of GTiff -dstnodata -9999.0 -overwrite "DBSCL_20180611_NSS.tif" "'+fout+'out_'+str(id)+'.tif"'
    # print(cmd)
    subprocess.Popen(cmd,shell=True)