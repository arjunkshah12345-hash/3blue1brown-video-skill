"""Convenience wrappers around Manim's axes that carry the house style.

The wrappers exist so an example can read like mathematics:

    curve = graph(axes, lambda x: x**2)
    self.play(Create(curve))

instead of spelling out colours, widths, and sampling ranges every time.
"""

from __future__ import annotations

from typing import Callable, Iterable, Sequence

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Axes,
    Dot,
    Line,
    MathTex,
    ValueTracker,
    VGroup,
)

from . import palette
from .style import CURVE_STROKE, LABEL_SIZE


def graph(
    axes: Axes,
    function: Callable[[float], float],
    *,
    x_range: Sequence[float] | None = None,
    color: str = palette.BLUE,
    stroke_width: float = CURVE_STROKE,
    **kwargs,
):
    """Plot ``function`` on ``axes`` with the default curve weight."""
    return axes.plot(
        function,
        x_range=x_range,
        color=color,
        stroke_width=stroke_width,
        **kwargs,
    )


def graph_label(
    axes: Axes,
    curve,
    x: float,
    text: str,
    *,
    direction: np.ndarray = UP,
    buff: float = 0.22,
    color: str = palette.CREAM,
    font_size: float = LABEL_SIZE,
) -> MathTex:
    """Place a formula label just off a curve at horizontal position ``x``."""
    label = MathTex(text, font_size=font_size, color=color)
    point = axes.i2gp(x, curve)
    label.next_to(point, direction, buff=buff)
    return label


def tangent(
    axes: Axes,
    function: Callable[[float], float],
    x: float,
    *,
    slope: float | None = None,
    half_width: float = 2.2,
    color: str = palette.ACCENT,
    stroke_width: float = 3.0,
) -> Line:
    """A tangent line at ``x``.

    If ``slope`` is omitted it is estimated with a central difference, which
    is accurate enough for drawing but not for a rigorous derivative label.
    """
    if slope is None:
        h = 1e-4
        slope = (function(x + h) - function(x - h)) / (2 * h)
    y = function(x)
    return Line(
        axes.c2p(x - half_width, y - slope * half_width),
        axes.c2p(x + half_width, y + slope * half_width),
        color=color,
        stroke_width=stroke_width,
    )


def secant_group(
    axes: Axes,
    curve,
    x: float,
    dx: float,
    *,
    dx_color: str = palette.YELLOW,
    dy_color: str = palette.RED,
    secant_color: str = palette.GREEN,
    secant_line_length: float = 12.0,
) -> VGroup:
    """The classic run/rise triangle plus the secant line through it."""
    return axes.get_secant_slope_group(
        x=x,
        graph=curve,
        dx=dx,
        dx_line_color=dx_color,
        dy_line_color=dy_color,
        include_secant_line=True,
        secant_line_color=secant_color,
        secant_line_length=secant_line_length,
    )


def area(
    axes: Axes,
    curve,
    x_range: tuple[float, float],
    *,
    color: str = palette.BLUE,
    opacity: float = 0.3,
    bounded_graph=None,
):
    """Fill the region between ``curve`` and the x-axis."""
    return axes.get_area(
        curve,
        x_range=x_range,
        color=color,
        opacity=opacity,
        bounded_graph=bounded_graph,
    )


def riemann(
    axes: Axes,
    curve,
    x_range: tuple[float, float],
    dx: float,
    *,
    color: str = palette.BLUE,
    opacity: float = 0.45,
    stroke_width: float = 1.0,
    sample: str = "left",
) -> VGroup:
    """Rectangles under ``curve``; animate ``dx`` to show the limit."""
    return axes.get_riemann_rectangles(
        curve,
        x_range=x_range,
        dx=dx,
        input_sample_type=sample,
        stroke_width=stroke_width,
        stroke_color=palette.BACKGROUND,
        fill_opacity=opacity,
        color=color,
    )


def dot_on_graph(
    axes: Axes,
    curve,
    tracker: ValueTracker,
    *,
    color: str = palette.ACCENT,
    radius: float = 0.08,
    direction: str = "x",
) -> Dot:
    """A dot that follows ``tracker`` along ``curve``.

    ``direction="y"`` plots ``axes.i2gp(curve_value, ...)`` semantics for
    parametric curves is out of scope; for ordinary graphs leave it as ``x``.
    """
    if direction not in {"x", "y"}:
        raise ValueError("direction must be 'x' or 'y'")
    dot = Dot(color=color, radius=radius)
    dot.add_updater(lambda m: m.move_to(axes.i2gp(tracker.get_value(), curve)))
    return dot
