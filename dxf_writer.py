from dxfwrite import DXFEngine

def WriteDXF(filename, lines, elevations):
    drawing = DXFEngine.drawing(filename)
    for idx in xrange(len( lines )):
        points = []
        for point in lines[idx]:
            points.append((point[0], point[1]))
        drawing.add(DXFEngine.polyline(points, polyline_elevation = (0,0,elevations[idx])))
    drawing.save()

#dxf = dxfgrabber.readfile(filename)
#print len(dxf.header)
#layer_count = len(dxf.layers) # collection of layer definitions
#block_definition_count = len(dxf.blocks) #  dict like collection of block definitions
#entity_count = len(dxf.entities) # list like collection of entities

#print layer_count, block_definition_count, entitiy_count
