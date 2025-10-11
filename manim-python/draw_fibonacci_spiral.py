from manim import *

def rescale(point:list, scale:float):
    return [c * scale for c in point]

class FibonacciSpiral(Scene):
    def construct(self):
        n = 7
        scale = 1 * 0.2
        side_lens = [1, 1]
        square_start_points = [[0, 0, 0], [1, -1, 0]]
        for i in range(2, n):
            side_len = side_lens[i-1]
            xx = square_start_points[i-1].copy()
            xx[0] += (side_len if i % 4 == 0 or i % 4 == 1 else -side_len)
            xx[1] += (side_len if i % 4 == 0 or i % 4 == 3 else -side_len)
            square_start_points.append(xx)
            side_lens.append(side_lens[i-1] + side_lens[i-2])
        print(f'side_lens = {side_lens}')
        
        square_center_points = []
        arc_center_points = []
        for i in range(len(square_start_points)):
            xx = square_start_points[i].copy()
            half_side_len = side_lens[i] / 2
            xx[0] += ( half_side_len if i % 4 == 0 or i % 4 == 3 else -half_side_len)
            xx[1] += (-half_side_len if i % 4 == 0 or i % 4 == 1 else  half_side_len)
            square_center_points.append(xx)
            xx = square_start_points[i].copy()
            side_len = side_lens[i]
            if i % 4 == 0:
                xx[1] -= side_len
            elif i % 4 == 1:
                xx[0] -= side_len
            elif i % 4 == 2:
                xx[1] += side_len
            elif i % 4 == 3:
                xx[0] += side_len
            arc_center_points.append(xx)
        print(f'square_center_points: {square_center_points}')
        print(f'arc_center_points: = {arc_center_points}')

        squares, dots, arcs = [], [], []
        for i in range(n):
            square = Square(side_lens[i] * scale, stroke_width=0.3)
            square.move_to(rescale(square_center_points[i], scale))
            squares.append(square)
            dot = Dot(rescale(square_start_points[i], scale), 0.2*scale, color=BLUE)
            dots.append(dot)
            arc = Arc(radius=side_lens[i]*scale, start_angle= -i * PI / 2 + PI / 2, angle= -PI / 2, arc_center=rescale(arc_center_points[i], scale), stroke_color=RED, stroke_width=1)
            arcs.append(arc)
            
        for i in range(n):
            self.add(dots[i])
            self.play(Create(squares[i]), Create(arcs[i]))