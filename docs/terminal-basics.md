## 터미널 실습

### 터미널(Terminal)이란?
터미널은 마우스 클릭(GUI 환경) 대신 **텍스트로 된 명령어(CLI 환경)**를 입력하여 운영체제나 컴퓨터 시스템과 직접 대화하고 제어할 수 있게 해주는 도구(프로그램)입니다.

---

### 절대 경로와 상대 경로의 차이
터미널에서 명령어(`cd`, `ls` 등)를 사용할 때 파일이나 폴더의 위치를 지정하는 방식은 크게 두 가지로 나뉩니다.

* **절대 경로 (Absolute Path):** 
  * 시스템의 최상위 루트(`/`)부터 시작하여 목표 대상까지의 전체 경로를 명시합니다.
  * 어디서 명령어를 실행하든 도착지가 항상 동일합니다.
  * _예시:_ `/Users/{username}/.../README.md`
* **상대 경로 (Relative Path):** 
  * 현재 자신이 머물고 있는 위치(현재 디렉토리)를 기준으로 대상을 가리키는 경로입니다.
  * 주로 `.` (현재 디렉토리), `..` (상위/부모 디렉토리) 기호를 함께 사용합니다.
  * _예시:_ `cd ../docs` (현재 위치에서 한 단계 위 폴더로 이동한 뒤, `docs` 폴더로 진입)

---

### 실습

#### 현재 위치 확인
```bash
$ pwd
/Users/{username}/...
```

#### 목록 확인 (숨김 파일 포함)
```bash
$ ls -al
total 48
drwxr-xr-x   7 {username}  staff    224 Mar 31 14:15 .
drwxr-xr-x   4 {username}  staff    128 Mar 31 12:50 ..
drwxr-xr-x@ 12 {username}  staff    384 Mar 31 13:25 .git
-rw-r--r--@  1 {username}  staff      6 Mar 31 13:00 .gitignore
drwxr-xr-x@  3 {username}  staff     96 Mar 31 14:21 docs
-rw-r--r--@  1 {username}  staff    545 Mar 31 14:21 README.md
-rw-r--r--@  1 {username}  staff  12570 Mar 31 14:26 tmp.md
```

#### 생성 (디렉토리)
```bash
$ mkdir practice_directory
```

#### 이동
```bash
$ cd practice_directory
```

#### 빈 파일 생성
```bash
$ touch practice_directory/test_file.txt
```

#### 파일 내용 추가
```bash
$ echo "Hello World" > practice_directory/test_file.txt
```

#### 복사
```bash
$ cp practice_directory/test_file.txt practice_directory/copy_file.txt
```

#### 이동 및 이름 변경
```bash
$ mv practice_directory/copy_file.txt practice_directory/renamed_file.txt
```

#### 파일 내용 확인
```bash
$ cat practice_directory/renamed_file.txt
```

#### 삭제
```bash
$ rm practice_directory/test_file.txt
$ rm -r practice_directory
```

