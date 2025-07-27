from manim import *

class VMobjectDemo(Scene):
    def construct(self):
        plane = NumberPlane()
        vmo = VMobject(color=GREEN)
        sub_curve0 = [np.array([-2, -1, 0]), np.array([-3, 1, 0]), np.array([0, 3, 0]), np.array([1, 3, 0])]
        sub_curve1 = [np.array([1,  3,  0]), np.array([ 0, 1, 0]), np.array([4, 3, 0]), np.array([4, -2, 0])]
        curve_points = sub_curve0 + sub_curve1
        vmo.points = curve_points
        self.add(plane, vmo)
        
        # self.wait(1)
        # vmo0 = VMobject(color=RED)
        # vmo0.points = sub_curve0
        
        # vmo1 = VMobject(color=ORANGE)
        # vmo1.points = sub_curve1
        
        # self.add(vmo0, vmo1)
        
        # self.play(vmo)