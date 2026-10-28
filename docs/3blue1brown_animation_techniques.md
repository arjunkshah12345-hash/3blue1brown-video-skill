# 3Blue1Brown Animation Techniques: Deep Dive into Manim Patterns

This document analyzes the animation and visual techniques used by 3Blue1Brown, as implemented in the [3b1b/manim](https://github.com/3b1b/manim) library.

Companion document: [3blue1brown_narration_techniques.md](3blue1brown_narration_techniques.md) covers the scripting and voiceover side — sentence metrics, question placement, the "let's" taxonomy, openings, endings, and how narration is written *against* the animation timeline.

## Table of Contents
- [Core Philosophy](#core-philosophy)
- [Animation System](#animation-system)
- [Creation Animations](#creation-animations)
- [Transform Animations](#transform-animations)
- [Indication & Emphasis](#indication--emphasis)
- [Camera Movement](#camera-movement)
- [Updaters & Interactivity](#updaters--interactivity)
- [Geometric Visualizations](#geometric-visualizations)
- [Equation & Text Animations](#equation--text-animations)
- [Color Usage](#color-usage)
- [Typography](#typography)
- [Graphing & Coordinate Systems](#graphing--coordinate-systems)
- [3D Visualization](#3d-visualization)
- [Best Practices & Patterns](#best-practices--patterns)

## Core Philosophy

3Blue1Brown's visual style is characterized by:
- **Clarity through motion**: Animations serve to guide attention and reveal structure
- **Smooth morphing**: Seamless transitions between representations to show equivalence
- **Mathematical intuition**: Visual metaphors that make abstract concepts concrete
- **Deliberate pacing**: Using `wait()`, lag ratios, and timing to control information flow
- **Color as meaning**: Consistent color-coding to track mathematical objects

## Animation System

### Base Animation Class
Located in `manimlib/animation/animation.py`, the animation system provides:
- **Interpolation framework**: Animations interpolate between start and end states over time
- **Rate functions**: Control easing (`smooth`, `linear`, `there_and_back`, etc.)
- **Run time control**: Precise timing of animations
- **Lag ratios**: Stagger animations across submobjects

Key patterns:
```python
self.play(Animation(mobject, run_time=2, rate_func=smooth))
```

## Creation Animations

From `manimlib/animation/creation.py`:

### `ShowCreation` / `Create`
Draws the boundary/path of a VMobject from start to end.
```python
self.play(ShowCreation(grid))
```
- Uses `pointwise_become_partial()` to reveal paths progressively
- Great for showing graphs, lines, shapes being constructed

### `Write`
A more sophisticated creation animation for text and complex mobjects.
```python
self.play(Write(text, run_time=3, lag_ratio=0.01))
```
- Does "DrawBorderThenFill" - first traces outline, then fills
- Auto-calculates run time based on number of submobjects
- Auto-calculates lag ratio for natural writing effect
- Default stroke color matches the mobject's color

### `DrawBorderThenFill`
The underlying mechanism for Write:
1. Creates an outline copy
2. Animates drawing the outline (first half conceptually)
3. Transitions from outline to filled mobject (second phase)
4. Uses `double_smooth` rate function by default

### `Uncreate`
The reverse of ShowCreation - removes by undrawing.
```python
self.play(Uncreate(mobject, rate_func=lambda t: smooth(1-t)))
```

## Transform Animations

From `manimlib/animation/transform.py`:

### `Transform`
Core morphing animation that interpolates between mobjects.
```python
self.play(Transform(source, target, path_arc=PI/2))
```
- Aligns data between source and target via `align_data_and_family()`
- Supports curved paths via `path_arc` parameter
- Uses `interpolate()` on submobjects with optional custom `path_func`

### `ReplacementTransform`
Like Transform but replaces source with target in the scene.
```python
self.play(ReplacementTransform(old_graph, new_graph))
```
- Sets `replace_mobject_with_target_in_scene = True`
- Common pattern: morph one representation into another

### `TransformFromCopy`
Creates a copy that transforms to target (source remains).
```python
self.play(TransformFromCopy(equation["part"].copy(), other_location))
```
- Useful for showing the same element appears in different contexts

### `MoveToTarget`
Animates a mobject to its pre-defined `.target` attribute.
```python
mobject.generate_target()
mobject.target.shift(RIGHT)
self.play(MoveToTarget(mobject))
```
Pattern used extensively for complex multi-step movements.

### `ApplyMethod`
Animates calling a method on a mobject.
```python
self.play(ApplyMethod(square.shift, RIGHT))
# Or more commonly with animate syntax:
self.play(square.animate.shift(RIGHT))
```

## Transform Matching (Key 3B1B Technique)

From `manimlib/animation/transform_matching_parts.py` - this is quintessentially 3Blue1Brown.

### `TransformMatchingStrings`
Intelligently matches substrings between source and target text/equations.
```python
self.play(TransformMatchingStrings(
    source_tex,
    target_tex,
    key_map={"x": R"y"},  # Explicit mappings
    path_arc=-30 * DEG,
))
```
- Uses sequence matching to find longest common substrings
- Automatically matches identical parts
- Unmatched parts fade out/in from centers
- Preserves structure where possible

### `TransformMatchingShapes`
Matches geometric pieces regardless of mobject type.
```python
self.play(TransformMatchingShapes(text1, text2, run_time=3, path_arc=PI/2))
```
- Finds pairs with same shape via `has_same_shape_as()`
- Great for morphing between completely different visual representations
- Very effective for showing conceptual equivalence

### `TransformMatchingTex`
Alias for `TransformMatchingStrings`, optimized for LaTeX.

**Pattern**: This allows 3Blue1Brown to show algebraic manipulations where parts of equations smoothly transform into their new form, maintaining visual continuity.

## Indication & Emphasis

From `manimlib/animation/indication.py`:

### `Indicate`
Pulses and colors a mobject to draw attention.
```python
self.play(Indicate(equation[R"\pi"], color=YELLOW, scale_factor=1.2))
```
- Scales up then back down
- Changes color temporarily
- Uses `there_and_back` rate function

### `FlashAround`
Creates a rectangular flash around a mobject.
```python
self.play(FlashAround(equation["e"]))
```
- Draws a rectangle that briefly appears around the target
- Great for highlighting specific parts of equations/text

### `CircleIndicate`
Circles around a mobject with a pulsing effect.
```python
self.play(CircleIndicate(mobject, stroke_color=YELLOW))
```

### `Flash`
Creates radial line flashes at a point.
```python
self.play(Flash(point, color=YELLOW, num_lines=12))
```
- Converges lines from outside to center
- Good for marking important points/events

### `ShowPassingFlash`
Creates a traveling highlight along a path (like a scanning beam).
```python
self.play(ShowPassingFlash(graph, time_width=0.1))
```
- Moves a bright segment along the mobject
- Perfect for tracing along curves/graphs

### `FocusOn`
Dims everything except focus point.
```python
self.play(FocusOn(dot))
```
- Creates a large faded circle, shrinks to focus on target
- Useful for directing attention in complex scenes

## Camera Movement

From `manimlib/camera/` and scene usage:

### Camera Frame as Mobject
The camera frame is a mobject that can be animated like any other.
```python
self.play(self.camera.frame.animate.scale(0.5).move_to(point))
```

### Common Camera Patterns
```python
# Zoom in
self.play(self.frame.animate.scale(0.75))

# Pan to focus
self.play(self.frame.animate.move_to(mobject))

# Rotate in 3D
self.play(
    self.frame.animate.increment_phi(-10 * DEG),
    self.frame.animate.increment_theta(-20 * DEG),
)
```

### Camera Updaters for Continuous Movement
```python
self.frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))
```
Used for smooth ambient rotation in 3D scenes.

### Saving/Restoring Camera State
```python
self.camera.frame.save_state()
# ... make changes ...
self.play(Restore(self.camera.frame))
```

## Updaters & Interactivity

Updaters are crucial for dynamic, responsive visualizations.

### `always_redraw`
Recreates a mobject every frame based on current state.
```python
brace = always_redraw(Brace, square, UP)
label = always_redraw(lambda: Text(f"Width = {square.get_width():.2f}").next_to(brace, UP))
```
- Perfect for labels/braces that must track moving objects
- The function is called every frame with current object states

### `add_updater`
Adds a custom update function.
```python
dot.add_updater(lambda d: d.move_to(axes.c2p(x_tracker.get_value(), parabola(x_tracker.get_value()))))
```
- Can take `(mobject)` or `(mobject, dt)` 
- For time-based updates: `square.add_updater(lambda m, dt: m.rotate(dt))`

### `f_always`
Binds method calls to functions returning arguments.
```python
dot.f_always.move_to(lambda: axes.c2p(1, 1))
number.f_always.set_value(square.get_width)
```
More efficient/readable way to track dependencies.

### `ValueTracker`
Animates numerical parameters.
```python
x_tracker = ValueTracker(2)
self.play(x_tracker.animate.set_value(4), run_time=3)
```
Combined with updaters to drive animations.

## Geometric Visualizations

### Coordinate Systems
```python
axes = Axes(
    x_range=(-1, 10),
    y_range=(-2, 2, 0.5),
    height=6,
    width=10,
    axis_config=dict(stroke_color=GREY_A),
)
axes.add_coordinate_labels(font_size=20)
```
- `c2p()` / `coords_to_point()`: coordinate to pixel position
- `p2c()` / `point_to_coords()`: pixel to coordinate
- `get_h_line()`, `get_v_line()`: projection lines

### Graphing Functions
```python
sin_graph = axes.get_graph(lambda x: 2 * math.sin(x), color=BLUE)
```
- Auto-samples and interpolates smoothly by default
- `use_smoothing=False` for piecewise functions
- `discontinuities=[x0]` for jumps
- `get_graph_label()` for automatic labeling

### Shapes & Construction
Common patterns:
```python
square = Square()
circle = Circle()
triangle = Triangle()
line = Line(start, end)
dot = Dot()
```

### Visual Hierarchy
- Use `VGroup` to group related elements
- `to_corner()`, `to_edge()`, `next_to()`, `shift()` for positioning
- `scale()`, `stretch()` for sizing

## Equation & Text Animations

### LaTeX with `Tex`
```python
equation = Tex(R"e^{\pi i} = -1", font_size=144)
```
- Supports full LaTeX
- Can isolate specific parts with `isolate=[R"\infty"]`
- Access parts by substring: `equation[R"\pi"]`

### Text with `Text` / `TexText`
```python
text = Text("Hello World", font="CMU Serif", font_size=48)
```
Uses system fonts, more flexible than pure LaTeX for styling.

### String Indexing
```python
equation = Tex(R"A^2 + B^2 = C^2")
for part in equation[re.compile(r"\w\^2")]:
    self.play(FlashAround(part))
```
Powerful for highlighting terms by pattern.

### Transforming Equations
The signature 3B1B technique:
```python
self.play(TransformMatchingStrings(
    Tex(R"a^2 + b^2 = c^2"),
    Tex(R"(a+b)^2 - 2ab = c^2"),
    path_arc=PI/4,
    run_time=2,
))
```
Shows algebraic steps while maintaining visual connection between terms.

## Color Usage

From `manimlib/constants.py` and config:

### Color Palette (Manim's color system)
Standard 3B1B colors follow a graded system (A-E for light to dark):

**Blues**: `BLUE_A`, `BLUE_B`, `BLUE_C` (default BLUE), `BLUE_D`, `BLUE_E`
**Teals**: `TEAL_*`
**Greens**: `GREEN_*`
**Yellows**: `YELLOW_*` (often used for emphasis)
**Reds**: `RED_*`
**Maroons**: `MAROON_*`
**Greys**: `GREY_A` through `GREY_E`, `WHITE`, `BLACK`

### Color Philosophy
- **BLUE/GREEN**: Often represent "positive" or "constructive" elements
- **RED/MAROON**: Often represent "negative", "subtractive", or warnings
- **YELLOW**: Primary emphasis color (see `Indicate` default)
- **GREY**: Background elements, axes, less important details
- **Pure colors**: `PURE_RED`, `PURE_GREEN`, `PURE_BLUE` for specific needs

### Usage Patterns
```python
mobject.set_color(BLUE)
mobject.set_fill(color=BLUE_E, opacity=1)
mobject.set_stroke(color=WHITE, width=2)
```

## Typography

### Font Selection
3Blue1Brown typically uses:
- **CMU Serif**: For body text and mathematical exposition
- **Computer Modern**: Via LaTeX for equations
- **Sans-serif**: Occasionally for UI elements

```python
text = Text("3Blue1Brown", font="CMU Serif", weight=BOLD)
```

### Sizing
- Equations often use larger font sizes (`font_size=72`, `144`)
- Explanatory text varies by hierarchy
- Use `height` parameter as alternative sizing

### LaTeX Configuration
Fonts and rendering configured via `manim_config.tex`. The system uses `latex_to_svg()` pipeline.

## Graphing & Coordinate Systems

### Advanced Patterns
```python
# Track point on graph
dot = Dot()
dot.add_updater(lambda d: d.move_to(axes.i2gp(x_tracker.get_value(), graph)))
x_tracker = ValueTracker(initial_x)
self.play(x_tracker.animate.set_value(final_x), run_time=3)
```

### Projection Lines
```python
h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))
```
Creates connecting lines that update dynamically.

### Vertical/Horizontal Lines
Useful for showing relationships between values.

## 3D Visualization

From example scenes:

```python
# 3D surfaces
sphere = Sphere(radius=3)
surface = TexturedSurface(sphere, day_texture, night_texture)
self.play(ShowCreation(surface.mesh))

# Camera movement in 3D
self.play(
    Transform(surface, other_surface),
    self.frame.animate.increment_phi(-10 * DEG),
    self.frame.animate.increment_theta(-20 * DEG),
)
```

### 3D Patterns
- Use `Sphere`, `Cube`, `Surface`, etc.
- Camera can rotate with phi/theta (spherical coordinates)
- Add continuous rotation with updaters
- Light source can be moved and animated
- `fix_in_frame()` keeps text/UI elements facing camera

### 3D Best Practices
```python
light_text.fix_in_frame()  # Text stays oriented to camera
drag_text.fix_in_frame()
```

## Best Practices & Patterns

### Scene Structure
```python
class MyScene(Scene):
    def construct(self):
        # 1. Create objects
        mobject = Text("Hello")
        
        # 2. Animate introduction
        self.play(Write(mobject))
        self.wait()
        
        # 3. Transform/explain
        self.play(mobject.animate.shift(RIGHT))
        
        # 4. Clean up
        self.wait()
        self.play(FadeOut(mobject))
```

### Animation Timing
- Use `wait()` for pauses to let viewer absorb
- `lag_ratio` controls staggering (lower = more simultaneous, higher = more sequential)
- `run_time` typically 1-3 seconds for most animations
- Longer for complex transformations

### Chaining Animations
```python
self.play(
    ShowCreation(graph),
    Write(label),
    run_time=2,
)
```
Run multiple animations simultaneously.

### Succession vs Parallel
```python
from manimlib.animation.composition import Succession, LaggedStart
self.play(Succession(anim1, anim2))  # One after another
self.play(LaggedStartMap(FadeIn, group, lag_ratio=0.1))  # Staggered
```

### Performance Tips
- Use `VGroup` for related objects
- Clear updaters when no longer needed: `mobject.clear_updaters()`
- `remove()` objects not needed

### The 3B1B "Look"
Key signature elements:
1. **Smooth morphing** over cutting - use `TransformMatching*` liberally
2. **Progressive reveal** - build complexity step by step
3. **Color coding** - assign meaning to colors and stick to it
4. **Camera work** - zoom/pan to guide focus
5. **Equation manipulation** - show algebra transforming smoothly
6. **Geometric intuition** - ground abstract in shapes/diagrams
7. **Deliberate pacing** - wait after important reveals
8. **Updaters for relationships** - show dependencies dynamically

### Common Code Patterns

**Moving camera to focus on element:**
```python
self.play(self.camera.frame.animate.scale(0.5).move_to(important_part))
self.wait()
self.play(self.camera.frame.animate.scale(2).move_to(ORIGIN))
```

**Braces and annotations that track:**
```python
brace = always_redraw(Brace, group, DOWN)
text = always_redraw(lambda: TexText(f"Sum = ...").next_to(brace, DOWN))
```

**Function graph animation:**
```python
graph = axes.get_graph(func)
self.play(ShowCreation(graph))
dot = Dot().move_to(axes.i2gp(x0, graph))
self.add(dot)
x_tracker = ValueTracker(x0)
dot.add_updater(lambda d: d.move_to(axes.i2gp(x_tracker.get_value(), graph)))
self.play(x_tracker.animate.set_value(x1), run_time=3)
```

## References

- [3Blue1Brown Manim Repository](https://github.com/3b1b/manim)
- [Manim Documentation](https://3b1b.github.io/manim/)
- [3Blue1Brown YouTube Channel](https://www.youtube.com/@3blue1brown)
