from Mesh3D import Mesh3D
from ga import add_h4_attributes, make_rotor


class Plane(Mesh3D):
    def __init__(self, draw_type):
        super().__init__(color=(1, 0.5, 0.0))
        self.fixed_vertices = [
            (-0.5, -0.5, 0),  # 0
            (0.5, -0.5, 0),  # 1
            (-0.5, 0.5, 0),  # 2
            (0.5, 0.5, 0),  # 3
        ]

        add_h4_attributes(self)

        self.fixed_vertices_h = [
            self.e4 + v[0] * self.e1 + v[1] * self.e2 + v[2] * self.e3
            for v
            in self.fixed_vertices
        ]

        self.fixed_plane_h = self.fixed_vertices_h[0] ^ self.fixed_vertices_h[1] ^ self.fixed_vertices_h[3]

        self.triangles = [
            0, 1, 3, 0, 2, 3
        ]

        zero_rotation = make_rotor(
            axis_of_rotation=self.e1 ^ self.e4,
            angle_of_rotation=0.0
        )
        self.rotate(zero_rotation)

        Mesh3D.draw_type = draw_type

    def rotate(self, rotor):
        self.vertices_h = list()
        self.vertices = list()
        for v in self.fixed_vertices:
            v4 = self.e4 + self.e1 * v[0] + self.e2 * v[1] + self.e3 * v[2]
            rotated_v4 = rotor * v4 * ~rotor
            self.vertices_h.append(rotated_v4)
            self.vertices.append((rotated_v4[self.e1], rotated_v4[self.e2], rotated_v4[self.e3]))
        print(self.vertices_h)
        print(self.vertices)

