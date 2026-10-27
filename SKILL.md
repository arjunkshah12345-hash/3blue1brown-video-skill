---
name: 3blue1brown-video
description: Create 3Blue1Brown-style educational animations with narrative storytelling, visual metaphors, and Manim-like programmatic animation. Generates explainer videos with the signature question-driven storytelling, smooth transforms, and elegant math/CS visualizations.
user-invocable: true
argument-hint: [TOPIC=<value>] [AUDIENCE=<value>]
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

The scratch workspace contains a comprehensive example library at:
`/Users/arjunkshah21/.t3/scratch/2026-10-25-do-deep-research-on-3blue1brown-164b076f/examples/`

### Available Examples
- **01_morphing_equations.py** - Euler's identity derivation, Pythagorean theorem rearrangement using TransformMatchingTex
- **02_winding_circles.py** - Fourier series / Gibbs phenomenon with winding circles, updaters
- **03_vector_transformations.py** - Shear, rotation, scaling with determinant visualization

### Supporting Library (b3b/)
- `palette.py` - 3B1B color scheme
- `style.py` - Base scene classes with narration helpers
- `animations.py`, `camera.py`, `fourier.py`, `graphing.py` - Reusable utilities

### Documentation
- `docs/3blue1brown_animation_techniques.md` - Deep dive into Manim patterns
- `docs/3blue1brown_narration_techniques.md` - Script writing, pacing, narrative structure analysis

Use these as reference implementations for creating authentic 3Blue1Brown-style animations.

## Audio & Narration

3Blue1Brown videos have voiceover narration that follows specific patterns:

### Voice Characteristics
- Conversational, thoughtful tone (like explaining to a friend)
- Measured pacing with natural pauses
- Uses questions and thinking-out-loud phrasing
- Subtle enthusiasm without being over-dramatized
- Clear articulation, intellectual but accessible

### Adding Audio to Manim
```python
from manim import *
class SceneWithAudio(Scene):
    def construct(self):
        self.add_sound("narration.wav")
        # animations...
```

### TTS Options
- **Coqui XTTS** - Local, natural voice cloning
- **ElevenLabs** - High quality, API-based
- **Google TTS / Azure TTS** - Cloud options
- **pyttsx3** - Simple offline TTS
- **Tortoise TTS** - Very natural but slower

### Narration Script Generation
Follow the patterns from research:
- Write in second-person where possible ("you might notice...")
- Use long sentences with natural clauses
- Ask questions at structural joints
- Use "let's" sparingly (mostly for camera/directing)
- Say "notice that..." to draw attention
- Build anticipation, then reveal
- Pause after key insights

### Workflow with Audio
1. Generate narration script following 3B1B patterns
2. Generate audio via TTS
3. Time animations to match narration beats
4. Add pauses/waits to sync with speech
5. Use `self.add_sound()` or combine in post with ffmpeg

```bash
# Combine video and audio with ffmpeg
ffmpeg -i video.mp4 -i narration.wav -c:v copy -c:a aac output.mp4
```
