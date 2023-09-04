import wireframe
import numpy

cube = wireframe.Wireframe()
cube_nodes = [(x ,y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)]
cube.add_nodes(numpy.array(cube_nodes))
cube.add_edges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
