"""Shared scene classes, layout constants, and small mobject factories.

This module is deliberately thin.  Every helper either (a) applies the house
style, or (b) removes six or seven lines of boilerplate that would otherwise
hide the mathematical idea in an example.  Anything more opinionated belongs
in the example itself.
"""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Axes,
    Brace,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    LinearTransformationScene,
    MathTex,
    Mobject,
    MovingCameraScene,
    NumberPlane,
    Polygon,
    Scene,
    Tex,
    VGroup,
    Write,
    config,
)

from . import palette
from .audio import SoundMixin, speakable

# ---------------------------------------------------------------------------
# Layout constants.  Changing these changes every example at once, which is
# exactly what you want when you decide the channel reads better at 56pt.
# ---------------------------------------------------------------------------
TITLE_SIZE = 72
FORMULA_SIZE = 60
LABEL_SIZE = 36
CAPTION_SIZE = 34
SMALL_SIZE = 28

DOT_RADIUS = 0.075
VECTOR_STROKE = 6
CURVE_STROKE = 4
GRID_STROKE = 1.0


def style_scene(scene: Scene) -> None:
    """Apply the global look: black background, no default window chrome."""
    scene.camera.background_color = palette.BACKGROUND


def formula(
    tex: str,
    *,
    font_size: float = FORMULA_SIZE,
    color: str = palette.INK,
    **kwargs,
) -> MathTex:
    """A centred display equation."""
    return MathTex(tex, font_size=font_size, color=color, **kwargs)


def label(
    text: str,
    *,
    font_size: float = LABEL_SIZE,
    color: str = palette.CREAM,
    **kwargs,
) -> Tex:
    """A text label in the same Computer Modern family as the equations."""
    return Tex(text, font_size=font_size, color=color, **kwargs)


def axes_3b1b(
    x_range: Sequence[float] = (-7.0, 7.0, 1.0),
    y_range: Sequence[float] = (-4.0, 4.0, 1.0),
    *,
    width: float = 10.6,
    height: float = 5.8,
    x_label: str | None = None,
    y_label: str | None = None,
    numbers: bool = False,
    tip: bool = True,
) -> Axes:
    """Rectangular axes with the thin grey 3b1b treatment.

    Labels are attached to the axes object so they travel with it.  Use the
    returned ``Axes`` for ``c2p`` / ``i2gp`` / ``plot`` as usual.
    """
    axes = Axes(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=width,
        y_length=height,
        axis_config={
            "color": palette.AXIS,
            "stroke_width": 2.0,
            "include_tip": tip,
            "tip_width": 0.16,
            "tip_height": 0.16,
            "include_numbers": numbers,
            "font_size": 24,
            "numbers_to_include": [],
        },
        x_axis_config={"numbers_to_include": []},
        y_axis_config={"numbers_to_include": []},
    )
    if x_label is not None:
        tex = MathTex(x_label, font_size=SMALL_SIZE, color=palette.CREAM)
        tex.next_to(axes.x_axis.get_end(), DOWN, buff=0.18)
        axes.add(tex)
        axes.x_axis_label = tex
    if y_label is not None:
        tex = MathTex(y_label, font_size=SMALL_SIZE, color=palette.CREAM)
        tex.next_to(axes.y_axis.get_end(), LEFT, buff=0.18)
        axes.add(tex)
        axes.y_axis_label = tex
    return axes


def plane_3b1b(
    *,
    x_range: Sequence[float] = (-9.0, 9.0, 1.0),
    y_range: Sequence[float] = (-5.0, 5.0, 1.0),
    x_length: float = 15.0,
    y_length: float = 8.6,
    stroke_opacity: float = 0.45,
) -> NumberPlane:
    """A full-bleed NumberPlane with a faint blue grid."""
    return NumberPlane(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=x_length,
        y_length=y_length,
        background_line_style={
            "stroke_color": palette.GRID,
            "stroke_width": GRID_STROKE,
            "stroke_opacity": stroke_opacity,
        },
        axis_config={
            "color": palette.AXIS,
            "stroke_color": palette.AXIS,
            "stroke_width": 2.0,
            "stroke_opacity": 0.9,
            "include_tip": False,
        },
    )


def arrow(
    start: Sequence[float] | np.ndarray,
    end: Sequence[float] | np.ndarray,
    *,
    color: str = palette.BLUE,
    stroke_width: float = VECTOR_STROKE,
    tip_ratio: float = 0.14,
) -> Arrow:
    """A clean vector from ``start`` to ``end`` with no gap at the tail."""
    return Arrow(
        np.asarray(start, dtype=float),
        np.asarray(end, dtype=float),
        buff=0.0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=tip_ratio,
        max_stroke_width_to_length_ratio=20.0,
    )


def vector(
    direction: Sequence[float] | np.ndarray,
    *,
    color: str = palette.BLUE,
    stroke_width: float = VECTOR_STROKE,
) -> Arrow:
    """A vector rooted at the origin."""
    return arrow(ORIGIN, direction, color=color, stroke_width=stroke_width)


def dot_at(
    point: Sequence[float] | np.ndarray = ORIGIN,
    *,
    color: str = palette.ACCENT,
    radius: float = DOT_RADIUS,
) -> Dot:
    return Dot(np.asarray(point, dtype=float), radius=radius, color=color)


def brace(
    mobject: Mobject,
    text: str,
    *,
    direction: np.ndarray = DOWN,
    buff: float = 0.16,
    color: str = palette.CREAM,
    label_color: str | None = None,
    font_size: float = LABEL_SIZE,
) -> VGroup:
    """A brace hugging ``mobject`` with a label just beyond its tip."""
    b = Brace(mobject, direction=direction, buff=buff, color=color)
    tex = MathTex(
        text,
        font_size=font_size,
        color=label_color or color,
    )
    tex.next_to(b, direction, buff=0.14)
    return VGroup(b, tex)


def matrix(
    rows: Iterable[Iterable[float | str]],
    *,
    color: str = palette.INK,
    font_size: float = 46,
) -> MathTex:
    """A bracketed matrix, e.g. ``matrix([[1, 1], [0, 1]])``."""
    body = r" \\ ".join(" & ".join(str(entry) for entry in row) for row in rows)
    return MathTex(
        rf"\begin{{bmatrix}} {body} \end{{bmatrix}}",
        font_size=font_size,
        color=color,
    )


def unit_square(
    plane: NumberPlane,
    *,
    color: str = palette.ACCENT,
    fill_opacity: float = 0.28,
    stroke_width: float = 3.0,
) -> Polygon:
    """The unit square in a plane's coordinate system, ready to be transformed."""
    return Polygon(
        plane.c2p(0, 0),
        plane.c2p(1, 0),
        plane.c2p(1, 1),
        plane.c2p(0, 1),
        color=color,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_width=stroke_width,
    )


def underline(
    mobject: Mobject,
    *,
    color: str = palette.ACCENT,
    buff: float = 0.08,
    stroke_width: float = 2.5,
) -> Line:
    """A short rule under a term, useful for marking the current step."""
    line = Line(LEFT, RIGHT, color=color, stroke_width=stroke_width)
    line.match_width(mobject)
    line.next_to(mobject, DOWN, buff=buff)
    return line


# ---------------------------------------------------------------------------
# Scene mixins
# ---------------------------------------------------------------------------
class _B3BBase(SoundMixin):
    """Caption, title-card and sound conventions shared by all b3b scenes."""

    _caption: Mobject | None = None

    def setup(self) -> None:
        super().setup()
        style_scene(self)
        self._caption = None
        self._sound_init()

    # -- captions ----------------------------------------------------------
    def say(
        self,
        text: str,
        *,
        spoken: str | None = None,
        font_size: float = CAPTION_SIZE,
        buff: float = 0.45,
        color: str = palette.CREAM,
        run_time: float = 0.7,
        **kwargs,
    ) -> Tex:
        """Show a one-line caption at the bottom edge, replacing the last one.

        Keep captions to one short clause.  They are a scaffold for the
        viewer, not a script: the animation should still make sense muted.

        When a voice is on (see ``b3b.audio``) the caption is also spoken,
        as ``spoken`` if given (do this for captions with maths), otherwise
        as the caption with its TeX stripped.  ``spoken=""`` keeps it silent.
        """
        self.finish_narration()
        self.clear_caption(run_time=0.25)
        self.narrate(speakable(text) if spoken is None else spoken)
        caption = Tex(text, font_size=font_size, color=color, **kwargs)
        caption.to_edge(DOWN, buff=buff)
        self._caption = caption
        self.play(FadeIn(caption, shift=UP * 0.12), run_time=run_time)
        return caption

    def clear_caption(self, *, run_time: float = 0.35) -> None:
        if self._caption is not None:
            caption = self._caption
            self.play(FadeOut(caption), run_time=run_time)
            self.remove(caption)
            # LinearTransformationScene registers added mobjects (and their
            # families) in several special lists.  Any stale caption left in
            # ``moving_mobjects`` is re-interpolated on the next transform and
            # crashes with a family-size mismatch.
            stale = set(caption.get_family())
            for attr in (
                "foreground_mobjects",
                "background_mobjects",
                "transformable_mobjects",
                "moving_mobjects",
                "moving_vectors",
            ):
                current = getattr(self, attr, None)
                if current is not None:
                    setattr(self, attr, [m for m in current if m not in stale])
            self._caption = None

    # -- title cards -------------------------------------------------------
    def title_card(
        self,
        text: str,
        subtitle: str | None = None,
        *,
        font_size: float = TITLE_SIZE,
        color: str = palette.INK,
        underline_title: bool = True,
        hold: float = 1.3,
        run_time: float = 1.1,
        persist: bool = False,
    ) -> VGroup:
        """Write a title (and optional subtitle), hold, then clear it.

        With ``persist=True`` the card stays on screen and is returned; the
        caller is then responsible for fading it out.
        """
        title = Tex(text, font_size=font_size, color=color)
        group = VGroup(title)
        if subtitle:
            sub = Tex(subtitle, font_size=CAPTION_SIZE, color=palette.CREAM)
            sub.next_to(title, DOWN, buff=0.25)
            group.add(sub)
        group.move_to(UP * 0.35)

        animations: list = [Write(title)]
        rule = None
        if underline_title:
            rule = Line(LEFT, RIGHT, color=palette.ACCENT, stroke_width=3)
            rule.match_width(title)
            rule.next_to(title, DOWN, buff=0.22)
            animations.append(Create(rule))
        self.play(*animations, run_time=run_time)
        self.wait(hold)

        if rule is not None:
            group.add(rule)

        if persist:
            return group

        self.play(FadeOut(group), run_time=0.7)
        return group


class B3BScene(_B3BBase, Scene):
    """Ordinary 2D scene with the house style and caption helpers."""


class B3BMovingCameraScene(_B3BBase, MovingCameraScene):
    """Moving-camera scene with the same helpers."""


class B3BLinearTransformationScene(_B3BBase, LinearTransformationScene):
    """``LinearTransformationScene`` with the house palette and captions.

    Pass the usual ``background_plane_kwargs`` / ``foreground_plane_kwargs``
    to tune the grids; everything else behaves exactly like Manim's class.
    """
