import numpy as np

import pygame

from diffractGUI.ga import add_h4_attributes, make_rotor


class Transform:
    def __init__(self, position):
        self.set_position(position)

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = pygame.math.Vector3(position)

    def move_x(self, amount):
        self.position = pygame.math.Vector3(self.position.x + amount, self.position.y, self.position.z)

    def move_y(self, amount):
        self.position = pygame.math.Vector3(self.position.x, self.position.y + amount, self.position.z)


class Rotation:
    def __init__(self, name, axis_of_rotation, angle_of_rotation=0.0):
        self.name = name
        self.axis_of_rotation = axis_of_rotation
        self.angle_of_rotation = angle_of_rotation

    def __str__(self):
        return f"{self.angle_of_rotation} around {self.axis_of_rotation}"


class RotationList:
    def __init__(self):
        self._rotations = list()

        add_h4_attributes(self)

    def add(self, rotation):
        if len(self._rotations) == 0:
            self._rotations.append(rotation)
        else:
            last_rotation = self._rotations[-1]
            if last_rotation.axis_of_rotation == rotation.axis_of_rotation:
                last_rotation.angle_of_rotation += rotation.angle_of_rotation
            else:
                self._rotations.append(rotation)

    def get(self, index):
        return self._rotations[index]

    def length(self):
        return len(self._rotations)

    def __len__(self):
        return len(self._rotations)

    def __getitem__(self, index):
        return self._rotations[index]

    def rotor(self):
        rotor_list = list()
        if len(self._rotations) == 0:
            rotor_list.append(
                make_rotor(axis_of_rotation=self.e1 ^ self.e4, angle_of_rotation=0.0)
            )
        else:
            for r in self._rotations:
                axis_of_rotation_h = (
                    self.e4
                    + r.axis_of_rotation[0] * self.e1
                    + r.axis_of_rotation[1] * self.e2
                    + r.axis_of_rotation[2] * self.e3
                ) ^ self.e4
                angle_of_rotation_radians = np.deg2rad(r.angle_of_rotation)

                r_rotor = np.e**(axis_of_rotation_h.dual() * (angle_of_rotation_radians / 2))

                rotor_list.append(r_rotor)

        rotor_list.reverse()
        total_rotor = np.prod(rotor_list)
        return total_rotor
