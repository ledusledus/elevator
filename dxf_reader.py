import dxfgrabber

class PolylinePoints:
    def __init__(self, entity):
        self.e = entity
    def points(self):
        for p in self.e.points():
            yield p
class LWPolylinePoints:
    def __init__(self, entity):
        self.e = entity
    def points(self):
        for p in self.e.points:
            yield p

class DXFReader():
    def __init__(self, filename):
        print "reading", filename
        self.dxf = dxfgrabber.readfile(filename)
        print "reading done"
    def entities(self):
        for entity in self.dxf.entities:
            yield entity
    def lines(self):
        for e in self.entities():
            if type(e) is dxfgrabber.entities.Polyline:
                yield PolylinePoints(e)
            elif type(e) is dxfgrabber.entities.LWPolyline:
                yield LWPolylinePoints(e)

import unittest

# currently pretty much empty unittest
class TestDXFReader(unittest.TestCase):
    def test_sample_file(self):
        #dxf = DXFReader("sample_export_from_ocad2.dxf")
        dxf = DXFReader("a.dxf")
        for e in dxf.lines():
            pass
            #print type(e)
            #self.assertTrue(type(e) is dxfgrabber.entities.LWPolyline or type(e) is dxfgrabber.entities.Polyline)

if __name__ == "__main__":
    unittest.main()

