import re
from typing import List

URL    = re.compile(r"https?://[^\s]+|www\.[^\s]+", re.I)
PHONE  = re.compile(r"\b01[0-9]-?\d{3,4}-?\d{4}\b")
ACC    = re.compile(r"\b\d{2,4}[- ]?\d{2,6}[- ]?\d{2,6}[- ]?\d{1,6}\b")
MONEY  = re.compile(r"\b\d{1,3}(?:,\d{3})*(?:원|만원|억)\b")
EMER   = re.compile(r"(긴급|즉시|본인인증|정지|차단|승인|입금|환불|링크|인증)", re.I)
BRAND  = re.compile(r"(은행|국세청|경찰|택배|카카오|네이버|국민|신한|우리|농협)", re.I)

def rule_score(text: str) -> float:
    score = 0.0
    score += 0.35 if URL.search(text)   else 0.0
    score += 0.25 if ACC.search(text)   else 0.0
    score += 0.15 if PHONE.search(text) else 0.0
    score += 0.10 if MONEY.search(text) else 0.0
    score += 0.15 if EMER.search(text)  else 0.0
    return min(score, 1.0)

def intent_tags(text: str) -> List[str]:
    tags = []
    if EMER.search(text):  tags.append("긴박압박")
    if URL.search(text):   tags.append("링크유도")
    if ACC.search(text):   tags.append("계좌요구")
    if PHONE.search(text): tags.append("전화요청")
    if MONEY.search(text): tags.append("금전요구")
    if BRAND.search(text): tags.append("기관사칭")
    return tags[:4]
