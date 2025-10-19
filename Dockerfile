FROM python:3.11-slim
WORKDIR /app

# 최소 런타임 패키지
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt requests

COPY . .

# Streamlit 설정(텔레메트리 OFF)
ENV STREAMLIT_BROWSER_GATHERUSAGESTATS=false
EXPOSE 8000 7860
