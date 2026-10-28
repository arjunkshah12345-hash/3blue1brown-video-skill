#!/usr/bin/env bash
# Master the audio of rendered films for the web: two-pass loudnorm to
# -16 LUFS integrated, -1.5 dBTP, video stream copied untouched.
#
#   scripts/master_audio.sh OUT_DIR film.mp4 [film.mp4 ...]
#
# Needs only ffmpeg and python3.  Files without an audio stream are copied
# as-is (e.g. silent hero loops).
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "usage: $0 OUT_DIR film.mp4 [film.mp4 ...]" >&2
  exit 2
fi
out=$1; shift
mkdir -p "$out"
target="I=-16:TP=-1.5:LRA=11"

for src in "$@"; do
  dst="$out/$(basename "$src")"
  if [ -z "$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$src")" ]; then
    cp "$src" "$dst"; echo "copied (no audio)  $dst"; continue
  fi
  stats=$(ffmpeg -hide_banner -nostats -i "$src" -vn -af "loudnorm=$target:print_format=json" -f null - 2>&1 \
    | python3 -c 'import sys; t=sys.stdin.read(); print(t[t.rindex("{"):t.rindex("}")+1])')
  read -r mi mtp mlra mth off < <(python3 -c 'import json,sys; d=json.loads(sys.argv[1]); print(d["input_i"], d["input_tp"], d["input_lra"], d["input_thresh"], d["target_offset"])' "$stats")
  ffmpeg -hide_banner -loglevel error -y -i "$src" -c:v copy \
    -af "loudnorm=$target:measured_I=$mi:measured_TP=$mtp:measured_LRA=$mlra:measured_thresh=$mth:offset=$off:linear=true,aresample=48000" \
    -c:a aac -b:a 192k -movflags +faststart "$dst"
  echo "mastered ($mi LUFS in)  $dst"
done
