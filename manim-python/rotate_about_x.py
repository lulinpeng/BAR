from manim import *

class RotateDotAboutX(Scene):
    def construct(self):
        dot = Dot(point = [2, 0, 0])
        self.play(Create(dot))
        x = [0, 0, 0]
        for _ in range(10): # rotate 'dot' about the base point 'x'
            self.wait(1)
            self.play(Rotating(dot, about_point= x, radians=1, run_time=2))

class RotateLineAboutX(Scene):
    def construct(self):
        line = Line(start = [0, 0, 0])
        self.play(Create(line))
        x = [0, 0, 0]
        for _ in range(10): # rotate 'line' about the base point 'x'
            self.wait(1)
            self.play(Rotating(line, about_point=x, radians=1, run_time=2))
            
class RotateAllAboutX(Scene):
    def construct(self):
        line = Line(start = [0, 0, 0])
        dot = Dot(point = [2, 0, 0])
        self.play(Create(line), Create(dot))
        x = [0, 0, 0]
        for _ in range(10): # rotate 'line' and 'dot' about the base point 'x'
            self.wait(1)
            self.play(Rotating(line, about_point=x, radians=1, run_time=2), Rotating(dot, about_point=x, radians=1, run_time=2))
