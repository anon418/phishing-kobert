FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/cache/hf \
    PYTHONPATH=/app

WORKDIR /app

# 필수 패키지
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY . .

# 캐시 디렉터리
RUN mkdir -p /cache/hf

EXPOSE 8000 7860

# 기본 엔트리포인트는 compose에서 지정
