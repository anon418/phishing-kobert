import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import torch

MODEL_NAME = os.getenv("MODEL_NAME", "klue/roberta-base")  # 임시
MAX_LEN = int(os.getenv("MAX_LEN", "128"))

_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
_model.eval()

pipeline = TextClassificationPipeline(
    model=_model, tokenizer=_tokenizer, device=-1, return_all_scores=True, truncation=True
)

def predict_prob(text: str) -> float:
    out = pipeline(text, max_length=MAX_LEN)[0]
    # id=1이 "피싱" 클래스로 가정(내일 학습 모델로 바꾸면 자동 대체됨)
    # 현재는 데모라 로짓만 기준치 없이 softmax prob 사용
    probs = {x["label"]: x["score"] for x in out}
    # 라벨명이 "LABEL_0/1" 형태일 수 있음 → 1을 위험으로 가정
    return float(probs.get("LABEL_1", probs.get("1", 0.5)))
