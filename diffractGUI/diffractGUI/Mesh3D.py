import pygame.image
from OpenGL.GL import * #everything that starts with gl

class Mesh3D:
    def __init__(self, color=(0, 1, 0)):
        self.vertices = [(0.5, -0.5, 0.5),
                         (-0.5, -0.5, 0.5),
                         (0.5, 0.5, 0.5),
                         (-0.5, 0.5, 0.5),
                         (0.5, 0.5, -0.5),
                         (-0.5, 0.5, -0.5)]

        self.triangles = [0, 2, 3, 0, 3, 1]
        self.color = color

    def draw(self):
        glColor3fv(self.color)
        for t in range(0, len(self.triangles), 3):
            glBegin(GL_LINE_LOOP)
            #glBegin(GL_POLYGON)
            glVertex3fv(self.vertices[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t + 1]])
            glVertex3fv(self.vertices[self.triangles[t + 2]])
            glEnd()

class TextureMesh3D:
    def __init__(self):
        self.vertices = [(0.5, -0.5, 0.5),
                         (-0.5, -0.5, 0.5),
                         (0.5, 0.5, 0.5),
                         (-0.5, 0.5, 0.5),
                         (0.5, 0.5, -0.5),
                         (-0.5, 0.5, -0.5)]

        self.triangles = [0, 2, 3, 0, 3, 1]
        self.draw_type = GL_LINE_LOOP
        self.texture = pygame.image.load()
        self.texID = 0

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        for t in range(0, len(self.triangles), 3):
            glBegin(self.draw_type)
            glTexCoord2fv(self.uvs[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t]])
            glTexCoord2fv(self.uvs[self.triangles[t + 1]])
            glVertex3fv(self.vertices[self.triangles[t + 1]])
            glTexCoord2fv(self.uvs[self.triangles[t + 2]])
            glVertex3fv(self.vertices[self.triangles[t + 2]])
            glEnd()
        glDisable(GL_TEXTURE_2D)

    def int_texture(self):
        self.texID = glGenTextures(1)
        textureData = pygame.image.tostring(self.texture, "RGB", 1)
        width = self.texture.get_width()
        height = self.texture.get_height()
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

class XrayBeam:

    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def draw(self):
        glColor3fv((1, 1, 0))
        glBegin(GL_LINES)
        glVertex3fv((self.start_point[0], self.start_point[1],
                         self.start_point[2]))
        glVertex3fv((self.end_point[0], self.end_point[1],
                         self.end_point[2]))
        glEnd()

class Grid:

    def __init__(self, interval, halfsize, color=(0.6, 0.8, 1.0)):
        self.interval = interval
        self.halfsize = halfsize
        self.color = color

    def draw(self):
        glColor3fv(self.color)
        glBegin(GL_LINES)
        for x in range(-self.halfsize, self.halfsize):
            for y in range(-self.halfsize, self.halfsize):
                glVertex3fv((x * self.interval, y * self.interval - 10, 0))
                glVertex3fv((x * self.interval, y * self.interval + 500, 0))
                glVertex3fv((y * self.interval - 10, x * self.interval, 0))
                glVertex3fv((y * self.interval + 500, x * self.interval, 0))
        glEnd()