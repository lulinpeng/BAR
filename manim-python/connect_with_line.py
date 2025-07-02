from manim import *

class ConnectCircleAndSquare(Scene):
    def construct(self):
        start_circle = Circle(radius=0.2, color=BLUE)
        end_square = Square(side_length=0.3, color=RED)
        end_square.next_to(start_circle, RIGHT, buff=2)
        self.add(start_circle)
        self.play(end_square.animate.rotate(PI / 4))
        line = Line(start = start_circle, end = end_square)
        self.play(Create(line))
        
