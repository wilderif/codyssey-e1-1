## Git 설정 및 GitHub 연동 실습

### Git 사용자 정보 및 기본 브랜치 설정

#### 터미널에서 Git의 사용자 이름과 이메일, 그리고 기본 브랜치 이름을 설정합니다.

```bash
$ git config --global user.name "{username}"
$ git config --global user.email "{email}"
$ git config --global init.defaultBranch main
```

#### 설정 확인 (`git config --list`)
설정한 내용은 `git config --global --list` 명령어를 통해 확인할 수 있습니다.

```bash
$ git config --global --list
user.name={username}
user.email={email}
init.defaultbranch=main
```

---

### GitHub 저장소 연동 및 푸시
로컬 저장소와 GitHub 원격 저장소(Remote Repository)를 다루고 코드를 업로드합니다.

#### 원격 저장소 추가 및 푸시
```bash
$ git remote add origin {remote-repository-url}
$ git branch -M main
$ git push -u origin main
```

#### 연동 증거 (스크린샷)
```bash
$ git remote -v
origin  {remote-repository-url} (fetch)
origin  {remote-repository-url} (push)

$ git status
On branch main
Your branch is up to date with 'origin/main'.
```

---

### Git 사용자 정보 삭제

```bash
$ git config --global --unset user.name
$ git config --global --unset user.email
```

#### 설정 삭제 확인

```bash
$ git config --global --list
# user.name과 user.email 항목이 나타나지 않으면 정상적으로 삭제된 것입니다.
```
