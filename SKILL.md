---
name: 3blue1brown-video
description: Create 3Blue1Brown-style educational animations with narrative storytelling, visual metaphors, and Manim-like programmatic animation. Generates explainer videos with the signature question-driven storytelling, smooth transforms, and elegant math/CS visualizations.
user-invocable: true
argument-hint: "[TOPIC=<value>] [AUDIENCE=<value>]"
---

# 3Blue1Brown Video Creator

Create high-quality educational explainer animations in the style of 3Blue1Brown - combining precise visualizations, narrative storytelling, and elegant mathematical exposition.

## Core Philosophy

3Blue1Brown's approach is fundamentally different from typical math tutorials:

1. **Visual-first understanding** - Start with intuition and geometric intuition before formal definitions
2. **Question-driven narrative** - Every video asks a compelling question and answers it through discovery
3. **Smooth, purposeful animation** - Nothing moves without reason; every transform reveals something
4. **Metaphors and analogies** - Complex ideas become concrete through relatable visual metaphors
5. **Discovery over exposition** - Guide viewers to "aha moments" rather than just telling them
6. **Elegance and minimalism** - Clean visuals, uncluttered frames, beautiful typography

## Story Structure (Signature Pattern)

Follow the 3Blue1Brown narrative arc:

### Act 1: The Question/Mystery (0-20%)
- **Hook**: Start with a puzzling question, paradox, or real-world curiosity
- **Context**: Establish why this matters or why it's interesting
- **Setup**: Show the visual/object of interest before explaining formally

### Act 2: Exploration/Discovery (20-80%)
- **Intuition building**: Use concrete examples and visual analogies
- **Step by step revelation**: Break complex ideas into digestible visual steps
- **Interleave visual and verbal**: Animation and narration reinforce each other
- **Build complexity gradually**: Start simple, add layers as understanding grows
- **Aha moments**: Create moments where the visualization clicks

### Act 3: Resolution/Insight (80-100%)
- **Synthesis**: Connect back to the original question
- **Generalization**: Show broader implications or applications
- **Elegant conclusion**: Leave with a beautiful insight or visual
- **Optional**: Tease related ideas without overexplaining

## Animation Principles

### Visual Language
- **Color palette**: Primarily blues/oranges/teals, high contrast, purposeful color coding
- **Typography**: Clean sans-serif, equations rendered beautifully
- **Minimal UI**: No distracting elements, focus on the math/visual
- **Consistent style**: Objects have coherent visual identity

### Motion Design
- **Smooth transforms**: Morph between representations seamlessly
- **Purposeful movement**: Every animation serves to illuminate
- **Pacing**: Slow when building intuition, faster for obvious steps
- **Camera work**: Pan, zoom, focus attention without disorientation
- **Layering**: Build up complexity gradually by adding elements
- **Emphasis**: Highlight key elements through color/scale/movement

### Mathematical Visualization
- **Geometric intuition**: Show shapes, areas, vectors, transformations
- **Coordinate systems**: Use grids, axes elegantly
- **Equations as objects**: Animate terms appearing/moving/translating
- **Connections**: Draw lines/paths to show relationships
- **Scale and perspective**: Reveal patterns at different scales

## Manim Workflow

This skill generates Manim code (Python) following 3Blue1Brown's patterns.

### Scene Structure
```python
from manim import *
class VideoScene(Scene):
    def construct(self):
        # 1. Hook
        # 2. Build up
        # 3. Reveal
        # 4. Conclude
```

### Key Techniques
- **Write**: Show equations/labels appearing naturally
- **Transform**: Morph objects to show equivalence
- **MoveToTarget**: Orchestrate complex animations
- **Create/Uncreate**: Add/remove elements cleanly
- **Focus**: Use zoom/scale to direct attention
- **SurroundingRectangle**: Highlight important parts
- **AnimationGroup/lag_ratio**: Stagger animations for flow

### Narrative Writing
- Write narration in spoken, conversational tone
- Use questions to guide: "But why does this happen?"
- Build anticipation before reveals
- Define terms only when needed, show first
- Use concrete numbers/examples before abstractions

## Implementation Steps

When creating a 3blue1brown-style video:

1. **Research & outline**
   - Understand the core concept deeply
   - Identify the "aha moment" to build toward
   - Find compelling visual metaphors
   - Outline the narrative arc

2. **Script writing**
   - Write hook/question
   - Plan visual beats for each narration segment
   - Time narration with visual changes
   - Keep explanations conversational

3. **Storyboard**
   - Sketch key frames/visuals
   - Plan transitions between scenes
   - Identify what to animate vs show statically

4. **Manim implementation**
   - Create scene classes
   - Build animations beat by beat
   - Add text, equations, shapes
   - Polish timing and pacing

5. **Review & iterate**
   - Check: Does every animation illuminate?
   - Check: Is the narrative compelling?
   - Check: Does it build intuition naturally?
   - Check: Is it visually elegant?

## Best Practices
- **Show, don't tell** - If you can visualize it, animate it
- **One idea per beat** - Don't overwhelm
- **Restraint** - Less animation often more powerful
- **Beauty matters** - Craft each frame with care
- **Pedagogy first** - Accuracy and clarity over flashiness

## Tools & Resources
- **ManimGL** (3b1b's version): https://github.com/3b1b/manim
- **Manim Community**: https://www.manim.community/
- **3Blue1Brown**: https://www.3blue1brown.com/

## Advanced Techniques

### The "Winding" Pattern (Fourier Transform Style)
- Start with a concrete curve/signal
- Introduce complex numbers/rotation metaphor
- Show winding at different frequencies
- Center of mass reveals frequency content
- Build up to Fourier transform formula

### The "Transformation" Pattern (Linear Algebra Style)
- Start with geometric objects (vectors, shapes)
- Show how transformations act on basis
- Visualize the effect on entire plane
- Connect to matrix multiplication
- Reveal the geometry behind determinants/inverses

### The "Graph/Visual Derivation" Pattern
- Don't show formula first, show relationship
- Build area/visual proof step by step
- Let shapes rearrange to show equality
- Derive equation from rearranged visuals

### Camera Techniques
- Zoom in to focus on details
- Pan to follow action
- Scale entire frame to show big picture
- Move camera to guide eye
- Use `self.camera.frame` manipulation

### Color Strategy
- Use consistent color per mathematical object type
- Blue/orange often for complementary ideas
- Highlight with bright color, mute others
- Color equations by variable meaning
- Use color to track transformations

### Timing Secrets
- Pause after showing something important (2-4 seconds of thinking time)
- Don't rush transitions - let morphs complete fully
- Stagger related elements with lag_ratio
- Use longer waits before "aha" moments
- Faster pacing after intuition is established

## Manim Code Patterns

### Essential Imports
```python
from manim import *
```

### Common Patterns
```python
# Create and animate
circle = Circle()
self.play(Create(circle))
self.wait()

# Transform
square = Square()
self.play(Transform(circle, square))

# Write equation
eq = MathTex(r"E = mc^2")
self.play(Write(eq))
self.wait(2)
self.play(eq.animate.shift(UP))

# Highlight
self.play(Indicate(eq[0]))

# Camera move
self.play(self.camera.frame.animate.scale(0.5).move_to(eq))
```

### Best Practices in Code
- Break complex scenes into logical sections
- Use descriptive variable names
- Group related animations
- Add comments for narrative beats
- Test animations interactively with `-p` flag
- Keep scenes focused on one idea

## Creating Your First 3B1B-Style Video

1. **Pick a question**: What question would make someone curious?
2. **Find the visual**: What's the simplest visual that captures this?
3. **Outline beats**: Hook (10s) → Explore (60-90s) → Resolve (20-30s)
4. **Write narration**: Conversational, as if explaining to a friend
5. **Storyboard visually**: Sketch key frames
6. **Code in Manim**: Build step by step
7. **Polish timing**: Adjust waits and run_times
8. **Review**: Watch without sound first - does it tell the story visually?

## Resources
- [3Blue1Brown Channel](https://www.youtube.com/c/3blue1brown)
- [3b1b/manim (original)](https://github.com/3b1b/manim)
- [Manim Community](https://www.manim.community/)
- [Grant's blog posts about animation](https://www.3blue1brown.com/blog)

## Example Library

The skill ships its example library in `examples/` (next to this file). Render any scene with:

```bash
cd examples && manim render -r 1920,1080 --frame_rate 30 02_winding_circles.py SquareWaveEpicycles
```

Equations need LaTeX (`latex` and `dvisvgm` on PATH: MacTeX, TeX Live or TinyTeX). Render scenes one at a
time, or give each parallel job its own `--media_dir`: concurrent renders sharing one `media/Tex` cache race.

### Available Examples
- **01_morphing_equations.py** - Euler's identity derivation, Pythagorean theorem rearrangement using TransformMatchingTex
- **02_winding_circles.py** - Fourier series / Gibbs phenomenon with winding circles, updaters
- **03_vector_transformations.py** - Shear, rotation, scaling with determinant visualization
- **essence_of_derivative_simple.py** - Secant lines sliding into a tangent
- **launch_film.py** - The skill's launch film (about 100 seconds, narrated): question, growing-square proof of d/dx x² = 2x, the arc, the pipeline, a pattern montage and an end card. A full worked example of the three-act structure.

### Supporting Library (b3b/)
- `palette.py` - 3B1B color scheme
- `style.py` - Base scene classes with narration helpers
- `audio.py` - Built-in sound: procedural score, sound cues and voiceover (mixed into every b3b scene)
- `animations.py`, `camera.py`, `fourier.py`, `graphing.py` - Reusable utilities

### Documentation
- `docs/3blue1brown_animation_techniques.md` - Deep dive into Manim patterns
- `docs/3blue1brown_narration_techniques.md` - Script writing, pacing, narrative structure analysis

Use these as reference implementations for creating authentic 3Blue1Brown-style animations.

## Audio & Narration

Every b3b scene has sound built in. `b3b/audio.py` synthesises everything from numpy and scipy, then Manim mixes it into the MP4. It needs nothing that isn't already installed: no samples, no model downloads and no API keys.

### Music (automatic)
When a scene ends, a quiet felt-piano score in D major is laid under the whole scene. It plays a I-vi-IV-V progression whose arpeggios swell through the middle, then resolves on a rolled final chord timed to the scene's end. You don't need to do anything to get it.

- `self.score(bpm=56, duck_db=-14)`: call this as the last line of `construct()` to change the settings.
- `auto_score = False` on a scene class, or `B3B_SCORE=0` in the environment: render with no music.

### Sound cues
Put a cue on the beat it belongs to. `offset=` shifts it in seconds, which lets you place it partway through the next `play`.

```python
self.cue("pluck", note=74)                    # a felt-piano note; use for a dot, label or step landing
self.play(Create(dot))
self.cue("chime", note=81)                    # a bell for an "aha" or a box drawn round the answer
self.cue("whoosh", length=1.6)                # a camera move or zoom (rising=False to pull back)
self.cue("keys", count=len(text))             # typing, spaced 45 ms apart
self.cue("rise", length=1.2)                 # a build into a reveal; start it 1.2 s ahead
self.cue("thump")                             # a title landing
```

`b3b.audio.note_in_key(step, octave)` returns MIDI notes from the score's pentatonic scale, so a run of plucks (`62, 66, 69, 74, 78`) always sits in key with the music. Use cues sparingly: one per visual event, never on every `play`.

### Voiceover
When a voice is on, **every caption is spoken**. The line starts as the caption appears, and the animations keep playing underneath it. The next caption waits for the line to finish. For a caption with math in it, give the words to say:

```python
self.say(r"Picture $x^2$ as the area of a square.", spoken="Picture x squared as the area of a square.")
self.say("Two thin strips.", spoken="")            # stays silent
self.narrate("A line with no caption.")           # the same, without a caption
```

For a line that should drive an animation's length, use a block:

```python
with self.voiceover("Notice what happens as the step shrinks.") as vo:
    self.play(h_tracker.animate.set_value(0.01), run_time=vo.duration)
# The block waits until the line has finished before moving on.
```

The voice backend is set with `B3B_VOICE`:

| `B3B_VOICE` | What you get |
|---|---|
| `auto` (default) | ElevenLabs if a key is set, otherwise Kokoro if it is installed, otherwise `none` |
| `kokoro` | Open-weights Kokoro-82M, no key. `B3B_VOICE_ID` picks the voice (default `am_michael`) and `B3B_VOICE_SPEED` the pace (0.95) |
| `elevenlabs` | Real narration. `B3B_VOICE_ID` picks the voice and `B3B_VOICE_MODEL` the model (default `eleven_multilingual_v2`) |
| `say` | macOS `say`, offline. Draft quality, useful for checking timing |
| `none` | Silent. Durations are estimated at 2.6 words/s so pacing still matches the script |

When a voice is active, the score ducks about 11 dB under each line. Generated audio is cached in `media/b3b_audio/`, so re-renders are free.

### Rendering in the cloud (Kaggle)
To keep TeX, Manim and the voice model off your machine, render on a Kaggle CPU box. You only need the `kaggle` CLI, logged in. The script pushes a private kernel, installs everything there, renders the files in parallel with Kokoro narration, and downloads the MP4s:

```bash
python3 scripts/kaggle_render.py examples out/ \
    launch_film.py:LaunchFilm 02_winding_circles.py:SquareWaveEpicycles,GibbsPhenomenon
```

Add `--voice bm_george` for a British voice, or `--no-voice` for music and cues only.

### Mastering for the web
Manim's mix lands around -18 to -22 LUFS. Normalise to -16 LUFS / -1.5 dBTP. The video stream is copied untouched, and files with no audio are passed through:

```bash
scripts/master_audio.sh site/media media/videos/*/1080p60/*.mp4
```

### Writing narration
3Blue1Brown narration is conversational and thoughtful, with measured pacing and subtle enthusiasm. Follow the patterns in `docs/3blue1brown_narration_techniques.md`; `scripts/generate_narration.py` scaffolds a script.
- Write in second person where you can ("you might notice...")
- Ask questions at structural joints, then build anticipation before the reveal
- Say "notice that..." to direct attention, and pause after key insights
- Use one `voiceover` block per sentence, with the animation for that sentence inside it
