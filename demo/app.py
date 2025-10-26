import os
import requests
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="KoBERT 피싱 탐지 — Demo", layout="centered")
st.title("KoBERT 피싱 탐지 — Demo v0.2")

txt = st.text_area("문장 입력", height=160,
                   placeholder="예) [Web발신] 긴급! 계정이용중지. 아래 링크로 본인인증 http://ph1sh.me")

thr = st.slider("임계치(Threshold)", 0.0, 1.0, 0.50, 0.01)
band = st.slider("보류 밴드(±)", 0.0, 0.30, 0.05, 0.01)

c1, c2 = st.columns(2)

with c1:
    if st.button("분석"):
        if not txt.strip():
            st.warning("문장을 입력해주세요.")
        else:
            try:
                r = requests.post(f"{API}/predict",
                                  json={"text": txt, "threshold": thr, "abstain_band": band},
                                  timeout=60)
                st.json(r.json())
            except Exception as e:
                st.error(f"API 요청 실패: {e}")

with c2:
    if st.button("상태"):
        try:
            st.json(requests.get(f"{API}/health", timeout=10).json())
        except Exception as e:
            st.error(f"헬스체크 실패: {e}")

st.caption("※ 현재 모델은 데모용. 파인튜닝 체크포인트 연결 시 정확도가 향상됩니다. 로그는 PII 마스킹 후 저장 예정.")
