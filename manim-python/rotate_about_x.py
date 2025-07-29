from manim import *

class RotateAboutX(Scene):
    def construct(self):
        pos = [2.0, 0.0, 0.0]
        dot = Dot(pos)
        self.play(Create(dot))
        x = [0, 0, 0]
        # rotate 'dot' about the base point 'x'
        for _ in range(10):
            self.wait(1)
            self.play(Rotating(dot, about_point= x, radians=1, run_time=2))
