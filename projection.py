import pygame
import numpy

import wireframe

KEYS = {
    pygame.K_LEFT:   (lambda x: x.translate_all([-10, 0, 0])),
    pygame.K_RIGHT:  (lambda x: x.translate_all([10, 0, 0])),
    pygame.K_DOWN:   (lambda x: x.translate_all([0, 10, 0])),
    pygame.K_UP:     (lambda x: x.translate_all([0, -10, 0])),
    pygame.K_EQUALS: (lambda x: x.scale_all(1.25)),
    pygame.K_MINUS:  (lambda x: x.scale_all( 0.8)),
    pygame.K_q: (lambda x: x.rotate_all("x",  0.1)),
    pygame.K_w: (lambda x: x.rotate_all("x", -0.1)),
    pygame.K_a: (lambda x: x.rotate_all("y",  0.1)),
    pygame.K_s: (lambda x: x.rotate_all("y", -0.1)),
    pygame.K_z: (lambda x: x.rotate_all("z",  0.1)),
    pygame.K_x: (lambda x: x.rotate_all("z", -0.1))
}

class ProjectionViewer:
    """Displays 3D objects on a Pygame screen"""
    
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        
        self.background = (10,10,50)
        self.wireframes = {}
        self.show_nodes = True
        self.show_edges = True
        self.node_color = (255,255,255)
        self.edge_color = (200,200,200)
        self.node_radius = 4

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Wireframe Display")

    def run(self):
        """Create a pygame screen until it is closed"""

        pygame.key.set_repeat(1, 100)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key in KEYS:
                        KEYS[event.key](self)

            self.display()
            pygame.display.flip()

    def add_wireframe(self, wframe: wireframe.Wireframe, name: str):
        self.wireframes[name] = wframe

    def display(self):
        self.screen.fill(self.background)

        for wireframe in self.wireframes.values():
            if self.show_edges:
                for n1, n2 in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edge_color, wireframe.nodes[n1][:2], wireframe.nodes[n2][:2], 1)

            if self.show_nodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.node_color, (node[0], node[1]), self.node_radius, 0)

    def translate_all(self, vector):
        matrix = wireframe.translation_matrix(*vector)
        for i in self.wireframes:
            wframe = self.wireframes[i]
            wframe.transform(matrix)

    def scale_all(self, scale: int):
        center_x = self.width / 2
        center_y = self.height / 2

        for i in self.wireframes:
            wireframe = self.wireframes[i]
            wireframe.scale(scale, (center_x, center_y))

    def rotate_all(self, axis: str, theta: int, *, old_way: bool = True):
        if old_way:
            rotate_function = "rotate_" + axis

        for i in self.wireframes:
            wireframe = self.wireframes[i]
            center = wireframe.get_center()
            if old_way:
                getattr(wireframe, rotate_function)(center, theta)
            else:
                wireframe.rotate(axis, center, theta)
