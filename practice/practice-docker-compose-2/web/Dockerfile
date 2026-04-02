# python 3.11 슬림 버전을 베이스 이미지로 사용합니다.
FROM python:3.11-slim

# 컨테이너 내의 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# 파이썬 종속성 패키지 목록 파일을 복사합니다.
COPY requirements.txt .
# 캐시를 사용하지 않고 패키지를 설치하여 이미지 크기를 줄입니다.
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드를 복사합니다.
COPY main.py .

# 기본 환경 변수 값을 설정합니다. (실행 시 Docker Compose로 덮어쓸 수 있습니다)
ENV PORT=8000
ENV APP_MODE=development

# 셸을 사용하여 uvicorn 서버를 실행하고, 환경 변수 PORT 값을 활용해 수신 대기합니다.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]