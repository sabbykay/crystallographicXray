from itertools import combinations

import numpy as np

from diffractGUI.ga import add_h4_attributes, make_rotor, angle_between_line_and_plane


class AtomicPlanes:
    def __init__(self):
        self.cube_vertices = [
            (0.5, -0.5, 0.5),
            (-0.5, -0.5, 0.5),
            (0.5, 0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (0.5, -0.5, -0.5),
            (-0.5, -0.5, -0.5),
        ]

        add_h4_attributes(self)

        self.cube_vertices_h = [
            self.e4 + v[0] * self.e1 + v[1] * self.e2 + v[2] * self.e3 for v in self.cube_vertices
        ]

        zero_rotor = make_rotor(
            axis_of_rotation=self.e1^self.e4,
            angle_of_rotation=0.0
        )
        self.rotate_planes(rotor=zero_rotor)

    def rotate_planes(self, rotor):
        #print(f"rotor: {rotor}")
        self.atomic_planes = dict()
        for three_points in combinations(self.cube_vertices_h, r=3):
            atomic_plane = three_points[0] ^ three_points[1] ^ three_points[2]
            rotated_atomic_plane = rotor * atomic_plane * ~rotor
            self.atomic_planes[str(atomic_plane)] = {
                "points": three_points,
                "plane": atomic_plane,
                "normal": atomic_plane.dual(),
                "rotated_plane": rotated_atomic_plane,
                "rotated_normal": rotated_atomic_plane.dual(),
            }

    def angles_with_planes(self, a_line):
        a_line_h = (a_line[0] * self.e1 + a_line[1] * self.e2 + a_line[2] * self.e3 + self.e4) ^ self.e4
        angles_with_planes = dict()
        for plane_str, plane_info in self.atomic_planes.items():
            rotated_plane = plane_info["rotated_plane"]
            angle = angle_between_line_and_plane(a_line_h, rotated_plane)
            angles_with_planes[plane_str] = {"line": a_line, "angle": angle}
            angles_with_planes[plane_str].update(plane_info)

        return angles_with_planes
