"""Camera choreography for ``MovingCameraScene`` and ``ThreeDScene``.

The camera frame is a mobject, so "cinematography" is just animation.  Keep
two rules in mind:

* Scale the frame uniformly.  Setting only its width stretches the frame and
  changes the effective aspect ratio.
* Save the frame before a complex move and ``Restore`` it afterwards; this is
  cheaper and more reliable than trying to invert three separate tweens.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
from manim import ORIGIN, Restore, ThreeDScene, smooth


def frame(scene):
    """The camera frame mobject of a moving-camera scene."""
    return scene.camera.frame


def save_frame(scene) -> None:
    """Remember the current frame position and size."""
    scene.camera.frame.save_state()


def restore_frame(scene, *, run_time: float = 1.5, rate_func=smooth) -> None:
    """Animate back to the last saved frame state."""
    scene.play(Restore(scene.camera.frame), run_time=run_time, rate_func=rate_func)


def zoom_to(
    scene,
    point: Sequence[float] = ORIGIN,
    *,
    width: float = 7.0,
    run_time: float = 1.5,
    rate_func=smooth,
) -> None:
    """Zoom so the frame is ``width`` scene units wide, centred on ``point``."""
    cam_frame = scene.camera.frame
    factor = width / cam_frame.width
    scene.play(
        cam_frame.animate.scale(factor).move_to(np.asarray(point, dtype=float)),
        run_time=run_time,
        rate_func=rate_func,
    )


def zoom_to_mobject(
    scene,
    mobject,
    *,
    margin: float = 1.5,
    min_width: float = 3.0,
    max_width: float = 16.0,
    run_time: float = 1.5,
    rate_func=smooth,
) -> None:
    """Frame a mobject with breathing room, respecting the frame's aspect ratio."""
    cam_frame = scene.camera.frame
    aspect = cam_frame.width / cam_frame.height
    needed = max(mobject.width * margin, mobject.height * margin * aspect)
    width = float(np.clip(needed, min_width, max_width))
    zoom_to(scene, mobject.get_center(), width=width, run_time=run_time, rate_func=rate_func)


def pan_to(
    scene,
    point: Sequence[float],
    *,
    run_time: float = 1.5,
    rate_func=smooth,
) -> None:
    """Slide the view without changing zoom."""
    scene.play(
        scene.camera.frame.animate.move_to(np.asarray(point, dtype=float)),
        run_time=run_time,
        rate_func=rate_func,
    )


def follow(
    scene,
    target,
    *,
    offset: Sequence[float] = ORIGIN,
    smoothing: float = 8.0,
):
    """Attach an exponential-smoothed follow updater to the camera frame.

    ``smoothing`` is a rate in 1/seconds: larger values track more tightly.
    The return value is the updater function, which can be passed to
    :func:`stop_follow` (or simply use ``clear_updaters`` for a full reset).
    """
    cam_frame = scene.camera.frame
    offset = np.asarray(offset, dtype=float)

    def _update(mobject, dt: float) -> None:
        desired = target.get_center() + offset
        alpha = 1.0 - np.exp(-smoothing * dt)
        mobject.move_to(mobject.get_center() + (desired - mobject.get_center()) * alpha)

    cam_frame.add_updater(_update)
    return _update


def stop_follow(scene, updater=None) -> None:
    """Detach one follow updater, or all camera updaters when ``updater`` is None."""
    cam_frame = scene.camera.frame
    if updater is None:
        cam_frame.clear_updaters()
    else:
        cam_frame.remove_updater(updater)


def orbit(
    scene: ThreeDScene,
    *,
    theta: float | None = None,
    phi: float | None = None,
    zoom: float | None = None,
    run_time: float = 2.0,
) -> None:
    """Animate the spherical camera coordinates of a ``ThreeDScene``."""
    scene.move_camera(theta=theta, phi=phi, zoom=zoom, run_time=run_time)
