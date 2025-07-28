from manim import *
import math

class DrawCircle(Scene):
    def construct(self):
        plane = NumberPlane()
        vmo = VMobject(color=GREEN)
        points = []
        for i in range(100): # generate points
            x, y = math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)
            points.append(np.array([x, y, 0]))
        vmo.points = points
        self.add(plane, vmo)
