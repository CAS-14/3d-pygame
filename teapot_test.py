import wireframe
import projection
import shapes

def initial(viewer: projection.ProjectionViewer):
    viewer.translate_all([400, 298, 0])
    viewer.scale_all(85)
    viewer.rotate_all("x", -3)

viewer = projection.ProjectionViewer()
viewer.add_wireframe(wireframe.load_obj("teapot.obj"), "teapot", scale=85)
viewer.show_nodes = False




viewer.run()
