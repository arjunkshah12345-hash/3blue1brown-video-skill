"""The 3Blue1Brown colour palette, plus semantic aliases.

The hex values come from ``manim/manimlib/default_config.yml`` in the
3b1b/manim repository, so a scene written here can be moved to either
ManimGL or Manim Community and keep its look.

Two rules keep a scene readable:

1.  Pick a *meaning* for a colour and keep it.  Blue is the primary object,
    green is the input/basis, red is the thing that changes.
2.  Use at most three saturated colours in one frame.  Everything else
    should be white, cream, or grey.
"""

# ---------------------------------------------------------------------------
# Raw 3b1b family colours
# ---------------------------------------------------------------------------
BLUE_DARK = "#1C758A"  # blue_e
BLUE_DEEP = "#29ABCA"  # blue_d
BLUE = "#58C4DD"  # blue_c
BLUE_LIGHT = "#9CDCEB"  # blue_b
BLUE_PALE = "#C7E9F1"  # blue_a

TEAL = "#5CD0B3"  # teal_c
GREEN = "#83C167"  # green_c
GREEN_PALE = "#C9E2AE"  # green_a
YELLOW = "#FFFF00"  # yellow_c
YELLOW_SOFT = "#F4D345"  # yellow_d
GOLD = "#F0AC5F"  # gold_c
RED = "#FC6255"  # red_c
MAROON = "#C55F73"  # maroon_c
PURPLE = "#9A72AC"  # purple_c
PINK = "#D147BD"

# ---------------------------------------------------------------------------
# Neutrals
# ---------------------------------------------------------------------------
BACKGROUND = "#000000"
INK = "#FFFFFF"
CREAM = "#DDDDDD"  # grey_a -- secondary text and thin rules
MUTED = "#888888"  # grey_c -- de-emphasised text
AXIS = "#BBBBBB"  # grey_b -- axes and arrows
GRID = BLUE_DARK  # the faint blue grid in the calculus series

# ---------------------------------------------------------------------------
# Semantic aliases.  Prefer these in example code: they document intent.
# ---------------------------------------------------------------------------
PRIMARY = BLUE  # the object currently under discussion
SECONDARY = GREEN  # inputs, basis vectors, the "before" state
ACCENT = YELLOW  # the quantity being measured or revealed
WARNING = RED  # something changes, or a common mistake
HIGHLIGHT = YELLOW  # spotlight / indication
SHADOW = MAROON

I_HAT = GREEN  # x basis vector
J_HAT = RED  # y basis vector

#: Repeating palette for chains, series, and families of curves.
CYCLE = (BLUE, GREEN, YELLOW, RED, PURPLE, TEAL, GOLD)

#: A calmer palette for filled regions.
FILLS = (BLUE, GREEN, YELLOW, PURPLE)
