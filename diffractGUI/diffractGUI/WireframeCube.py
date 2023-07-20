import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from clifford import Cl
from OpenGL.GL import (
GL_COLOR_BUFFER_BIT,
GL_DEPTH_BUFFER_BIT,
glBegin,
glClear,
glEnd,
glLoadIdentity,
glRotatef,
glTranslatef,
glVertex3f,
glVertex3fv,
GL_LINES, 
)
from OpenGL.GLU import gluPerspective

unit_cell_dimensions = (0.5, 0.5, 0.5)  # Length, width, height

def draw_unit_cell():
    # Unit cell vertices and edges remain the same as before
    vertices = [
        (-unit_cell_dimensions[0] / 2, -unit_cell_dimensions[1] / 2, -unit_cell_dimensions[2] / 2),
        (unit_cell_dimensions[0] / 2, -unit_cell_dimensions[1] / 2, -unit_cell_dimensions[2] / 2),
        (unit_cell_dimensions[0] / 2, unit_cell_dimensions[1] / 2, -unit_cell_dimensions[2] / 2),
        (-unit_cell_dimensions[0] / 2, unit_cell_dimensions[1] / 2, -unit_cell_dimensions[2] / 2),
        (-unit_cell_dimensions[0] / 2, -unit_cell_dimensions[1] / 2, unit_cell_dimensions[2] / 2),
        (unit_cell_dimensions[0] / 2, -unit_cell_dimensions[1] / 2, unit_cell_dimensions[2] / 2),
        (unit_cell_dimensions[0] / 2, unit_cell_dimensions[1] / 2, unit_cell_dimensions[2] / 2),
        (-unit_cell_dimensions[0] / 2, unit_cell_dimensions[1] / 2, unit_cell_dimensions[2] / 2)
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def setup():
    pygame.init()
    width,  height = 800, 600
    window = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    gluPerspective(45, (width / height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(45, 1, 1, 0)

def main():
    setup()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_unit_cell()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()