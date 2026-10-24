# Analysis — 2026-10-18 09:36

## 1. Debate effect per run (R1 weighted vote -> R3 weighted vote)

| run | condition | n | before | after | Δ | wrong→right | right→wrong | McNemar p |
|---|---|---|---|---|---|---|---|---|
| 20261017_1147_main200_jeju_ev-on | ON (prompt rule) | 190 | 0.358 | 0.347 | -0.011 | 6 | 8 | 0.791 |
| 20261017_2145_main200_jeju_ev-hard | HARD (code-enforced) | 190 | 0.358 | 0.332 | -0.026 | 2 | 7 | 0.180 |
| 20261017_2336_main200_jeju_ev-off | OFF (no rule) | 190 | 0.358 | 0.337 | -0.021 | 7 | 11 | 0.481 |

## 2. Conditions compared on the same images (shared R1)

- **ON (prompt rule)** vs **HARD (code-enforced)**: only-second-right 6, only-first-right 9, McNemar p = 0.607
- **ON (prompt rule)** vs **OFF (no rule)**: only-second-right 5, only-first-right 7, McNemar p = 0.774
- **HARD (code-enforced)** vs **OFF (no rule)**: only-second-right 8, only-first-right 7, McNemar p = 1.000

## 3. Individual agents (accuracy R1 → R2 → R3, flips R1→R3)

| run | agent | R1 | R2 | R3 | changed | wrong→right | right→wrong |
|---|---|---|---|---|---|---|---|
| 20261017_1147_main200_jeju_ev-on | qwen2.5vl:3b | 0.347 | 0.358 | 0.342 | 26 | 5 | 8 |
| 20261017_1147_main200_jeju_ev-on | qwen2.5vl:7b | 0.337 | 0.337 | 0.332 | 16 | 3 | 4 |
| 20261017_1147_main200_jeju_ev-on | llava:7b | 0.263 | 0.374 | 0.374 | 66 | 27 | 6 |
| 20261017_2145_main200_jeju_ev-hard | qwen2.5vl:3b | 0.347 | 0.358 | 0.342 | 24 | 5 | 8 |
| 20261017_2145_main200_jeju_ev-hard | qwen2.5vl:7b | 0.337 | 0.337 | 0.326 | 6 | 1 | 3 |
| 20261017_2145_main200_jeju_ev-hard | llava:7b | 0.263 | 0.295 | 0.295 | 11 | 6 | 0 |
| 20261017_2336_main200_jeju_ev-off | qwen2.5vl:3b | 0.347 | 0.358 | 0.342 | 19 | 5 | 8 |
| 20261017_2336_main200_jeju_ev-off | qwen2.5vl:7b | 0.337 | 0.342 | 0.326 | 29 | 4 | 6 |
| 20261017_2336_main200_jeju_ev-off | llava:7b | 0.263 | 0.374 | 0.353 | 66 | 24 | 7 |

## 4. Rule compliance and convergence

| run | opinion changes (R1→R2, R2→R3) | changes with NO new evidence | reverted by code | unanimous R1 | unanimous R3 | self-named influence |
|---|---|---|---|---|---|---|
| 20261017_1147_main200_jeju_ev-on | 111 | 81 (73%) | 0 | 53% | 73% | 21 |
| 20261017_2145_main200_jeju_ev-hard | 42 | 0 (0%) | 106 | 53% | 53% | 25 |
| 20261017_2336_main200_jeju_ev-off | 121 | 100 (83%) | 0 | 53% | 77% | 37 |

## 5. Per class accuracy (before → after) and what the group answered

**20261017_1147_main200_jeju_ev-on**

- Aphid (n=50): 0.46 → 0.46  | final answers: Aphid 23, Healthy 18, Citrus Red Mite 8, Canker 1
- Canker (n=50): 0.10 → 0.02  | final answers: Citrus Red Mite 33, Healthy 15, Aphid 1, Canker 1
- Citrus Red Mite (n=50): 0.00 → 0.04  | final answers: Healthy 47, Citrus Red Mite 2, Canker 1
- Healthy (n=40): 1.00 → 1.00  | final answers: Healthy 40

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
