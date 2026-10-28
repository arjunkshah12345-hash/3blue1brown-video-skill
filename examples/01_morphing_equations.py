"""01 -- Morphing equations.

Three short scenes about the move that defines the 3b1b equation style:
instead of cutting from one line to the next, every symbol that survives the
algebra stays on screen and travels to its new home.

Run a single scene:

    manim -ql -p 01_morphing_equations.py EulerIdentityMorph
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (
    DEGREES,
    PI,
    Circumscribe,
    FadeOut,
    Indicate,
    MathTex,
    TransformMatchingTex,
    Write,
)

from b3b import B3BScene, palette


class EulerIdentityMorph(B3BScene):
    """Derive Euler's identity by keeping the surviving symbols alive."""

    def construct(self):
        self.title_card("Euler's identity", "Five constants, one line", hold=1.0)

        identity = MathTex(
            r"e^{i\pi}", "+", "1", "=", "0", font_size=76
        )
        identity[0].set_color(palette.BLUE)
        identity[2].set_color(palette.GREEN)
        identity[4].set_color(palette.ACCENT)

        self.play(Write(identity), run_time=2.0)
        self.say("Start with the identity.")
        self.wait(0.3)

        self.play(Indicate(identity[0], color=palette.BLUE, scale_factor=1.15))
        self.say(r"Move the 1 to the other side.")
        solved = MathTex(r"e^{i\pi}", "=", "-1", font_size=76)
        solved[0].set_color(palette.BLUE)
        solved[2].set_color(palette.ACCENT)
        self.play(
            TransformMatchingTex(
                identity,
                solved,
                path_arc=20 * DEGREES,
                run_time=2.0,
            )
        )
        self.wait(0.4)

        self.say(r"Now expand $e^{i\pi}$ with Euler's formula.", spoken="Now expand e to the i pi with Euler's formula.")
        expanded = MathTex(
            r"\cos\pi", "+", r"i\sin\pi", "=", "-1", font_size=68
        )
        expanded[0].set_color(palette.GREEN)
        expanded[2].set_color(palette.BLUE)
        expanded[4].set_color(palette.ACCENT)
        self.play(
            TransformMatchingTex(
                solved,
                expanded,
                transform_mismatches=True,
                path_arc=25 * DEGREES,
                run_time=2.2,
            )
        )
        self.wait(0.3)

        self.play(Indicate(expanded[0], color=palette.GREEN))
        self.play(Indicate(expanded[2], color=palette.BLUE))
        self.say(r"$\cos\pi = -1$ and $\sin\pi = 0$.", spoken="Cosine of pi is minus one, and sine of pi is zero.")

        evaluated = MathTex("-1", "+", "0", "=", "-1", font_size=76)
        evaluated[0].set_color(palette.ACCENT)
        evaluated[2].set_color(palette.GREEN)
        evaluated[4].set_color(palette.ACCENT)
        self.play(
            TransformMatchingTex(
                expanded,
                evaluated,
                run_time=2.0,
            )
        )
        self.wait(0.4)

        self.say("Everything collapses to a single truth.")
        final = MathTex("-1", "=", "-1", font_size=86)
        final.set_color_by_tex("-1", palette.ACCENT)
        self.play(TransformMatchingTex(evaluated, final, run_time=1.8))
        self.play(Circumscribe(final, color=palette.HIGHLIGHT, buff=0.15))
        self.wait(0.5)

        # Bookend: return to the form everyone remembers.
        self.play(FadeOut(final), run_time=0.8)
        closing = MathTex(r"e^{i\pi}", "+", "1", "=", "0", font_size=86)
        closing[0].set_color(palette.BLUE)
        closing[2].set_color(palette.GREEN)
        closing[4].set_color(palette.ACCENT)
        self.play(Write(closing), run_time=1.8)
        self.say("Five constants. One equation.")
        self.wait(1.2)


class PythagoreanRearrangement(B3BScene):
    """Reorder a theorem, then solve it, without cutting away."""

    def construct(self):
        self.title_card("The Pythagorean theorem", hold=1.0)

        equation = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=84)
        equation[0].set_color(palette.BLUE)
        equation[2].set_color(palette.GREEN)
        equation[4].set_color(palette.ACCENT)

        self.play(Write(equation), run_time=2.0)
        self.say("Two legs and the hypotenuse.")
        self.wait(0.4)

        reordered = MathTex("c^2", "=", "a^2", "+", "b^2", font_size=84)
        reordered[0].set_color(palette.ACCENT)
        reordered[2].set_color(palette.BLUE)
        reordered[4].set_color(palette.GREEN)
        self.say("The same statement, read from the other end.")
        self.play(
            TransformMatchingTex(
                equation,
                reordered,
                path_arc=30 * DEGREES,
                run_time=2.0,
            )
        )
        self.wait(0.5)

        self.play(Indicate(reordered[4], color=palette.GREEN, scale_factor=1.15))
        self.say(r"Subtract $b^2$ from both sides.", spoken="Subtract b squared from both sides.")
        solved = MathTex("a^2", "=", "c^2", "-", "b^2", font_size=84)
        solved[0].set_color(palette.BLUE)
        solved[2].set_color(palette.ACCENT)
        solved[4].set_color(palette.GREEN)
        self.play(
            TransformMatchingTex(
                reordered,
                solved,
                path_arc=-15 * DEGREES,
                run_time=2.0,
            )
        )
        self.wait(0.4)

        self.play(Circumscribe(solved[0], color=palette.HIGHLIGHT, buff=0.1))
        self.say("Solve for either leg.")
        self.wait(1.2)


class DerivativeDefinition(B3BScene):
    """Build the derivative from a difference quotient, one limit at a time."""

    def construct(self):
        self.title_card("The derivative", "From average to instantaneous", hold=1.0)

        quotient = MathTex(
            r"\frac{f(x+h)-f(x)}{h}",
            font_size=92,
            substrings_to_isolate=["h"],
        )
        quotient.set_color_by_tex("h", palette.GREEN)
        self.play(Write(quotient), run_time=2.0)
        self.say("Average rate of change over a step h.")
        self.wait(0.4)

        limit = MathTex(
            r"\lim_{h\to 0}",
            r"\frac{f(x+h)-f(x)}{h}",
            font_size=76,
            substrings_to_isolate=["h"],
        )
        limit[0].set_color(palette.ACCENT)
        limit.set_color_by_tex("h", palette.GREEN)
        self.say("Now let the step shrink.")
        self.play(
            TransformMatchingTex(
                quotient,
                limit,
                path_arc=20 * DEGREES,
                run_time=2.0,
            )
        )
        self.wait(0.4)

        self.play(Indicate(limit[1], color=palette.BLUE, scale_factor=1.04))
        derivative = MathTex(r"f'(x)", font_size=110)
        derivative.set_color(palette.BLUE)
        self.say("What survives is the derivative.")
        self.play(
            TransformMatchingTex(
                limit,
                derivative,
                transform_mismatches=True,
                path_arc=25 * DEGREES,
                run_time=2.4,
            )
        )
        self.play(Circumscribe(derivative, color=palette.HIGHLIGHT, buff=0.18))
        self.wait(1.4)
