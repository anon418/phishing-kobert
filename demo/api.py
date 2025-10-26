import os
import logging
from typing import Dict, Any, List

from fastapi import FastAPI
from pydantic import BaseModel

# 내부 유틸/모듈
from src.utils.pii import mask
from src.features.rules import score as rule_score, intents as rule_intents
from demo.predict import predict_prob

# ---------- 설정 ----------
# 환경변수(없으면 디폴트)
THRESHOLD = float(os.getenv("THRESHOLD", "0.50"))
ABSTAIN_BAND = float(os.getenv("ABSTAIN_BAND", "0.05"))
FUSION_LM = float(os.getenv("FUSION_LM", "0.7"))
FUSION_RULE = float(os.getenv("FUSION_RULE", "0.3"))

# 로깅(PII는 반드시 마스킹된 텍스트만 기록)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("phish_api")

# FastAPI 앱
app = FastAPI(title="KoBERT Phishing API", version="0.3.0")


class Inp(BaseModel):
    text: str


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True}


@app.post("/predict")
def predict(x: Inp) -> Dict[str, Any]:
    """
    - bert_prob: 언어모델(KoBERT/KoRoBERTa) 확률(피싱일 확률로 가정)
    - rule_prob: 룰/피처 기반 점수(0~1)
    - prob: Late Fusion으로 결합된 최종 점수
    - decision: phish / benign / abstain
    - intents: 간단 의도/전술 태그 샘플
    - masked: PII 마스킹 텍스트
    - threshold/abstain_band/fusion_weights: 현재 의사결정 파라미터
    """
    text = x.text or ""
    masked_text = mask(text)

    # 1) 모델 확률
    bert_prob: float = float(predict_prob(text))  # 0~1

    # 2) 룰 점수(0~1) + 의도 태그
    rule_prob: float = float(rule_score(text))    # 0~1
    intents: List[str] = rule_intents(text)

    # 3) Late Fusion
    #    (가중치 합이 1이 아니어도 내부에서 비율로 동작하지만 기본은 0.7/0.3 권장)
    w_sum = (FUSION_LM + FUSION_RULE) or 1.0
    prob = (FUSION_LM * bert_prob + FUSION_RULE * rule_prob) / w_sum

    # 4) Abstain 정책
    #    임계치 근처(±ABSTAIN_BAND)면 보류
    distance = abs(prob - THRESHOLD)
    abstain = distance <= ABSTAIN_BAND

    if abstain:
        decision = "abstain"
    else:
        decision = "phish" if prob >= THRESHOLD else "benign"

    # 5) 로그(마스킹된 텍스트만 기록)
    log.info(
        "masked=%s bert=%.4f rule=%.4f prob=%.4f thr=%.2f band=%.2f decision=%s",
        masked_text, bert_prob, rule_prob, prob, THRESHOLD, ABSTAIN_BAND, decision
    )

    # 6) 응답
    return {
        "bert_prob": round(bert_prob, 4),
        "rule_prob": round(rule_prob, 4),
        "prob": round(prob, 4),
        "decision": decision,
        "intents": intents,
        "masked": masked_text,
        "threshold": THRESHOLD,
        "abstain_band": ABSTAIN_BAND,
        "fusion_weights": {"lm": FUSION_LM, "rule": FUSION_RULE},
    }
