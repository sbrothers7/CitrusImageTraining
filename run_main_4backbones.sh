#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
source .venv/bin/activate

python run_1_prepare.py

for MODEL in efficientnet_b0 resnet50 densenet121 mobilenetv3_large_100; do
  echo
  echo "############################################################"
  echo "  MAIN RUN: $MODEL  [$(date '+%Y-%m-%d %H:%M:%S')]"
  echo "############################################################"
  for script in run_2_train.py run_3_evaluate.py run_4_gradcam.py run_5_report.py; do
    echo "--- $script --model $MODEL ---"
    python "$script" --model "$MODEL"
  done
done

echo
echo "MAIN RUN (4 backbones) COMPLETE  [$(date '+%Y-%m-%d %H:%M:%S')]"
