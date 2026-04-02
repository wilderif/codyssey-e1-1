from fastapi import FastAPI
import os
import requests

app = FastAPI()

@app.get("/")
def read_root():
    # 환경 변수에서 동작 설정값을 수신합니다 (기본값 제공).
    port = os.getenv("PORT", "8000")
    mode = os.getenv("APP_MODE", "development")
    
    # 통신할 대상(보조 서비스)의 URL을 환경 변수에서 가져옵니다.
    # 도커 컴포즈 내부 네트워크에서는 서비스 이름('helper')이 곧 도메인이 됩니다.
    helper_url = os.getenv("HELPER_URL", "http://helper:8001")

    helper_response = None
    try:
        # 보조 서비스에 HTTP GET 요청을 보내 응답을 JSON 형식으로 파싱합니다.
        response = requests.get(helper_url, timeout=2)
        helper_response = response.json()
    except Exception as e:
        # 네트워크 통신 실패 시 오류 메세지를 담습니다.
        helper_response = {"error": str(e)}

    # 클라이언트 요청 시 웹 서비스 정보와 보조 서비스 응답 결과를 함께 반환합니다.
    return {
        "service": "web",
        "message": "Hello from web service",
        "port": port,
        "mode": mode,
        "helper_url": helper_url,
        "helper_response": helper_response,
    }
