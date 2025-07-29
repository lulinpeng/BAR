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

class DrawCurve(Scene):
    def construct(self):
        plane = NumberPlane()
        vmo = VMobject(color=GREEN)
        sub_curve0 = [np.array([-2, -1, 0]), np.array([-3, 1, 0]), np.array([0, 3, 0]), np.array([1, 3, 0])]
        sub_curve1 = [np.array([1,  3,  0]), np.array([ 0, 1, 0]), np.array([4, 3, 0]), np.array([4, -2, 0])]
        curve_points = sub_curve0 + sub_curve1
        vmo.points = curve_points
        self.add(plane, vmo)
