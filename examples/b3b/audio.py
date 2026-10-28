"""Sound for b3b scenes: narration, cue sounds, and a felt-piano score.

Everything here is synthesised with numpy/scipy or produced by an external
TTS command, written as a WAV under ``<media_dir>/b3b_audio/`` (cached by
content hash), and handed to Manim's own ``Scene.add_sound``.  Manim then
mixes it and muxes it into the final MP4, so there is no post step.

Three layers, used from inside ``construct``:

``self.cue("chime")``
    A short procedural sound at the current time.  Cues are tuned to the
    score's key so they sit inside the music rather than on top of it.

``with self.voiceover("Picture x squared as an area.") as vo:``
    Narration.  The block plays its animations, then waits out whatever is
    left of the line, so picture and voice stay in sync.  ``vo.duration``
    is available for ``run_time=``.

``self.say("...")`` (captions, in ``style.py``)
    When a voice is on, every caption is also spoken.  The line starts with
    the caption and the animations carry on underneath it; the next caption
    waits for it to finish.  Pass ``spoken=`` for captions with maths in
    them (``spoken="Picture x squared as an area."``), or ``spoken=""`` to
    keep a caption silent.  ``self.narrate(text)`` does the same without a
    caption.

``self.score()``
    A felt-piano bed exactly as long as the scene, ducked under every
    voiceover line, laid under everything at t=0.  It runs by itself when
    the scene ends; call it last only to change its settings, or set
    ``auto_score = False`` for silence.

Voices, picked by ``B3B_VOICE`` (default ``auto``):

* ``elevenlabs`` -- the ``sag`` CLI; needs ``ELEVENLABS_API_KEY``.
* ``kokoro``     -- the open-weights Kokoro-82M model, offline once its
                    weights are cached.  Needs ``pip install kokoro
                    soundfile`` and espeak-ng, so it is meant for a cloud
                    box (see ``scripts/kaggle_render.py``).  Voice via
                    ``B3B_VOICE_ID`` (default ``am_michael``), pace via
                    ``B3B_VOICE_SPEED`` (default 0.95).
* ``say``        -- macOS ``say``.  Draft quality; good for timing.
* ``none``       -- no audio; each line still takes the time it would
                    take to speak, so the cut is already timed.
* ``auto``       -- ``elevenlabs`` if a key is set, else ``kokoro`` if it
                    is importable, else ``none``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import wave
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator, Sequence

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48_000

# Score key: D major.  Cue pitches are drawn from it.
_PENTATONIC = [62, 64, 66, 69, 71]  # D E F# A B (MIDI)


def midi_hz(note: float) -> float:
    return 440.0 * 2.0 ** ((note - 69) / 12)


def db(x: float) -> float:
    return 10.0 ** (x / 20.0)


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------
def _audio_dir() -> Path:
    from manim import config

    root = Path(config.media_dir) / "b3b_audio"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _key(*parts) -> str:
    return hashlib.sha1(json.dumps(parts, sort_keys=True, default=str).encode()).hexdigest()[:16]


def write_wav(path: Path, signal: np.ndarray) -> Path:
    """Write float audio (mono or (n, 2)) as 16-bit stereo at 48 kHz."""
    if signal.ndim == 1:
        signal = np.stack([signal, signal], axis=1)
    pcm = np.clip(signal, -1.0, 1.0)
    wavfile.write(path, SR, (pcm * 32767).astype(np.int16))
    return path


def wav_duration(path: Path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / float(w.getframerate())


def _cached(name: str, params: dict, build: Callable[[], np.ndarray]) -> Path:
    path = _audio_dir() / f"{name}-{_key(name, params)}.wav"
    if not path.exists():
        # Write beside the target and rename, so a failed write (e.g. a full
        # disk) never leaves a truncated file that later renders trust.
        tmp = path.with_suffix(".part.wav")
        write_wav(tmp, build())
        tmp.replace(path)
    return path


# ---------------------------------------------------------------------------
# DSP pieces
# ---------------------------------------------------------------------------
def _t(seconds: float) -> np.ndarray:
    return np.arange(int(seconds * SR)) / SR


def _lowpass(x: np.ndarray, hz: float, order: int = 2) -> np.ndarray:
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x, axis=0)


def _highpass(x: np.ndarray, hz: float, order: int = 2) -> np.ndarray:
    return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x, axis=0)


def _bandpass(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x, axis=0)


def _reverb(dry: np.ndarray, *, seconds: float = 2.4, wet: float = 0.28, seed: int = 7) -> np.ndarray:
    """Stereo room from decaying filtered noise.  Mono in, (n, 2) out."""
    rng = np.random.default_rng(seed)
    t = _t(seconds)
    env = np.exp(-t / (seconds / 6.5))
    pre = int(0.018 * SR)
    channels = []
    for _ in range(2):
        ir = _lowpass(rng.standard_normal(t.size) * env, 5200)
        ir = np.concatenate([np.zeros(pre), ir])
        ir /= np.sqrt(np.sum(ir**2))
        channels.append(fftconvolve(dry, ir)[: dry.size + ir.size - 1])
    n = max(c.size for c in channels)
    out = np.zeros((n, 2))
    for i, c in enumerate(channels):
        out[: c.size, i] = c * wet
    out[: dry.size, 0] += dry * (1 - wet * 0.5)
    out[: dry.size, 1] += dry * (1 - wet * 0.5)
    return out


def _normalise(x: np.ndarray, peak_db: float) -> np.ndarray:
    peak = np.max(np.abs(x)) or 1.0
    return x / peak * db(peak_db)


def felt_note(note: float, length: float, velocity: float = 0.7, *, seed: int = 0) -> np.ndarray:
    """One soft felt-piano note: stretched partials, two detuned strings,
    upper partials dying first, a muted hammer, and a damper release."""
    rng = np.random.default_rng(seed)
    f0 = midi_hz(note)
    tail = 1.4
    t = _t(length + tail)
    out = np.zeros(t.size)
    # Low notes ring longer; felt darkens the top.
    ring = 4.2 * (196.0 / f0) ** 0.45
    for n in range(1, 10):
        fn = n * f0 * np.sqrt(1 + 0.00035 * n * n)
        if fn > 9000:
            break
        amp = (velocity**1.6) / n**1.35 * np.exp(-((fn / (1800 + 2200 * velocity)) ** 2))
        tau = ring / (1 + 0.85 * (n - 1))
        for detune in (-0.35, 0.35):
            f = fn * 2 ** (detune / 1200)
            out += 0.5 * amp * np.sin(2 * np.pi * f * t + rng.uniform(0, 2 * np.pi)) * np.exp(-t / tau)
    attack = 1 - np.exp(-t / (0.006 + 0.01 * (1 - velocity)))
    damper = np.ones(t.size)
    k = int(length * SR)
    damper[k:] = np.exp(-(t[k:] - length) / 0.22)
    hammer = _lowpass(rng.standard_normal(t.size) * np.exp(-t / 0.012), 1400) * 0.05 * velocity
    return (out * attack + hammer) * damper


# ---------------------------------------------------------------------------
# Cues
# ---------------------------------------------------------------------------
def _cue_pluck(note: float = 74, gain: float = -11) -> np.ndarray:
    x = felt_note(note, 0.35, 0.55, seed=int(note))
    return _normalise(_reverb(x, seconds=1.6, wet=0.32), gain)


def _cue_chime(note: float = 81, gain: float = -11) -> np.ndarray:
    """Soft bell: inharmonic partials, long ring.  For an 'aha'."""
    t = _t(3.0)
    f = midi_hz(note)
    x = np.zeros(t.size)
    for ratio, amp, tau in ((1.0, 1.0, 1.2), (2.0, 0.45, 0.7), (2.76, 0.3, 0.45), (5.4, 0.12, 0.18)):
        x += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / tau)
    x *= 1 - np.exp(-t / 0.003)
    return _normalise(_reverb(x, seconds=2.8, wet=0.4), gain)


def _cue_whoosh(length: float = 0.9, gain: float = -14, rising: bool = True) -> np.ndarray:
    """Air moving past: noise through a band that sweeps with the motion."""
    rng = np.random.default_rng(3)
    t = _t(length)
    noise = rng.standard_normal(t.size)
    out = np.zeros(t.size)
    bands = 12
    for i in range(bands):
        a, b = i * t.size // bands, (i + 1) * t.size // bands
        p = (i + 0.5) / bands
        centre = 300 + 2600 * (p if rising else 1 - p)
        seg = _bandpass(noise, centre * 0.6, centre * 1.6)
        out[a:b] = seg[a:b]
    env = np.sin(np.pi * np.clip(t / length, 0, 1)) ** 1.6
    out = _lowpass(out * env, 4000)
    return _normalise(_reverb(out, seconds=1.2, wet=0.25), gain)


def _cue_keys(count: int = 20, spacing: float = 0.045, gain: float = -17) -> np.ndarray:
    """Soft key taps for text typed on screen."""
    rng = np.random.default_rng(count)
    total = count * spacing + 0.3
    out = np.zeros(int(total * SR))
    tap_t = _t(0.05)
    for i in range(count):
        tap = _bandpass(rng.standard_normal(tap_t.size), 1800, 5200) * np.exp(-tap_t / 0.006)
        tap += 0.4 * np.sin(2 * np.pi * rng.uniform(180, 240) * tap_t) * np.exp(-tap_t / 0.01)
        start = int((i * spacing + rng.uniform(-0.006, 0.006)) * SR)
        start = max(start, 0)
        out[start : start + tap.size] += tap * rng.uniform(0.55, 1.0)
    return _normalise(_reverb(out, seconds=0.6, wet=0.15), gain)


def _cue_thump(gain: float = -9) -> np.ndarray:
    """A low, round impact for a title landing."""
    t = _t(1.6)
    f = 55 * (1 + 0.6 * np.exp(-t / 0.05))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.35)
    x += 0.3 * felt_note(38, 0.6, 0.6)[: t.size]
    return _normalise(_reverb(x, seconds=1.8, wet=0.3), gain)


def _cue_rise(length: float = 1.6, gain: float = -15) -> np.ndarray:
    """A breath in before a reveal: a pad swelling into the cut."""
    t = _t(length)
    x = sum(np.sin(2 * np.pi * midi_hz(n) * t) for n in (50, 57, 62, 66))
    x *= (t / length) ** 2.2
    x[-int(0.04 * SR):] *= np.linspace(1, 0, int(0.04 * SR))
    return _normalise(_reverb(_lowpass(x, 2500), seconds=1.4, wet=0.3), gain)


CUES: dict[str, Callable[..., np.ndarray]] = {
    "pluck": _cue_pluck,
    "chime": _cue_chime,
    "whoosh": _cue_whoosh,
    "keys": _cue_keys,
    "thump": _cue_thump,
    "rise": _cue_rise,
}


def cue_file(name: str, **params) -> Path:
    if name not in CUES:
        raise ValueError(f"unknown cue {name!r}; choose from {sorted(CUES)}")
    return _cached(f"cue-{name}", params, lambda: CUES[name](**params))


def note_in_key(step: int, octave: int = 0) -> int:
    """The ``step``-th note of the D major pentatonic, for melodic cues."""
    return _PENTATONIC[step % 5] + 12 * (octave + step // 5)


# ---------------------------------------------------------------------------
# Score
# ---------------------------------------------------------------------------
# Dmaj9 - Bm11 - Gmaj7#11 - Asus2, voiced low and open.
PROGRESSION: list[tuple[int, list[int]]] = [
    (50, [57, 61, 64, 66, 69]),
    (47, [54, 57, 62, 64, 66]),
    (43, [54, 59, 61, 62, 66]),
    (45, [52, 57, 59, 64, 69]),
]
FINAL_CHORD = (50, [57, 61, 64, 66, 69, 73, 78])


def _default_intensity(x: float) -> float:
    """Sparse at the hook, fuller through the middle, easing into the end."""
    return float(np.clip(0.35 + 0.75 * x - 0.45 * max(0.0, x - 0.75) * 4, 0.3, 0.95))


def render_score(
    duration: float,
    *,
    ducks: Sequence[tuple[float, float]] = (),
    bpm: float = 64.0,
    intensity: Callable[[float], float] = _default_intensity,
    duck_db: float = -11.0,
    seed: int = 11,
) -> np.ndarray:
    """A felt-piano bed exactly ``duration`` seconds long.

    Chords change every bar.  Each bar is a bass note plus a slow arpeggio
    whose density follows ``intensity`` (0..1 over normalised time).  The
    last few seconds become a single rolled tonic chord left to ring.
    """
    rng = np.random.default_rng(seed)
    beat = 60.0 / bpm
    bar = 4 * beat
    final_at = max(0.0, duration - 6.5)
    n = int((duration + 3) * SR)
    dry = np.zeros(n)

    def place(note: float, at: float, length: float, vel: float) -> None:
        at = max(0.0, at + rng.normal(0, 0.006))
        x = felt_note(note, length, vel, seed=int(rng.integers(1 << 30)))
        i = int(at * SR)
        j = min(n, i + x.size)
        dry[i:j] += x[: j - i]

    t = 0.0
    k = 0
    while t + bar <= final_at + 1e-6:
        bass, upper = PROGRESSION[k % len(PROGRESSION)]
        level = intensity(t / max(duration, 1e-6))
        place(bass, t, bar * 0.95, 0.34 + 0.16 * level)
        # Arpeggio over eight 8th-note slots, up then partly back down.
        order = [0, 1, 2, 3, 4, 3, 2, 1]
        for slot, idx in enumerate(order):
            if slot and rng.random() > 0.25 + 0.7 * level:
                continue
            vel = (0.3 + 0.25 * level) * (1.0 if slot in (0, 4) else 0.82) * rng.uniform(0.9, 1.05)
            place(upper[idx], t + slot * beat / 2, beat * 1.6, vel)
        # A high answering note every other bar once things open up.
        if k % 2 == 1 and level > 0.5:
            place(upper[rng.integers(2, 5)] + 12, t + beat * 2.5, beat * 2, 0.24 + 0.12 * level)
        t += bar
        k += 1

    # Roll the final chord in from the bottom.
    bass, notes = FINAL_CHORD
    roll_at = t if t > final_at - bar * 0.5 else final_at
    place(bass - 12, roll_at, 6.0, 0.26)
    place(bass, roll_at, 6.0, 0.4)
    for i, note in enumerate(notes):
        place(note, roll_at + 0.07 * (i + 1), 6.0 - 0.07 * i, 0.42 - 0.02 * i)

    dry = _highpass(_lowpass(dry, 5200), 75)
    mix = _reverb(dry, seconds=3.2, wet=0.34)[: int(duration * SR)]

    # Fades and voice ducking as one gain curve.
    times = _t(duration)
    gain = np.ones(times.size)
    gain *= np.clip(times / 1.5, 0, 1)
    gain *= np.clip((duration - times) / 2.5, 0, 1)
    if ducks:
        duck = np.ones(times.size)
        low = db(duck_db)
        for a, b in ducks:
            ramp_in = np.clip((times - (a - 0.25)) / 0.25, 0, 1)
            ramp_out = np.clip(((b + 0.35) - times) / 0.35, 0, 1)
            duck = np.minimum(duck, 1 - (1 - low) * np.minimum(ramp_in, ramp_out))
        gain *= duck
    mix *= gain[:, None]
    return _normalise(mix, -8.0)


# ---------------------------------------------------------------------------
# Narration
# ---------------------------------------------------------------------------
WORDS_PER_SECOND = 2.6


def _voice_backend() -> str:
    choice = os.environ.get("B3B_VOICE", "auto").lower()
    if choice != "auto":
        return choice
    has_key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("SAG_API_KEY")
    if has_key and shutil.which("sag"):
        return "elevenlabs"
    if importlib.util.find_spec("kokoro") is not None:
        return "kokoro"
    return "none"


def speakable(tex: str) -> str:
    """Caption TeX to plain words: drops ``$``, ``\\textit{}`` and other
    commands.  Maths does not survive this; pass ``spoken=`` for that."""
    text = re.sub(r"\\text(?:it|bf|tt|rm)?\{([^}]*)\}", r"\1", tex)
    text = text.replace(r"\%", " percent").replace("$", "")
    text = re.sub(r"\\[A-Za-z]+", "", text).replace("{", "").replace("}", "")
    return " ".join(text.split())


_KOKORO: dict[str, object] = {}


def _kokoro_say(text: str, voice: str, speed: float, dst: Path) -> None:
    import soundfile
    from kokoro import KPipeline

    lang = voice[0]  # Kokoro voice ids start with their language: a, b, ...
    if lang not in _KOKORO:
        _KOKORO[lang] = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")
    chunks = [
        audio.detach().cpu().numpy() if hasattr(audio, "detach") else np.asarray(audio)
        for _, _, audio in _KOKORO[lang](text, voice=voice, speed=speed)
    ]
    soundfile.write(str(dst), np.concatenate(chunks), 24_000)


def _to_wav(src: Path, dst: Path) -> None:
    subprocess.run(
        # Level every backend to the same speech loudness so lines sit above
        # the (ducked) score whichever voice made them.
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", "loudnorm=I=-17:TP=-2:LRA=7",
         "-ar", str(SR), "-ac", "2", str(dst)],
        check=True,
    )


def speak(text: str) -> tuple[Path | None, float]:
    """Synthesise ``text`` and return (wav path or None, seconds)."""
    backend = _voice_backend()
    words = len(text.split())
    if backend == "none":
        return None, max(1.0, words / WORDS_PER_SECOND + 0.35)

    voice = os.environ.get("B3B_VOICE_ID", "")
    speed = float(os.environ.get("B3B_VOICE_SPEED", "0.95"))
    path = _audio_dir() / f"vo-{backend}-{_key(text, voice, speed if backend == 'kokoro' else None)}.wav"
    if not path.exists():
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw"
            if backend == "elevenlabs":
                raw = raw.with_suffix(".mp3")
                cmd = ["sag", "speak", "--no-play", "--no-stream", "-o", str(raw),
                       "--model-id", os.environ.get("B3B_VOICE_MODEL", "eleven_multilingual_v2")]
                if voice:
                    cmd += ["-v", voice]
                subprocess.run(cmd + [text], check=True)
            elif backend == "say":
                raw = raw.with_suffix(".aiff")
                cmd = ["say", "-o", str(raw)]
                if voice:
                    cmd += ["-v", voice]
                subprocess.run(cmd + [text], check=True)
            elif backend == "kokoro":
                raw = raw.with_suffix(".wav")
                _kokoro_say(text, voice or "am_michael", speed, raw)
            else:
                raise ValueError(f"unknown B3B_VOICE {backend!r}")
            part = path.with_suffix(".part.wav")
            _to_wav(raw, part)
            part.replace(path)
    return path, wav_duration(path)


@dataclass
class Voiceover:
    text: str
    start: float
    duration: float

    @property
    def end(self) -> float:
        return self.start + self.duration


class SoundMixin:
    """Mixed into the b3b scene classes; see the module docstring."""

    #: Lay the score under the scene automatically when it ends.  Set to
    #: ``False`` on a scene (or ``B3B_SCORE=0`` in the environment) for no
    #: music, or call ``self.score(...)`` yourself to change its settings.
    auto_score: bool = True

    def _sound_init(self) -> None:
        self._voiceovers: list[Voiceover] = []
        self._scored = False

    def tear_down(self) -> None:
        self.finish_narration(0.8)
        if self.auto_score and not self._scored and os.environ.get("B3B_SCORE", "1") != "0":
            self.score()
        super().tear_down()

    def add_sound(self, sound_file: str, time_offset: float = 0, gain: float | None = None, **kwargs) -> None:
        """``Scene.add_sound`` that survives Manim's render cache.

        Manim marks a cached play as skipped and leaves the flag set until
        the next uncached play, so its ``add_sound`` silently drops every
        sound placed after a cache hit.  The clock still advances on cached
        plays, so checking the user's own skip setting is enough.
        """
        if self.renderer._original_skipping_status:
            return
        self.renderer.file_writer.add_sound(sound_file, self.time + time_offset, gain, **kwargs)

    def cue(self, name: str, *, offset: float = 0.0, gain: float = 0.0, **params) -> None:
        """Play a procedural cue now (or ``offset`` seconds from now)."""
        self.add_sound(str(cue_file(name, **params)), time_offset=offset, gain=gain or None)

    @contextmanager
    def voiceover(self, text: str, *, pad: float = 0.25) -> Iterator[Voiceover]:
        """Speak ``text`` while the block's animations play, then wait out
        the rest of the line (plus ``pad``) before moving on."""
        path, seconds = speak(text)
        vo = Voiceover(text, self.time, seconds)
        if path is not None:
            self.add_sound(str(path))
        self._voiceovers.append(vo)
        yield vo
        left = vo.end + pad - self.time
        if left > 0.02:
            self.wait(left)

    def narrate(self, text: str, *, gap: float = 0.3) -> Voiceover | None:
        """Start speaking ``text`` now and carry straight on with the next
        animations.  A line never overlaps the one before it: if that is
        still playing, this waits for it (plus ``gap``) first.  Does nothing
        when no voice is on, so silent renders keep their original timing."""
        if _voice_backend() == "none" or not text.strip():
            return None
        self.finish_narration(gap)
        path, seconds = speak(text)
        vo = Voiceover(text, self.time, seconds)
        self.add_sound(str(path))
        self._voiceovers.append(vo)
        return vo

    def finish_narration(self, pad: float = 0.3) -> None:
        """Wait until the last spoken line (plus ``pad``) has finished."""
        if self._voiceovers:
            left = self._voiceovers[-1].end + pad - self.time
            if left > 0.02:
                self.wait(left)

    def score(self, **kwargs) -> None:
        """Lay a piano bed under the whole scene.  Call at the very end."""
        self.finish_narration(0.8)
        self._scored = True
        if self.renderer._original_skipping_status or self.time <= 0:
            return
        duration = float(self.time)
        ducks = [(v.start, v.end) for v in self._voiceovers] if _voice_backend() != "none" else []
        params = {"duration": round(duration, 3), "ducks": ducks, **kwargs}
        path = _cached("score", params, lambda: render_score(duration, ducks=ducks, **kwargs))
        self.add_sound(str(path), time_offset=-duration)
