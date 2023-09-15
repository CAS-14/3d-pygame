import numpy

AXES = ["x", "y", "z"]

def translation_matrix(dx: int = 0, dy: int = 0, dz: int = 0):
    return numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]
    ])

def scale_matrix(sx: int = 0, sy: int = 0, sz: int = 0):
    return numpy.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def rotate_matrix(axis: str, radians: int):
    c = numpy.cos(radians)
    s = numpy.sin(radians)

    if axis == "x":
        matrix = numpy.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])
    
    elif axis == "y":
        matrix = numpy.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])
    
    elif axis == "z":
        matrix = numpy.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    return matrix

class Wireframe:
    def __init__(self, nodes: list = None, edges: list = None):
        self.nodes = numpy.zeros((0, 4))
        self.edges = []

        if nodes: self.add_nodes(nodes)
        if edges: self.add_edges(edges)

    def add_nodes(self, nodes: list):
        ones_column = numpy.ones((len(nodes), 1))
        ones_added = numpy.hstack((nodes, ones_column))
        self.nodes = numpy.vstack((self.nodes, ones_added))

    def add_edges(self, edges: list):
        self.edges += edges

    def get_nodes(self):
        print("\nALL nodes:")
        for i, (x, y, z) in enumerate(self.nodes):
            print(f"{i}. ({x}, {y}, {z})")
        print()

    def get_edges(self):
        print("\nALL edges:")
        for i, (node1, node2) in enumerate(self.edges):
            print(f"{i}. {node1} -> {node2}")
        print()

    def translate(self, axis: str, distance: int):
        if axis in AXES:
            for node in self.nodes:
                node[AXES.index(axis)] = node[AXES.index(axis)] + distance

    def scale(self, scale: int, point: tuple = (0, 0)):
        point_x, point_y = point

        for node in self.nodes:
            node[0] = point_x + scale * (node[0] - point_x)
            node[1] = point_y + scale * (node[1] - point_y)
            node[2] *= scale

    def get_center(self):
        node_count = len(self.nodes)
        mean_x = sum([node[0] for node in self.nodes]) / node_count
        mean_y = sum([node[1] for node in self.nodes]) / node_count
        mean_z = sum([node[2] for node in self.nodes]) / node_count
        
        return mean_x, mean_y, mean_z

    def rotate_x(self, point: tuple, radians: int):
        cx, cy, cz = point

        for node in self.nodes:
            y = node[1] - cy
            z = node[2] - cz
            d = numpy.hypot(y, z)
            theta = numpy.arctan2(y, z) + radians
            node[2] = cz + d * numpy.cos(theta)
            node[1] = cy + d * numpy.sin(theta)

    def rotate_y(self, point: tuple, radians: int):
        cx, cy, cz = point

        for node in self.nodes:
            x = node[0] - cx
            z = node[2] - cz
            d = numpy.hypot(x, z)
            theta = numpy.arctan2(x, z) + radians
            node[2] = cz + d * numpy.cos(theta)
            node[0] = cx + d * numpy.sin(theta)

    def rotate_z(self, point: tuple, radians: int):
        cx, cy, cz = point

        for node in self.nodes:
            x = node[0] - cx
            y = node[1] - cy
            d = numpy.hypot(y, x)
            theta = numpy.arctan2(y, x) + radians
            node[0] = cx + d * numpy.cos(theta)
            node[1] = cy + d * numpy.sin(theta)

    def rotate(self, axis: str, point: tuple, radians: int):
        if axis not in AXES:
            return None

        use_pair = None
        for pair in [["y", "z"], ["x", "z"], ["x", "y"]]:
            if axis not in pair:
                use_pair = pair
                print(f"PAIR! {use_pair}")
                break

        dir1, dir2 = use_pair
        for node in self.nodes:
            p1 = getattr(node, dir1) - point[AXES.index(dir1)]
            p2 = getattr(node, dir2) - point[AXES.index(dir2)]
            d = numpy.hypot(p1, p2)
            theta = numpy.arctan2(p1, p2) + radians
            setattr(node, dir1, (point[AXES.index(dir1)] + d * numpy.cos(theta)))
            setattr(node, dir2, (point[AXES.index(dir2)] + d * numpy.sin(theta)))

    def transform(self, matrix: numpy.matrix):
        self.nodes = numpy.dot(self.nodes, matrix)

def load_obj(path: str):
    with open(path, "r") as f:
        obj = f.read()
    
    wireframe = Wireframe()

    last_v = False
    start = True
    balls = True
    nodes = []
    edges = []

    for line in obj.splitlines():
        command = line.strip().split()

        if not command:
            continue

        if command[0] == "v":
            if not last_v:
                if start:
                    start = False
                else:
                    wireframe.add_edges(edges)
                    edges.clear()

            coords = tuple([float(arg) for arg in command[1:4]])
            print(f"Coords: {coords}")
            nodes.append(coords)
            last_v = True

        elif command[0] == "f":
            if last_v:
                wireframe.add_nodes(numpy.array(nodes))
                nodes.clear()
                last_v = False

            face_node_indices = tuple([int(arg) for arg in command[1:]])

            pairs_done = []
            skip = False
            for i in face_node_indices:
                ii = i-1
                for j in face_node_indices:
                    ji = j-1
                    for pair in pairs_done:
                        if ii in pair and ji in pair:
                            skip = True

                    if skip:
                        skip = False
                        continue

                    edge = [ii, ji]
                    
                    if ii < len(wireframe.nodes):
                        if ji < len(wireframe.nodes):
                            edges.append(edge)
                            pairs_done.append(edge)
                            if balls:
                                print(edge)

                        else:
                            print(f"Skipped invalid edge ({ii}, {ji}) [invalid indice {ji}]")

                    else:
                        print(f"Skipped invalid edge ({ii}, {ji}) [invalid indice {ii}]")

            if balls:
                balls = False
                    

    return wireframe
