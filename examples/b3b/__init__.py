"""``b3b`` -- a small, opinionated layer over Manim Community for 3b1b-style scenes.

Import the pieces you need, e.g.::

    from b3b import B3BScene, palette, formula, morph_tex

The package intentionally does not monkey-patch Manim or hide its API.  Every
example is still an ordinary Manim scene and can be rendered with the ``manim``
CLI.
"""

from . import animations, audio, camera, fourier, graphing, palette, style

from .animations import (
    EquationMorph,
    count_up,
    dim,
    fade_in_all,
    flash_at,
    focus_box,
    highlight,
    morph_shapes,
    morph_tex,
    passing_flash,
    restore,
    traced_path,
    write_all,
)
from .camera import (
    follow,
    orbit,
    pan_to,
    restore_frame,
    save_frame,
    stop_follow,
    zoom_to,
    zoom_to_mobject,
)
from .fourier import (
    EpicycleChain,
    Harmonic,
    partial_sum,
    square_wave,
    square_wave_harmonics,
    tip_position,
)
from .graphing import area, dot_on_graph, graph, graph_label, riemann, secant_group, tangent
from .style import (
    B3BMovingCameraScene,
    B3BLinearTransformationScene,
    B3BScene,
    arrow,
    axes_3b1b,
    brace,
    dot_at,
    formula,
    label,
    matrix,
    plane_3b1b,
    style_scene,
    underline,
    unit_square,
    vector,
)

__all__ = [
    "B3BMovingCameraScene",
    "B3BLinearTransformationScene",
    "B3BScene",
    "EquationMorph",
    "EpicycleChain",
    "Harmonic",
    "animations",
    "area",
    "arrow",
    "audio",
    "axes_3b1b",
    "brace",
    "camera",
    "count_up",
    "dim",
    "dot_at",
    "dot_on_graph",
    "fade_in_all",
    "flash_at",
    "focus_box",
    "follow",
    "formula",
    "fourier",
    "graph",
    "graph_label",
    "graphing",
    "highlight",
    "label",
    "matrix",
    "morph_shapes",
    "morph_tex",
    "orbit",
    "palette",
    "pan_to",
    "partial_sum",
    "passing_flash",
    "plane_3b1b",
    "restore",
    "restore_frame",
    "riemann",
    "save_frame",
    "secant_group",
    "square_wave",
    "square_wave_harmonics",
    "stop_follow",
    "style",
    "style_scene",
    "tangent",
    "tip_position",
    "traced_path",
    "underline",
    "unit_square",
    "vector",
    "write_all",
    "zoom_to",
    "zoom_to_mobject",
]
