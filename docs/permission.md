## 권한 실습

### 권한(Permission)이란?
리눅스/macOS 시스템에서는 보안을 위해 파일이나 디렉토리(폴더)를 누가 열어보고(읽기), 수정하고(쓰기), 실행할 수 있는지 자격을 엄격하게 통제하는데, 이를 **권한(Permission)**이라고 부릅니다. 이를 통해 허가받지 않은 다른 사용자가 파일을 삭제하거나 변경하는 것을 막을 수 있습니다.

---

### 파일 권한과 숫자 표기법

리눅스와 맥(macOS) 환경에서 터미널에 `ls -l` 명령어를 입력하면 `drwxrwxrwx`나 `-rw-r--r--`와 같이 10자리 문자열로 파일의 상세 권한 정보가 나옵니다. \
이 10자리는 **파일 유형 1자리 + 대상별 권한 9자리**로 구성됩니다.
* **첫 번째 글자 (파일 유형):**
  * `d` : 디렉토리 (폴더)
  * `-` : 일반 파일

* **나머지 9글자 (권한의 적용 대상):**
  나머지 9글자는 세 자리씩 똑같이 끊어서 **소유자(User) / 속한 그룹(Group) / 기타 사용자(Others)**의 권한 순서로 표기합니다. (예: `rwx` / `rwx` / `rwx`)

**권한의 종류 (r/w/x):**
  세 그룹에 공통적으로 들어가는 권한 속성(3자리)은 다음과 같으며, 각각 고유한 숫자값을 가집니다.
  * `r` (Read, 읽기) = 숫자 **4**: 파일 내용 읽기, 폴더 내 파일 목록 확인
  * `w` (Write, 쓰기) = 숫자 **2**: 파일 내용 수정, 폴더 내 파일 생성/삭제
  * `x` (eXecute, 실행) = 숫자 **1**: 프로그램 실행, 폴더 내부 접근(`cd` 명령어)
  * `-` (권한 없음) = 숫자 **0**

**숫자 표기법 연산 및 실전 예시:**
  `chmod` 명령어 등으로 권한을 변경할 때는 각 그룹에 부여된 숫자(4, 2, 1)를 모두 더해서 3자리 숫자로 변환해 사용합니다.
  * *예시 1 (`644`)*: 소유자 **6** (`rw-`), 그룹 **4** (`r--`), 기타 **4** (`r--`) \
    `-rw-r--r--` : 소유자만 읽고 쓸 수 있으며, 남들은 읽기만 가능 (일반 파일의 기본값)
  * *예시 2 (`755`)*: 소유자 **7** (`rwx`), 그룹 **5** (`r-x`), 기타 **5** (`r-x`) \
    `drwxr-xr-x` : 소유자는 모든 권한을 가지고, 남들은 읽기와 접근만 가능 (일반 디렉토리의 기본값)

---

### 실습

#### 실습용 디렉토리 및 파일 생성
```bash
$ mkdir perm_practice
$ touch perm_practice/test_file.txt
```

#### 변경 전 초기 권한 확인
```bash
$ ls -ld perm_practice
$ ls -l perm_practice/test_file.txt
drwxr-xr-x@ 3 {username}  staff  96 Mar 31 15:25 perm_practice
-rw-r--r--@ 1 {username}  staff  0 Mar 31 15:25 perm_practice/test_file.txt
```

#### 파일 권한 변경 및 확인 (모든 권한 부여)
```bash
$ chmod 777 perm_practice/test_file.txt
$ ls -l perm_practice/test_file.txt
-rwxrwxrwx@ 1 {username}  staff  0 Mar 31 15:25 perm_practice/test_file.txt
```

#### 파일 권한 복원
```bash
$ chmod 644 perm_practice/test_file.txt
$ ls -l perm_practice/test_file.txt
-rw-r--r--@ 1 {username}  staff  0 Mar 31 15:25 perm_practice/test_file.txt
```

#### 디렉토리 권한 변경 및 확인 (소유자 전용 접근)
```bash
$ chmod 700 perm_practice
$ ls -ld perm_practice
drwx------@ 3 {username}  staff  96 Mar 31 15:25 perm_practice
```

#### 디렉토리 권한 복원
```bash
$ chmod 755 perm_practice
$ ls -ld perm_practice
drwxr-xr-x@ 3 {username}  staff  96 Mar 31 15:25 perm_practice
```

#### 실습 정리 및 삭제
```bash
$ rm -r perm_practice
```
