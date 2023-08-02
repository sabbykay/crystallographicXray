import math

from Cube import Cube
from Mesh3D import Mesh3D, Grid
from Object import * #Object for the humans
from OpenGL.GL import * #everything starting with gl
from OpenGL.GLU import * #everything starting with glu
from pygame.locals import DOUBLEBUF, OPENGL
from Settings import window_dimensions, gui_dimensions

pygame.init()
screen_width = math.fabs(window_dimensions[1] - window_dimensions[0])
screen_height = math.fabs(window_dimensions[3] - window_dimensions[2])

pygame.display.set_caption("OpenGL in Python")
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)

done = False
white = pygame.Color(255, 255, 255)

objects_3d = []
objects_2d = []

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
        rotations.add(Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0), angle_of_rotation=0.1))
    if keys[pygame.K_x] and keys[pygame.K_DOWN]:
        rotations.add(Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0), angle_of_rotation=-0.1))
    if keys[pygame.K_y] and keys[pygame.K_UP]:
        rotations.add(Rotation(name="Y", axis_of_rotation=(0.0, 1.0, 0.0), angle_of_rotation=0.1))
    if keys[pygame.K_y] and keys[pygame.K_DOWN]:
        rotations.add(Rotation(name="Y", axis_of_rotation=(0.0, 1.0, 0.0), angle_of_rotation=-0.1))
    if keys[pygame.K_z] and keys[pygame.K_UP]:
        rotations.add(Rotation(name="Z", axis_of_rotation=(0.0, 0.0, 0.0), angle_of_rotation=0.1))
    if keys[pygame.K_z] and keys[pygame.K_DOWN]:
        rotations.add(Rotation(name="Z", axis_of_rotation=(0.0, 0.0, 0.0), angle_of_rotation=-0.1))

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
