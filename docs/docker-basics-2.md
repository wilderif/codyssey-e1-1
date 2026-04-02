## Docker 실습 2

### Dockerfile(도커파일)이란?
Dockerfile은 도커 컨테이너를 만들기 위한 **설계도**입니다. 어떤 운영체제(OS)를 기본적으로 사용할지, 어떤 패키지 라이브러리를 설치할지, 어떤 소스 코드를 복사해서 넣을지 등을 하나의 텍스트 파일에 적어두면, 도커가 이를 읽어 똑같은 환경을 갖춘 나만의 커스텀 이미지를 Build 해 줍니다.

---

### 기존 Dockerfile 기반 커스텀 이미지 제작

**선택한 베이스 이미지 및 커스텀 목적**
* **베이스 이미지:** `nginx:1.28.3`
* **커스텀 목적:** 로컬 환경의 커스텀 `index.html` 파일을 복사하여 기존 Nginx 기본 웹 페이지를 대체

---

### 빌드 및 실행 명령과 결과 기록

**practice-docker** 디렉토리에서 실습

#### Dockerfile

```dockerfile
# 1.28.3 버전의 nginx 베이스 이미지를 가져옵니다.
FROM nginx:1.28.3

# (참고) 이 컨테이너는 내부적으로 80번 포트를 사용한다고 문서화해 둡니다. (실제 연결은 run -p 에서 수행)
EXPOSE 80

# (참고) 컨테이너 내부의 특정 경로를 외부에 데이터를 보존할 볼륨 마운트 포인트로 지정합니다. (실제 마운트는 run -v 에서 수행)
VOLUME ["/app/data"]

# 로컬에 작성된 커스텀 index.html 파일을 컨테이너 내부의 Nginx 기본 서비스 경로에 덮어쓰기 복사합니다.
COPY index.html /usr/share/nginx/html/index.html
```

#### 이미지 빌드 실행

* **`-t`**: 이미지의 `이름:태그` 지정 (`my-nginx:1.0`)
* **`.`**: 빌드 컨텍스트 지정 (현재 디렉토리를 기준으로 빌드)

```bash
$ docker build -t my-nginx:1.0 .
[+] Building 9.7s (7/7) FINISHED                                 docker:desktop-linux
 => [internal] load build definition from Dockerfile             0.0s
 => => transferring dockerfile: 311B                             0.0s
 => [internal] load metadata for docker.io/library/nginx:1.28.3  5.9s
 => [internal] load .dockerignore                                0.0s
 => => transferring context: 2B                                  0.0s
 => [internal] load build context                                0.0s
 => => transferring context: 566B                                0.0s
 ...
```

#### 빌드한 이미지로 컨테이너 실행

* **`-d`**: 백그라운드(Detach) 모드로 실행 (터미널 반환)
* **`-p 8080:80`**: 포트 매핑 (`localhost-port:container-port`)
* **`--name`**: 컨테이너 고유 이름 지정 (`my-nginx-container`)
* **`my-nginx:1.0`**: 실행할 대상 이미지 `이름:태그`

```bash
$ docker run -d -p 8080:80 --name my-nginx-container my-nginx:1.0
{container_id}

$ docker ps
CONTAINER ID     IMAGE          COMMAND                  CREATED          STATUS          PORTS                                     NAMES
{container_id}   my-nginx:1.0   "/docker-entrypoint.…"   22 seconds ago   Up 22 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-nginx-container
```

---

### 포트 매핑 및 접속 증거
```bash
$ curl http://localhost:8080
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Codyssey Docker Practice</title>
    <style>
        body { font-family: sans-serif; text-align: center; margin-top: 50px; }
        h1 { color: #0066cc; }
    </style>
</head>
<body>
    <h1>커스텀 Nginx 웹 서버 띄우기 성공!</h1>
    <p>성공 성공 성공 성공 성공 성공 성공 성공 성공 성공 성공 성공 성공 성공 성공</p>
</body>
</html>
```

---

### Docker 볼륨 영속성 검증
컨테이너가 파괴되어도 데이터가 날아가지 않고 안전하게 보존되는지 볼륨(Volume) 마운트를 통해 증명합니다.

#### Docker 볼륨 생성
```bash
$ docker volume create my_test_volume
my_test_volume
```

#### 볼륨을 연결(-v)하여 컨테이너 띄우기

* **`-v`**: 볼륨 마운트 (`볼륨명:컨테이너 내부 경로`)

```bash
$ docker run -d -v my_test_volume:/app/data --name my-nginx-container1 my-nginx:1.0
{container_id}
```

#### 컨테이너 내부 파일 쓰기

* **`docker exec`**: 컨테이너 내부에서 명령 실행
* **`sh -c`**: 쉘 명령 실행
* **`echo 'Volume Storage Test!' > /app/data/test.txt`**: 파일 쓰기

```bash
$ docker exec my-nginx-container1 sh -c "echo 'Volume Storage Test!' > /app/data/test.txt"
```

#### 컨테이너 내부 파일 확인

```bash
$ docker exec -it my-nginx-container1 bash
root@dbe10df12cf9:/# ls
app  bin  boot  dev  docker-entrypoint.d  docker-entrypoint.sh  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@dbe10df12cf9:/# cd app
root@dbe10df12cf9:/app# ls
data
root@dbe10df12cf9:/app# cd data
root@dbe10df12cf9:/app/data# ls
test.txt
```

#### 컨테이너 삭제

* **`docker rm -f`**: 컨테이너 강제 삭제

```bash
$ docker rm -f my-nginx-container1
my-nginx-container1
```

#### 동일한 볼륨을 두 번째 임시 컨테이너에 연결해서 기존 데이터가 살아있는지 검증

* **`--rm`**: 컨테이너 종료 시 해당 컨테이너 자동으로 삭제
* **`-v`**: 볼륨 마운트 (`볼륨명:컨테이너 내부 경로`)

```bash
$ docker run --rm -v my_test_volume:/app/data --name my-nginx-container2 my-nginx:1.0 cat /app/data/test.txt
Volume Storage Test!
```

#### Docker Volume 삭제
```bash
$ docker volume rm my_test_volume
my_test_volume
```

---

### Bind Mount 실습

도커 볼륨(`Volume`) 방식과 달리, 현재 내 컴퓨터(호스트)의 특정 물리적 폴더를 컨테이너 내부에 직접 연결합니다. 로컬에서 코드를 수정하면 새로고침만으로 컨테이너에 실시간 반영되기 때문에 개발 환경에서 가장 많이 쓰이는 방식입니다.

#### 바인드 마운트 실행

* **`-v`**: 바인드 마운트 (`호스트의_절대경로:컨테이너_내부경로`)
  * `$(pwd)`는 현재 작업 중인 터미널의 절대 경로(Print Working Directory)를 자동으로 가져오는 편리한 명령어입니다. 이 때, 경로에 공백이 포함되어 있을 경우를 대비해 따옴표(`""`)로 감싸주는 것이 안전합니다.

```bash
# 호스트 폴더를 Nginx 컨테이너의 기본 웹루트에 바인드 마운트
$ docker run -d -p 8080:80 -v "$(pwd)/bind-test":/usr/share/nginx/html --name my-bind-nginx my-nginx:1.0
{container_id}
```

#### 컨테이너에서 동기화 확인 (로컬 폴더에 index.html 파일이 없을 경우)

```bash
$ curl http://localhost:8080
<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.28.3</center>
</body>
</html>
```

#### 로컬 호스트 폴더에서 직접 파일 생성하기

```bash
$ echo '<h1>Hello Bind Mount Sync!</h1>' > bind-test/index.html
```

#### 컨테이너에서 실시간 동기화 확인 (로컬 변경 후)

```bash
$ curl http://localhost:8080
<h1>Hello Bind Mount Sync!</h1>
```

#### 실습 컨테이너 정리

```bash
$ docker rm -f my-bind-nginx
$ rm bind-test/index.html
```
