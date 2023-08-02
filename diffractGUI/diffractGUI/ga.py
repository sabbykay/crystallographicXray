import numpy as np

import clifford

def add_h4_attributes(an_object):
    _, blades = clifford.Cl(4)
    an_object.one_h = blades[""]
    for blade_name, blade in blades.items():
        if len(blade_name) > 0:
            setattr(an_object, blade_name, blade)


def make_rotor(axis_of_rotation, angle_of_rotation):
    #print(f"axis_of_rotation: {axis_of_rotation}")
    bivector_of_rotation = axis_of_rotation.dual()
    #print(f"bivector_of_rotation: {bivector_of_rotation}")
    rotor = np.e**(bivector_of_rotation * (angle_of_rotation/2))
    #print(f"rotor: {rotor}")
    return rotor


def angle_between_line_and_plane(line, plane):
    normal_to_plane = plane.dual()
    inner_product_line_and_normal = line | normal_to_plane
    # inner_product_normal_and_line = normal_to_plane | line
    angle_between_line_and_normal = np.arccos(
        abs(inner_product_line_and_normal) / (abs(line) * abs(normal_to_plane))
    )
    # angle_between_line_and_normal_degrees = np.rad2deg(angle_between_line_and_normal)
    angle = (np.pi / 2) - angle_between_line_and_normal
    # angle_degrees = np.rad2deg(angle)
    return angle


def angle_between_planes(plane1, plane2):
    normal1 = plane1.dual()
    normal2 = plane2.dual()
    angle = np.arccos(
        abs(normal1 | normal2) / (abs(normal1) * abs(normal2))
    )
    return angle
