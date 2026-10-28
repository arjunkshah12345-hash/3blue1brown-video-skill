#!/usr/bin/env python3
"""Render b3b scenes on a Kaggle CPU box, with Kokoro narration.

Everything heavy (Manim, TeX, the Kokoro voice model) is installed on Kaggle,
not on this machine.  Locally you only need the ``kaggle`` CLI, logged in.

    python3 scripts/kaggle_render.py examples OUT_DIR \\
        launch_film.py:LaunchFilm 01_morphing_equations.py:EulerIdentityMorph,DerivativeDefinition

Each ``file.py:SceneA,SceneB`` argument is rendered at 1080p60 into
``OUT_DIR/<Scene>.mp4``.  The kernel is private; it is pushed as a new
version of ``<user>/b3b-render`` each run.  Options:

    --voice am_michael   Kokoro voice id (a* American, b* British)
    --speed 0.95         speaking rate
    --no-voice           music and cues only
    --slug b3b-render    kernel name
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

REMOTE = r'''
import base64, io, os, subprocess, tarfile, shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PAYLOAD = "{payload}"
JOBS = {jobs!r}
ENV = {env!r}

def sh(cmd):
    print("+", cmd, flush=True)
    subprocess.run(cmd, shell=True, check=True)

sh("apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -qq install -y --no-install-recommends "
   "libcairo2-dev libpango1.0-dev pkg-config ffmpeg espeak-ng fonts-dejavu-core "
   "texlive texlive-latex-extra texlive-fonts-recommended texlive-lang-english dvisvgm > /dev/null")
# Kokoro needs Python <= 3.12 and Kaggle's image may be newer, so render in
# a uv-made 3.12 venv (seeded with pip: misaki fetches its spaCy model via pip).
sh("pip install -q uv && uv venv -q --seed -p 3.12 /tmp/venv")
PY = "/tmp/venv/bin/python"
sh(f"uv pip install -q -p {{PY}} torch --index-url https://download.pytorch.org/whl/cpu")
sh(f"uv pip install -q -p {{PY}} manim==0.21.0 'kokoro>=0.9.4' soundfile scipy")

# The scenes ask for Menlo (macOS); Menlo is derived from DejaVu Sans Mono.
conf = Path.home() / ".config/fontconfig/fonts.conf"
conf.parent.mkdir(parents=True, exist_ok=True)
conf.write_text("<?xml version='1.0'?><!DOCTYPE fontconfig SYSTEM 'fonts.dtd'><fontconfig>"
                "<alias><family>Menlo</family><prefer><family>DejaVu Sans Mono</family></prefer></alias>"
                "</fontconfig>")
sh("fc-cache -f > /dev/null")

src = Path("/tmp/b3b-src")
tarfile.open(fileobj=io.BytesIO(base64.b64decode(PAYLOAD)), mode="r:gz").extractall(src)
out = Path("/kaggle/working")
env = {{**os.environ, **ENV}}

if ENV.get("B3B_VOICE") == "kokoro":
    # Fetch the model and voice once, before the parallel renders race for them.
    sh("cd /tmp/b3b-src && " + PY + " -c \"from b3b.audio import _kokoro_say; from pathlib import Path; "
       "_kokoro_say('Ready.', '" + ENV.get("B3B_VOICE_ID", "am_michael") + "', 1.0, Path('/tmp/warm.wav'))\"")

def render(job):
    file, scenes = job
    media = Path("/tmp/media") / Path(file).stem   # one media dir per file: TeX caches race
    log = out / f"{{Path(file).stem}}.log"
    with open(log, "w") as fh:
        code = subprocess.run(
            [PY, "-m", "manim", "render", "--media_dir", str(media), "-r", "1920,1080", file, *scenes],
            cwd=src, env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
    for scene in scenes:
        for mp4 in media.glob(f"videos/*/*/{{scene}}.mp4"):
            shutil.copy(mp4, out / f"{{scene}}.mp4")
    return file, code

with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
    results = list(pool.map(render, JOBS))
for file, code in results:
    print(f"{{file}}: exit {{code}}", flush=True)
print("DONE", sorted(p.name for p in out.glob("*.mp4")), flush=True)
if any(code for _, code in results):
    raise SystemExit(1)
'''


def kaggle_user() -> str:
    view = subprocess.run(["kaggle", "config", "view"], capture_output=True, text=True).stdout
    match = re.search(r"username:\s*(\S+)", view)
    if not match:
        sys.exit("kaggle CLI is not logged in (kaggle config view shows no username)")
    return match.group(1)


def pack(src: Path) -> str:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for path in sorted(src.rglob("*")):
            rel = path.relative_to(src)
            if path.is_file() and not {"media", "__pycache__"} & set(rel.parts) and path.suffix == ".py":
                tar.add(path, arcname=str(rel))
    return base64.b64encode(buf.getvalue()).decode()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path, help="folder holding the scene files and b3b/")
    ap.add_argument("out", type=Path, help="where to download the MP4s")
    ap.add_argument("jobs", nargs="+", help="file.py:SceneA,SceneB")
    ap.add_argument("--voice", default="am_michael")
    ap.add_argument("--speed", default="0.95")
    ap.add_argument("--no-voice", action="store_true")
    ap.add_argument("--slug", default="b3b-render")
    args = ap.parse_args()

    jobs = []
    for job in args.jobs:
        file, _, scenes = job.partition(":")
        if not (args.src / file).is_file() or not scenes:
            sys.exit(f"bad job {job!r}: want file.py:Scene[,Scene] with the file under {args.src}")
        jobs.append((file, scenes.split(",")))
    env = {"B3B_VOICE": "none"} if args.no_voice else {
        "B3B_VOICE": "kokoro", "B3B_VOICE_ID": args.voice, "B3B_VOICE_SPEED": args.speed}

    user = kaggle_user()
    ref = f"{user}/{args.slug}"
    with tempfile.TemporaryDirectory() as tmp:
        kernel = Path(tmp)
        (kernel / "run.py").write_text(REMOTE.format(payload=pack(args.src), jobs=jobs, env=env))
        (kernel / "kernel-metadata.json").write_text(json.dumps({
            "id": ref, "title": args.slug, "code_file": "run.py", "language": "python",
            "kernel_type": "script", "is_private": True, "enable_gpu": False,
            "enable_internet": True, "dataset_sources": [], "competition_sources": [],
            "kernel_sources": [],
        }, indent=2))
        subprocess.run(["kaggle", "kernels", "push", "-p", str(kernel)], check=True)

    print(f"running https://www.kaggle.com/code/{ref}", flush=True)
    time.sleep(30)
    while True:
        status = subprocess.run(["kaggle", "kernels", "status", ref], capture_output=True, text=True).stdout
        state = re.search(r'status "?(?:KernelWorkerStatus\.)?(\w+)', status)
        state = state.group(1).lower() if state else status.strip()
        print(time.strftime("%H:%M:%S"), state, flush=True)
        if state not in ("queued", "running"):
            break
        time.sleep(60)

    args.out.mkdir(parents=True, exist_ok=True)
    subprocess.run(["kaggle", "kernels", "output", ref, "-p", str(args.out), "-o",
                    "--file-pattern", r".*\.(mp4|log)$"], check=True)
    if state != "complete":
        sys.exit(f"kernel ended {state}; logs are in {args.out}")


if __name__ == "__main__":
    main()
