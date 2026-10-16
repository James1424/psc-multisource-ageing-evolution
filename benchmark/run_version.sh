#!/usr/bin/env bash
set -euo pipefail
VER=${1:?version required, e.g. v0.6}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
V="$ROOT/versions/$VER"
if [ ! -d "$V" ]; then echo "Unknown version $VER" >&2; exit 2; fi
rm -rf "$V/data/processed"
mkdir -p "$V/data/processed" "$V/results"
cp -a "$ROOT/data/processed/." "$V/data/processed/"
cd "$V"
export PYTHONPATH=src
case "$VER" in
  v0.1) python scripts/03_run_benchmark.py --train-devices 12 ;;
  v0.2) python scripts/03_run_benchmark.py --quick ;;
  v0.3) python scripts/06_source_usefulness_diagnostics.py --quick ;;
  v0.4) python scripts/09_automatic_source_auditor.py --quick ;;
  v0.5) python scripts/12_safe_adaptive_multisource_fusion.py --quick ;;
  v0.6) python scripts/15_adaptive_granularity_alignment.py --quick --seeds 3 ;;
  v0.7) python scripts/17_optional_diffraction_source.py --seeds 3 --n 12 ;;
  v0.8) python scripts/18_stage_shared_specific.py --seeds 3 --quick ;;
  *) echo "Unsupported version $VER" >&2; exit 3 ;;
esac
