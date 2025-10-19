import re
URL = re.compile(r"https?://\S+")
MONEY = re.compile(r"(\d{1,3}(?:,\d{3})+|\d+)\s*(원|만원|억|w|krw)", re.I)
ACCOUNT = re.compile(r"\b\d{2,4}[- ]?\d{2,6}[- ]?\d{2,6}[- ]?\d{1,6}\b")
PHONE = re.compile(r"\b01[0-9]-?\d{3,4}-?\d{4}\b")
URGENTS = ["긴급","즉시","중지","정지","지금","한시","마감","본인인증","승인","차단","보류"]
INSTALL = ["앱설치","apk","설치","다운로드","앱 다운","앱을 설치"]

def rule_score(text:str)->float:
    t = text.lower()
    score = 0.0
    # 가벼운 가중치 합(0~1)
    score += 0.25 if URL.search(t) else 0.0
    score += 0.15 if MONEY.search(t) else 0.0
    score += 0.15 if ACCOUNT.search(t) else 0.0
    score += 0.10 if PHONE.search(t) else 0.0
    score += min(0.35, 0.07*sum(1 for w in URGENTS if w in t))
    score += 0.10 if any(w in t for w in INSTALL) else 0.0
    return min(1.0, score)

def intent_tags(text:str):
    tags = []
    t = text.lower()
    if MONEY.search(t) or any(w in t for w in ["입금","송금","결제","납부","환급"]):
        tags.append("금전요구")
    if URL.search(t):
        tags.append("링크유도")
    if any(w in t for w in ["국세청","검찰","경찰","금감원","카카오","토스","국민은행","신한","우리","농협","쿠팡","네이버","택배","우체국","행안부","질병청"]):
        tags.append("기관사칭")
    if any(w in t for w in URGENTS):
        tags.append("긴박압박")
    if any(w in t for w in ["로그인","비밀번호","otp","본인인증","계정","보안강화"]):
        tags.append("자격증명")
    if any(w in t for w in INSTALL):
        tags.append("설치유도")
    return list(dict.fromkeys(tags))  # 중복 제거, 순서 보존
