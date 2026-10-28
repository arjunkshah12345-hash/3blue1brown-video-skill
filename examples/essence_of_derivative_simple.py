from __future__ import annotations

from manim import *
from b3b import B3BScene, palette

class EssenceOfDerivative(B3BScene):
    def construct(self):
        self.title_card("The essence of the derivative", "Slope at a point", hold=1.2)
        
        # Hook
        question = Text("What is slope at a single point?", font_size=42)
        self.play(Write(question))
        self.wait(2)
        self.play(FadeOut(question))
        
        # Setup axes and curve
        axes = Axes(
            x_range=[-0.5, 3, 1],
            y_range=[-0.5, 4, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": palette.AXIS}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        graph = axes.plot(lambda x: x**2/2, color=palette.BLUE, stroke_width=3)
        
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph))
        self.wait(1.5)
        
        # Pick a point
        x0 = 2
        point = Dot(axes.c2p(x0, (x0**2)/2), color=palette.ACCENT)
        point_label = Text("P", font_size=36).next_to(point, UP)
        self.play(Create(point), Write(point_label))
        self.wait(1)
        
        # Move point to nearby
        x1 = x0 + 1.5
        point_q = Dot(axes.c2p(x1, (x1**2)/2), color=palette.GREEN)
        q_label = Text("Q", font_size=36).next_to(point_q, UP)
        self.play(Create(point_q), Write(q_label))
        self.wait(1)
        
        # Draw secant line
        secant = Line(point.get_center(), point_q.get_center(), color=palette.GREEN, stroke_width=2)
        self.play(Create(secant))
        self.wait(1.5)
        
        # Move Q closer multiple times
        for dx in [0.8, 0.4, 0.2, 0.1, 0.05]:
            self.play(
                point_q.animate.move_to(axes.c2p(x0 + dx, ((x0+dx)**2)/2)),
                q_label.animate.move_to(axes.c2p(x0 + dx, ((x0+dx)**2)/2) + UP),
                secant.animate.put_start_and_end_on(point.get_center(), axes.c2p(x0 + dx, ((x0+dx)**2)/2)),
                run_time=1.2
            )
            self.wait(0.3)
        
        # Show tangent
        tangent = axes.plot(lambda x: x + ( (x0**2)/2 - x0 ), x_range=[x0-1, x0+1], color=palette.ACCENT, stroke_width=3)
        self.play(Transform(secant, tangent))
        self.play(FadeOut(point_q), FadeOut(q_label))
        self.wait(2)
        
        # Formula without LaTeX if issues
        formula_text = Text("f'(x) = lim (f(x+h)-f(x))/h as h->0", font_size=32)
        formula_text.to_edge(UP)
        self.play(Write(formula_text))
        self.wait(3)
        
        # Conclusion
        conclusion = Text("The derivative is the slope of the tangent line.", font_size=32)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(4)
