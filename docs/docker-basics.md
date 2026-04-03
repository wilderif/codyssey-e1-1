## Docker 실습 1

### Docker(도커)란?
도커는 프로그램이 돌아가는데 필요한 모든 환경(코드, 런타임, 라이브러리 등)을 **컨테이너(Container)**라는 독립된 박스 하나로 포장해 주는 기술입니다. 이를 통해 어디서든 똑같은 상태로 애플리케이션을 빠르게 띄울 수 있습니다.

---

### Docker 설치 및 기본 점검

#### Docker 버전 확인
```bash
$ docker --version
Docker version 29.2.1, build a5c7197
```

#### Docker 데몬 동작 여부 확인
```bash
$ docker info
Client:
 Version:    29.2.1
 Context:    desktop-linux
 Debug Mode: false
 Plugins:
 ...

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 29.2.1
 ...
```

---

### Docker 기본 운영 명령 수행

#### 이미지 다운로드 및 목록 확인
`hello-world`와 `ubuntu` 이미지를 다운로드(pull) 받고, 내 컴퓨터(Local)에 저장된 이미지 목록을 확인합니다.
```bash
$ docker pull hello-world
$ docker pull ubuntu
$ docker images
IMAGE                            ID             DISK USAGE   CONTENT SIZE   EXTRA
hello-world:latest               452a468a4bf9       22.6kB         10.3kB
ubuntu:latest                    186072bba1b2        141MB         30.8MB

```

---

### 컨테이너 실행 실습

#### hello-world 컨테이너 실행
```bash
$ docker run hello-world
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

#### 컨테이너 구동 목록 확인
구동 중인 컨테이너(`ps`)와 종료된 컨테이너까지 모두 포함하여(`ps -a`) 확인해 봅니다. \
`hello-world`는 실행(출력) 직후 바로 종료되기 때문에 `-a` 옵션을 통해서만 이력을 볼 수 있습니다.
```bash
$ docker ps
CONTAINER ID   IMAGE          COMMAND   CREATED   STATUS    PORTS     NAMES

$ docker ps -a
CONTAINER ID     IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
{container_id}   hello-world   "/hello"   47 seconds ago   Exited (0) 47 seconds ago             {container_name}
```

#### 컨테이너 중지 및 삭제
```bash
$ docker stop {container_id | container_name}
$ docker rm {container_id | container_name}
```

---

### 컨테이너 내부 진입 (Ubuntu)

#### Ubuntu 컨테이너 상호작용 모드로 실행
`-it` 옵션은 컨테이너 내부 환경을 로컬 터미널처럼 직접 제어할 수 있게 연결해주는 필수 옵션입니다. 크게 두 가지 기능이 합쳐져 있습니다.
* **`-i` (Interactive):** 표준 입력(STDIN)을 열어 키보드 입력값을 컨테이너 내부로 전달합니다. (이 옵션이 없으면 명령어를 쳐도 컨테이너가 듣지 못합니다.)
* **`-t` (TTY):** 가상 터미널 환경을 할당하여, 컨테이너 내부 셸(Bash 등)과 사용자의 터미널을 연결하는 역할을 합니다.
```bash
$ docker run -it {image_name} {command}
```

```bash
$ docker run -it ubuntu bash
root@{container_id}:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@{container_id}:/# echo "Hello Ubuntu Container!"
Hello Ubuntu Container!
root@{container_id}:/# exit
exit
```

---

### Docker 운영 상태 및 자원 모니터링

#### 컨테이너 로그 확인
컨테이너에서 발생한 표준 출력(stdout) 기록을 확인할 수 있습니다.
```bash
$ docker logs {container_id | container_name}
```
```bash
$ docker logs {container_id}
root@{container_id}:/# #
root@{container_id}:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@{container_id}:/# echo "Hello Ubuntu Container!"
Hello Ubuntu Container!
root@{container_id}:/# exit
exit
```

#### 컨테이너 리소스 모니터링
현재 구동 중인 컨테이너의 실시간 자원(CPU, Memory) 상태를 확인합니다.
(현재 계속 실행 중인 컨테이너가 없다면 빈 화면이 뜰 수 있습니다.)
```bash
$ docker stats
CONTAINER ID     NAME               CPU %     MEM USAGE / LIMIT     MEM %     NET I/O         BLOCK I/O    PIDS
{container_id}   {container_name}   0.00%     1.273MiB / 7.652GiB   0.02%     1.17kB / 126B   455kB / 0B   1
```

---


### 컨테이너 접속 시 `attach` vs `exec` 의 차이점

현재 백그라운드에서 구동 중인 컨테이너 내부에 접속하여 작업을 수행할 때, 주로 두 가지 명령어를 사용합니다. 두 명령어는 **프로세스를 다루고 연결하는 방식**에서 확연한 차이를 보입니다.

| 명령어 | 접속 방식 및 특징 | 터미널 종료(`exit` 등) 시 결과 | 주요 사용 목적 |
| :---: | :--- | :--- | :--- |
| **`docker attach <컨테이너ID>`** | **메인 프로세스에 직접 연결**<br>컨테이너 실행 시 최초로 생성된 메인 프로세스(PID 1)의 표준 입출력(StdIO)을 현재 터미널과 연결합니다. | 터미널 세션이 종료되면 메인 프로세스도 함께 종료되어 **컨테이너 전체가 중지(Exited)** 될 수 있습니다. | 1. Foreground 상태에서 웹 서버나 런타임 프로세스가 출력하는 실시간 로그 및 에러 내역을 직접적으로 모니터링할 때<br>2. 키보드 입력이 대기 중인 인터랙티브 애플리케이션과 소통할 때 |
| **`docker exec -it <컨테이너ID> bash`** | **독립적인 신규 프로세스 생성**<br>실행 중인 컨테이너 환경 내부에 완전히 독립된 새로운 보조 프로세스(Bash 셸 등)를 생성하여 접속합니다. | 신규 생성된 셸 프로세스만 종료되므로 **기존 컨테이너는 중단 없이 안정적인 구동 상태를 유지**합니다. | 1. 중단 없이 서비스되어야 하는 운영 서버(웹, DB) 컨테이너에 접속하여 환경 설정 파일을 변경할 때<br>2. 내부 네트워크 상태 점검, 핫픽스, 추가 라이브러리 설치 등 관리 유지보수 목적의 디버깅을 수행할 때 |

**주의사항**: `attach` 상태에서 터미널에 `Ctrl + C`를 입력하면 메인 프로세스에 중지 신호(SIGINT)가 전달되어 컨테이너가 멈추게 됩니다. 컨테이너의 구동 상태를 유지한 채 접속만 해제(Detach)하려면 `Ctrl + P`, `Ctrl + Q`를 순차적으로 입력해야 합니다.

```bash
$ docker attach {container_id | container_name}
root@{container_id}:/# read escape sequence
```

```bash
$ docker exec -it {container_id | container_name} bash
root@{container_id}:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@{container_id}:/# exit
exit
```

**요약**: 실무에서는 사용자의 실수로 컨테이너 시스템이 죽는 것을 방지하기 위해 컨테이너 내부 환경 조작 시 **`docker exec`** 방식을 사용하는 것이 압도적인 표준입니다.
