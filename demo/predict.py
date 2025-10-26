import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = os.getenv("MODEL_NAME", "klue/roberta-base")
MAX_LEN    = int(os.getenv("MAX_LEN", "128"))

_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
_model.eval()

@torch.no_grad()
def predict_prob(text: str, temp: float = 1.0) -> float:
    """
    긍정(=피싱) 확률 반환. 2클래스 모델에서 id=1을 피싱으로 가정.
    """
    enc = _tokenizer(text, truncation=True, max_length=MAX_LEN, return_tensors="pt")
    logits = _model(**enc).logits / max(temp, 1e-6)
    probs = torch.softmax(logits, dim=-1).squeeze(0).tolist()
    if len(probs) >= 2:
        return float(probs[1])
    return float(probs[-1])
