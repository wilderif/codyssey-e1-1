## Docker Compose 실습

### Docker Compose란?

Docker Compose는 다중 컨테이너 Docker 애플리케이션을 정의하고 실행하기 위한 도구입니다. `YAML` 파일을 사용하여 애플리케이션의 서비스를 구성하며, 단일 명령어를 통해 설정된 모든 서비스를 한 번에 생성하고 시작할 수 있습니다.

---

### Docker Compose 기초

docker-compose.yml의 기본 구조를 학습하고, 단일 서비스를 Compose로 실행합니다.

**practice-docker-compose-1** 디렉토리에서 실습

#### docker-compose.yml 작성

```yaml
# 실행할 컨테이너 서비스들을 정의합니다.
services:
  # 'web'이라는 이름의 서비스를 선언합니다.
  web:
    # 현재 디렉토리 기준 ./web 폴더에 있는 Dockerfile을 사용하여 이미지를 빌드합니다.
    build: ./web
    # 호스트(로컬)의 8000번 포트와 컨테이너 내부의 8000번 포트를 연결(포트 포워딩)합니다.
    ports:
      - "8000:8000"
    # 컨테이너 내부에 주입할 환경 변수들을 설정합니다.
    environment:
      PORT: 8000
      APP_MODE: development
```

#### 단일 서비스 실행

```bash
$ docker compose up --build
...
web-1  | INFO:     Started server process [7]
web-1  | INFO:     Waiting for application startup.
web-1  | INFO:     Application startup complete.
web-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

```bash
$ curl http://localhost:8000
{"service":"web","message":"Hello from web service","port":"8000","mode":"development"}
```

---

### Docker Compose 멀티 컨테이너

웹 서버와 임의의 보조 서비스, 2개 이상을 Compose로 함께 실행하고 네트워크 통신을 확인합니다.
* **배움 포인트:** 네트워크/서비스 디스커버리 개념 맛보기

**practice-docker-compose-2** 디렉토리에서 실습

#### 멀티 컨테이너용 docker-compose.yml 작성

```yaml
# 실행할 컨테이너 서비스들을 정의합니다.
services:
  # 'web'이라는 이름의 메인 애플리케이션 서비스를 선언합니다.
  web:
    # ./web 폴더의 Dockerfile을 기반으로 이미지를 빌드합니다.
    build: ./web
    # 호스트 8000번 포트와 컨테이너 내부 8000번 포트를 연결(포트 포워딩)합니다.
    ports:
      - "8000:8000"
    # 컨테이너 내부에 환경 변수를 주입합니다.
    environment:
      PORT: 8000
      APP_MODE: development
      # 내부 네트워크 안의 다른 서비스 'helper'를 목적지로 하는 URL (서비스 이름으로 통신)
      HELPER_URL: http://helper:8001
    # web 컨테이너가 실행되기 전에 helper 서비스가 먼저 실행되도록 실행 순서를 제어합니다.
    depends_on:
      - helper

  # 'helper'라는 이름의 보조 서비스를 선언합니다.
  helper:
    # ./helper 폴더의 Dockerfile을 기반으로 이미지를 빌드합니다.
    build: ./helper
    # 호스트 8001번 포트와 컨테이너 내부 8001번 포트를 연결합니다. (외부 노출 목적)
    ports:
      - "8001:8001"
    environment:
      PORT: 8001
```

#### 컨테이너 간 네트워크 통신 확인

```bash
$ docker compose up --build
Attaching to helper-1, web-1
helper-1  | INFO:     Started server process [7]
helper-1  | INFO:     Waiting for application startup.
helper-1  | INFO:     Application startup complete.
helper-1  | INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
web-1     | INFO:     Started server process [7]
web-1     | INFO:     Waiting for application startup.
web-1     | INFO:     Application startup complete.
web-1     | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

```bash
$ curl http://localhost:8000
{"service":"web","message":"Hello from web service","port":"8000","mode":"development","helper_url":"http://helper:8001","helper_response":{"service":"helper","message":"Hello from helper service"}}
```

---

### Compose 운영 명령어 습득

`up`, `down`, `ps`, `logs`를 사용해 실행/종료/상태/로그를 관리합니다.
* **배움 포인트:** 운영 관점의 “상태 확인 루틴” 만들기

| 명령어 (`docker compose ...`) | 빌드 여부 | 실행 모드 | 주요 용도 |
| :--- | :--- | :--- | :--- |
| **`up`** | 이미지가 없을 때만 빌드 | foreground | 첫 실행 및 실시간 로그 확인 |
| **`up -d`** | 이미지가 없을 때만 빌드 | background | 서비스 상시 가동 |
| **`up --build`** | 무조건 새로 빌드 | foreground | 코드 수정 후 즉시 반영 확인 |
| **`up -d --build`** | 무조건 새로 빌드 | background | 코드 수정 후 반영 확인 (백그라운드 실행) |

#### 상태 확인 및 로그 조회

docker compose ps는 현재 위치에 있는 docker-compose.yaml 파일을 기반으로 실행 중인 컨테이너들의 목록을 보여줍니다.

```bash
$ docker compose ps
NAME                                 IMAGE                              COMMAND                  SERVICE   CREATED         STATUS         PORTS
practice-docker-compose-2-helper-1   practice-docker-compose-2-helper   "sh -c 'uvicorn main…"   helper    6 minutes ago   Up 6 minutes   0.0.0.0:8001->8001/tcp, [::]:8001->8001/tcp
practice-docker-compose-2-web-1      practice-docker-compose-2-web      "sh -c 'uvicorn main…"   web       6 minutes ago   Up 6 minutes   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
```

```bash
$ docker compose logs
web-1     | INFO:     Started server process [7]
web-1     | INFO:     Waiting for application startup.
helper-1  | INFO:     Started server process [7]
helper-1  | INFO:     Waiting for application startup.
helper-1  | INFO:     Application startup complete.
helper-1  | INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
helper-1  | INFO:     {client_ip}:47334 - "GET / HTTP/1.1" 200 OK
web-1     | INFO:     Application startup complete.
web-1     | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
web-1     | INFO:     {host_ip}:43886 - "GET / HTTP/1.1" 200 OK
```

특정 컨테이너의 로그만 보고 싶을 때
```bash
$ docker compose logs web
$ docker compose logs helper
```

실시간 로그 추적
```bash
$ docker compose logs -f
```

#### 컨테이너 종료 및 리소스 정리

```bash
$ docker compose down
[+] down 3/3
 ✔ Container practice-docker-compose-2-web-1    Removed
 ✔ Container practice-docker-compose-2-helper-1 Removed
 ✔ Network practice-docker-compose-2_default    Removed
```

---

### 환경 변수 활용

Dockerfile 또는 Compose에서 환경 변수를 주입해 서버 포트/모드를 변경해봅니다.
* **배움 포인트:** 설정과 코드의 분리

**practice-docker-compose-3** 디렉토리에서 실습

#### 환경 변수 주입 설정 (.env 또는 docker-compose.yml)

```yaml
# 실행할 컨테이너 서비스들을 정의합니다.
services:
  # 'web'이라는 이름의 메인 애플리케이션 서비스를 선언합니다.
  web:
    # ./web 폴더의 Dockerfile을 기반으로 이미지를 빌드합니다.
    build: ./web
    # 호스트 포트와 컨테이너 내부 포트를 환경 변수에서 가져와 연결합니다. (기본값 8000)
    ports:
      - "${WEB_PORT:-8000}:${WEB_PORT:-8000}"
    # 컨테이너 내부에 환경 변수를 주입합니다. (.env 파일의 값을 전달)
    environment:
      PORT: ${WEB_PORT:-8000}
      APP_MODE: ${APP_MODE:-development}
      # 내부 네트워크 안의 다른 서비스 'helper'를 목적지로 하는 URL (환경 변수로 포트 지정, 기본값 8001)
      HELPER_URL: http://helper:${HELPER_PORT:-8001}
    # web 컨테이너가 실행되기 전에 helper 서비스가 먼저 실행되도록 실행 순서를 제어합니다.
    depends_on:
      - helper

  # 'helper'라는 이름의 보조 서비스를 선언합니다.
  helper:
    # ./helper 폴더의 Dockerfile을 기반으로 이미지를 빌드합니다.
    build: ./helper
    # 호스트 포트와 컨테이너 내부 포트를 환경 변수에서 가져와 연결합니다. (기본값 8001)
    ports:
      - "${HELPER_PORT:-8001}:${HELPER_PORT:-8001}"
    # 컨테이너 내부에 통신 포트 환경 변수를 주입합니다. (.env 파일의 값을 전달)
    environment:
      PORT: ${HELPER_PORT:-8001}
```

#### 환경 변수 적용 확인

--env-file 옵션으로 Compose 파일의 변수 치환에 사용할 값을 불러오고, environment 항목을 통해 해당 값들을 컨테이너 내부 환경 변수로 전달합니다.
(.env 파일을 사용할 때는 --env-file 옵션을 사용하지 않아도 됩니다.)

```bash
$ docker compose --env-file .env up --build
Attaching to helper-1, web-1
helper-1  | INFO:     Started server process [7]
helper-1  | INFO:     Waiting for application startup.
helper-1  | INFO:     Application startup complete.
helper-1  | INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
web-1     | INFO:     Started server process [7]
web-1     | INFO:     Waiting for application startup.
web-1     | INFO:     Application startup complete.
web-1     | INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
helper-1  | INFO:     {host_ip}:23955 - "GET / HTTP/1.1" 200 OK
helper-1  | INFO:     {client_ip}:47608 - "GET / HTTP/1.1" 200 OK
web-1     | INFO:     {host_ip}:34668 - "GET / HTTP/1.1" 200 OK
```

```bash
$ curl http://localhost:8002
{"service":"web","message":"Hello from web service in PRODUCTION mode","port":"8002","mode":"production"}
```

```bash
$ docker compose down
```
