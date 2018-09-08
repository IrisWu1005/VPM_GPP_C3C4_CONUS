#-------------------------------------------------------------------------------
# Name:        aggregate_cdl2modis-M1.py
# Purpose:
#
# Author:      eomf
#
# Created:     10/05/2014
# Copyright:   (c) eomf 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import multiprocessing              #############adding in
import numpy
import pyproj
from osgeo import gdal
from osgeo.gdalconst import *
import time
startTime=time.time()
import os, sys
##try:
##    inFilename=sys.argv[1]
##except:
##    print "please specify the file!"
##    sys.exit(2)

#inPath="/data/eomf/users/jcui/VPM/nass-cdl/2013_30m_cdls/"

#fileList=['h08v04_cdl_sb.img','h08v05_cdl_sb.img','h08v06_cdl_sb.img','h09v04_cdl_sb.img','h09v05_cdl_sb.img','h09v06_cdl_sb.img','h10v04_cdl_sb.img','h10v05_cdl_sb.img','h10v06_cdl_sb.img','h11v04_cdl_sb.img','h11v05_cdl_sb.img','h12v04_cdl_sb.img','h12v05_cdl_sb.img','h13v04_cdl_sb.img']
#inFilename="h10v05_cdl_cultivated.img"
#fileList=['h12v04_cdl_sb.img','h12v05_cdl_sb.img','h13v04_cdl_sb.img']
def aggregate_cdl(fileList):
#fileList=['h09v06_cdl_C4.img','h10v04_cdl_C4.img']


  #  for inFilename in fileList:
    inPath=os.getcwd()+"/"
    inDs = gdal.Open(inPath+fileList)

    if inDs is None:
        print 'Could not open ' +inPath+fileList
        sys.exit(1)


    rows = inDs.RasterYSize
    cols = inDs.RasterXSize

    print 'reading image..'
    cropData=inDs.ReadAsArray()


    sP=pyproj.Proj("+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs")
    tP=pyproj.Proj("+proj=sinu +R=6371007.181 +nadgrids=@null +wktext")
    # open the cdl, find the extend, remember that we want the coordinates for the centrod points
    # h10v04
    ##xAlb=numpy.arange(-2044665+15, 390915,30)
    ##yAlb=numpy.arange(3172605-15,1885515,-30).reshape(rows,1)
    ##
    ##xSin_orig=-8895604.157333
    ##ySin_orig=4447802.078667
    #h10v05
    #[0-modis product name, 1-modis left, 2-right, 3-top, 4-down, cdl 5-left, 6-right, 7-top, 8-down]



    tileList=[
    ['MOD09A1.A2013001.h08v04.005.2013017012727.evi.tif',-11119505.196667,-10007554.677,5559752.598333,4447802.078667,-2356095,-1802805,3172605,2091645],
    ['MOD09A1.A2013001.h08v05.005.2013017012926.evi.tif',-11119505.196667,-10007554.677,4447802.078667, 3335851.559,-2356095,-762765,2412345,801195],
    ['MOD09A1.A2013001.h08v06.005.2013017012344.evi.tif',-11119505.196667,-10007554.677,3335851.559,2223901.039333,-1863495,-359235,960945,276915],
    ['MOD09A1.A2013001.h09v04.005.2013017012721.evi.tif',-10007554.677,-8895604.157333,5559752.598333,4447802.078667,-2356095,-712665,3172605,1918605],
    ['MOD09A1.A2013001.h09v05.005.2013017014034.evi.tif',-10007554.677,-8895604.157333,4447802.078667,3335851.559,-1802835,349995,2091675,766755],
    ['MOD09A1.A2013001.h09v06.005.2013017012828.evi.tif',-10007554.677,-8895604.157333,3335851.559,2223901.039333,-762765,781845,801195,276915],
    ['MOD09A1.A2013001.h10v04.005.2013017013906.evi.tif',-8895604.157333,-7783653.637667,5559752.598333,4447802.078667,-2044665,390915,3172605,1885515],
    ['MOD09A1.A2013001.h10v05.005.2013017013653.evi.tif',-8895604.157333,-7783653.637667,4447802.078667,3335851.559001,-712665,1456005,1918635,776055],
    ['MOD09A1.A2013001.h10v06.005.2013017014029.evi.tif',-8895604.157333,-7783653.637667,3335851.559,2223901.039334,341115,2023725,888975,276915],
    ['MOD09A1.A2013001.h11v04.005.2013017013530.evi.tif',-7783653.637667,-6671703.118,5559752.598333,4447802.078667,-938025,1487115,3061605,1896495],
    ['MOD09A1.A2013001.h11v05.005.2013017014607.evi.tif',-7783653.637667,-6671703.118,4447802.078667,3335851.559,390915,2258235,2025705,885855],
    ['MOD09A1.A2013001.h12v04.005.2013017012856.evi.tif',-6671703.118,-5559752.59833,5559752.598333,4447802.078667,193725,2258235,3000525,2025675],
    ['MOD09A1.A2013001.h12v05.005.2013017012801.evi.tif',-6671703.118,-5559752.59833,4447802.078667,3335851.559,1487115,2258205,2303775,1129005],
    ['MOD09A1.A2013001.h13v04.005.2013017013739.evi.tif',-5559752.598333,-4447802.078667,5559752.598333,4447802.078667,1299915,2258235,3172605,2488095]
    ]


    for tile in tileList:

        if fileList[0:6] in tile[0]:
            record=tile
            print record



    xAlb=numpy.arange(record[5]+15, record[6],30)
    yAlb=numpy.arange(record[7]-15,record[8],-30)#.reshape(rows,1)

    xSin_orig=record[1]
    ySin_orig=record[4]

    Mask=numpy.zeros((2400,2400),dtype='int8')

    MODIS=numpy.zeros((2400,2400),dtype='int32')

    # remeber the cooridnates of original point returned by gdalinfo is the upper left point, however
    # the xSin_orig and ySin_orig is the coordinates of the lower left point
    # check the lower left point's coordinate using the arcgis


    print "start to aggregate"+fileList
    for i in range(rows):
        temp=numpy.ones((cols,),dtype='int32')*yAlb[i]
        xAlb1=xAlb.tolist()
        temp1=temp.tolist()
        xSin1,ySin1=pyproj.transform(sP,tP,xAlb1,temp1)
        xSin=numpy.asarray(xSin1)
        ySin=numpy.asarray(ySin1)

        xSin=(xSin-xSin_orig)//463.3127165 # column number
        xSin=xSin.astype(int)
        xSin=xSin.reshape(cols,1)

        ySin=2399-(ySin-ySin_orig)//463.3127165  # row nunmber
        ySin=ySin.astype(int)
        ySin=ySin.reshape(cols,1)

        crop=cropData[i,:].reshape(cols,1)

        rowcolcrop=numpy.hstack((ySin,xSin,crop))

        ySin=None
        xSin=None
        crop=None

        for (row,col,crop) in rowcolcrop:
            if(0<= row <= 2399) and (0<= col <= 2399):
                MODIS[row,col]+=10000
                if crop==1:
                    MODIS[row,col]+=1
                if crop==99:
                    Mask[row,col]=1
        if (i%100==0):
            print"processing", i//100*100, 'rows'

    cropData=None

    MODIS=numpy.where((MODIS==0)|(Mask==1),32767,(MODIS%10000)*1000/(MODIS//10000))
    print "aggregating is done"


    print"saving file..."
    inMODIS = gdal.Open(record[0])
    geoTran=inMODIS.GetGeoTransform()
    geoProj=inMODIS.GetProjection()


    dr=gdal.GetDriverByName("HFA")
    dr.Register()

    outFilename=fileList.split('.')[0]

    do=dr.Create(outFilename+'_Perc.img',2400,2400,1,gdal.GDT_Int16)


    do.SetGeoTransform(geoTran)
    do.SetProjection(geoProj)


    do.GetRasterBand(1).WriteArray(MODIS)
    do.GetRasterBand(1).FlushCache()

    Mask=None
    MODIS=None
    endTime=time.time()
    print"Processing is finished. It took", (endTime-startTime)/3600., "hours"
def process_list(fileList=None,mp=True,count=1):
    if mp:
        pool=multiprocessing.Pool(processes=count)
        pool.map(aggregate_cdl,fileList)

fileList=['h08v04_cdl_C4.img','h08v05_cdl_C4.img','h08v06_cdl_C4.img','h09v04_cdl_C4.img','h09v05_cdl_C4.img','h09v06_cdl_C4.img','h10v04_cdl_C4.img','h10v05_cdl_C4.img','h10v06_cdl_C4.img','h11v04_cdl_C4.img','h11v05_cdl_C4.img','h12v04_cdl_C4.img','h12v05_cdl_C4.img','h13v04_cdl_C4.img']
process_list(fileList=fileList,mp=True,count=5)
