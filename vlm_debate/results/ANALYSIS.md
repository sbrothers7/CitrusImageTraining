# Analysis — 2026-10-24 17:18

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
| 20261017_1057_main200_citrusA_ev-on | ON (prompt rule) | 190 | 0.379 | 0.384 | +0.005 | 4 | 3 | 1.000 |
| 20261017_1127_main200_citrusA_ev-off | OFF (no rule) | 190 | 0.379 | 0.400 | +0.021 | 8 | 4 | 0.388 |
| 20261017_1147_main200_jeju_ev-on | ON (prompt rule) | 190 | 0.358 | 0.347 | -0.011 | 6 | 8 | 0.791 |
| 20261017_1150_main200_citrusA_ev-hard | HARD (code-enforced) | 190 | 0.379 | 0.379 | +0.000 | 7 | 7 | 1.000 |
| 20261017_1407_main180_zenodo_ev-on | ON (prompt rule) | 180 | 0.206 | 0.222 | +0.017 | 5 | 2 | 0.453 |
| 20261017_2145_main200_jeju_ev-hard | HARD (code-enforced) | 190 | 0.358 | 0.332 | -0.026 | 2 | 7 | 0.180 |
| 20261017_2336_main200_jeju_ev-off | OFF (no rule) | 190 | 0.358 | 0.337 | -0.021 | 7 | 11 | 0.481 |
| 20261024_1155_arch_granite_ev-on | ON (prompt rule) | 190 | 0.389 | 0.379 | -0.011 | 8 | 10 | 0.815 |
| 20261024_1221_arch_granite_ev-off | OFF (no rule) | 190 | 0.389 | 0.400 | +0.011 | 8 | 6 | 0.791 |
| 20261024_1241_arch_granite_ev-hard | HARD (code-enforced) | 190 | 0.389 | 0.384 | -0.005 | 8 | 9 | 1.000 |
| 20261024_1301_arch_gemma_ev-on | ON (prompt rule) | 190 | 0.389 | 0.342 | -0.047 | 6 | 15 | 0.078 |
| 20261024_1329_arch_gemma_ev-off | OFF (no rule) | 190 | 0.389 | 0.342 | -0.047 | 2 | 11 | 0.022 |
| 20261024_1351_arch_gemma_ev-hard | HARD (code-enforced) | 190 | 0.389 | 0.347 | -0.042 | 2 | 10 | 0.039 |

## 2. Conditions compared on the same images (shared R1)

- **ON (prompt rule)** vs **OFF (no rule)**: only-second-right 4, only-first-right 5, McNemar p = 1.000
- **ON (prompt rule)** vs **HARD (code-enforced)**: only-second-right 3, only-first-right 7, McNemar p = 0.344
- **OFF (no rule)** vs **HARD (code-enforced)**: only-second-right 3, only-first-right 6, McNemar p = 0.508
- **ON (prompt rule)** vs **OFF (no rule)**: only-second-right 17, only-first-right 22, McNemar p = 0.522
- **ON (prompt rule)** vs **HARD (code-enforced)**: only-second-right 28, only-first-right 16, McNemar p = 0.096
- **OFF (no rule)** vs **HARD (code-enforced)**: only-second-right 34, only-first-right 17, McNemar p = 0.024
- **ON (prompt rule)** vs **OFF (no rule)**: only-second-right 7, only-first-right 4, McNemar p = 0.549
- **ON (prompt rule)** vs **HARD (code-enforced)**: only-second-right 6, only-first-right 7, McNemar p = 1.000
- **OFF (no rule)** vs **HARD (code-enforced)**: only-second-right 6, only-first-right 10, McNemar p = 0.454
- **ON (prompt rule)** vs **HARD (code-enforced)**: only-second-right 6, only-first-right 9, McNemar p = 0.607
- **ON (prompt rule)** vs **OFF (no rule)**: only-second-right 5, only-first-right 7, McNemar p = 0.774
- **HARD (code-enforced)** vs **OFF (no rule)**: only-second-right 8, only-first-right 7, McNemar p = 1.000
- **ON (prompt rule)** vs **OFF (no rule)**: only-second-right 9, only-first-right 5, McNemar p = 0.424
- **ON (prompt rule)** vs **HARD (code-enforced)**: only-second-right 6, only-first-right 5, McNemar p = 1.000
- **OFF (no rule)** vs **HARD (code-enforced)**: only-second-right 5, only-first-right 8, McNemar p = 0.581
- **ON (prompt rule)** vs **OFF (no rule)**: only-second-right 8, only-first-right 8, McNemar p = 1.000
- **ON (prompt rule)** vs **HARD (code-enforced)**: only-second-right 10, only-first-right 9, McNemar p = 1.000
- **OFF (no rule)** vs **HARD (code-enforced)**: only-second-right 7, only-first-right 6, McNemar p = 1.000

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
| 20261017_1057_main200_citrusA_ev-on | qwen2.5vl:7b | 0.395 | 0.411 | 0.379 | 54 | 19 | 22 |
| 20261017_1057_main200_citrusA_ev-on | qwen2.5vl:3b | 0.363 | 0.363 | 0.384 | 20 | 5 | 1 |
| 20261017_1057_main200_citrusA_ev-on | llava:7b | 0.274 | 0.374 | 0.411 | 68 | 35 | 9 |
| 20261017_1127_main200_citrusA_ev-off | qwen2.5vl:7b | 0.395 | 0.416 | 0.395 | 48 | 16 | 16 |
| 20261017_1127_main200_citrusA_ev-off | qwen2.5vl:3b | 0.363 | 0.363 | 0.368 | 24 | 5 | 4 |
| 20261017_1127_main200_citrusA_ev-off | llava:7b | 0.274 | 0.400 | 0.437 | 79 | 40 | 9 |
| 20261017_1147_main200_jeju_ev-on | qwen2.5vl:3b | 0.347 | 0.358 | 0.342 | 26 | 5 | 8 |
| 20261017_1147_main200_jeju_ev-on | qwen2.5vl:7b | 0.337 | 0.337 | 0.332 | 16 | 3 | 4 |
| 20261017_1147_main200_jeju_ev-on | llava:7b | 0.263 | 0.374 | 0.374 | 66 | 27 | 6 |
| 20261017_1150_main200_citrusA_ev-hard | qwen2.5vl:7b | 0.395 | 0.384 | 0.374 | 5 | 0 | 4 |
| 20261017_1150_main200_citrusA_ev-hard | qwen2.5vl:3b | 0.363 | 0.347 | 0.347 | 28 | 5 | 8 |
| 20261017_1150_main200_citrusA_ev-hard | llava:7b | 0.274 | 0.279 | 0.295 | 8 | 5 | 1 |
| 20261017_1407_main180_zenodo_ev-on | qwen2.5vl:7b | 0.244 | 0.228 | 0.222 | 29 | 1 | 5 |
| 20261017_1407_main180_zenodo_ev-on | llava:7b | 0.178 | 0.211 | 0.211 | 66 | 10 | 4 |
| 20261017_1407_main180_zenodo_ev-on | qwen2.5vl:3b | 0.139 | 0.144 | 0.183 | 58 | 10 | 2 |
| 20261017_2145_main200_jeju_ev-hard | qwen2.5vl:3b | 0.347 | 0.358 | 0.342 | 24 | 5 | 8 |
| 20261017_2145_main200_jeju_ev-hard | qwen2.5vl:7b | 0.337 | 0.337 | 0.326 | 6 | 1 | 3 |
| 20261017_2145_main200_jeju_ev-hard | llava:7b | 0.263 | 0.295 | 0.295 | 11 | 6 | 0 |
| 20261017_2336_main200_jeju_ev-off | qwen2.5vl:3b | 0.347 | 0.358 | 0.342 | 19 | 5 | 8 |
| 20261017_2336_main200_jeju_ev-off | qwen2.5vl:7b | 0.337 | 0.342 | 0.326 | 29 | 4 | 6 |
| 20261017_2336_main200_jeju_ev-off | llava:7b | 0.263 | 0.374 | 0.353 | 66 | 24 | 7 |
| 20261024_1155_arch_granite_ev-on | qwen2.5vl:3b | 0.395 | 0.389 | 0.368 | 54 | 13 | 18 |
| 20261024_1155_arch_granite_ev-on | qwen2.5vl:7b | 0.363 | 0.395 | 0.432 | 35 | 22 | 9 |
| 20261024_1155_arch_granite_ev-on | granite3.2-vision:latest | 0.358 | 0.353 | 0.326 | 13 | 3 | 9 |
| 20261024_1221_arch_granite_ev-off | qwen2.5vl:3b | 0.395 | 0.389 | 0.405 | 37 | 11 | 9 |
| 20261024_1221_arch_granite_ev-off | qwen2.5vl:7b | 0.363 | 0.400 | 0.432 | 27 | 19 | 6 |
| 20261024_1221_arch_granite_ev-off | granite3.2-vision:latest | 0.358 | 0.358 | 0.363 | 10 | 5 | 4 |
| 20261024_1241_arch_granite_ev-hard | qwen2.5vl:3b | 0.395 | 0.389 | 0.379 | 46 | 11 | 14 |
| 20261024_1241_arch_granite_ev-hard | qwen2.5vl:7b | 0.363 | 0.342 | 0.347 | 8 | 2 | 5 |
| 20261024_1241_arch_granite_ev-hard | granite3.2-vision:latest | 0.358 | 0.358 | 0.368 | 7 | 4 | 2 |
| 20261024_1301_arch_gemma_ev-on | qwen2.5vl:7b | 0.384 | 0.368 | 0.337 | 33 | 10 | 19 |
| 20261024_1301_arch_gemma_ev-on | qwen2.5vl:3b | 0.358 | 0.358 | 0.368 | 51 | 14 | 12 |
| 20261024_1301_arch_gemma_ev-on | gemma3:4b | 0.242 | 0.242 | 0.316 | 106 | 45 | 31 |
| 20261024_1329_arch_gemma_ev-off | qwen2.5vl:7b | 0.384 | 0.358 | 0.347 | 26 | 8 | 15 |
| 20261024_1329_arch_gemma_ev-off | qwen2.5vl:3b | 0.358 | 0.358 | 0.368 | 59 | 16 | 14 |
| 20261024_1329_arch_gemma_ev-off | gemma3:4b | 0.242 | 0.242 | 0.311 | 93 | 40 | 27 |
| 20261024_1351_arch_gemma_ev-hard | qwen2.5vl:7b | 0.384 | 0.368 | 0.353 | 6 | 0 | 6 |
| 20261024_1351_arch_gemma_ev-hard | qwen2.5vl:3b | 0.358 | 0.358 | 0.368 | 43 | 11 | 9 |
| 20261024_1351_arch_gemma_ev-hard | gemma3:4b | 0.242 | 0.237 | 0.274 | 38 | 14 | 8 |

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
| 20261017_1057_main200_citrusA_ev-on | 146 | 123 (84%) | 0 | 18% | 72% | 62 |
| 20261017_1127_main200_citrusA_ev-off | 153 | 121 (79%) | 0 | 18% | 69% | 58 |
| 20261017_1147_main200_jeju_ev-on | 111 | 81 (73%) | 0 | 53% | 73% | 21 |
| 20261017_1150_main200_citrusA_ev-hard | 41 | 0 (0%) | 183 | 18% | 25% | 58 |
| 20261017_1407_main180_zenodo_ev-on | 173 | 116 (67%) | 0 | 32% | 59% | 42 |
| 20261017_2145_main200_jeju_ev-hard | 42 | 0 (0%) | 106 | 53% | 53% | 25 |
| 20261017_2336_main200_jeju_ev-off | 121 | 100 (83%) | 0 | 53% | 77% | 37 |
| 20261024_1155_arch_granite_ev-on | 113 | 46 (41%) | 0 | 15% | 44% | 73 |
| 20261024_1221_arch_granite_ev-off | 80 | 32 (40%) | 0 | 15% | 36% | 93 |
| 20261024_1241_arch_granite_ev-hard | 62 | 0 (0%) | 62 | 15% | 35% | 78 |
| 20261024_1301_arch_gemma_ev-on | 192 | 106 (55%) | 0 | 11% | 65% | 22 |
| 20261024_1329_arch_gemma_ev-off | 183 | 95 (52%) | 0 | 11% | 69% | 26 |
| 20261024_1351_arch_gemma_ev-hard | 87 | 0 (0%) | 116 | 11% | 31% | 24 |

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

**20261017_1057_main200_citrusA_ev-on**

- Black Spot (n=50): 0.18 → 0.20  | final answers: Greening 27, Healthy 10, Black Spot 10, Canker 3
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 43, Greening 6, Healthy 1
- Greening (n=50): 0.58 → 0.60  | final answers: Greening 30, Healthy 17, Black Spot 3
- Healthy (n=40): 0.85 → 0.82  | final answers: Healthy 33, Greening 7

**20261017_1127_main200_citrusA_ev-off**

- Black Spot (n=50): 0.18 → 0.24  | final answers: Greening 28, Black Spot 12, Healthy 8, Canker 2
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 44, Greening 5, Healthy 1
- Greening (n=50): 0.58 → 0.68  | final answers: Greening 34, Healthy 13, Black Spot 3
- Healthy (n=40): 0.85 → 0.75  | final answers: Healthy 30, Greening 10

**20261017_1147_main200_jeju_ev-on**

- Aphid (n=50): 0.46 → 0.46  | final answers: Aphid 23, Healthy 18, Citrus Red Mite 8, Canker 1
- Canker (n=50): 0.10 → 0.02  | final answers: Citrus Red Mite 33, Healthy 15, Aphid 1, Canker 1
- Citrus Red Mite (n=50): 0.00 → 0.04  | final answers: Healthy 47, Citrus Red Mite 2, Canker 1
- Healthy (n=40): 1.00 → 1.00  | final answers: Healthy 40

**20261017_1150_main200_citrusA_ev-hard**

- Black Spot (n=50): 0.18 → 0.20  | final answers: Greening 29, Healthy 10, Black Spot 10, Canker 1
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 43, Greening 6, Healthy 1
- Greening (n=50): 0.58 → 0.70  | final answers: Greening 35, Healthy 13, Black Spot 2
- Healthy (n=40): 0.85 → 0.68  | final answers: Healthy 27, Greening 11, Black Spot 2

**20261017_1407_main180_zenodo_ev-on**

- Greasy Spot (n=15): 0.67 → 0.93  | final answers: Greasy Spot 14, Healthy 1
- Greening (n=15): 0.33 → 0.27  | final answers: Greasy Spot 5, Healthy 4, Greening 4, Iron Deficiency 2
- Healthy (n=15): 1.00 → 1.00  | final answers: Healthy 15
- Iron Deficiency (n=15): 0.00 → 0.00  | final answers: Healthy 14, Greasy Spot 1
- Leaf Miner (n=15): 0.47 → 0.47  | final answers: Leaf Miner 7, Greasy Spot 6, Healthy 2
- Magnesium Deficiency (n=15): 0.00 → 0.00  | final answers: Greasy Spot 11, Iron Deficiency 2, Greening 1, Healthy 1
- Manganese Deficiency (n=15): 0.00 → 0.00  | final answers: Greasy Spot 10, Magnesium Deficiency 2, Iron Deficiency 2, Greening 1
- Nitrogen Deficiency (n=15): 0.00 → 0.00  | final answers: Healthy 9, Greasy Spot 6
- Red Scale (n=15): 0.00 → 0.00  | final answers: Greasy Spot 12, Red Scale Sequelae 3
- Red Scale Sequelae (n=15): 0.00 → 0.00  | final answers: Greasy Spot 13, Iron Deficiency 1, Healthy 1
- Texas Mite (n=15): 0.00 → 0.00  | final answers: Healthy 15
- Zinc Deficiency (n=15): 0.00 → 0.00  | final answers: Greasy Spot 5, Magnesium Deficiency 4, Healthy 4, Iron Deficiency 2

**20261017_2145_main200_jeju_ev-hard**

- Aphid (n=50): 0.46 → 0.42  | final answers: Aphid 21, Healthy 20, Citrus Red Mite 9
- Canker (n=50): 0.10 → 0.08  | final answers: Healthy 24, Citrus Red Mite 21, Canker 4, Aphid 1
- Citrus Red Mite (n=50): 0.00 → 0.00  | final answers: Healthy 48, Canker 2
- Healthy (n=40): 1.00 → 0.95  | final answers: Healthy 38, Citrus Red Mite 2

**20261017_2336_main200_jeju_ev-off**

- Aphid (n=50): 0.46 → 0.42  | final answers: Aphid 21, Healthy 18, Citrus Red Mite 10, Canker 1
- Canker (n=50): 0.10 → 0.06  | final answers: Citrus Red Mite 30, Healthy 16, Canker 3, Aphid 1
- Citrus Red Mite (n=50): 0.00 → 0.00  | final answers: Healthy 49, Canker 1
- Healthy (n=40): 1.00 → 1.00  | final answers: Healthy 40

**20261024_1155_arch_granite_ev-on**

- Black Spot (n=50): 0.34 → 0.44  | final answers: Greening 25, Black Spot 22, Healthy 3
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 45, Greening 5
- Greening (n=50): 0.64 → 0.70  | final answers: Greening 35, Black Spot 10, Healthy 5
- Healthy (n=40): 0.62 → 0.38  | final answers: Greening 15, Healthy 15, Black Spot 10

**20261024_1221_arch_granite_ev-off**

- Black Spot (n=50): 0.34 → 0.40  | final answers: Greening 26, Black Spot 20, Healthy 4
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 44, Greening 5, Healthy 1
- Greening (n=50): 0.64 → 0.72  | final answers: Greening 36, Black Spot 8, Healthy 6
- Healthy (n=40): 0.62 → 0.50  | final answers: Healthy 20, Greening 14, Black Spot 6

**20261024_1241_arch_granite_ev-hard**

- Black Spot (n=50): 0.34 → 0.42  | final answers: Greening 25, Black Spot 21, Healthy 4
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 44, Greening 5, Healthy 1
- Greening (n=50): 0.64 → 0.72  | final answers: Greening 36, Healthy 7, Black Spot 7
- Healthy (n=40): 0.62 → 0.40  | final answers: Healthy 16, Greening 14, Black Spot 10

**20261024_1301_arch_gemma_ev-on**

- Black Spot (n=50): 0.28 → 0.30  | final answers: Greening 33, Black Spot 15, Healthy 2
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 42, Greening 8
- Greening (n=50): 0.92 → 0.82  | final answers: Greening 41, Black Spot 5, Healthy 4
- Healthy (n=40): 0.35 → 0.23  | final answers: Black Spot 18, Greening 13, Healthy 9

**20261024_1329_arch_gemma_ev-off**

- Black Spot (n=50): 0.28 → 0.28  | final answers: Greening 35, Black Spot 14, Healthy 1
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 42, Greening 8
- Greening (n=50): 0.92 → 0.88  | final answers: Greening 44, Black Spot 5, Healthy 1
- Healthy (n=40): 0.35 → 0.17  | final answers: Greening 16, Black Spot 16, Healthy 7, Canker 1

**20261024_1351_arch_gemma_ev-hard**

- Black Spot (n=50): 0.28 → 0.28  | final answers: Greening 36, Black Spot 14
- Canker (n=50): 0.00 → 0.00  | final answers: Black Spot 46, Greening 4
- Greening (n=50): 0.92 → 0.90  | final answers: Greening 45, Black Spot 5
- Healthy (n=40): 0.35 → 0.17  | final answers: Greening 19, Black Spot 14, Healthy 7
