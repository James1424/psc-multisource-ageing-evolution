#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$ROOT/results/run_logs"
for v in v0.1 v0.2 v0.3 v0.4 v0.5 v0.6 v0.7 v0.8; do
  echo "===== $v ====="
  "$ROOT/benchmark/run_version.sh" "$v" 2>&1 | tee "$ROOT/results/run_logs/${v}.log"
done
python "$ROOT/benchmark/aggregate_results.py"
