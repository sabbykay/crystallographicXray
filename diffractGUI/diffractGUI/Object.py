from Button import * #Button
from Mesh3D import Mesh3D, XrayBeam, Grid
from OpenGL.GL import * #everything that starts with gl
from Transform import Transform, Rotation, RotationList


class Object:
    def __init__(self, obj_name):
        self.name = obj_name
        self.components = []

    def add_component(self, component):
        if isinstance(component, Transform):
            self.components.insert(0, self.components)
        self.components.append(component)

    def update(self, events = None):
        glPushMatrix()
        for c in self.components:
            if isinstance(c, Transform):
                pos = c.get_position()
                glTranslatef(pos.x, pos.y, pos.z)
            if isinstance(c, Rotation):
                glRotated(
                    c.angle_of_rotation,
                    c.axis_of_rotation[0],
                    c.axis_of_rotation[1],
                    c.axis_of_rotation[2]
                )
            if isinstance(c, RotationList):
                for rotation in c:
                    glRotated(
                        rotation.angle_of_rotation,
                        rotation.axis_of_rotation[0],
                        rotation.axis_of_rotation[1],
                        rotation.axis_of_rotation[2]
                    )
            if isinstance(c, Mesh3D):
                c.draw()
            if isinstance(c, Button):
                c.draw(events)
            if isinstance(c, XrayBeam):
                c.draw()
            if isinstance(c, Grid):
                c.draw()
        glPopMatrix()

    def get_component(self, class_type):
        for c in self.components:
            if type(c) is class_type:
                return c
        return None
