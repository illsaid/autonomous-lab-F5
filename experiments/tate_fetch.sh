#!/usr/bin/env bash
# tate_fetch.sh — reproducibly regenerate the stratified Tate sample.
#
# Fetches every STRIDE-th artwork subdirectory (sorted; ~100 records each)
# from the pinned CC0 snapshot of github.com/tategallery/collection using a
# blob:none clone + sparse-checkout (only the sampled blobs are downloaded),
# then converts to met_tail JSONL schema via tate_convert.py.
#
# Deterministic: pinned commit + sorted directory list + fixed stride.
# STRIDE=20 (default) -> 37 of 738 dirs -> 3,458 records (~2.4 MB), the
# committed experiments/tate_stratified.jsonl. STRIDE=1 fetches everything
# (69,202 records) if you want the full collection locally.
#
# Usage: ./tate_fetch.sh [STRIDE] [OUT.jsonl]
set -euo pipefail

COMMIT=a51d8afc988ed083557e2950f4d0b644e7719f4a   # snapshot Oct 2014, CC0 1.0
STRIDE="${1:-20}"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${2:-$HERE/tate_stratified.jsonl}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

git clone --quiet --filter=blob:none --no-checkout \
  https://github.com/tategallery/collection.git "$WORK"
cd "$WORK"
git ls-tree -r "$COMMIT" --name-only artworks/ \
  | awk -F/ '{print $1"/"$2"/"$3}' | sort -u \
  | awk -v s="$STRIDE" 'NR % s == 1 {print $0 "/*"}' > sparse-dirs.txt
git sparse-checkout set --no-cone --stdin < sparse-dirs.txt
git checkout --quiet "$COMMIT"

python3 "$HERE/tate_convert.py" "$WORK/artworks" -o "$OUT"
