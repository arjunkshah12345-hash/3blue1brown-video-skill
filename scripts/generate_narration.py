#!/usr/bin/env python3
"""
Generate 3Blue1Brown-style narration scripts
"""
import sys

def generate_script(topic):
    script = f"""# Narration script for: {topic}

[INTRODUCTION - Hook]
"Suppose I were to ask you: what exactly do we mean when we talk about {topic}? 
It seems simple enough at first glance, but there might be more to it than meets the eye."

[SETUP - Build curiosity]
"Let's think about this from a visual perspective. Rather than jumping straight 
to formulas, maybe it's better to start with something concrete that you can see."

[EXPLORATION - Discovery]
"Now notice what happens as we make this change..."
"As you can see, something interesting emerges..."
"Here's the key insight..."

[RESOLUTION - Conclusion]
"So putting it all together, what we see is..."
"This is why {topic} is so beautiful - it connects geometry and algebra in this elegant way."
"""
    return script

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "the derivative"
    print(generate_script(topic))
