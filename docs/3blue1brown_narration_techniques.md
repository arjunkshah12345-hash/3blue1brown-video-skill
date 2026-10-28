# 3Blue1Brown Narration Techniques: How the Scripts Are Written

A close analysis of Grant Sanderson's spoken script across 14 videos (256 minutes, 45,466 words, 1,788 sentences), derived from YouTube captions plus his own account of his process. Companion to `3blue1brown_animation_techniques.md`, which covers the Manim side.

Every claim below is tied to either a measured count or a quoted line with a video ID and timestamp.

## Table of Contents
- [Method and Corpus](#method-and-corpus)
- [The Measured Shape of the Prose](#the-measured-shape-of-the-prose)
- [Finding 1: It Is Second-Person, Not "We"](#finding-1-it-is-second-person-not-we)
- [Finding 2: The Sentences Are Long](#finding-2-the-sentences-are-long)
- [Finding 3: Questions Are Structural, and Rare](#finding-3-questions-are-structural-and-rare)
- [The Four Openings](#the-four-openings)
- ["Let's" Is Not the Verb You Think It Is](#lets-is-not-the-verb-you-think-it-is)
- [Explain vs. Show: The Division of Labor](#explain-vs-show-the-division-of-labor)
- [Technique: Narrate the Viewer's Own Reasoning](#technique-narrate-the-viewers-own-reasoning)
- [Technique: Withhold, Then Pay Off](#technique-withhold-then-pay-off)
- [Technique: Pre-empt the Objection](#technique-pre-empt-the-objection)
- [Technique: Admit Imprecision Out Loud](#technique-admit-imprecision-out-loud)
- [Technique: Negative Definition](#technique-negative-definition)
- [Technique: Recap Insurance](#technique-recap-insurance)
- [The Endings](#the-endings)
- [Pacing and Silence](#pacing-and-silence)
- [The Process Behind the Prose](#the-process-behind-the-prose)
- [How the Style Changed](#how-the-style-changed)
- [A Reproducible Recipe](#a-reproducible-recipe)
- [Anti-Patterns: What He Does Not Do](#anti-patterns-what-he-does-not-do)
- [Appendix: Tables](#appendix-tables)

## Method and Corpus

Transcripts came from YouTube auto-captions, which preserve punctuation well enough for sentence-level statistics. Two videos were excluded from the quantitative analysis and are noted here so the numbers can be reproduced:

- `ga9Qk38FaHM` ("The unexpected probability result confusing everyone") is a **Stand-up Maths** video, not 3Blue1Brown. The narrator says he told the fact to Grant Sanderson. Useful as an outside control; not part of the corpus.
- `d-o3eB9sfls` (Basel problem) has unpunctuated ASR — 3,031 words and effectively no sentence boundaries — so it is quoted qualitatively only.

The 14 analysed videos:

| ID | Subject | Length |
|---|---|---|
| `WUvTyaaNkzM` | essence of calculus | 16.7 min |
| `9vKqVkMQHKk` | paradox of the derivative | 16.8 min |
| `aircAruvnKk` | what is a neural network | 18.4 min |
| `r6sGWTCMz2k` | Fourier series / drawing with circles | 24.8 min |
| `mvmuCPvRoWQ` | Euler's formula via group theory | 24.1 min |
| `3s7h2MHQtxc` | fractals and space-filling curves | 17.9 min |
| `p_di4Zn4wz4` | differential equations (pendulum) | 26.9 min |
| `wjZofJX0v4M` | transformers | 26.9 min |
| `KuXjwB4LzSA` | convolution | 22.7 min |
| `spUNpyF58BY` | Fourier transform | 19.5 min |
| `HEfHFsfGXjs` | colliding blocks compute pi | 5.2 min |
| `v0YEaeIClKY` | e^(iπ) in 3.14 minutes | 3.8 min |
| `EK32jo7i5LQ` | prime spirals | 22.3 min |
| `fNk_zzaMoSs` | what is a vector | 9.9 min |

## The Measured Shape of the Prose

Aggregate over the clean corpus:

| Metric | Value |
|---|---|
| Narration rate | **178 words/min** (range 159–204) |
| Sentence rate | **~7 sentences/min** |
| Mean sentence | **25.4 words** |
| Median sentence | **24 words** |
| p10 / p25 / p75 / p90 / p95 | 10 / 16 / 33 / 43 / 50 words |
| Longest sentence | 94 words |
| Sentences ≤ 5 words | **3.0%** |
| Sentences ≤ 8 words | 6.9% |
| Sentences ≥ 35 words | **22.3%** |
| Sentences ≥ 45 words | 8.9% |
| Questions | 94 (**5.3%** of sentences, 2.07 per 1,000 words) |
| One question every | **~163 seconds** |
| Questions that are tag questions | 14 of 94 (15%) |

For comparison, ordinary conversational English averages roughly 15–20 words per sentence. His median sentence is a third longer than that, and nearly one in four sentences runs past 35 words.

## Finding 1: It Is Second-Person, Not "We"

The usual description of 3Blue1Brown is "conversational, like a friendly lecturer using *we*." The pronoun counts say otherwise.

| Pronoun | Uses | Per 1,000 words |
|---|---|---|
| **you** (you / your / you're / you'll / you've) | 944 | **20.8** |
| I / I'm / I'll / I've | 378 | 8.3 |
| we / we're / we'll / we've | 329 | 7.2 |

He addresses the viewer **2.9× more often than he refers to himself, and 2.9× more often than he says "we."** Handing the reasoning to the viewer is not a stylistic garnish; it is the dominant grammatical mode of the scripts.

It shows up in small choices continuously:

- "**Your** position on a number line." — `v0YEaeIClKY` @ 0:20
- "The farther away from 0 **you** are, the faster **you** move." — `v0YEaeIClKY` @ 0:33
- "**You** know that **you'll** be accelerating, and at an accelerating rate." — `v0YEaeIClKY` @ 0:49
- "So just to sum up where we are, **you've** broken up the area of the circle into all of these rings, and **you're** approximating the area of each one of those…" — `WUvTyaaNkzM` @ 4:07

That last line is the tell. A lecturer summarising would say "we have broken up the area." He says *you've* — crediting the viewer with work they did not literally do, because by then the diagram has made them feel they did.

Measured: **"you've" appears 0.45 times per 1,000 words, twice as often as "we've" (0.22).**

## Finding 2: The Sentences Are Long

The common assumption about YouTube pacing — short sentences, quick cuts, no subordinate clauses — is false here, and measurably so.

Only **3% of sentences are five words or shorter**. Runs of three consecutive sentences of seven words or fewer occur **three times in 45,000 words** — twice in the 5-minute colliding-blocks video (once as the sign-off) and once in the Euler's-formula video.

Instead the rhythm is long sentence → long sentence → long sentence, with the punch delivered *inside* a sentence as a short final clause:

> "So after pi seconds you've traced a distance of pi around, **so e to the i times pi should be negative 1.**"
> — `v0YEaeIClKY` @ 3:05

> "This dt is always a finitely small non-zero value, **it's just that it approaches 0 is all.**"
> — `9vKqVkMQHKk` @ 8:53

The brevity lives in the clause, not the sentence. That is why the prose reads as dense on the page but feels unhurried when heard at 178 wpm.

Where genuinely short sentences do appear, they are almost never exposition — they are **verdicts and invitations**:

- "Clearly something fishy is afoot." — `p_di4Zn4wz4`
- "But it gets worse." — `p_di4Zn4wz4`
- "Which is pretty neat." — `KuXjwB4LzSA`
- "That's really cool to me." — `KuXjwB4LzSA`
- "Why is that?" / "Here, let's compute it." — `EK32jo7i5LQ`
- "It's weird, isn't it?" / "I think that's really clever." / "Do you see the paradox?" — `9vKqVkMQHKk`
- "And its thickness?" — `WUvTyaaNkzM` @ 3:08

Note "**And its thickness?**" — a two-word fragment used as a paragraph pivot. The preceding sentence explained the rectangle's width; instead of a transition sentence, he asks a question of the object itself and answers it next: "Well, that depends on how finely you chopped up the circle in the first place."

## Finding 3: Questions Are Structural, and Rare

94 questions in 256 minutes — **one every 2 minutes 43 seconds**. They are not filler to keep attention; they mark structural joints. Five types recur:

**1. The naive-viewer question** — states what the audience half-knows, then finds the hole.
> "One way to think about the function e to the t is to ask what properties does it have?"
> — `v0YEaeIClKY` @ 0:00 (this is the entire opening line of the video)

**2. The dramatised question, delivered by a fictional colleague.** He stages a character who exists only to be asked, and lets her carry the exposition as dialogue.
> "When you tell your mathematician friend about this idea, she says, why not use a Hilbert curve? **When you ask her what that is, she stumbles for a moment.** So it's not a curve, but an infinite family of curves. She starts, well no, it's just one thing, but I need to tell you about a certain infinite family first."
> — `3s7h2MHQtxc` @ 3:32, and again at 7:32: "So you go back to your mathematician friend and ask her, what was the original motivation for defining one of these curves?"

Note the stumble. The invented expert is allowed to be unsure, which is what makes the device read as a memory of a real conversation rather than a ventriloquist act.

**3. The self-interrogation** — he asks why he is doing what he is doing, on the viewer's behalf.
> "Now why am I telling you this, you might ask?"
> — `spUNpyF58BY` @ 13:44

**4. The anticipation question** — tees up the next visual and stops.
> "Is the car moving at time t equals 0?"
> — `9vKqVkMQHKk`, followed by a **4.82-second pause** before "Do you see the paradox?"

**5. The agreement tag** — a question whose answer is not in doubt, used to close a step.
> "…which is 2 pi times r, right?" — `WUvTyaaNkzM` @ 3:03
> "Really the choice is yours." — `spUNpyF58BY` (declarative version of the same move)

Tag questions are **15% of all questions** and cluster in the videos that are hardest to follow: `9vKqVkMQHKk` (3), `EK32jo7i5LQ` (3), `WUvTyaaNkzM` (2), `spUNpyF58BY` (2), `mvmuCPvRoWQ` (2).

Question density by video ranges from **1.8 per 100 sentences** (`KuXjwB4LzSA`) to **11.1** (`v0YEaeIClKY`) — a 6× spread. Questions track *conceptual vertigo*, not runtime, which is why the 3.8-minute Euler video is the most question-dense in the corpus and the 27-minute transformer video has **zero**.

## The Four Openings

None of the fourteen opens with "hey guys, welcome back." Each begins by manufacturing the reason to care, and he rotates among four devices.

**A. Decode the term.** Take the title word apart, and save the interesting part for last.
> "The initials GPT stand for Generative Pretrained Transformer. So that first word is straightforward enough… Pretrained refers to… But the last word, **that's the real key piece.**"
> — `wjZofJX0v4M` @ 0:00

**B. Goal, then immediate admission of a trap.**
> "The goal here is simple, explain what a derivative is. **The thing is though, there's some subtlety to this topic, and a lot of potential for paradoxes if you're not careful.**"
> — `9vKqVkMQHKk` @ 0:15

Then he names the trap in the very next breath: "it's common for people to say that the derivative measures an instantaneous rate of change, but when you think about it, **that phrase is actually an oxymoron.**" The video now has stakes: a phrase you have used your whole life is nonsense.

**C. Provenance story.** Where the idea came from, with real names.
> "I first saw this pattern that I'm about to show you in a question on the Math Stack Exchange. It was asked by a user under the name Dwymark, and answered by Greg Martin…"
> — `EK32jo7i5LQ` @ 0:03

Followed immediately by permission to enjoy it: "There is no practical reason to do this, it's purely fun, we're just frolicking around in the playground of data visualization."

**D. Second-person construction.** Hand the viewer a task and let the concept be forced into existence.
> "Suppose I give you two different lists of numbers… and I ask you to think of all the ways you might combine those two lists… Maybe one simple way that comes to mind is to simply add them together term by term."
> — `KuXjwB4LzSA` @ 0:00

By the time he says the word "convolution" at 0:34, the viewer has already tried and rejected the two obvious operations. The definition arrives as a *gap being filled*, not a term being introduced.

The classic-era opening still exists but is the least used: "Hey everyone, Grant here." (`WUvTyaaNkzM` @ 0:14) — and even there, the greeting is followed in the same breath by the series structure and the goal.

## "Let's" Is Not the Verb You Think It Is

"Let's think about…" is remembered as his signature. It appears **twice in 45,000 words** (the whole "let's think" family, three times). "Let's" itself is common — 78 uses, 1.7 per 1,000 words — but it is almost never an invitation to reason. Broken down by what follows:

| Function | Count | Share | Example |
|---|---|---|---|
| Direct the eyes or hands | 26 | 33% | "let's watch what happens" |
| Stipulate a case | 19 | 24% | "let's say you wanted to write some software…" |
| Soften / reset / set aside | 16 | 21% | "let's temporarily set aside worries about whether this would actually work" |
| Name or define an object | 8 | 10% | "let's call that thickness dr" |
| Invite reasoning | 5 | 6% | "let's think about what the car's speedometer is probably doing" |
| Other ("lets you…") | 4 | 5% | "lets you ignore much of that mess" |

So "let's" is a **camera instruction and a hedge**, not a thinking prompt. "Let's say" does the heavy lifting: it opens a hypothetical the viewer can inhabit without commitment ("Let's say we have two vectors, one pointing up and a little to the right…"), and it lets him build a wrong version on purpose before correcting it.

The reset variant is the most distinctive and the least discussed:
> "Let's just move forward with this approximation, **keeping in the back of our minds that it's slightly wrong**, but it's going to become more accurate for smaller and smaller choices of dr."
> — `WUvTyaaNkzM` @ 3:53

He gives permission to proceed with an imperfect model *while naming the imperfection*. That single move is what makes calculus feel safe: the approximation is never hidden and never punished.

## Explain vs. Show: The Division of Labor

Once the animation is carrying the geometry, the words stop describing and start **interpreting**. The clearest extended example is the rings-to-rectangle derivation in `WUvTyaaNkzM` (2:42–6:05), where the visual shows the unwrapping and the narration only does the four things a picture cannot:

1. **Assign the choice.** "Maybe you start by imagining straightening out this ring. And you could try thinking through exactly what this new shape is and what its area should be, but for simplicity, let's just approximate it as a rectangle." — the animation *executes* the unwrap; the words explain that a *decision* was made.
2. **Name the variable.** "let's call that thickness dr for a tiny difference in the radius from one ring to the next" — a label appears on screen, and the words give it a reason to exist.
3. **State the error budget.** "for smaller and smaller choices of dr, this is actually going to be a better and better approximation… since the top and the bottom sides of this shape are going to get closer and closer to being exactly the same length."
4. **Narrate the production constraint.** "Pictures like this 2 pi r can get tall for the screen, I mean 2 times pi times 3 is around 19, so let's just throw up a y axis that's scaled a little differently so that we can actually fit all of these rectangles on the screen." — `WUvTyaaNkzM` @ 5:09

That fourth one is unusual and worth stealing: **he explains a staging decision as if the viewer were helping him draw.** It converts an arbitrary visual choice into a shared problem.

Two more measured signatures of "show" narration:

- **Deictic sentence openers.** 4–14% of sentences begin with *this / that / these / those / here / it*, i.e. pointing at something on screen. Highest in the pendulum video (14%), lowest in the tightly-scripted 3.8-minute Euler video (4%).
- **The verb "notice."** 27 uses (0.6 per 1,000 words). Almost always imperative and sentence-initial: "Notice, polar coordinates are not unique…" (`EK32jo7i5LQ` @ 0:51), "And notice that the spacing between the values here corresponds to the thickness dr…" (`WUvTyaaNkzM` @ 4:33), "Another thing to notice is that when you're on a patch that's all the same color, everything goes to zero…" (`KuXjwB4LzSA`).

"Notice" is doing something specific: it asserts that the viewer could have found this themselves, which is the same claim the endings make explicitly ("I want you to feel that you could have invented calculus yourself").

## Technique: Narrate the Viewer's Own Reasoning

The single most transferable device in the corpus: run the viewer's inner monologue as a sequence of *considered options*, including the ones you reject.

> "Suppose I give you two different lists of numbers, or maybe two different functions, and I ask you to think of all the ways you might combine those two lists… **Maybe one simple way that comes to mind is to simply add them together term by term.**… In a similar vein, **you could also** multiply the two lists term by term… **But there's another kind of combination just as fundamental as both of those, but a lot less commonly discussed**, known as a convolution."
> — `KuXjwB4LzSA` @ 0:00–0:30

Structure: *here is the task → here is the obvious move → here is the second obvious move → neither is it → hence the concept.* The viewer's failed attempts are scripted for them, so the eventual definition satisfies an appetite that already exists.

Variant with the objection built in:
> "And you could try thinking through exactly what this new shape is and what its area should be, but for simplicity, let's just approximate it as a rectangle." — `WUvTyaaNkzM` @ 2:50

Variant in the middle of a long derivation, when the viewer is lost:
> "So just to sum up where we are, you've broken up the area of the circle into all of these rings…" — `WUvTyaaNkzM` @ 4:07

## Technique: Withhold, Then Pay Off

Measured from caption gaps longer than 4 seconds:

- `EK32jo7i5LQ` 3.4% of runtime silent, including one **22.5-second** stretch (the end card) and a 4.7-second gap right after "…classes, **wouldn't you agree?**"
- `r6sGWTCMz2k` 4.0%, including 19.2 s and 13.4 s stretches
- `HEfHFsfGXjs` 3.2%, including a 10.0-second hold on the final frame before the sign-off
- `v0YEaeIClKY` 3.0%, a single **6.8-second** gap immediately after "e to the i times t equals a number that's t radians around this unit circle in the complex plane" — the pause lands **after** the payoff, letting it sit
- `spUNpyF58BY` 2.6%, including a **12.5-second** and a **12.3-second** stretch during the winding-machine reveal
- Most videos: 0.0–1.1%

So genuine silence is rare — he almost never stops talking — and when it happens it is at a reveal or on the final frame, never to fill time. The withholding is usually done **in words** instead: pose the question, then let the animation answer while he keeps narrating the mechanics.

The clearest measured pair:
> "Is the car moving at time t equals 0?" — `9vKqVkMQHKk`, then **4.82 s of silence**, then "**Do you see the paradox?**"

And the honest version of withholding — a promise with a schedule attached:
> "I promise I will explain to you all the relevant physics in due course, it's not entirely obvious how you would predict the dynamics here, **but in the spirit of getting to the punchline, let's watch what happens.**"
> — `HEfHFsfGXjs` @ 1:01

That is the whole trick in one sentence: acknowledge the debt, defer it explicitly, and go to the payoff anyway. The viewer trusts the deferral because it was named.

## Technique: Pre-empt the Objection

He says the thing the viewer is about to think, before they think it. It is not constant — roughly a dozen times in 45,000 words: 9 uses of "you might think", 5 of "you might ask / say / complain", plus a few one-off phrasings — but each one lands at a joint where the argument would otherwise be exposed. It buys credibility at exactly the moments he hand-waves.

> "**The astute among you might complain** that such collisions would make no sound, but your goal here is to count how many collisions take place, so in slight conflict with that assumption I want to leave a little clack sound to better draw your attention to that count."
> — `HEfHFsfGXjs` @ 0:28

> "**Now why am I telling you this, you might ask?** Well it gives us a really nice way to write down the idea of winding up the graph into a single tight little formula."
> — `spUNpyF58BY` @ 13:44

> "**Now you might ask, why e? Why not some other base?** Well, the full answer resides in calculus."
> — `mvmuCPvRoWQ`

> "**Nevertheless, something might still feel immoral** about putting an imaginary number up in that exponent, **and you would be right to question that.**"
> — `v0YEaeIClKY` @ 3:28

That last one is the strongest form: he predicts a *feeling*, grants that the feeling is correct, and then says the notation is to blame rather than the viewer — "What we write as e to the t is a bit of notational disaster, giving the number e and the idea of repeated multiplication way more emphasis than they deserve."

## Technique: Admit Imprecision Out Loud

Related but distinct: he flags his own looseness before anyone can catch him at it.

> "**You'll notice I'm being a little loose with language** using the words vector and complex numbers somewhat interchangeably, in large part because thinking of complex numbers as little arrows makes the idea of adding a lot of them together…"
> — `r6sGWTCMz2k`

> "Again, we're being approximate here." — `WUvTyaaNkzM` @ 5:36

> "So let's just move forward with this approximation, keeping in the back of our minds that it's slightly wrong…" — `WUvTyaaNkzM` @ 3:53

The habit generalises into the word choice itself: **"kind of / sort of" runs 1.5 per 1,000 words** and **"actually" 1.6 per 1,000** — both unusually high for prepared script. "Just" is higher still, at **4.7 per 1,000 words.**

These are not verbal tics to be cleaned up. They are the mechanism by which a scripted video keeps the texture of someone thinking in front of you: hedged claims, self-corrections, and admissions that the model is a model.

## Technique: Negative Definition

Instead of saying what a thing is, say what it is not — and refuse the wrong reading explicitly.

> "**Now notice what I'm not saying.** I'm not saying that the derivative is whatever happens when dt is infinitely small, whatever that would mean. **Nor am I saying that you plug in 0 for dt.** This dt is always a finitely small non-zero value, **it's just that it approaches 0 is all.**"
> — `9vKqVkMQHKk` @ 8:42

> "But unlike the previous two cases, **it's not something that's merely inherited from an operation you can do to numbers. It's something genuinely new** for the context of lists of numbers or combining functions."
> — `KuXjwB4LzSA` @ 0:34

Used sparingly, negative definition is what makes the later formalism land: the misconception is killed before the definition arrives, so the definition has nothing to compete with.

## Technique: Recap Insurance

Long videos contain small recaps placed where comprehension typically breaks. They are short, second-person, and oriented to *state of play* rather than to content review.

- "So just to sum up where we are, **you've** broken up the area of the circle into all of these rings…" — `WUvTyaaNkzM` @ 4:07
- "As a quick reminder **so we're all on the same page**, this means labeling points in 2D space not with the usual xy coordinates, but instead with…" — `EK32jo7i5LQ` @ 0:22
- "Remember, that approximation, 2 pi r times dr, gets less and less wrong as the size of dr gets smaller and smaller." — `WUvTyaaNkzM` @ 5:42
- "**Again,** you look at all the primes up to some bound x…" — `EK32jo7i5LQ`

"Remember" runs 0.39 per 1,000 words and "again," (as a callback opener) 0.51 — together about one spaced-repetition nudge every 1,100 words, i.e. roughly every 6 minutes.

## The Endings

Four distinct closing moves, and he almost never ends on a summary of the video he just made.

**1. The lesson as an imperative to the viewer.**
> "**The lesson to take away here is that even when a statement seems very far removed from reality, you should always be willing to look under the hood and at the nuts and bolts of what's really being said.** Who knows, you might find insights for representing numbers from divergent sums, or for seeing with your ears from filling space."
> — `3s7h2MHQtxc` @ 17:37

**2. The permission slip** — the meta-claim about how to learn, stated as a wish for the viewer.
> "At all points, **I want you to feel that you could have invented calculus yourself**, that if you drew the right pictures and played with each idea in just the right way, these formulas and rules and constructs that are presented could have just as easily popped out naturally from your own explorations."
> — `WUvTyaaNkzM` @ 15:54

> "…but **there is something special about rediscovering these topics on your own.** If you effectively reinvent Euler's totient function before you've ever seen it defined… then when you do learn those topics, you'll see them as familiar friends, not as arbitrary definitions."
> — `EK32jo7i5LQ` @ 21:28

**3. Handoff to the next chapter, with the door explicitly open.**
> "A lot of the goal with this chapter was to lay the foundations for understanding the attention mechanism, Karate Kid wax-on-wax-off style… then understanding the attention mechanism, this cornerstone piece in the whole modern boom in AI, should be relatively smooth. **For that, come join me in the next chapter.**"
> — `wjZofJX0v4M` @ 26:03

**4. Homework** — hand the viewer a question and leave.
> "If you want a little homework, here's something that's fun to think about. Explain why when you multiply two different numbers… what you're doing is basically a convolution between the digits of those numbers."
> — `KuXjwB4LzSA` @ 21:48, ending on "And next up, we'll turn our attention to the continuous case with a special focus on probability distributions."

The sign-off itself is a fixed, small ritual: **"Thanks for watching. I'll see you next time. Bye."** (`HEfHFsfGXjs`) or the two-word **"Thank you."** (`EK32jo7i5LQ`, `r6sGWTCMz2k`). No like-and-subscribe script, no mid-roll plea. Patreon thanks exist but are placed *before* the sign-off and framed as gratitude rather than as an ask:

> "I'm still astounded that I can spend time working on videos like these, and in a very direct way, **you are the one to thank for that.**" — `WUvTyaaNkzM` @ 16:37

## Pacing and Silence

- Narration runs **159–204 words/min**, mean 178. That is brisk for conversation but well short of the compressed, high-retention edit pace common on YouTube; it sits near audiobook pace with far longer sentences.
- Sentence rate is remarkably stable at **6.5–7.5 per minute** across all fourteen videos, 2017–2024. Whatever else changed, the underlying cadence did not.
- Silence over 4 seconds: 0.0–4.0% of runtime, median ~0.6%.
- The longest silences cluster at **reveals and at the very end**: the winding machine (`spUNpyF58BY`, 12.5 s and 12.3 s), the drawing-machine payoff (`r6sGWTCMz2k`, 19.2 s), the Euler derivation (`v0YEaeIClKY`, 6.8 s), the closing note (`EK32jo7i5LQ`, 22.5 s).

That distribution is worth stating plainly, because it inverts the usual advice: **he does not pause before the answer, he pauses after it.** The pre-answer tension is carried by a question sentence and about 5 seconds of quiet; the real silence is reserved for letting the viewer look at what just happened. The single most instructive instance is the tag question that gets a 4.7-second beat: "…it actually seems like the primes are pretty evenly distributed among the remaining classes, **wouldn't you agree?**" (`EK32jo7i5LQ` @ 14:32) — the silence falls where the viewer is expected to answer for themselves.

## The Process Behind the Prose

From the Dwarkesh Patel interview, section "How Grant makes videos" (1:05:12):

> "I start by laying out all of the animations and stuff that I want in a timeline and then once I record the voiceover, **the actual editing is like a day.**"

> "…all of the little cuts that I'm making along the way are my way of even thinking about what I want the final piece to be."

Three consequences that explain the prose style better than any stylistic theory:

1. **Animation-first, voiceover-second.** The script is written *to* a finished visual timeline, not the reverse. That is why narration can afford to be interpretive instead of descriptive — it never has to describe something the viewer cannot yet see.
2. **The edit is one day.** The thinking happened before the edit, in the animation and the voiceover. The 178 wpm, the long clauses, and the specific mix of hedges are locked in at recording time.
3. **He does all of it himself** (confirmed in the same interview: "Yes."). There is no separate scriptwriter whose words he is performing, which is why the hedges ("kind of", "actually", "maybe") survive into the final cut — nobody is polishing them out.

The practical implication for anyone borrowing from this: the narration techniques above are not decorators applied to a script. They are what a script looks like when it is written against a visual that already exists.

## How the Style Changed

The corpus spans 2017–2024, and the trend is unambiguous:

| | `WUvTyaaNkzM` (2017) | `9vKqVkMQHKk` (2017) | `EK32jo7i5LQ` (2019) | `KuXjwB4LzSA` (2023) | `wjZofJX0v4M` (2024) |
|---|---|---|---|---|---|
| Mean sentence | 25.5 w | 21.6 w | 24.1 w | 28.3 w | **31.3 w** |
| Sentences ≥ 35 w | 21.1% | 16.3% | 18.8% | 29.4% | **32.9%** |
| Questions | 8 (7.0%) | 9 (6.7%) | 11 (6.9%) | 3 (1.8%) | **0 (0.0%)** |
| Words/min | 174 | 174 | 173 | 204 | 191 |

The newer videos are **denser, faster, and less interrogative**. The 2024 transformer chapter has zero questions in 27 minutes and nearly a third of its sentences over 35 words. The question-driven, "let's think about it together" mode has given way to confident declarative exposition — presumably because the material is now a technical walkthrough of a system rather than a rediscovery of an idea, and because the audience for it already trusts him.

The stable core across all of it: second person, long clauses, "notice," explicit error budgets, and a hard split between what the picture shows and what the sentence claims.

## A Reproducible Recipe

A synthesis of the patterns above, in the order they occur in a typical video:

1. **Open on the reason, never on yourself.** Decode the term, state the goal and its hidden trap, tell the provenance story, or hand the viewer a task that forces the concept into existence.
2. **Assign the viewer the work.** Second-person process narration: "maybe you start by…", "you could try…, but for simplicity let's…". Script their failed attempts before their successful one.
3. **Ask one structural question every ~2.5 minutes**, at joints only. Make one in seven of them a tag question at the end of a hard step.
4. **Use "let's say" to open a hypothetical**, "let's call" to name, "let's just" to defer a worry, "let's watch" to point at the screen. Use "let's think" almost never.
5. **Let the animation describe; let the sentence interpret.** Narrate choices, name variables, state error budgets, and explain staging constraints out loud.
6. **Say "notice" and mean it** — assert the viewer could have found the pattern themselves.
7. **Kill the misconception explicitly** before the definition: "now notice what I'm not saying," "it's not merely inherited from."
8. **Pre-empt the objection** in the viewer's own words and grant it before answering: "the astute among you might complain…", "you would be right to question that."
9. **Flag your own looseness**: "I'll be a little loose with language here, because…"
10. **Recap state-of-play every ~6 minutes**, in second person, crediting the viewer: "so just to sum up where we are, you've broken up…"
11. **Withhold with a named debt**: "I promise I'll explain the physics in due course, but in the spirit of getting to the punchline, let's watch what happens." Pause *after* the payoff, not before.
12. **End on a lesson, a permission slip, a handoff, or homework** — then sign off in three flat sentences.

## Anti-Patterns: What He Does Not Do

Each of these is verified absent or near-absent in 45,466 words:

- **No staccato.** Only 3% of sentences are ≤5 words; three-in-a-row almost never happens.
- **No "we" as the default voice.** "We" is used a third as often as "you."
- **No descriptive narration.** He does not narrate what the animation is doing frame by frame; he narrates what it *means* and what choice produced it.
- **No unanswered promises.** Every deferral is named and dated ("in the next video", "in due course", "I'll spare you the full rant until the next video").
- **No engagement-bait.** No mid-video subscribe asks, no "smash that like button," no rhetorical hype.
- **No fake stakes.** The urgency is always intellectual ("that phrase is actually an oxymoron"), never "this will blow your mind."
- **No summary ending.** The close reaches outward — a lesson, a question, a next chapter — rather than restating the video.

## Appendix: Tables

### Per-video metrics

| Video | Min | Words | WPM | Sents | Mean len | ≥35 w | Questions | Q % | Tag Q | Silent >4 s |
|---|---|---|---|---|---|---|---|---|---|---|
| `3s7h2MHQtxc` | 17.9 | 2,855 | 159 | 119 | 24.0 | 15.1% | 5 | 4.2% | 0 | 1.1% |
| `p_di4Zn4wz4` | 26.9 | 4,548 | 169 | 192 | 23.7 | 17.2% | 9 | 4.7% | 1 | 0.3% |
| `wjZofJX0v4M` | 26.9 | 5,137 | 191 | 164 | 31.3 | 32.9% | 0 | 0.0% | 0 | 0.3% |
| `KuXjwB4LzSA` | 22.7 | 4,614 | 204 | 163 | 28.3 | 29.4% | 3 | 1.8% | 0 | 0.3% |
| `spUNpyF58BY` | 19.5 | 3,528 | 181 | 140 | 25.2 | 20.7% | 8 | 5.7% | 2 | 2.6% |
| `HEfHFsfGXjs` | 5.2 | 893 | 172 | 48 | 18.6 | 14.6% | 3 | 6.2% | 0 | 3.2% |
| `v0YEaeIClKY` | 3.8 | 699 | 184 | 27 | 25.9 | 18.5% | 3 | 11.1% | 0 | 3.0% |
| `EK32jo7i5LQ` | 22.3 | 3,858 | 173 | 160 | 24.1 | 18.8% | 11 | 6.9% | 3 | 3.4% |
| `fNk_zzaMoSs` | 9.9 | 1,800 | 182 | 73 | 24.7 | 21.9% | 3 | 4.1% | 0 | 0.0% |
| `WUvTyaaNkzM` | 16.7 | 2,906 | 174 | 114 | 25.5 | 21.1% | 8 | 7.0% | 2 | 0.0% |
| `9vKqVkMQHKk` | 16.8 | 2,917 | 174 | 135 | 21.6 | 16.3% | 9 | 6.7% | 3 | 0.9% |
| `aircAruvnKk` | 18.4 | 3,357 | 182 | 131 | 25.6 | 26.0% | 14 | 10.7% | 1 | 0.8% |
| `r6sGWTCMz2k` | 24.8 | 4,426 | 179 | 161 | 27.5 | 28.6% | 11 | 6.8% | 0 | 4.0% |
| `mvmuCPvRoWQ` | 24.1 | 3,928 | 163 | 161 | 24.4 | 20.5% | 7 | 4.3% | 2 | 0.6% |
| **Total** | **256** | **45,466** | **178** | **1,788** | **25.4** | **22.3%** | **94** | **5.3%** | **14** | **~0.6% median** |

### Sentence-length distribution

| Range | Share |
|---|---|
| ≤ 5 words | 3.0% |
| 6–10 | 7.4% |
| 11–20 | 29.5% |
| 21–30 | 29.4% |
| 31–40 | 17.8% |
| 41–50 | 8.1% |
| > 50 | 4.8% |

### Most common sentence openers

| Opener | Count |
|---|---|
| And | 186 |
| The | 120 |
| So | 109 |
| But | 86 |
| In | 81 |
| This | 69 |
| For | 60 |
| If | 60 |
| Now | 41 |
| You | 38 |
| It's | 38 |
| What | 37 |
| I | 36 |
| That | 27 |
| Well | 26 |
| When | 25 |
| Then | 23 |

Coordinating conjunctions (*and, so, but*) open **381** sentences — 21% of all of them. The prose is built to feel like one continuous chain of reasoning rather than a series of discrete statements: each sentence arrives attached to the previous one.

### Lexical signature (per 1,000 words)

| Token | Rate |
|---|---|
| you (all forms) | 20.8 |
| just | 4.7 |
| I (all forms) | 8.3 |
| we (all forms) | 7.2 |
| so | 5.5 |
| actually | 1.6 |
| let's | 1.7 |
| now | 1.7 |
| kind of / sort of | 1.5 |
| maybe | 0.9 |
| notice | 0.6 |
| remember | 0.4 |
| "you might ask/wonder/object" | 0.3 |
