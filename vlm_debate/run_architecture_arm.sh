#!/usr/bin/env bash
# Swap-one-agent architecture-capability arm.
# Keeps qwen2.5vl:7b + qwen2.5vl:3b fixed, swaps the third agent through
# the other available, non-excluded screened candidates. Dataset A only,
# same OFF/ON/HARD protocol as the original 3-agent ablation.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
mkdir -p logs

run_triad() {
  local AGENTS="$1" TAGBASE="$2"
  echo "=========================================================="
  echo "TRIAD: $AGENTS  tag=$TAGBASE  [$(date '+%Y-%m-%d %H:%M:%S')]"
  echo "=========================================================="

  echo "--- ON ---"
  OUT_ON=$(.venv/bin/python -u tools/run_experiment.py \
    --dataset data/citrusA_mendeley_4cls.json --n 200 --seed 42 \
    --agents "$AGENTS" --tag "${TAGBASE}_ev-on" 2>&1 | tee -a "logs/arch_${TAGBASE}.log" | grep -oP '(?<=out=)\S+' | tail -1)
  echo "ON output dir: $OUT_ON"
  R1="$OUT_ON/vida_raw_bank.json"

  echo "--- OFF (reuse R1) ---"
  .venv/bin/python -u tools/run_experiment.py \
    --dataset data/citrusA_mendeley_4cls.json --n 200 --seed 42 \
    --agents "$AGENTS" --no-evidence --reuse-r1 "$R1" --tag "${TAGBASE}_ev-off" 2>&1 | tee -a "logs/arch_${TAGBASE}.log"

  echo "--- HARD (reuse R1) ---"
  .venv/bin/python -u tools/run_experiment.py \
    --dataset data/citrusA_mendeley_4cls.json --n 200 --seed 42 \
    --agents "$AGENTS" --enforce --reuse-r1 "$R1" --tag "${TAGBASE}_ev-hard" 2>&1 | tee -a "logs/arch_${TAGBASE}.log"
}

run_triad "granite3.2-vision:latest,qwen2.5vl:7b,qwen2.5vl:3b" "arch_granite"
run_triad "gemma3:4b,qwen2.5vl:7b,qwen2.5vl:3b" "arch_gemma"

bash run.sh analyze

echo "ARCHITECTURE ARM COMPLETE  [$(date '+%Y-%m-%d %H:%M:%S')]"
