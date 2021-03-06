
'''
python script designed to find all the level 10 AusPIX cells for bushfire polygon areas
once complete, these cells are attributed with SA1, LGA, DEM, CAPAD, etc
Joseph Bell Geoscience Australia Jan 2020
'''

import shapefile  #to read and write shapefiles
import auspixdggs.callablemodules.dggs_in_poly  # this is script written by GA - see GitHub AusPix DGGS enablement folder
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS() # make an instance

# identify path to a shape file to get your polygons from
myFile = r'xxxxxBurnAreas10thJan.shp'

#myFile = r'C:xxxxxFires\Burnt\Boundaries15-01-2020\Test_one02shp.shp'

r = shapefile.Reader(myFile) # read in the file
# get the attribute table records (combined with shapes) ie shapeRecords
shapeRecs = r.shapeRecords()
resolution = 10 # set resolution to be used
resArea = (rdggs.cell_area(resolution, plane=False))/10000
#print('Area in ha', resArea)

#set up shapefile for output
#w = shapefile.Writer(shapefile.POINT)  # in this case points == centroids of cells   #old version of shapefile
thisShapeFile = r'C:\temp\BurntAreasDGGS'  # don't add .shp

w= shapefile.Writer(thisShapeFile)
w.field('DGGSrHEALPix', 'C', '20')
w.field('uri', 'C', '150')  #using 'C' = character = ensures the correct number
w.field('DGGS_ha', 'C', '20')
w.field('Status', 'C', '20')

n=0

# now go line by line through the attribute table of the source shapefile
for row in shapeRecs:

        n+= 1
        print('doing', n, 'of' len(shapeRecs')
        polyShape = row.shape  # get the spatial component
        polyRecord = row.record  # get the attributes record (row)
        # call the "poly_to_DGGS_tool" function to return all the DGGS cells (within each polygon) includes long & lat
        cells_in_poly = dggs_in_poly.poly_to_DGGS_tool(polyShape, resolution)
        # cells_in_poly == list of [DGGSid , longitude of centroid, latitude of centroid]

        #go through the cells one by one - build them into the new attribute table
        #make a shapefile of the DGGS centroids
        for dggs_cell in cells_in_poly:
            uri = 'http://ec2-52-63-73-113.ap-southeast-2.compute.amazonaws.com/AusPIX-DGGS-dataset/ausPIX/' + dggs_cell[0]
            #print(dggs_cell[1], dggs_cell[2])
            longitude = dggs_cell[1]
            latitude = dggs_cell[2]
            w.point(longitude, latitude)# insert the spatial x y into the shapefile
            w.record(DGGSrHEALPix=dggs_cell[0], uri=uri, DGGS_ha = resArea, Status = 'burnt')


w.autoBalance = 1
print('saving to file . . . ')

#w.save(thisShapeFile)
# a simple method of writing a single projection so it can be opened in spatial software
prj = open("%s.prj" % thisShapeFile, "w")
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
prj.close()
