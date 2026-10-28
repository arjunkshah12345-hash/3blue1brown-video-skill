"""Winding circles: the geometry behind sine waves and Fourier series.

Three scenes:

* ``WindingUnitCircle`` -- the height of a point on a unit circle traces a
  sine wave.  This is the "aha" that makes everything else in the video feel
  inevitable.
* ``SquareWaveEpicycles`` -- add odd harmonics head-to-tail and the tip draws
  a square wave.
* ``GibbsPhenomenon`` -- more terms sharpen the corners, but the overshoot at
  each jump does not shrink (Wilbraham-Gibbs).

Run one scene (from the ``examples`` directory):

    python3 -m manim -qh 02_winding_circles.py WindingUnitCircle
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    TAU,
    UP,
    Axes,
    Circle,
    Create,
    DashedLine,
    DecimalNumber,
    Dot,
    FadeIn,
    Indicate,
    Line,
    MathTex,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
    linear,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))

from b3b import palette
from b3b.animations import traced_path
from b3b.fourier import (
    EpicycleChain,
    partial_sum,
    square_wave,
    square_wave_harmonics,
)
from b3b.style import B3BScene, arrow, axes_3b1b, dot_at, label


class WindingUnitCircle(B3BScene):
    """A rotating point's height traces sine."""

    def construct(self) -> None:
        self.title_card("Winding around the unit circle", "where sine comes from")

        center = LEFT * 3.7 + UP * 0.25
        radius = 1.45
        circle = Circle(
            radius=radius,
            color=palette.BLUE,
            stroke_width=3,
            stroke_opacity=0.85,
        ).move_to(center)

        axes = axes_3b1b(
            x_range=(0, TAU, PI / 2),
            y_range=(-1.4, 1.4, 1),
            width=5.4,
            height=2.9,
            x_label=r"t",
            y_label=r"\sin t",
        )
        axes.move_to(RIGHT * 3.05 + DOWN * 0.2)

        phase = ValueTracker(0.01)

        def tip_point() -> np.ndarray:
            t = phase.get_value()
            return center + radius * np.array([np.cos(t), np.sin(t), 0.0])

        def base_point() -> np.ndarray:
            return np.array([tip_point()[0], center[1], 0.0])

        tip = always_redraw(lambda: dot_at(tip_point(), color=palette.ACCENT))
        vector = always_redraw(
            lambda: arrow(center, tip_point(), color=palette.BLUE, stroke_width=6)
        )
        horizontal = always_redraw(
            lambda: Line(
                center,
                base_point(),
                color=palette.GREEN,
                stroke_width=3,
            )
        )
        vertical = always_redraw(
            lambda: Line(
                base_point(),
                tip_point(),
                color=palette.RED,
                stroke_width=3,
            )
        )
        cos_label = MathTex(r"\cos\theta", font_size=30, color=palette.GREEN)
        cos_label.add_updater(
            lambda m: m.move_to(
                center
                + RIGHT * (tip_point()[0] - center[0]) / 2
                + DOWN * 0.24
            )
        )
        sin_label = MathTex(r"\sin\theta", font_size=30, color=palette.RED)
        sin_label.add_updater(
            lambda m: m.move_to(
                np.array([tip_point()[0], center[1], 0.0])
                + UP * (tip_point()[1] - center[1]) / 2
                + RIGHT * 0.42
            )
        )

        wave_dot = Dot(radius=0.075, color=palette.ACCENT)
        wave_dot.move_to(axes.c2p(0, 0))
        wave_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(phase.get_value(), np.sin(phase.get_value()))
            )
        )
        trace = traced_path(wave_dot, color=palette.ACCENT, stroke_width=2.6)

        guide = always_redraw(
            lambda: DashedLine(
                tip_point(),
                wave_dot.get_center(),
                color=palette.CREAM,
                stroke_width=1.1,
                stroke_opacity=0.28,
                dash_length=0.09,
            )
        )

        self.play(Create(circle), Create(axes), run_time=1.8)
        self.say(r"A point moves around the circle at constant speed.")
        self.add(guide, trace, horizontal, vertical, vector, tip)
        self.add(wave_dot, cos_label, sin_label)
        self.play(
            phase.animate.set_value(TAU - 0.01),
            run_time=12,
            rate_func=linear,
        )
        self.say(r"Its height traces a sine wave.")
        self.wait(1.5)


class SquareWaveEpicycles(B3BScene):
    """Seven odd harmonics draw a convincing square wave."""

    def construct(self) -> None:
        self.title_card("A square wave from spinning circles", "the Fourier series")

        harmonics = square_wave_harmonics(count=7, base_radius=0.80)
        chain = EpicycleChain(harmonics, origin=LEFT * 3.6 + UP * 0.25)

        axes = axes_3b1b(
            x_range=(0, TAU, PI / 2),
            y_range=(-1.5, 1.5, 1),
            width=6.1,
            height=3.1,
            x_label=r"t",
            y_label=r"f(t)",
        )
        axes.move_to(RIGHT * 3.15 + DOWN * 0.2)

        phase = ValueTracker(0.01)

        wave_dot = Dot(radius=0.075, color=palette.ACCENT)
        wave_dot.move_to(axes.c2p(0, 0))
        wave_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(
                    phase.get_value(),
                    partial_sum(phase.get_value(), harmonics),
                )
            )
        )
        trace = traced_path(wave_dot, color=palette.ACCENT, stroke_width=2.8)

        guide = always_redraw(
            lambda: DashedLine(
                chain.tip.get_center(),
                wave_dot.get_center(),
                color=palette.CREAM,
                stroke_width=1.0,
                stroke_opacity=0.22,
                dash_length=0.09,
            )
        )

        self.play(Create(axes), run_time=1.4)
        self.play(Create(chain), run_time=2.0)
        chain.follow(phase)
        self.add(guide, trace, wave_dot)
        self.say("Odd harmonics, each smaller than the last.")
        self.play(
            phase.animate.set_value(TAU - 0.01),
            run_time=14,
            rate_func=linear,
        )

        ideal = VGroup(
            Line(
                axes.c2p(0.02, 1),
                axes.c2p(PI, 1),
                color=palette.CREAM,
                stroke_width=2,
                stroke_opacity=0.4,
            ),
            Line(
                axes.c2p(PI, -1),
                axes.c2p(TAU - 0.02, -1),
                color=palette.CREAM,
                stroke_width=2,
                stroke_opacity=0.4,
            ),
        )
        self.play(Create(ideal), run_time=1.0)
        self.say("Seven terms already look square.")
        self.wait(1.5)


class GibbsPhenomenon(B3BScene):
    """The overshoot at a jump survives every finite truncation."""

    def construct(self) -> None:
        self.title_card("The Gibbs phenomenon", "the overshoot that refuses to vanish")

        axes = axes_3b1b(
            x_range=(0, TAU, PI / 2),
            y_range=(-1.6, 1.6, 1),
            width=10.2,
            height=4.8,
            x_label=r"t",
        )
        axes.move_to(DOWN * 0.2)

        ideal = VGroup(
            Line(
                axes.c2p(0.02, 1),
                axes.c2p(PI, 1),
                color=palette.CREAM,
                stroke_width=1.8,
                stroke_opacity=0.28,
            ),
            Line(
                axes.c2p(PI, -1),
                axes.c2p(TAU - 0.02, -1),
                color=palette.CREAM,
                stroke_width=1.8,
                stroke_opacity=0.28,
            ),
        )
        self.play(Create(axes), *[Create(line) for line in ideal], run_time=1.5)

        harmonics = square_wave_harmonics(count=13, base_radius=1.0)
        terms = ValueTracker(1)

        def current_curve():
            n = max(1, int(terms.get_value()))
            return axes.plot(
                lambda t: partial_sum(t, harmonics[:n]),
                x_range=[0.015, TAU - 0.015],
                color=palette.BLUE,
                stroke_width=3.2,
            )

        curve = always_redraw(current_curve)

        readout = DecimalNumber(
            1,
            num_decimal_places=0,
            font_size=34,
            color=palette.CREAM,
        )
        readout.add_updater(
            lambda m: m.set_value(2 * max(1, int(terms.get_value())) - 1)
        )
        prefix = MathTex("N =", font_size=34, color=palette.CREAM)
        counter = VGroup(prefix, readout).arrange(RIGHT, buff=0.12)
        counter.next_to(axes, UP, buff=0.2).align_to(axes, LEFT)

        self.add(curve, counter)
        self.say("Adding terms sharpens the corners.")
        self.play(
            terms.animate.set_value(13),
            run_time=12,
            rate_func=linear,
        )

        gibbs_height = 1.1789797444721672
        overshoot_line = DashedLine(
            axes.c2p(0.05, gibbs_height),
            axes.c2p(TAU - 0.05, gibbs_height),
            color=palette.RED,
            stroke_width=1.5,
            stroke_opacity=0.65,
        )
        overshoot_label = MathTex(
            r"\approx 9\%", font_size=30, color=palette.RED
        ).next_to(overshoot_line, RIGHT, buff=0.12)
        self.play(Create(overshoot_line), FadeIn(overshoot_label), run_time=1.0)
        self.play(Indicate(overshoot_label, color=palette.RED, scale_factor=1.08))
        self.say("The overshoot stays at about 9 percent, no matter how many terms.")
        self.wait(1.6)
