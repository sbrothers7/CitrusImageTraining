# Analysis — 2026-10-11 17:42

## 1. Debate effect per run (R1 weighted vote -> R3 weighted vote)

| run | condition | n | before | after | Δ | wrong→right | right→wrong | McNemar p |
|---|---|---|---|---|---|---|---|---|
| 20260923_1719_main200_citrusA_ev-on | ON (prompt rule) | 190 | 0.368 | 0.389 | +0.021 | 7 | 3 | 0.344 |
| 20260924_0018_main200_citrusA_ev-off | OFF (no rule) | 190 | 0.368 | 0.384 | +0.016 | 5 | 2 | 0.453 |
| 20260924_1014_main200_citrusA_ev-hard | HARD (code-enforced) | 190 | 0.368 | 0.368 | +0.000 | 2 | 2 | 1.000 |
| 20260924_1638_main180_zenodo_ev-on | ON (prompt rule) | 180 | 0.189 | 0.206 | +0.017 | 7 | 4 | 0.549 |
| 20261011_1354_main200_citrusA_ev-on | ON (prompt rule) | 190 | 0.347 | 0.237 | -0.111 | 16 | 37 | 0.005 |
| 20261011_1429_main200_citrusA_ev-off | OFF (no rule) | 190 | 0.347 | 0.211 | -0.137 | 17 | 43 | 0.001 |
| 20261011_1512_main200_citrusA_ev-hard | HARD (code-enforced) | 190 | 0.347 | 0.300 | -0.047 | 2 | 11 | 0.022 |
| 20261011_1528_main180_zenodo_ev-on | ON (prompt rule) | 180 | 0.256 | 0.222 | -0.033 | 10 | 16 | 0.327 |

## 2. Conditions compared on the same images (shared R1)

- **ON (prompt rule)** vs **OFF (no rule)**: only-second-right 4, only-first-right 5, McNemar p = 1.000
- **ON (prompt rule)** vs **HARD (code-enforced)**: only-second-right 3, only-first-right 7, McNemar p = 0.344
- **OFF (no rule)** vs **HARD (code-enforced)**: only-second-right 3, only-first-right 6, McNemar p = 0.508
- **ON (prompt rule)** vs **OFF (no rule)**: only-second-right 17, only-first-right 22, McNemar p = 0.522
- **ON (prompt rule)** vs **HARD (code-enforced)**: only-second-right 28, only-first-right 16, McNemar p = 0.096
- **OFF (no rule)** vs **HARD (code-enforced)**: only-second-right 34, only-first-right 17, McNemar p = 0.024

## 3. Individual agents (accuracy R1 → R2 → R3, flips R1→R3)

| run | agent | R1 | R2 | R3 | changed | wrong→right | right→wrong |
|---|---|---|---|---|---|---|---|
| 20260923_1719_main200_citrusA_ev-on | qwen2.5vl:7b | 0.363 | 0.379 | 0.384 | 60 | 26 | 22 |
| 20260923_1719_main200_citrusA_ev-on | qwen2.5vl:3b | 0.363 | 0.363 | 0.347 | 24 | 4 | 7 |
| 20260923_1719_main200_citrusA_ev-on | llava:7b | 0.284 | 0.374 | 0.389 | 76 | 36 | 16 |
| 20260924_0018_main200_citrusA_ev-off | qwen2.5vl:7b | 0.363 | 0.389 | 0.400 | 55 | 25 | 18 |
| 20260924_0018_main200_citrusA_ev-off | qwen2.5vl:3b | 0.363 | 0.363 | 0.326 | 25 | 3 | 10 |
| 20260924_0018_main200_citrusA_ev-off | llava:7b | 0.284 | 0.379 | 0.432 | 84 | 45 | 17 |
| 20260924_1014_main200_citrusA_ev-hard | qwen2.5vl:7b | 0.363 | 0.358 | 0.358 | 1 | 0 | 1 |
| 20260924_1014_main200_citrusA_ev-hard | qwen2.5vl:3b | 0.363 | 0.363 | 0.374 | 21 | 4 | 2 |
| 20260924_1014_main200_citrusA_ev-hard | llava:7b | 0.284 | 0.289 | 0.305 | 11 | 6 | 2 |
| 20260924_1638_main180_zenodo_ev-on | qwen2.5vl:7b | 0.239 | 0.233 | 0.217 | 42 | 3 | 7 |
| 20260924_1638_main180_zenodo_ev-on | llava:7b | 0.167 | 0.189 | 0.211 | 60 | 10 | 2 |
| 20260924_1638_main180_zenodo_ev-on | qwen2.5vl:3b | 0.128 | 0.128 | 0.161 | 66 | 12 | 6 |
| 20261011_1354_main200_citrusA_ev-on | qwen2.5vl:7b | 0.347 | 0.321 | 0.237 | 79 | 16 | 37 |
| 20261011_1354_main200_citrusA_ev-on | gemma3:4b | 0.242 | 0.226 | 0.268 | 86 | 35 | 30 |
| 20261011_1354_main200_citrusA_ev-on | moondream:latest | 0.000 | 0.000 | 0.074 | 36 | 14 | 0 |
| 20261011_1429_main200_citrusA_ev-off | qwen2.5vl:7b | 0.347 | 0.305 | 0.211 | 86 | 17 | 43 |
| 20261011_1429_main200_citrusA_ev-off | gemma3:4b | 0.242 | 0.226 | 0.211 | 48 | 17 | 23 |
| 20261011_1429_main200_citrusA_ev-off | moondream:latest | 0.000 | 0.005 | 0.047 | 25 | 9 | 0 |
| 20261011_1512_main200_citrusA_ev-hard | qwen2.5vl:7b | 0.347 | 0.300 | 0.300 | 11 | 1 | 10 |
| 20261011_1512_main200_citrusA_ev-hard | gemma3:4b | 0.242 | 0.232 | 0.237 | 82 | 28 | 29 |
| 20261011_1512_main200_citrusA_ev-hard | moondream:latest | 0.000 | 0.000 | 0.053 | 30 | 10 | 0 |
| 20261011_1528_main180_zenodo_ev-on | gemma3:4b | 0.256 | 0.261 | 0.183 | 44 | 14 | 12 |
| 20261011_1528_main180_zenodo_ev-on | moondream:latest | 0.000 | 0.000 | 0.000 | 2 | 1 | 0 |
| 20261011_1528_main180_zenodo_ev-on | qwen2.5vl:7b | 0.000 | 0.000 | 0.000 | 0 | 0 | 0 |

## 4. Rule compliance and convergence

| run | opinion changes (R1→R2, R2→R3) | changes with NO new evidence | reverted by code | unanimous R1 | unanimous R3 | self-named influence |
|---|---|---|---|---|---|---|
| 20260923_1719_main200_citrusA_ev-on | 167 | 143 (86%) | - | 12% | 70% | 51 |
| 20260924_0018_main200_citrusA_ev-off | 168 | 144 (86%) | - | 12% | 62% | 60 |
| 20260924_1014_main200_citrusA_ev-hard | 33 | 0 (0%) | 207 | 12% | 23% | 50 |
| 20260924_1638_main180_zenodo_ev-on | 195 | 129 (66%) | 0 | 32% | 57% | 41 |
| 20261011_1354_main200_citrusA_ev-on | 209 | 118 (56%) | 0 | 0% | 5% | 24 |
| 20261011_1429_main200_citrusA_ev-off | 169 | 114 (67%) | 0 | 0% | 7% | 5 |
| 20261011_1512_main200_citrusA_ev-hard | 125 | 32 (26%) | 83 | 0% | 3% | 24 |
| 20261011_1528_main180_zenodo_ev-on | 52 | 36 (69%) | 0 | 0% | 0% | 0 |

## 5. Per class accuracy (before → after) and what the group answered

**20260923_1719_main200_citrusA_ev-on**

- Black Spot (n=50): 0.20 → 0.28  | final answers: Greening 25, Black Spot 14, Healthy 10, Canker 1
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 43, Greening 5, Healthy 2
- Greening (n=50): 0.60 → 0.64  | final answers: Greening 32, Healthy 17, Black Spot 1
- Healthy (n=40): 0.75 → 0.70  | final answers: Healthy 28, Greening 12

**20260924_0018_main200_citrusA_ev-off**

- Black Spot (n=50): 0.20 → 0.22  | final answers: Greening 27, Healthy 11, Black Spot 11, Canker 1
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 44, Greening 4, Healthy 2
- Greening (n=50): 0.60 → 0.66  | final answers: Greening 33, Healthy 16, Black Spot 1
- Healthy (n=40): 0.75 → 0.72  | final answers: Healthy 29, Greening 11

**20260924_1014_main200_citrusA_ev-hard**

- Black Spot (n=50): 0.20 → 0.22  | final answers: Greening 31, Black Spot 11, Healthy 8
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 45, Greening 3, Healthy 2
- Greening (n=50): 0.60 → 0.62  | final answers: Greening 31, Healthy 15, Black Spot 4
- Healthy (n=40): 0.75 → 0.70  | final answers: Healthy 28, Greening 11, Black Spot 1

**20260924_1638_main180_zenodo_ev-on**

- Greasy Spot (n=15): 0.53 → 0.87  | final answers: Greasy Spot 13, Healthy 2
- Greening (n=15): 0.27 → 0.20  | final answers: Healthy 4, Greasy Spot 4, Greening 3, Iron Deficiency 3
- Healthy (n=15): 1.00 → 1.00  | final answers: Healthy 15
- Iron Deficiency (n=15): 0.00 → 0.00  | final answers: Healthy 14, Greasy Spot 1
- Leaf Miner (n=15): 0.40 → 0.40  | final answers: Greasy Spot 6, Leaf Miner 6, Red Scale Sequelae 1, Red Scale 1
- Magnesium Deficiency (n=15): 0.07 → 0.00  | final answers: Greasy Spot 9, Healthy 5, Iron Deficiency 1
- Manganese Deficiency (n=15): 0.00 → 0.00  | final answers: Greasy Spot 9, Iron Deficiency 3, Magnesium Deficiency 1, Healthy 1
- Nitrogen Deficiency (n=15): 0.00 → 0.00  | final answers: Healthy 8, Greasy Spot 7
- Red Scale (n=15): 0.00 → 0.00  | final answers: Greasy Spot 13, Red Scale Sequelae 2
- Red Scale Sequelae (n=15): 0.00 → 0.00  | final answers: Greasy Spot 10, Healthy 2, Leaf Miner 1, Iron Deficiency 1
- Texas Mite (n=15): 0.00 → 0.00  | final answers: Healthy 14, Greasy Spot 1
- Zinc Deficiency (n=15): 0.00 → 0.00  | final answers: Healthy 5, Magnesium Deficiency 4, Greening 3, Iron Deficiency 2

**20261011_1354_main200_citrusA_ev-on**

- Black Spot (n=50): 0.20 → 0.50  | final answers: Black Spot 25, Greening 18, Canker 7
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 47, Greening 3
- Greening (n=50): 0.92 → 0.40  | final answers: Black Spot 27, Greening 20, Canker 3
- Healthy (n=40): 0.25 → 0.00  | final answers: Black Spot 37, Greening 2, Canker 1

**20261011_1429_main200_citrusA_ev-off**

- Black Spot (n=50): 0.20 → 0.54  | final answers: Black Spot 27, Greening 17, Canker 6
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 48, Greening 2
- Greening (n=50): 0.92 → 0.26  | final answers: Black Spot 33, Greening 13, Canker 3, Healthy 1
- Healthy (n=40): 0.25 → 0.00  | final answers: Black Spot 34, Greening 4, Canker 2

**20261011_1512_main200_citrusA_ev-hard**

- Black Spot (n=50): 0.20 → 0.24  | final answers: Greening 35, Black Spot 12, Canker 3
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 44, Greening 6
- Greening (n=50): 0.92 → 0.90  | final answers: Greening 45, Black Spot 5
- Healthy (n=40): 0.25 → 0.00  | final answers: Greening 20, Black Spot 19, Canker 1

**20261011_1528_main180_zenodo_ev-on**

- Images (n=60): 0.77 → 0.55  | final answers: Images 47, Masks 12, Rois 1
- Masks (n=60): 0.00 → 0.12  | final answers: Images 49, Masks 11
- Rois (n=60): 0.00 → 0.00  | final answers: Images 42, Masks 18
