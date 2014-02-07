import dxfgrabber
from dxfwrite import DXFEngine

class DXFReader():
    def __init__(self, filename):
        self.dxf = dxfgrabber.readfile(filename)
    def entities(self):
        for entity in self.dxf.entities:
            yield entity
    def lwpolylines(self):
        for e in self.entities():
            if type(e) is dxfgrabber.entities.LWPolyline:
                yield e

import unittest

class TestDXFReader(unittest.TestCase):
    def test_sample_file(self):
        dxf = DXFReader("sample_export_from_ocad2.dxf")
        for e in dxf.lwpolylines():
            self.assertTrue(type(e) is dxfgrabber.entities.LWPolyline)

if __name__ == "__main__":
    unittest.main()

filename = "sample_export_from_ocad2.dxf"
#dxf = dxfgrabber.readfile(filename)
#print len(dxf.header)
#layer_count = len(dxf.layers) # collection of layer definitions
#block_definition_count = len(dxf.blocks) #  dict like collection of block definitions
#entity_count = len(dxf.entities) # list like collection of entities

#print layer_count, block_definition_count, entitiy_count
#drawing = DXFEngine.drawing('test.dxf')

#for entity in dxf.entities:
#    points = []
#    for point in entity.points:
#        points.append((point[0], point[1], 0))
#    drawing.add(DXFEngine.polyline(points))
#
#drawing.save()