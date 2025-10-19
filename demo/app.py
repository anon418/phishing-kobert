import os, requests, streamlit as st
API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="KoBERT 피싱 탐지", layout="centered")
st.title("KoBERT 피싱 탐지 — Demo v0.2")

txt = st.text_area("문장 입력", height=140, placeholder="예) [Web발신] 긴급! 계정이용중지. 아래 링크로 본인인증 http://ph1sh.me")
c1, c2 = st.columns(2)
thr = c1.slider("임계치(Threshold)", 0.1, 0.9, 0.5, 0.01)
band = c2.slider("보류 밴드(±)", 0.0, 0.2, 0.05, 0.01)

b1, b2 = st.columns(2)
with b1:
    if st.button("분석"):
        if not txt.strip():
            st.warning("문장을 입력해주세요.")
        else:
            r = requests.post(f"{API}/predict", json={"text": txt, "threshold": thr, "abstain_band": band}, timeout=30)
            data = r.json()
            # 상단 배지로 요약
            st.markdown(f"**결정:** `{data['decision']}`  |  **prob:** {data['prob']}  (bert:{data['bert_prob']}, rule:{data['rule_prob']})")
            if data["abstain"]:
                st.warning("판단 보류(abstain): 애매한 케이스입니다. 사람이 리뷰하세요.")
            st.json(data)

with b2:
    if st.button("상태"):
        st.json(requests.get(f"{API}/health", timeout=10).json())

st.caption("※ 현재 모델은 데모용. KoBERT 파인튜닝 모델로 교체 시 prob/의도 정확도가 상승합니다. 로그는 PII 마스킹 후 저장 예정.")
