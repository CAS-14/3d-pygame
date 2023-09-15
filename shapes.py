import wireframe
import projection
import numpy

class Cube(wireframe.Wireframe):
    def __init__(self):
        cube_nodes = [(x ,y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)]
        cube_edges = [(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)]

        super().__init__(cube_nodes, cube_edges)

if __name__ == "__main__":
    cube = Cube()

    viewer = projection.ProjectionViewer()
    viewer.add_wireframe(cube, "cube")
    viewer.run()