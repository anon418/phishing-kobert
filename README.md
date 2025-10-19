# phishing-kobert

한국어 피싱 탐지 데모(API+UI). KoBERT/KoRoBERTa 기반 분류 확률과 룰 피처를 **Late Fusion**으로 결합.
PII 마스킹, 임계치/보류(Abstain) 슬라이더 제공. Docker & GHCR로 배포.

## Features
- FastAPI `/predict`, `/health`
- 룰 피처 & 의도 태그 샘플: `src/features/rules.py`
- PII 마스킹: `src/utils/pii.py` (계좌/전화/메일/URL/주소 → 토큰화)
- Late Fusion(예: 0.7*LM + 0.3*Rule), 임계치/보류 슬라이더(UI)
- Dockerfile / docker-compose, GitHub Actions → GHCR 자동 빌드

## Quickstart (WSL/Ubuntu)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# 터미널1
uvicorn demo.api:app --host 0.0.0.0 --port 8000
# 터미널2
streamlit run demo/app.py --server.port=7860 --server.address=0.0.0.0
# UI: http://localhost:7860  /  API: http://localhost:8000/health
