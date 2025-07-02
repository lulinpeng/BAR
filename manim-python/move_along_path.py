from manim import *

class MoveAlongLineAndCircle(Scene):
    def construct(self):
        circle = Circle(radius=0.5, color=BLUE)
        x = [-4, 0, 0]
        y = [ 4, 0, 0]
        circle.move_to(x)
        
        path0 = Line(x, y, color=GREEN) # take Line as path
        self.add(path0)
        self.play(MoveAlongPath(circle, path0), run_time=4)
        
        path1 = Line(y, [2,0,0]) # take Line as path
        self.play(MoveAlongPath(circle, path1), run_time=4)
        
        self.play(FadeOut(path0))
        
        path2 = Circle(radius=2) # take Circle as path
        self.add(path2)
        self.play(MoveAlongPath(circle, path2), run_time=6)
