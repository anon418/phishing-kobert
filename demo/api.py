from fastapi import FastAPI
from pydantic import BaseModel
from src.utils.pii import mask
from src.features.rules import rule_score, intent_tags
from demo.predict import predict_prob

app = FastAPI(title="KoBERT Phishing API", version="0.2.0")

class Inp(BaseModel):
    text: str
    threshold: float | None = 0.5  # UI에서 조절
    abstain_band: float | None = 0.05  # 0.5 ± band 이내면 보류

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/predict")
def predict(x: Inp):
    bert = predict_prob(x.text)              # 0~1
    rule = rule_score(x.text)                # 0~1
    prob = 0.7*bert + 0.3*rule               # Late Fusion(간단 가중)
    tags = intent_tags(x.text)

    thr = x.threshold if x.threshold is not None else 0.5
    band = x.abstain_band if x.abstain_band is not None else 0.05
    abstain = abs(prob - 0.5) < band         # 애매하면 보류

    return {
        "bert_prob": round(bert, 4),
        "rule_prob": round(rule, 4),
        "prob": round(prob, 4),
        "decision": (None if abstain else ("phish" if prob >= thr else "benign")),
        "intents": tags if not abstain else [],
        "masked": mask(x.text),
        "abstain": abstain,
        "threshold": thr,
        "abstain_band": band
    }
