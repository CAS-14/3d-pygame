import wireframe
import projection
import shapes

viewer = projection.ProjectionViewer()
viewer.add_wireframe(wireframe.load_obj("teapot.obj"), "teapot")
viewer.run()
