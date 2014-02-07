from osgeo import gdal
import unittest

def GetTiffSize(filename):
    """
    returns sixtet of (width, height, minx, miny, maxx, maxy)
    from stackoverflow, somewhere
    """
    ds = gdal.Open(filename)
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5] 
    maxx = gt[0] + width*gt[1] + height*gt[2]
    maxy = gt[3]
    return (width, height, minx, miny, maxx, maxy)

class TestTiffSize(unittest.TestCase):
    def test_back_tiff(self):
        self.assertEqual((7390, 3832, 399539.4683832784, 6334007.500456138, 406929.4683832784, 6337839.500456138), GetTiffSize("back.tif") )

if __name__ == "__main__":
    unittest.main()