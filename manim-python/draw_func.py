from manim import *

class DrawSine(Scene):
    def construct(self):
        x_step, y_step = 1, 0.5
        axes = Axes(x_range=[-10, 10, x_step], y_range=[-2, 2, y_step], axis_config={"color": BLUE})
        self.add(axes)
        graph = axes.plot(lambda x: np.sin(x), color=RED)
        self.play(Create(graph), run_time=3)

class DrawLog2(Scene):
    def construct(self):
        x_step, y_step = 1, 1
        axes = Axes(x_range=[1, 10, x_step], y_range=[-2, 8, y_step], axis_config={"color": BLUE})
        self.add(axes)
        graph = axes.plot(lambda x: np.log2(x), color=RED)
        self.play(Create(graph), run_time=3)
        
class DrawSqrt(Scene): # \sqrt{x}
    def construct(self):
        x_step, y_step = 1, 1
        axes = Axes(x_range=[0, 10, x_step], y_range=[-2, 8, y_step], axis_config={"color": BLUE})
        self.add(axes)
        graph = axes.plot(lambda x: np.sqrt(x), color=RED)
        self.play(Create(graph), run_time=3)

class DrawRecip(Scene): # Reciprocal 1/x
    def construct(self):
        x_step, y_step = 0.5, 1
        axes = Axes(x_range=[-8, 8, x_step], y_range=[-12, 12, y_step], axis_config={"color": BLUE})
        self.add(axes)
        f = lambda x: 1/x
        graph_left = axes.plot(f, x_range=[0.1, 5, 0.01], color=RED)
        graph_right = axes.plot(f, x_range=[-0.1, -5, -0.01], color=BLUE)
        self.play(Create(graph_left), Create(graph_right), run_time=3)
