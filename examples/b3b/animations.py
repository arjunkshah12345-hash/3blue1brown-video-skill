"""Reusable animation factories for the moves 3b1b uses constantly.

These are plain functions returning ``Animation`` objects, plus two thin
``Animation`` subclasses.  Nothing here changes Manim's semantics: you can
always reach for the underlying class instead.
"""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np
from manim import (
    DOWN,
    UP,
    AnimationGroup,
    Circumscribe,
    Create,
    FadeIn,
    FadeOut,
    Flash,
    Indicate,
    LaggedStart,
    ShowPassingFlash,
    Succession,
    SurroundingRectangle,
    TransformMatchingShapes,
    TransformMatchingTex,
    TracedPath,
    ValueTracker,
    VMobject,
    Write,
    smooth,
)

from . import palette


# ---------------------------------------------------------------------------
# Equation morphing
# ---------------------------------------------------------------------------
class EquationMorph(TransformMatchingTex):
    """Morph one equation into another, keeping shared symbols alive.

    ``TransformMatchingTex`` splits both sides into substrings and matches
    them.  That is why ``e^{i\\pi} + 1 = 0`` can become
    ``e^{i\\pi} = -1`` without the ``e`` or the equals sign ever fading out.

    Pass ``key_map={"old": "new"}`` when the same idea is written differently
    (for example ``"h" -> "dx"``); pass ``transform_mismatches=True`` when
    every unmatched piece should slide to its new position instead of
    cross-fading.
    """


def morph_tex(source, target, **kwargs) -> TransformMatchingTex:
    """Shortcut for the most common equation-to-equation transition."""
    return TransformMatchingTex(source, target, **kwargs)


def morph_shapes(source, target, **kwargs) -> TransformMatchingShapes:
    """Morph between representations whose glyphs are not text (diagram -> text)."""
    return TransformMatchingShapes(source, target, **kwargs)


# ---------------------------------------------------------------------------
# Writing and staging
# ---------------------------------------------------------------------------
def write_all(*mobjects, lag_ratio: float = 0.2, run_time: float = 1.8) -> LaggedStart:
    """Write several mobjects with a gentle stagger."""
    return LaggedStart(
        *(Write(mob) for mob in mobjects),
        lag_ratio=lag_ratio,
        run_time=run_time,
    )


def fade_in_all(*mobjects, lag_ratio: float = 0.1, run_time: float = 1.0, shift=UP * 0.15) -> LaggedStart:
    """Fade in a row of labels, each rising slightly into place."""
    return LaggedStart(
        *(FadeIn(mob, shift=shift) for mob in mobjects),
        lag_ratio=lag_ratio,
        run_time=run_time,
    )


# ---------------------------------------------------------------------------
# Emphasis
# ---------------------------------------------------------------------------
def highlight(
    mobject,
    *,
    color: str = palette.HIGHLIGHT,
    scale_factor: float = 1.08,
    buff: float = 0.08,
    run_time: float = 1.2,
    box: bool = True,
) -> AnimationGroup:
    """Pulse a mobject (and optionally box it) without moving the layout."""
    animations = [Indicate(mobject, color=color, scale_factor=scale_factor)]
    if box:
        animations.append(Circumscribe(mobject, color=color, buff=buff))
    return AnimationGroup(*animations, lag_ratio=0.0, run_time=run_time)


def focus_box(
    mobject,
    *,
    color: str = palette.HIGHLIGHT,
    buff: float = 0.12,
    corner_radius: float = 0.08,
    stroke_width: float = 2.5,
) -> SurroundingRectangle:
    """A rounded rectangle that stays put; pair with ``Create``/``FadeOut``."""
    return SurroundingRectangle(
        mobject,
        color=color,
        buff=buff,
        corner_radius=corner_radius,
        stroke_width=stroke_width,
    )


def flash_at(point: Sequence[float], *, color: str = palette.YELLOW, **kwargs) -> Flash:
    return Flash(np.asarray(point, dtype=float), color=color, line_length=0.18, num_lines=12, **kwargs)


def passing_flash(
    path: VMobject,
    *,
    color: str = palette.YELLOW,
    time_width: float = 0.35,
    run_time: float = 1.6,
) -> ShowPassingFlash:
    """A bright segment travelling along a curve."""
    return ShowPassingFlash(
        path.copy().set_stroke(color=color, width=5),
        time_width=time_width,
        run_time=run_time,
    )


def dim(mobjects: Iterable, *, opacity: float = 0.18, run_time: float = 0.8):
    """Return a list of animation objects that fade a group into the background."""
    return [mob.animate.set_opacity(opacity) for mob in mobjects]


def restore(mobjects: Iterable, *, run_time: float = 0.8):
    """Undo :func:`dim`."""
    return [mob.animate.set_opacity(1.0) for mob in mobjects]


# ---------------------------------------------------------------------------
# Numeric animation
# ---------------------------------------------------------------------------
def count_up(
    tracker: ValueTracker,
    value: float,
    *,
    run_time: float = 2.5,
    rate_func=smooth,
):
    """Animate a ValueTracker to a new value.

    Everything attached through an updater follows automatically.  This is
    the cleanest way to drive a whole diagram from one scalar.
    """
    return tracker.animate(rate_func=rate_func, run_time=run_time).set_value(value)


def traced_path(
    mobject,
    *,
    color: str = palette.BLUE,
    stroke_width: float = 2.5,
    stroke_opacity: float = 0.9,
    **kwargs,
) -> TracedPath:
    """A fading trail behind a moving mobject."""
    return TracedPath(
        mobject.get_center,
        stroke_color=color,
        stroke_width=stroke_width,
        stroke_opacity=stroke_opacity,
        **kwargs,
    )
