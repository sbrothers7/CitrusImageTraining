# 감귤 병해 진단 — 시각-언어 모델(VLM) 다중 에이전트 토론 실험

VIDA(독립 진단) → PANDA(이름을 부르는 동료 토론) 파이프라인
(Al Juboori et al., 2026, *Frontiers in Plant Science*)을 감귤 잎 데이터에 맞춰
다시 구현하고, **반-아첨(anti-sycophancy) 장치**의 효과를 제거 실험으로 검증한 코드입니다.

- 같은 리포지토리 루트의 CNN 파이프라인(run_1~run_5)은 "공개 데이터로 학습한 CNN이 다른
  출처 사진에서 무너지는가"를 보는 기준 실험이고, 이 폴더는 학습 없이 진단하는 VLM 쪽 실험입니다.
- 모든 모델은 **로컬(Ollama)** 에서 실행합니다. 상용 API 모델은 예고 없이 폐기되어
  나중에 재현이 불가능하기 때문입니다.

## macOS · Linux (Arch 포함)

```bash
cd vlm_debate
bash run.sh selftest      # 1) 코드 점검 — 모델·데이터 없이 몇 초
```

**1. Ollama 설치 (한 번만)**

| OS | 명령 |
|---|---|
| macOS | `brew install ollama` (또는 https://ollama.com/download 앱) |
| Arch (NVIDIA) | `sudo pacman -S ollama-cuda` |
| Arch (AMD / CPU) | `sudo pacman -S ollama-rocm` / `sudo pacman -S ollama` |
| 기타 Linux | `curl -fsSL https://ollama.com/install.sh \| sh` |

서버가 꺼져 있으면 `run.sh` 가 `ollama serve` 를 백그라운드로 띄웁니다
(Arch 에서 서비스로 쓰려면 `sudo systemctl enable --now ollama`).

**2. 준비와 실험**

```bash
bash run.sh prepare       # 모델 3종 + Mendeley·Zenodo 다운로드(약 15 GB), 중복 검사
bash run.sh finalize      # Zenodo 768px 변환, 모델 선정 확인, 10장 파일럿
bash run.sh main          # 데이터셋 A: ON → OFF   (GPU 기준 7~8시간)
bash run.sh night2        # 데이터셋 A: HARD, 데이터셋 B: ON
bash run.sh analyze       # results/ANALYSIS.md
bash run.sh app           # 웹 콘솔 http://localhost:8765
```

- 파이썬 패키지는 처음 실행할 때 `.venv/` 에 자동 설치됩니다 (Arch·Homebrew 의 시스템 pip 제한 회피).
- 이미지는 `~/citrus-data` 에 저장됩니다. 다른 곳을 쓰려면 `export CITRUS_DATA=/경로` 또는 `.env` 에 적습니다.
  `data/*.json` 의 경로는 이 폴더 기준 **상대경로**라서 OS 에 상관없이 그대로 씁니다.
- 같은 seed 면 Windows·macOS·Linux 에서 **같은 이미지가 뽑히도록** 정렬 순서를 맞춰 두었습니다.
- Apple Silicon 은 GPU(Metal)를 자동으로 씁니다. 모델 속도는 `bash run.sh bench` 로 확인하세요.

**3. 제주 온주밀감 데이터 (AI Hub 635) 로 실험하기**

AI Hub 데이터는 라이선스상 이 저장소에 올리지 않습니다. 각자 받아야 합니다.

1. https://aihub.or.kr 에서 「고품질 과수 작물 통합 데이터」(635) 이용 신청 → 승인 후 API 키 발급
2. AI Hub 의 `aihubshell` 을 `~/Downloads/aihubshell` 에 저장 (다른 곳이면 `--shell 경로`)
3. `.env` 에 `AIHUB_APIKEY=키` 한 줄 추가 (`.env` 는 커밋 금지)

```bash
bash run.sh aihub          # 감귤 4개 파일만(TS1/TL1/VS1/VL1, 약 1.5 GB) → ~/citrus-data/aihub
bash run.sh aihub-prepare  # 라벨 18,000개 전수 검사, 검증용 2,000장 768px 복사, data/citrusJ_aihub_*.json
bash run.sh jeju           # 잎 190장(정상 40, 궤양병·귤응애·진딧물 각 50): ON → HARD → OFF, 약 13시간
bash run.sh jeju-cnn       # 제주 학습용 잎으로 densenet121 학습 → 같은 190장에서 VLM 과 비교 (약 2시간)
```

중간에 끊겨도 `bash run.sh jeju` 를 다시 실행하면 끝난 조건은 건너뜁니다.
다른 사진(직접 찍은 제주 사진 등)은 `data/citrusJ_aihub_leaf.json` 과 같은 형식의 명세를 만들어
`bash run.sh run --dataset data/내명세.json ...` 으로 실행합니다.

## 실행 순서 (Windows, 더블클릭)

| 파일 | 하는 일 |
|---|---|
| `0_selftest.bat` | 가짜 에이전트로 코드 점검 (키·데이터 불필요) |
| `4_prepare_all.bat` | Ollama 설치, 모델 다운로드, Mendeley·Zenodo 데이터 다운로드, 중복 검사 |
| `5_diagnose.bat` | 모델별 속도·형식 준수·GPU 사용 여부 진단 |
| `7_gpu_fix.bat` | Ollama 가 GPU 를 못 잡을 때 복구 (VC++ 런타임 재설치 등) + 모델 선정 + 10장 파일럿 |
| `8_main_overnight.bat` | 본 실험 1: 데이터셋 A 190장, 반-아첨 ON → OFF |
| `9_night2.bat` | 본 실험 2: 데이터셋 A HARD(코드 강제) + 데이터셋 B(Zenodo) ON |
| `3_run.bat` | 웹 콘솔 (http://localhost:8765) |
| `13_aihub_download.bat` | AI Hub 635 감귤 데이터 다운로드·압축 해제 (`.env` 의 `AIHUB_APIKEY`, Git for Windows 필요) |
| `14_aihub_prepare.bat` | 라벨 전수 검사 + 768px 복사본 + 실험 명세 생성 |
| `15_jeju_overnight.bat` | 제주 잎 190장 ON → HARD → OFF + `results/ANALYSIS_jeju.md` |
| `17_jeju_cnn.bat` | 제주 학습용 잎 12,593장으로 densenet121 학습(seed 42/1/2) → 같은 190장에서 VLM 과 비교, `results/jeju_cnn.md` (macOS·Linux: `bash run.sh jeju-cnn`) |
| `11_verify_student_cnn.bat` | 루트의 CNN 실험 재현 검증: densenet121, 단일 출처 vs 두 출처, seed 42/1/2 → `results/verify_student_cnn.md` (macOS·Linux: `bash run.sh verify-student`) |

분석: `py tools\analyze.py` → `results\ANALYSIS.md`
직접 실행: `py tools\run_experiment.py --dataset data\jeju.json --n 100 --tag jeju_ev-on` (옵션은 아래 macOS·Linux 절과 같음)

## 실험 조건

| 조건 | 내용 |
|---|---|
| OFF | 답 변경 제한 없음 |
| ON | R2 지시문에 "새 시각 근거가 있을 때만 바꿀 것" 명시 (원 논문 방식) |
| HARD | ON + 새 근거 없이 바꾼 답을 **코드가 되돌림** |

세 조건은 같은 이미지와 **같은 R1 답**(`--reuse-r1`)을 공유하므로, 차이는 토론 규칙에서만 생깁니다.

## 주요 결과 (공개 데이터)

| 데이터 | 조건 | 토론 전 → 후 | Δ | McNemar p |
|---|---|---|---|---|
| A (Mendeley, 4클래스, 190장) | OFF | 0.368 → 0.384 | +0.016 | 0.45 |
| A | ON | 0.368 → 0.389 | +0.021 | 0.34 |
| A | HARD | 0.368 → 0.368 | 0.000 | 1.00 |
| B (CitrusUAT, 12클래스, 180장) | ON | 0.189 → 0.206 | +0.017 | 0.55 |

- 지시문 규칙은 답 변경의 66–86% 에서 무시됨 (새 근거 "NONE" 인 채로 변경)
- 약한 모델(llava:7b)의 향상(0.284 → 0.43)은 HARD 에서 사라짐(→ 0.305) → 향상의 출처는 **근거 없는 동조**
- 세부: `results/ANALYSIS.md`

## 주요 결과 (제주 온주밀감, AI Hub 635 검증용 잎 190장)

| 조건 | 토론 전 → 후 | Δ | McNemar p | 답 변경 중 새 근거 없음 |
|---|---|---|---|---|
| OFF | 0.358 → 0.337 | −0.021 | 0.48 | 100/121 (83%) |
| ON | 0.358 → 0.347 | −0.011 | 0.79 | 81/111 (73%) |
| HARD | 0.358 → 0.332 | −0.026 | 0.18 | 0/42 (되돌림 106) |

- 실제 상태별 정답률(ON, 토론 후): 정상 100%, 진딧물 46%, 궤양병 2%(대부분 '귤응애'로 답함), 귤응애 4%(대부분 '정상')
- llava:7b 만 오름(0.263 → 0.374, ON) — 대부분 qwen2.5vl:3b 의 답을 따라간 변경
- AI Hub 폴리곤 1,977개는 병변이 아니라 잎·열매 전체 윤곽 → 병변 위치 채점에는 쓸 수 없음
- 세부: `results/ANALYSIS_jeju.md`, `results/aihub_overview.json`

## 폴더

```
src/        vp_core.py (파이프라인 본체), vp_app.py (웹 콘솔), prepare_dataset.py
tools/      prepare_all, diagnose, gpu_check, run_experiment, run_main, run_night2, analyze,
            aihub_fetch, aihub_prepare, run_jeju ...
data/       데이터셋 명세 json (이미지는 C:\citrus-data 에 있고 경로만 참조)
results/    실험별 결과 (CSV, 토론 원문, summary.json, ANALYSIS.md)
```

## 환경

RTX 3070 Laptop (8 GB), Ryzen 7 5800H, Ollama 0.34.3,
모델: llava:7b, qwen2.5vl:7b, qwen2.5vl:3b (temperature 0.2, max 700 tokens), seed 42.
