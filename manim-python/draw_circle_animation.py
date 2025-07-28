from manim import *
import math

class DrawCircle(Scene):
    def construct(self):
        plane = NumberPlane()
        vmo = VMobject(color=GREEN)
        points = []
        n = 100
        for i in range(n): # generate points
            x, y = math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)
            points.append(np.array([x, y, 0]))
        vmo.points = points
        self.add(plane, vmo)
        self.wait(2)
        self.remove(vmo)
        self.wait(2)
