"""Launch film for the 3Blue1Brown Video Skill.

The film follows the skill's own arc: a question, a discovery that makes the
product's case by *being* the product (a growing-square proof that
d/dx x^2 = 2x), then the reveal that an agent wrote it from one sentence.

    manim render -r 1920,1080 --frame_rate 60 launch_film.py LaunchFilm

Sound is built in: felt-piano score, cue sounds on each beat (see
``b3b/audio.py``).  Nothing to install; the MP4 comes out with audio.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import (
    DEGREES,
    DOWN,
    LEFT,
    ORIGIN,
    PI,
    RIGHT,
    TAU,
    UL,
    UP,
    AddTextLetterByLetter,
    AnimationGroup,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    NumberPlane,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    ShowPassingFlash,
    Square,
    Succession,
    Tex,
    Text,
    TracedPath,
    Transform,
    TransformMatchingTex,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
    linear,
    smooth,
    there_and_back,
)

from b3b import (
    B3BMovingCameraScene,
    EpicycleChain,
    axes_3b1b,
    palette,
    partial_sum,
    square_wave_harmonics,
)

MONO = "Menlo"


def panel(width: float, height: float) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        stroke_color=palette.MUTED,
        stroke_width=1.4,
        stroke_opacity=0.6,
    )


class LaunchFilm(B3BMovingCameraScene):
    def construct(self) -> None:
        self.hook()
        self.growing_square()
        self.the_reveal()
        self.the_arc()
        self.the_pipeline()
        self.the_library()
        self.end_card()
        self.score()

    # ------------------------------------------------------------------
    # Act 1: the question
    # ------------------------------------------------------------------
    def hook(self) -> None:
        question = Tex(
            r"What makes an explanation \textit{click}?",
            font_size=64,
            color=palette.INK,
        )
        self.cue("pluck", note=69)
        self.play(Write(question), run_time=2.0)
        self.wait(1.4)

        derivative = MathTex(
            r"\frac{d}{dx}", r"x^2", "=", r"2x", font_size=96
        )
        derivative[1].set_color(palette.BLUE)
        derivative[3].set_color(palette.GREEN)
        self.cue("pluck", note=74)
        self.play(
            FadeOut(question, shift=UP * 0.4),
            FadeIn(derivative, shift=UP * 0.4),
            run_time=1.2,
        )
        self.say(r"A formula tells you \textit{what} is true.")
        self.wait(1.6)
        self.say(r"A picture can tell you \textit{why}.")
        self.cue("whoosh", length=1.2)
        self.play(
            derivative.animate.scale(0.55).to_corner(UL, buff=0.6),
            run_time=1.2,
        )
        self.derivative = derivative

    # ------------------------------------------------------------------
    # Act 2a: the discovery (the product, demonstrated)
    # ------------------------------------------------------------------
    def growing_square(self) -> None:
        side = 3.2
        dx = 0.55
        origin = np.array([-5.0, -2.1, 0.0])

        sq = Square(side_length=side)
        sq.set_stroke(palette.BLUE, 3).set_fill(palette.BLUE, 0.35)
        sq.move_to(origin + np.array([side / 2, side / 2, 0]))

        x_bottom = MathTex("x", font_size=44, color=palette.BLUE)
        x_bottom.next_to(sq, DOWN, buff=0.2)
        x_left = MathTex("x", font_size=44, color=palette.BLUE)
        x_left.next_to(sq, LEFT, buff=0.2)
        area = MathTex("x^2", font_size=56, color=palette.INK).move_to(sq)

        self.cue("pluck", note=66)
        self.play(GrowFromCenter(sq), run_time=1.2)
        self.play(
            LaggedStart(
                Write(x_bottom), Write(x_left), Write(area), lag_ratio=0.3
            ),
            run_time=1.4,
        )
        self.say(r"Picture $x^2$ as the area of a square.", spoken="Picture x squared as the area of a square.")
        self.wait(0.8)

        right_strip = Rectangle(width=dx, height=side)
        right_strip.set_stroke(palette.GREEN, 2.5).set_fill(palette.GREEN, 0.45)
        right_strip.next_to(sq, RIGHT, buff=0)
        top_strip = Rectangle(width=side, height=dx)
        top_strip.set_stroke(palette.GREEN, 2.5).set_fill(palette.GREEN, 0.45)
        top_strip.next_to(sq, UP, buff=0)
        corner = Square(side_length=dx)
        corner.set_stroke(palette.ACCENT, 2.5).set_fill(palette.ACCENT, 0.55)
        corner.next_to(right_strip, UP, buff=0)

        dx_right = MathTex("dx", font_size=36, color=palette.GREEN)
        dx_right.next_to(right_strip, DOWN, buff=0.2)
        dx_top = MathTex("dx", font_size=36, color=palette.GREEN)
        dx_top.next_to(top_strip, LEFT, buff=0.2)

        self.say(r"Nudge $x$ by a tiny amount, $dx$.", spoken="Nudge x by a tiny amount, d x.")
        self.cue("pluck", note=71)
        self.play(
            FadeIn(right_strip, shift=LEFT * 0.3),
            FadeIn(top_strip, shift=DOWN * 0.3),
            FadeIn(corner, scale=0.6),
            Write(dx_right),
            Write(dx_top),
            run_time=1.6,
        )
        self.wait(0.6)

        change = MathTex(
            r"d(x^2)", "=", r"x\,dx", "+", r"x\,dx", "+", r"(dx)^2",
            font_size=50,
        )
        change.to_edge(RIGHT, buff=0.55).shift(UP * 0.4)
        change[2].set_color(palette.GREEN)
        change[4].set_color(palette.GREEN)
        change[6].set_color(palette.ACCENT)

        self.say("How much new area did we add?")
        self.play(Write(change[0:2]), run_time=0.9)
        self.cue("pluck", note=74)
        self.cue("pluck", note=76, offset=0.75)
        self.play(
            ReplacementTransform(right_strip.copy(), change[2]),
            Write(change[3]),
            ReplacementTransform(top_strip.copy(), change[4]),
            run_time=1.5,
        )
        self.cue("pluck", note=78)
        self.play(
            Write(change[5]),
            ReplacementTransform(corner.copy(), change[6]),
            run_time=1.1,
        )
        self.wait(0.8)

        # Zoom into the corner: the "aha".
        frame = self.camera.frame
        frame.save_state()
        self.say(r"That corner is tiny squared. It vanishes.")
        self.cue("whoosh", length=2.0)
        self.play(
            frame.animate.scale(0.32).move_to(corner),
            run_time=2.0,
        )
        self.play(corner.animate.scale(0.25, about_edge=DOWN + LEFT), run_time=1.4)
        self.play(FadeOut(corner), run_time=0.6)
        self.cue("whoosh", length=1.8, rising=False)
        self.play(frame.animate.restore(), run_time=1.8)

        approx = MathTex(r"d(x^2)", r"\approx", r"2x\,dx", font_size=50)
        approx[2].set_color(palette.GREEN)
        approx.move_to(change)
        self.play(
            change[6].animate.set_opacity(0.25),
            change[5].animate.set_opacity(0.25),
            run_time=0.6,
        )
        self.play(
            TransformMatchingTex(change, approx, path_arc=-20 * DEGREES),
            run_time=1.4,
        )

        final = MathTex(r"\frac{d(x^2)}{dx}", "=", r"2x", font_size=60)
        final[2].set_color(palette.GREEN)
        final.move_to(approx)
        self.say("Two thin strips. That is the whole derivative.")
        self.play(TransformMatchingTex(approx, final), run_time=1.4)
        box = RoundedRectangle(
            width=final.width + 0.6,
            height=final.height + 0.45,
            corner_radius=0.12,
            stroke_color=palette.ACCENT,
            stroke_width=3,
        ).move_to(final)
        self.cue("chime", note=81)
        self.play(Create(box), Indicate(self.derivative, color=palette.ACCENT), run_time=1.2)
        self.wait(1.6)

        self.clear_caption()
        self.play(
            *[
                FadeOut(m)
                for m in (
                    sq, x_bottom, x_left, area, right_strip, top_strip,
                    dx_right, dx_top, final, box, self.derivative,
                )
            ],
            run_time=1.0,
        )

    # ------------------------------------------------------------------
    # Act 2b: the reveal
    # ------------------------------------------------------------------
    def the_reveal(self) -> None:
        lead = Tex(
            r"That clip was written by an agent,\\ from one sentence.",
            font_size=52,
            color=palette.INK,
        ).shift(UP * 1.4)
        self.play(Write(lead), run_time=2.0)

        chevron = Text(">", font=MONO, font_size=30, color=palette.BLUE)
        prompt = Text(
            "make a 3b1b-style video on why d/dx x² = 2x",
            font=MONO,
            font_size=28,
            color=palette.CREAM,
        )
        prompt.next_to(chevron, RIGHT, buff=0.3)
        VGroup(chevron, prompt).move_to(DOWN * 0.6)
        bar = RoundedRectangle(
            width=chevron.width + prompt.width + 1.6, height=1.05,
            corner_radius=0.22, stroke_color=palette.BLUE, stroke_width=2,
        ).set_fill("#0b1418", 1).move_to(VGroup(chevron, prompt)).shift(RIGHT * 0.1)
        self.play(FadeIn(bar, shift=UP * 0.2), FadeIn(chevron), run_time=0.8)
        self.cue("keys", count=len(prompt.text.replace(" ", "")), spacing=0.045)
        self.play(AddTextLetterByLetter(prompt, time_per_char=0.045))
        cursor = Rectangle(width=0.14, height=0.42, stroke_width=0).set_fill(palette.BLUE, 1)
        cursor.next_to(prompt, RIGHT, buff=0.08)
        self.add(cursor)
        for _ in range(2):
            self.wait(0.35)
            cursor.set_opacity(0)
            self.wait(0.35)
            cursor.set_opacity(1)
        self.wait(0.4)

        title = Tex(r"3Blue1Brown Video Skill", font_size=84, color=palette.INK)
        rule = Line(LEFT, RIGHT, color=palette.ACCENT, stroke_width=3)
        rule.match_width(title).next_to(title, DOWN, buff=0.22)
        sub = Tex(
            r"an agent skill for explainers that \textit{show} before they \textit{tell}",
            font_size=36,
            color=palette.CREAM,
        ).next_to(rule, DOWN, buff=0.3)
        card = VGroup(title, rule, sub).move_to(ORIGIN)

        self.cue("rise", length=0.9)
        self.play(
            FadeOut(VGroup(lead, bar, chevron, prompt, cursor), shift=UP * 0.3),
            run_time=0.8,
        )
        self.cue("thump")
        self.play(Write(title), Create(rule), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(card), run_time=0.8)

    # ------------------------------------------------------------------
    # Act 2c: the arc every video follows
    # ------------------------------------------------------------------
    def the_arc(self) -> None:
        axes = axes_3b1b(
            x_range=(0, 10, 1),
            y_range=(0, 6, 1),
            width=10.5,
            height=4.6,
            x_label=r"\text{time}",
            y_label=r"\text{curiosity}",
        ).shift(DOWN * 0.35)

        def curiosity(t: float) -> float:
            hook = 2.6 * np.exp(-((t - 0.9) ** 2) / 0.35)
            climb = 0.9 + 0.42 * t
            steps = sum(0.55 / (1 + np.exp(-(t - c) * 7)) for c in (3.4, 5.4, 7.2))
            settle = -1.3 / (1 + np.exp(-(t - 9.0) * 5))
            return hook * 0.55 + climb + steps + settle

        acts = [
            (0.0, 2.0, palette.BLUE, r"Question"),
            (2.0, 8.0, palette.GREEN, r"Discovery"),
            (8.0, 10.0, palette.ACCENT, r"Insight"),
        ]
        curves = VGroup()
        fills = VGroup()
        labels = VGroup()
        for a, b, color, name in acts:
            g = axes.plot(curiosity, x_range=[a, b], color=color, stroke_width=5)
            curves.add(g)
            fills.add(
                axes.get_area(g, x_range=[a, b], color=color, opacity=0.16)
            )
            lab = Tex(name, font_size=34, color=color)
            lab.move_to(axes.c2p((a + b) / 2, 0.55))
            labels.add(lab)

        self.cue("pluck", note=62)
        self.play(Create(axes), run_time=1.3)
        self.say("Every video it writes follows the same arc.")
        tracer = Dot(radius=0.09, color=palette.INK)
        tracer.move_to(axes.c2p(0, curiosity(0)))
        self.add(tracer)
        for note, curve, fill, lab in zip((66, 69, 74), curves, fills, labels):
            self.cue("pluck", note=note)
            self.play(
                Create(curve, rate_func=linear),
                FadeIn(fill),
                FadeIn(lab, shift=UP * 0.15),
                tracer.animate(rate_func=linear).move_to(curve.get_end()),
                run_time=1.6 if curve is not curves[1] else 2.6,
            )

        ahas = VGroup()
        for c in (3.4, 5.4, 7.2):
            p = axes.c2p(c + 0.15, curiosity(c + 0.15))
            ahas.add(Dot(p, radius=0.07, color=palette.ACCENT))
        aha_label = Tex(r"aha moments", font_size=30, color=palette.ACCENT)
        aha_label.next_to(ahas[1], UP, buff=0.45)
        self.say(r"Hook in the first 20\%. Aha moments, spaced out. Then pay it off.")
        for i, note in enumerate((78, 81, 83)):
            self.cue("chime" if i == 2 else "pluck", note=note, offset=0.26 * i)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in ahas], lag_ratio=0.3),
            FadeIn(aha_label, shift=DOWN * 0.1),
            run_time=1.4,
        )
        self.wait(2.0)
        self.clear_caption()
        self.play(
            FadeOut(VGroup(axes, curves, fills, labels, tracer, ahas, aha_label)),
            run_time=0.9,
        )

    # ------------------------------------------------------------------
    # Act 2d: what the agent actually does
    # ------------------------------------------------------------------
    def the_pipeline(self) -> None:
        steps = [
            ("Question", "find the aha", palette.BLUE),
            ("Script", "spoken, curious", palette.TEAL),
            ("Storyboard", "one idea per beat", palette.GREEN),
            ("Manim", "python scenes", palette.GOLD),
            ("Render", "mp4", palette.ACCENT),
        ]
        nodes = VGroup()
        for name, hint, color in steps:
            box = RoundedRectangle(
                width=2.25, height=1.15, corner_radius=0.16,
                stroke_color=color, stroke_width=2.5,
            ).set_fill(color, 0.08)
            t = Tex(name, font_size=34, color=palette.INK).move_to(box)
            h = Tex(hint, font_size=24, color=palette.MUTED)
            h.next_to(box, DOWN, buff=0.22)
            nodes.add(VGroup(box, t, h))
        nodes.arrange(RIGHT, buff=0.42).shift(UP * 0.2)

        arrows = VGroup(
            *[
                Arrow(
                    nodes[i][0].get_right(),
                    nodes[i + 1][0].get_left(),
                    buff=0.06,
                    stroke_width=3,
                    color=palette.AXIS,
                    max_tip_length_to_length_ratio=0.35,
                )
                for i in range(len(nodes) - 1)
            ]
        )

        self.say("From a sentence to a rendered video, in five steps.")
        for i, note in enumerate((62, 66, 69, 74, 78)):
            self.cue("pluck", note=note, offset=0.44 * i)
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(FadeIn(n, shift=UP * 0.2), *( [Create(arrows[i - 1])] if i else []))
                    for i, n in enumerate(nodes)
                ],
                lag_ratio=0.35,
            ),
            run_time=3.0,
        )

        spark = Line(
            nodes[0][0].get_center(), nodes[-1][0].get_center(),
            color=palette.ACCENT, stroke_width=6,
        ).shift(UP * 0.62)
        self.cue("whoosh", length=1.6)
        self.play(
            ShowPassingFlash(spark, time_width=0.35),
            LaggedStart(
                *[Indicate(n[0], color=steps[i][2], scale_factor=1.06) for i, n in enumerate(nodes)],
                lag_ratio=0.25,
            ),
            run_time=2.4,
        )
        self.say("Your agent does all of it. You just ask.")
        self.wait(1.6)
        self.clear_caption()
        self.play(FadeOut(VGroup(nodes, arrows)), run_time=0.8)

    # ------------------------------------------------------------------
    # Act 2e: the pattern library
    # ------------------------------------------------------------------
    def the_library(self) -> None:
        w, h = 4.2, 3.3
        frames = VGroup(panel(w, h), panel(w, h), panel(w, h))
        frames.arrange(RIGHT, buff=0.35).shift(UP * 0.35)
        names = VGroup(
            Tex("Fourier series", font_size=30, color=palette.CREAM),
            Tex("Linear maps", font_size=30, color=palette.CREAM),
            Tex("Equation morphs", font_size=30, color=palette.CREAM),
        )
        for n, f in zip(names, frames):
            n.next_to(f, DOWN, buff=0.22)

        self.say("Built on a library of the channel's signature moves.")
        for i, note in enumerate((69, 74, 78)):
            self.cue("pluck", note=note, offset=0.2 * i)
        self.play(
            LaggedStart(*[Create(f) for f in frames], lag_ratio=0.2),
            LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.2),
            run_time=1.2,
        )

        # Panel 1: epicycles drawing a square wave.
        c1 = frames[0].get_center()
        harmonics = square_wave_harmonics(count=5, base_radius=0.42)
        chain = EpicycleChain(
            harmonics, origin=c1 + LEFT * 1.1, line_stroke_width=1.8,
            circle_stroke_width=1.0, tip_radius=0.045,
        )
        phase = ValueTracker(0.01)
        wave_x0 = c1[0] - 0.1
        wave_w = 1.95

        def wave_point() -> np.ndarray:
            t = phase.get_value()
            return np.array(
                [wave_x0 + wave_w * t / (2 * TAU), c1[1] + partial_sum(t, harmonics), 0]
            )

        pen = Dot(wave_point(), radius=0.04, color=palette.ACCENT)
        pen.add_updater(lambda m: m.move_to(wave_point()))
        trail = TracedPath(
            pen.get_center, stroke_color=palette.ACCENT, stroke_width=2.4,
        )
        link = always_redraw(
            lambda: DashedLine(
                chain.tip.get_center(), pen.get_center(),
                stroke_width=0.8, stroke_opacity=0.3, color=palette.CREAM,
                dash_length=0.06,
            )
        )

        # Panel 2: a small grid under a shear.
        c2 = frames[1].get_center()
        plane = NumberPlane(
            x_range=(-2, 2, 1), y_range=(-2, 2, 1),
            x_length=4 * 0.45, y_length=4 * 0.45,
            background_line_style={
                "stroke_color": palette.BLUE_DARK, "stroke_width": 1.2,
                "stroke_opacity": 0.8,
            },
            axis_config={"stroke_color": palette.AXIS, "stroke_width": 1.5},
        ).move_to(c2)
        u = 0.45
        i_hat = Arrow(c2, c2 + RIGHT * u, buff=0, color=palette.I_HAT, stroke_width=4,
                      max_tip_length_to_length_ratio=0.3)
        j_hat = Arrow(c2, c2 + UP * u, buff=0, color=palette.J_HAT, stroke_width=4,
                      max_tip_length_to_length_ratio=0.3)
        grid = VGroup(plane, i_hat, j_hat)
        grid.set_z_index(-1)

        # Panel 3: Euler's identity, symbols travelling.
        c3 = frames[2].get_center()
        e1 = MathTex(r"e^{i\pi}", "+", "1", "=", "0", font_size=54).move_to(c3)
        e1[0].set_color(palette.BLUE)
        e1[2].set_color(palette.GREEN)
        e1[4].set_color(palette.ACCENT)
        e2 = MathTex(r"e^{i\pi}", "=", "-1", font_size=54).move_to(c3)
        e2[0].set_color(palette.BLUE)
        e2[2].set_color(palette.GREEN)

        self.play(
            Create(chain), FadeIn(grid), Write(e1), run_time=1.2,
        )
        chain.follow(phase)
        self.add(trail, pen, link)

        shear = np.array([[1.0, 1.0], [0.0, 1.0]])
        self.play(
            phase.animate(rate_func=linear).set_value(TAU * 1.25),
            Succession(
                grid.animate(run_time=2.2).apply_matrix(shear, about_point=c2),
                TransformMatchingTex(e1, e2, path_arc=30 * DEGREES, run_time=1.8),
                grid.animate(run_time=1.8).apply_matrix(
                    np.linalg.inv(shear) @ np.array([[0.0, -1.0], [1.0, 0.0]]),
                    about_point=c2,
                ),
            ),
            run_time=6.0,
        )
        self.say(r"Palette, pacing, camera, captions: all baked in.")
        self.play(phase.animate(rate_func=linear).set_value(TAU * 1.99), run_time=2.6)

        chain.clear_updaters()
        pen.clear_updaters()
        self.clear_caption()
        self.play(
            FadeOut(VGroup(frames, names, chain, pen, trail, link, grid, e2)),
            run_time=0.9,
        )

    # ------------------------------------------------------------------
    # Act 3: the end card
    # ------------------------------------------------------------------
    def end_card(self) -> None:
        ring = Circle(radius=0.75, color=palette.BLUE, stroke_width=4)
        ring.shift(UP * 1.6)
        angle = ValueTracker(PI / 2)
        tip = Dot(radius=0.1, color=palette.ACCENT)
        tip.add_updater(
            lambda m: m.move_to(
                ring.get_center()
                + 0.75 * np.array([np.cos(angle.get_value()), np.sin(angle.get_value()), 0])
            )
        )
        spoke = always_redraw(
            lambda: Line(ring.get_center(), tip.get_center(), color=palette.BLUE_LIGHT, stroke_width=3)
        )
        trail = TracedPath(tip.get_center, stroke_color=palette.ACCENT, stroke_width=4, dissipating_time=0.9)

        title = Tex(r"3Blue1Brown Video Skill", font_size=76, color=palette.INK)
        title.next_to(ring, DOWN, buff=0.6)
        tagline = Tex(r"Show it. Then name it.", font_size=40, color=palette.ACCENT)
        tagline.next_to(title, DOWN, buff=0.3)
        ask = Text(
            "“make a 3b1b-style video on ...”",
            font=MONO, font_size=26, color=palette.CREAM,
        ).next_to(tagline, DOWN, buff=0.55)
        fine = Tex(
            r"Unofficial. Inspired by Grant Sanderson's 3Blue1Brown. Built on Manim.",
            font_size=26,
            color=palette.MUTED,
        ).to_edge(DOWN, buff=0.4)

        self.cue("pluck", note=62)
        self.play(Create(ring), run_time=1.0)
        self.add(spoke, trail, tip)
        self.cue("thump")
        self.play(
            angle.animate(rate_func=smooth).set_value(PI / 2 + TAU),
            Write(title),
            run_time=2.0,
        )
        self.cue("chime", note=81)
        self.play(FadeIn(tagline, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(ask, shift=UP * 0.1), FadeIn(fine), run_time=0.9)
        self.play(
            angle.animate(rate_func=smooth).set_value(PI / 2 + 2 * TAU),
            run_time=2.6,
        )
        self.wait(1.2)
        tip.clear_updaters()
        self.play(
            FadeOut(VGroup(ring, spoke, tip, trail, title, tagline, ask, fine)),
            run_time=1.2,
        )
        self.wait(0.4)
