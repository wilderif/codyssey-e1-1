# 1.28.3 버전의 nginx 베이스 이미지를 가져옵니다.
FROM nginx:1.28.3

# 로컬에 작성된 커스텀 index.html 파일을 컨테이너 내부의 Nginx 기본 서비스 경로에 덮어쓰기 복사합니다.
COPY index.html /usr/share/nginx/html/index.html

# (참고) 이 컨테이너는 내부적으로 80번 포트를 사용한다고 문서화해 둡니다. (실제 로컬 포트 연결은 run -p 에서 수행)
EXPOSE 80

# (참고) 컨테이너 내부의 특정 경로를 외부에 데이터를 보존할 볼륨 마운트 포인트로 지정합니다. (실제 연결은 run -v 에서 수행)
VOLUME ["/app/data"]
