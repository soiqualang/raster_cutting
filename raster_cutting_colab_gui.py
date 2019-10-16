import os
import subprocess
from osgeo import gdal, ogr, osr
import shutil

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

def raster_cutting():
    make_empty_folder(fout)
    code_arr=GetSQLiteLayer(tblName)
    for code in code_arr:
        cmd='"gdalwarp" -cutline "'+dbName+'" -csql "select * from '+tblName+' where "'+dkCol+'"=\''+str(code)+'\'" -crop_to_cutline -of GTiff -dstnodata -9999.0 -overwrite "'+rasterFile+'" "'+fout+'t1_'+str(code)+'.tif"'
        # print(cmd)
        subprocess.Popen(cmd,shell=True)

def make_empty_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        shutil.rmtree(folder_name,ignore_errors=True)
        os.makedirs(folder_name)

def delete_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name,ignore_errors=True)
    else:
        print('Thư mục không tồn tại!')

def make_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        print('Thư mục đã tồn tại!')

def zip_folder(folder_name):
    finalchar=folder_name[len(folder_name)-1]
    if(finalchar=='/'):
        output_filename=folder_name[:-1]
    else:
        output_filename=folder_name
    shutil.make_archive(output_filename, 'zip', folder_name)
