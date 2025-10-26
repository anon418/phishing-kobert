import re, random

# 동형문자/비슷한 문자 치환 후보
_HOMO_PAIRS = [("0","O"),("1","l"),("5","S"),("2","Z")]
# 경고 이모지
_EMOJIS = ["❗","⚠️","‼️","🚨"]
# 한영 혼용 사전
_ENGMIX = {"계정":"account","본인인증":"verify","확인":"check","긴급":"urgent","정지":"suspend"}
# URL 탐지
_URL_RE = re.compile(r"(\bhttps?://[^\s]+)")

def _homo(s: str) -> str:
    out = s
    for a, b in _HOMO_PAIRS:
        r = random.random()
        if r < 0.33:
            out = out.replace(a, b)
        elif r < 0.66:
            out = out.replace(b, a)
    return out

def _spaces(s: str) -> str:
    # 인접한 비공백 사이에 확률적으로 공백 삽입(가독성 깨기)
    return re.sub(r"(?<=\S)(?=\S)", lambda m: " " if random.random() < 0.1 else "", s)

def _emoji(s: str) -> str:
    return s + (" " + random.choice(_EMOJIS) if random.random() < 0.7 else "")

def _eng_mix(s: str) -> str:
    out = s
    for k, v in _ENGMIX.items():
        if k in out and random.random() < 0.6:
            out = out.replace(k, f"{k}({v})")
    return out

def _url_obfuscate(s: str) -> str:
    # URL의 점을 [.]로 치환
    def rep(m: re.Match) -> str:
        u = m.group(1)
        return u.replace(".", "[.]")
    return _URL_RE.sub(rep, s)

def perturb(text: str) -> str:
    ops = [_homo, _spaces, _emoji, _eng_mix, _url_obfuscate]
    random.shuffle(ops)
    out = text
    for f in ops:
        if random.random() < 0.8:  # 완전 랜덤 적용(각 80% 확률)
            out = f(out)
    return out
