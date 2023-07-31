import pygame

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