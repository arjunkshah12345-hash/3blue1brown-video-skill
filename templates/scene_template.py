from manim import *

class TemplateScene(Scene):
    def construct(self):
        # HOOK - Start with a question
        question = Text("But why does this happen?", font_size=48)
        self.play(Write(question))
        self.wait(2)
        self.play(FadeOut(question))
        
        # SETUP - Show the visual/object
        # Build intuition here
        
        # EXPLORATION - Step by step discovery
        # Transform and reveal
        
        # RESOLUTION - Connect back to question
        conclusion = Text("And that's the key insight.", font_size=36)
        self.play(Write(conclusion))
        self.wait(3)
