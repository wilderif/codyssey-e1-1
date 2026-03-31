## 터미널 조작 로그 기록

### 현재 위치 확인
```bash
$ pwd
/Users/{username}/...

```

### 목록 확인 (숨김 파일 포함)
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

### 생성 (디렉토리)
```bash
$ mkdir practice_directory
```

### 이동
```bash
$ cd practice_directory
```

### 빈 파일 생성
```bash
$ touch practice_directory/test_file.txt
```

### 파일 내용 추가
```bash
$ echo "Hello World" > practice_directory/test_file.txt
```

### 복사
```bash
$ cp practice_directory/test_file.txt practice_directory/copy_file.txt
```

### 이동 및 이름 변경
```bash
$ mv practice_directory/copy_file.txt practice_directory/renamed_file.txt
```

### 파일 내용 확인
```bash
$ cat practice_directory/renamed_file.txt
```

### 삭제
```bash
$ rm practice_directory/test_file.txt
$ rm -r practice_directory
```

