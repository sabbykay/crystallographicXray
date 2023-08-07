import math
import numpy as np
from AtomicPlanes import AtomicPlanes
from ga import angle_between_planes, make_rotor
from Cube import Cube
from Mesh3D import Mesh3D, Grid
from Plane import Plane
from Object import * #Object for the humans 
from OpenGL.GL import * #everything that starts with gl
from OpenGL.GLU import * #everything that starts with glu
from pygame.locals import DOUBLEBUF, OPENGL
from Settings import window_dimensions, gui_dimensions

pygame.init()
screen_width = math.fabs(window_dimensions[1] - window_dimensions[0])
screen_height = math.fabs(window_dimensions[3] - window_dimensions[2])

pygame.display.set_caption("Atomic Plane and Crystal Display")
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)

done = False
white = pygame.Color(255, 255, 255)

objects_3d = []
objects_2d = []

atomic_planes = AtomicPlanes()

rotations = RotationList()

cube = Object("Cube")
cube.add_component(Transform((0, 0, -5)))
cube.add_component(rotations)
cube.add_component(Cube(GL_POLYGON))

objects_3d.append(cube)

xraybeam = Object("XrayBeam")
xraybeam.add_component(Transform((0, 0, -5)))
xraybeam.add_component(XrayBeam((-10, 0, 0), (20, 0, 0)))

objects_3d.append(xraybeam)

plane = Plane(GL_POLYGON)
plane_object_3d = Object("Plane")
plane_object_3d.add_component(Transform((0, 0, -5)))
plane_object_3d.add_component(plane)

objects_3d.append(plane_object_3d)

grid = Object("Grid")
grid.add_component(Transform((0, 0, -5)))
grid.add_component(Grid(0.5, 8, (0, 0, 255)))

objects_3d.append(grid)


def button_click(the_rotation, increment):
    """
    Increment the_rotation.angle_of_rotation
    Parameters
    ----------
    the_rotation: Rotation
        the rotation Transformation to be incremented or decremented
    increment: float
        degrees to increment the angle of rotation
    """
    print(f"incrementing {the_rotation} by {increment}")
    the_rotation.angle_of_rotation += increment


white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

clock = pygame.time.Clock()
fps = 30


def set_2d():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # reset projection matrix
    # gluOrtho2D(0, screen.get_width(), 0, screen.get_height())
    gluOrtho2D(gui_dimensions[0], gui_dimensions[1], gui_dimensions[3], gui_dimensions[2])

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()  # reset modelview matrix
    glViewport(0, 0, screen.get_width(), screen.get_height())


def set_3d():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)


glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

trans: Transform = cube.get_component(Transform)

angle_increment = 1.0

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        trans.move_x(-0.1)
    if keys[pygame.K_RIGHT]:
        trans.move_x(0.1)
    if keys[pygame.K_x] and keys[pygame.K_UP]:
        rotations.add(Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0), angle_of_rotation=angle_increment))
    if keys[pygame.K_x] and keys[pygame.K_DOWN]:
        rotations.add(Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0), angle_of_rotation=-angle_increment))
    if keys[pygame.K_y] and keys[pygame.K_UP]:
        rotations.add(Rotation(name="Y", axis_of_rotation=(0.0, 1.0, 0.0), angle_of_rotation=angle_increment))
    if keys[pygame.K_y] and keys[pygame.K_DOWN]:
        rotations.add(Rotation(name="Y", axis_of_rotation=(0.0, 1.0, 0.0), angle_of_rotation=-angle_increment))
    if keys[pygame.K_z] and keys[pygame.K_UP]:
        rotations.add(Rotation(name="Z", axis_of_rotation=(0.0, 0.0, 1.0), angle_of_rotation=angle_increment))
    if keys[pygame.K_z] and keys[pygame.K_DOWN]:
        rotations.add(Rotation(name="Z", axis_of_rotation=(0.0, 0.0, 1.0), angle_of_rotation=-angle_increment))

    # find angle between xray beam and atomic planes
    rotor = rotations.rotor()
    atomic_planes.rotate_planes(rotor=rotor)
    angles_with_planes = atomic_planes.angles_with_planes(a_line=(1.0, 0.0, 0.0))
    print(f"looking for 45 degree angles")
    planes_at_45_degrees = list()
    for plane_str, angle_info in angles_with_planes.items():
        # print(f"plane {plane_str} is at angle {angle_info['angle']} to xray beam")
        if np.isclose(angle_info["angle"], np.deg2rad(45.0), atol=0.005):
            planes_at_45_degrees.append(angle_info)
    if len(planes_at_45_degrees) == 0:
        if plane_object_3d in objects_3d:
            objects_3d.remove(plane_object_3d)
    else:
        if plane_object_3d not in objects_3d:
            objects_3d.append(plane_object_3d)
        for angle_info in planes_at_45_degrees:
            rotated_atomic_plane = angle_info["rotated_plane"]
            line_of_intersection = plane.fixed_plane_h.meet(rotated_atomic_plane)
            angle_of_intersection = angle_between_planes(plane1=plane.fixed_plane_h, plane2=rotated_atomic_plane)
            rotor = make_rotor(axis_of_rotation=line_of_intersection, angle_of_rotation=angle_of_intersection)
            plane.rotate(rotor=rotor)
            print(f"  plane {plane_str} is at angle {np.rad2deg(angle_info['angle'])} with the xray beam")
            break

    glPushMatrix()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    set_3d()
    for o in objects_3d:
        o.update()

    set_2d()
    for o in objects_2d:
        o.update(events)

    glPopMatrix()
    pygame.display.flip()
    clock.tick(fps)
    # print(pygame.mouse.get_pos())
pygame.quit()
