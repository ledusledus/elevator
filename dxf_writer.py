from dxfwrite import DXFEngine

def writeDXF(filename, lines_w_elevation):
    drawing = DXFEngine.drawing('test.dxf')
    for entity in lines_w_elevation:
        points = []
        for point in lines_w_elevation.points:
            points.append((point[0], point[1], lines_w_elevation.elevation))
        drawing.add(DXFEngine.polyline(points))
    drawing.save()

#dxf = dxfgrabber.readfile(filename)
#print len(dxf.header)
#layer_count = len(dxf.layers) # collection of layer definitions
#block_definition_count = len(dxf.blocks) #  dict like collection of block definitions
#entity_count = len(dxf.entities) # list like collection of entities

#print layer_count, block_definition_count, entitiy_count
