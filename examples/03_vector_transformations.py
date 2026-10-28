"""Linear transformations: what a matrix does to space.

``LinearTransformationScene`` already supplies the moving grid, basis
vectors, and transformable bookkeeping.  These scenes stay close to that
machinery so the code reads like the idea: pick a matrix, watch the plane
move, read the determinant.

Run one scene:

    python3 -m manim -qh 03_vector_transformations.py ShearTransform
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import DOWN, LEFT, UP, MathTex, Write

sys.path.insert(0, str(Path(__file__).resolve().parent))

from b3b import palette
from b3b.style import B3BLinearTransformationScene, matrix


def show_matrix(scene, rows, *, corner=LEFT * 5.5 + UP * 2.2):
    """Write a matrix in the upper-left and return ``(matrix, label)``."""
    mat = matrix(rows, font_size=44).move_to(corner)
    tag = MathTex("M =", font_size=38, color=palette.CREAM).next_to(
        mat, LEFT, buff=0.18
    )
    scene.play(Write(tag), Write(mat), run_time=0.8)
    return mat


class ShearTransform(B3BLinearTransformationScene):
    """A shear keeps area fixed while tilting every vertical line."""

    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=False,
            leave_ghost_vectors=True,
            i_hat_color=palette.I_HAT,
            j_hat_color=palette.J_HAT,
            background_plane_kwargs={
                "background_line_style": {
                    "stroke_color": palette.GRID,
                    "stroke_width": 1.0,
                    "stroke_opacity": 0.55,
                },
                "axis_config": {
                    "color": palette.AXIS,
                    "stroke_width": 2.0,
                },
            },
            foreground_plane_kwargs={
                "background_line_style": {
                    "stroke_color": palette.BLUE,
                    "stroke_width": 1.2,
                    "stroke_opacity": 0.38,
                },
                "faded_line_style": {
                    "stroke_color": palette.BLUE,
                    "stroke_width": 1.0,
                    "stroke_opacity": 0.16,
                },
            },
            **kwargs,
        )

    def construct(self) -> None:
        self.title_card("A shear leaves area alone", hold=0.7)
        mat = show_matrix(self, [[1, 1], [0, 1]])

        self.add_unit_square(
            animate=True,
            color=palette.BLUE,
            opacity=0.3,
            stroke_width=2.0,
        )
        vector = self.add_vector([1, 1], color=palette.ACCENT, animate=True)
        self.add_transformable_label(
            vector, "v", new_label="v", color=palette.ACCENT, animate=True
        )

        self.wait(0.5)
        self.say("Every point slides sideways by its height.")
        self.wait(0.8)
        self.clear_caption()
        self.apply_matrix([[1, 1], [0, 1]], run_time=2.6)
        self.wait(0.4)

        det = MathTex(r"\det = 1", font_size=36, color=palette.GREEN)
        det.next_to(mat, DOWN, buff=0.35)
        self.play(Write(det), run_time=0.7)
        self.say("The determinant is 1, so the area did not change.")
        self.wait(1.4)


class RotationTransform(B3BLinearTransformationScene):
    """A 90 degree rotation is an isometry: lengths and area survive."""

    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=False,
            leave_ghost_vectors=True,
            i_hat_color=palette.I_HAT,
            j_hat_color=palette.J_HAT,
            background_plane_kwargs={
                "background_line_style": {
                    "stroke_color": palette.GRID,
                    "stroke_width": 1.0,
                    "stroke_opacity": 0.55,
                },
                "axis_config": {"color": palette.AXIS, "stroke_width": 2.0},
            },
            foreground_plane_kwargs={
                "background_line_style": {
                    "stroke_color": palette.BLUE,
                    "stroke_width": 1.2,
                    "stroke_opacity": 0.38,
                },
                "faded_line_style": {
                    "stroke_color": palette.BLUE,
                    "stroke_width": 1.0,
                    "stroke_opacity": 0.16,
                },
            },
            **kwargs,
        )

    def construct(self) -> None:
        self.title_card("A rotation turns the whole plane", hold=0.7)
        mat = show_matrix(self, [[0, -1], [1, 0]])

        self.add_unit_square(
            animate=True,
            color=palette.BLUE,
            opacity=0.3,
            stroke_width=2.0,
        )
        vector = self.add_vector([1, 1], color=palette.ACCENT, animate=True)
        self.add_transformable_label(
            vector, "v", new_label="v", color=palette.ACCENT, animate=True
        )

        self.wait(0.4)
        self.say("The basis vectors trade places, up to a sign.")
        self.wait(0.8)
        self.clear_caption()
        self.apply_matrix([[0, -1], [1, 0]], run_time=2.6)
        self.wait(0.3)

        det = MathTex(r"\det = 1", font_size=36, color=palette.GREEN)
        det.next_to(mat, DOWN, buff=0.35)
        self.play(Write(det), run_time=0.7)
        self.say("Lengths and area are preserved.")
        self.wait(1.4)


class ScaleAndDeterminant(B3BLinearTransformationScene):
    """A diagonal matrix scales each axis; the determinant scales area."""

    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=False,
            leave_ghost_vectors=True,
            i_hat_color=palette.I_HAT,
            j_hat_color=palette.J_HAT,
            background_plane_kwargs={
                "background_line_style": {
                    "stroke_color": palette.GRID,
                    "stroke_width": 1.0,
                    "stroke_opacity": 0.55,
                },
                "axis_config": {"color": palette.AXIS, "stroke_width": 2.0},
            },
            foreground_plane_kwargs={
                "background_line_style": {
                    "stroke_color": palette.BLUE,
                    "stroke_width": 1.2,
                    "stroke_opacity": 0.38,
                },
                "faded_line_style": {
                    "stroke_color": palette.BLUE,
                    "stroke_width": 1.0,
                    "stroke_opacity": 0.16,
                },
            },
            **kwargs,
        )

    def construct(self) -> None:
        self.title_card("Scaling the axes scales the area", hold=0.7)
        mat = show_matrix(self, [[2, 0], [0, 1.5]])

        self.add_unit_square(
            animate=True,
            color=palette.BLUE,
            opacity=0.3,
            stroke_width=2.0,
        )

        self.wait(0.4)
        self.say("Stretch x by two and y by one and a half.")
        self.wait(0.8)
        self.clear_caption()
        self.apply_matrix([[2, 0], [0, 1.5]], run_time=2.6)
        self.wait(0.3)

        det = MathTex(r"\det = 2 \cdot 1.5 = 3", font_size=36, color=palette.GREEN)
        det.next_to(mat, DOWN, buff=0.35)
        self.play(Write(det), run_time=0.8)
        self.say("The unit square grows to area three.")
        self.wait(1.5)
