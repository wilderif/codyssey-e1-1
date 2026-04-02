## 에러 트러블 슈팅 (Troubleshooting Logs)

---

### 이슈 1: Nginx 바인드 마운트 실습 중 `403 Forbidden` 에러 발생

#### 문제

Docker `Bind Mount` 실습 중 `docker run`으로 컨테이너를 띄우고 호스트 로컬 폴더에 `index.html`을 생성하였으나, `curl`로 접속 시 기대했던 내용 대신 Nginx 기본 에러인 **`403 Forbidden`** 화면이 출력됨.

```bash
# 터미널에서 확인한 에러 응답
$ curl http://localhost:8080
<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.28.3</center>
</body>
</html>
```

#### 원인 가설

Nginx 웹 서버는 자신이 바라보고 있는 기본 디렉토리(`/usr/share/nginx/html`) 안에 읽어들일 수 있는 `index.html` 파일이 존재하지 않거나, 권한이 없을 경우 보안을 위해 무조건 `403 Forbidden`을 뱉어낸다.
따라서, **"호스트에선 정상적으로 파일을 만들었으나, 컨테이너가 엇갈린 폴더(빈 폴더)를 잘못 마운트하고 있을 가능성"**이 높다고 판단함.

#### 확인

1. **도커 컨테이너 내부 구조 직접 탐색** 
   * `docker exec` 명령어로 Nginx 컨테이너 내부 쉘로 들어가 해당 웹루트 경로를 나열해 본 결과, 디렉토리가 완전히 비어 있음(`index.html`이 없음)을 확인.
2. **컨테이너 실행 설정(Mount Source) 확인**
   * `docker inspect` 명령어로 띄워진 컨테이너를 검사해 보니, 호스트 측 경로가 `practice-docker/bind_test_dir`로 마운트되어 있었음.
   * 반면에 실제로 명령어를 타이핑하여 `index.html` 파일을 생성한 곳은 `pratice/bind-test` 폴더였음.
   * 결론적으로 **경로 오타 및 싱크 어긋남**으로 인해 빈 폴더가 마운트되고 있었음이 입증됨.

#### 해결

`docker run` 명령어의 바인드 마운트 볼륨 이름(`-v`)을 내가 실제로 수정한 호스트 폴더의 이름과 완벽히 일치하도록 경로명을 맞추고, 기존 컨테이너를 삭제 후 재실행함.

```bash
# 1. 잘못된 경로로 마운트된 기존 에러 컨테이너 철거
$ docker rm -f my-bind-nginx

# 2. 로컬 파일이 저장되어 있는 'pratice/bind-test' 경로로 명확하게 일치시켜 컨테이너 재가동
$ docker run -d -p 8080:80 -v $(pwd)/pratice/bind-test:/usr/share/nginx/html --name my-bind-nginx my-nginx:1.0

# 3. 실시간 바인드 마운트 정상 동기화 여부 검증
$ curl http://localhost:8080
<h1>Hello Bind Mount Sync!</h1>
```


---

### 이슈 2: Docker 컨테이너 포트 충돌 (`port is already allocated`)

#### 문제

포트 매핑 실습을 위해 `docker run -p 8080:80` 명령어로 새 Nginx 컨테이너를 실행하려 했으나, **포트 할당 에러가 발생하며 컨테이너 생성이 실패**함.

```bash
$ docker run -d -p 8080:80 --name my-web2 nginx
docker: Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint my-web2 {container_id}: Bind for 0.0.0.0:8080 failed: port is already allocated
```

#### 원인 가설

호스트(로컬 컴퓨터)의 특정 포트(ex: `8080`)는 동시에 두 개 이상의 프로세스나 컨테이너가 점유할 수 없음. 
따라서 "이미 `8080` 포트를 사용 중인 다른 컨테이너가 켜져 있어서 충돌이 나는 것"이라고 판단함.

#### 확인

1. **실행 중인 컨테이너 목록 확인**
   * `docker ps` 명령어로 가동 중인 컨테이너 리스트를 확인함.
   * 확인 결과, 이전 실습에서 띄워둔 다른 컨테이너가 여전히 구동 중이며 호스트의 `8080` 포트를 선점하고 있었음.

#### 해결

8080 포트를 점검 중인 기존 컨테이너를 종료하여 포트를 비워준 뒤, 실패했던 명령어를 다시 실행함.

```bash
# 1. 8080 포트를 점유하고 있는 기존 컨테이너 정리
$ docker rm -f my-bind-nginx

# 2. 실패했던 빈 포트에 할당하는 명령어 재실행
$ docker run -d -p 8080:80 --name my-web2 nginx
# 성공적으로 컨테이너가 생성됨!
```
