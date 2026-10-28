"""Fourier-series machinery: epicycles, partial sums, and the square wave.

A ``Harmonic`` is a single rotating complex number

.. math::

    z_n(t) = A_n e^{i(\\omega_n t + \\phi_n)}.

Chaining harmonics means placing the tail of each rotating vector at the tip
of the previous one.  ``EpicycleChain`` owns that chain and can be driven by a
``ValueTracker``; the tip's y-coordinate is the Fourier partial sum used for
the wave trace.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

import numpy as np
from manim import (
    DOWN,
    ORIGIN,
    RIGHT,
    Circle,
    Dot,
    Line,
    ValueTracker,
    VGroup,
)

from . import palette


@dataclass(frozen=True)
class Harmonic:
    """One term of a Fourier series.

    Parameters
    ----------
    frequency
        Integer multiple of the fundamental (1 for the fundamental).
    amplitude
        Radius of this circle in scene units.
    phase
        Phase offset in radians.  Use ``phase=-PI/2`` to turn a sine term into
        a cosine term.
    color
        Stroke colour for this harmonic's circle and vector.
    """

    frequency: int
    amplitude: float
    phase: float = 0.0
    color: str = palette.BLUE

    def value(self, t: float) -> complex:
        """The complex offset contributed at parameter ``t``."""
        return self.amplitude * np.exp(1j * (self.frequency * t + self.phase))


def square_wave_harmonics(
    count: int = 7,
    *,
    base_radius: float = 0.85,
    start_index: int = 0,
) -> list[Harmonic]:
    """The first ``count`` odd harmonics of a unit square wave.

    The series is

    .. math:: \\frac{4}{\\pi} \\sum_{n \\text{ odd}} \\frac{\\sin(nt)}{n}.

    ``base_radius`` scales the whole chain to fit the frame; it does not change
    the shape of the partial sum once normalised.
    """
    harmonics = []
    for i, n in enumerate(range(1, 2 * count, 2)):
        harmonics.append(
            Harmonic(
                frequency=n,
                amplitude=base_radius * 4.0 / (np.pi * n),
                color=palette.CYCLE[(i + start_index) % len(palette.CYCLE)],
            )
        )
    return harmonics


def partial_sum(t: float, harmonics: Iterable[Harmonic], *, projection: str = "sin") -> float:
    """Sum the chain at ``t`` and return the requested projection.

    ``projection="sin"`` takes the imaginary part (the usual sine series);
    ``"cos"`` takes the real part.
    """
    z = sum(h.value(t) for h in harmonics)
    return float(z.imag if projection == "sin" else z.real)


def square_wave(t: float) -> float:
    """Ideal unit square wave: +1 on the first half of each period, -1 after."""
    return float(np.sign(np.sin(t)))


class EpicycleChain(VGroup):
    """A chain of rotating vectors, drawn as circles plus a pen dot.

    The group is updated by :meth:`update_from_phase`.  Bind it to a tracker
    with :meth:`follow` and the whole chain stays in sync with anything else
    driven by the same scalar.

    Parameters
    ----------
    harmonics
        Ordered outer-to-inner terms.
    scale
        Extra uniform scale applied to every radius.
    show_circles
        Draw the guiding circles (usually desirable for teaching, noisy for
        a final flourish).
    """

    def __init__(
        self,
        harmonics: Sequence[Harmonic],
        *,
        scale: float = 1.0,
        show_circles: bool = True,
        line_stroke_width: float = 2.2,
        circle_stroke_width: float = 1.3,
        circle_opacity: float = 0.3,
        tip_color: str = palette.ACCENT,
        tip_radius: float = 0.065,
        origin: Sequence[float] = ORIGIN,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.harmonics = list(harmonics)
        self.scale = scale
        self.origin = np.asarray(origin, dtype=float)

        self.circles = VGroup()
        self.lines = VGroup()
        for h in self.harmonics:
            radius = h.amplitude * scale
            if show_circles and radius > 1e-6:
                self.circles.add(
                    Circle(
                        radius=radius,
                        color=h.color,
                        stroke_width=circle_stroke_width,
                        stroke_opacity=circle_opacity,
                    )
                )
            self.lines.add(
                Line(
                    ORIGIN,
                    RIGHT * radius,
                    color=h.color,
                    stroke_width=line_stroke_width,
                )
            )

        self.tip = Dot(radius=tip_radius, color=tip_color)
        self.add(self.circles, self.lines, self.tip)
        self.update_from_phase(0.0)

    # -- geometry ----------------------------------------------------------
    def update_from_phase(self, t: float) -> None:
        """Place every vector head-to-tail at parameter ``t``."""
        center = self.origin.copy()
        for h, line in zip(self.harmonics, self.lines):
            angle = h.frequency * t + h.phase
            offset = h.amplitude * self.scale * np.array(
                [np.cos(angle), np.sin(angle), 0.0]
            )
            line.put_start_and_end_on(center, center + offset)
            center = center + offset
        self.tip.move_to(center)

        # Circles are centred where their vector starts.  Doing this in a
        # second pass keeps the loop above easy to read.
        circle_index = 0
        center = self.origin.copy()
        for h in self.harmonics:
            radius = h.amplitude * self.scale
            if len(self.circles) > circle_index and radius > 1e-6:
                self.circles[circle_index].move_to(center)
                circle_index += 1
            angle = h.frequency * t + h.phase
            center = center + h.amplitude * self.scale * np.array(
                [np.cos(angle), np.sin(angle), 0.0]
            )

        self.pen_point = center

    @property
    def value(self) -> float:
        """The pen's y-coordinate relative to ``origin``: the partial sum."""
        return float(self.tip.get_center()[1] - self.origin[1])

    # -- drivers -----------------------------------------------------------
    def follow(self, tracker: ValueTracker) -> "EpicycleChain":
        """Tie the chain's phase to ``tracker`` (returns self for chaining)."""
        self.add_updater(lambda m: m.update_from_phase(tracker.get_value()))
        return self

    def freeze(self) -> None:
        """Remove the phase updater, leaving the chain where it is."""
        self.clear_updaters()


def tip_position(harmonics: Sequence[Harmonic], t: float, *, scale: float = 1.0) -> np.ndarray:
    """Static helper for the chain tip, useful when laying out a wave axis."""
    z = sum(h.value(t) for h in harmonics) * scale
    return np.array([z.real, z.imag, 0.0])
