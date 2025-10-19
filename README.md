````markdown
# phishing-kobert

한국어 피싱 탐지 데모(API+UI). KoBERT/KoRoBERTa 확률 + 룰 피처를 **Late Fusion**으로 결합.  
PII 마스킹, 임계치/보류(Abstain) 슬라이더 제공. Docker/Compose · GHCR 배포.  
> Python 3.10+ 권장

## 🚀 Quickstart

### A) Docker Compose (권장)
```bash
# .env 파일을 아래 예시대로 만들고 실행
docker compose up -d
# UI: http://localhost:7860
# API: http://localhost:8000/health
````

### B) Local Dev (WSL/Ubuntu)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 터미널 1: API
uvicorn demo.api:app --host 0.0.0.0 --port 8000

# 터미널 2: UI
export API_URL=http://localhost:8000
streamlit run demo/app.py --server.port=7860 --server.address=0.0.0.0
```

---

## 🧰 Environment (.env 예시)

```dotenv
MODEL_NAME=klue/roberta-base
MAX_LEN=128
HF_HOME=/cache/hf
API_URL=http://api:8000
```

| 변수           | 기본값                 | 설명                                        |
| ------------ | ------------------- | ----------------------------------------- |
| `MODEL_NAME` | `klue/roberta-base` | HF 모델 이름(추후 KoBERT 파인튜닝 체크포인트 연동)         |
| `MAX_LEN`    | `128`               | 토큰 최대 길이                                  |
| `HF_HOME`    | `/cache/hf`         | HF 모델 캐시 경로(도커 권장)                        |
| `API_URL`    | `http://api:8000`   | UI→API 엔드포인트(로컬은 `http://localhost:8000`) |

---

## 🐳 docker-compose.yml

```yaml
services:
  api:
    image: ghcr.io/anon418/phishing-kobert:latest
    command: uvicorn demo.api:app --host 0.0.0.0 --port 8000
    ports: ["8000:8000"]
    environment:
      - MODEL_NAME=${MODEL_NAME}
      - MAX_LEN=${MAX_LEN}
      - HF_HOME=${HF_HOME}
    volumes:
      - hf-cache:/cache/hf

  ui:
    image: ghcr.io/anon418/phishing-kobert:latest
    depends_on: [api]
    ports: ["7860:7860"]
    environment:
      - API_URL=${API_URL}
    command: bash -lc 'streamlit run demo/app.py --server.port=7860 --server.address=0.0.0.0'

volumes:
  hf-cache:
```

---

## 🔌 REST API (요약)

### `GET /health`

* 200 OK: `{"status":"ok"}`

### `POST /predict` (예시)

**Request**

```json
{"text":"국민은행 인증이 만료되었습니다. 링크에서 재인증하세요.","threshold":0.5}
```

**Response**

```json
{"prob_lm":0.82,"score_rule":0.67,"score_fused":0.77,"decision":"phishing","abstained":false,"masked_text":"○○은행 인증이 만료되었습니다. 링크에서 재인증하세요.","intents":["credential-harvest","banking"]}
```

---

## 🧩 Features

* **FastAPI** 엔드포인트: `/predict`, `/health`
* **룰 피처 & 의도 태그**: `src/features/rules.py`
* **PII 마스킹**: `src/utils/pii.py` (계좌/전화/메일/URL/주소 토큰화)
* **Late Fusion**: `0.7 × LM + 0.3 × Rule` (UI 임계치/Abstain 슬라이더)
* **Dockerfile / docker-compose**, GH Actions → **GHCR** 자동 빌드

---

## 🧠 Notes

* 기본 모델: `klue/roberta-base` (환경변수로 교체 가능 / KoBERT 파인튜닝 연동 예정)
* Fused Score: `α × P_lm + (1-α) × S_rule` (기본 `α=0.7`)

---

## 📜 License & Data

공개 데이터셋의 원저작권/라이선스 준수. PII는 **마스킹 후** 저장.

```
```
