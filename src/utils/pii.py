import re

ACCOUNT = re.compile(r'\b(\d{2,4}[- ]?\d{2,6}[- ]?\d{2,6}[- ]?\d{1,6})\b')
PHONE   = re.compile(r'\b(01[0-9]-?\d{3,4}-?\d{4})\b')
EMAIL   = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b')
URL     = re.compile(r'(https?://[^\s]+|www\.[^\s]+)')
ADDR    = re.compile(r'(?:서울|부산|대구|인천|광주|대전|울산).{0,20}\d{1,4}(?:-?\d{0,4})?호?')

def mask(t: str) -> str:
    for p, tok in [
        (ACCOUNT, "<ACC>"), (PHONE, "<TEL>"), (EMAIL, "<MAIL>"),
        (URL, "<URL>"), (ADDR, "<ADDR>")
    ]:
        t = p.sub(tok, t)
    return t
