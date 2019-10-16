import subprocess
from osgeo import gdal, ogr, osr
import os

fbin='C:/Program Files/QGIS 2.18/bin/gdalwarp'
rasterFile='C:/Users/soiqu/Desktop/raster_cutting/input/DBSCL_20180611_NSS.tif'
fout='C:/Users/soiqu/Desktop/raster_cutting/output/'
databaseServer = "localhost"
databaseName = "raster_cutting"
databaseUser = "postgres"
#Your password to login PostgreSQL
databasePW = "******"
#Your PostgreSQL port (defaul is 5432)
databasePort = "5433"
connString = "PG: host=%s dbname=%s user=%s password=%s port=%s" % (databaseServer,databaseName,databaseUser,databasePW,databasePort)
#Vector table (layer) name
tblName='dbscl'
#Column name which used as condition to define each feature (ex. each province in dbscl layer)
dkCol='ten_eng'

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
        val=f.GetField(dkCol)
        # print(val)
        id_arr.append(val)

    #return (featureCount)
    return id_arr

    # Close connection
    conn = None

id_arr=GetPGLayer(tblName)


for id in id_arr:
    cmd='"'+fbin+'" -cutline "PG:dbname=\''+databaseName+'\' host='+databaseServer+' port='+databasePort+' user=\''+databaseUser+'\' password=\''+databasePW+'\'" -csql "select * from '+tblName+' where "'+dkCol+'"=\''+str(id)+'\'" -crop_to_cutline -of GTiff -dstnodata -9999.0 -overwrite "'+rasterFile+'" "'+fout+'t1_'+str(id)+'.tif"'
    # print(cmd)
    subprocess.Popen(cmd,shell=True)