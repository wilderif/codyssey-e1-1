## GitHub HTTPS vs SSH 정리

GitHub 원격 저장소에 연결하는 방식은 대표적으로 **HTTPS**와 **SSH** 두 가지가 있습니다. 둘 다 `clone`, `pull`, `push` 같은 Git 작업을 수행할 수 있지만, **접속 방식과 인증 방식**에서 차이가 있습니다.

### 1. HTTPS 방식

HTTPS는 웹사이트 주소처럼 GitHub 저장소에 접속하는 방식입니다.

```bash
https://github.com/user/repo.git
```

이 방식은 GitHub와 통신할 때 HTTPS 프로토콜을 사용합니다. 예전에는 아이디와 비밀번호를 직접 입력하는 경우가 많았지만, 현재는 보통 Personal Access Token(PAT), 운영체제의 자격 증명 관리자, 또는 GitHub CLI 로그인 정보를 사용해 인증합니다.

**특징**
- 설정이 비교적 쉽고 직관적입니다.
- SSH 키를 따로 생성하거나 등록하지 않아도 됩니다.
- 회사, 학교, 공용 네트워크 환경에서도 비교적 무난하게 동작하는 편입니다.
- 다만 환경에 따라 인증 정보를 다시 요구받을 수 있고, 토큰 관리가 필요할 수 있습니다.

**예시**
```bash
$ git clone https://github.com/user/repo.git
```

### 2. SSH 방식

SSH는 SSH 키 기반 인증을 사용해 GitHub에 접속하는 방식입니다.

```bash
git@github.com:user/repo.git
```

이 방식은 로컬 컴퓨터에서 공개키(public key)와 개인키(private key)를 생성한 뒤, 공개키를 GitHub 계정에 등록해서 사용합니다. 이후 GitHub는 해당 키를 가진 사용자인지 확인하여 인증합니다.

**특징**
- 초기에 SSH 키를 생성하고 등록하는 설정 과정이 필요합니다.
- 한 번 설정해두면 `push`, `pull` 할 때 인증이 매우 편합니다.
- 개인 개발 환경, 맥북, 리눅스, 터미널 중심 워크플로우에서 많이 선호됩니다.
- 다만 조직 네트워크나 보안 정책에 따라 SSH 연결이 제한되는 경우도 있습니다.

**예시**
```bash
$ git clone git@github.com:user/repo.git
```

**기본 설정 흐름**
```bash
# SSH 키 생성 / -t: 키 타입 지정 (ed25519: 권장되는 알고리즘), -C: 코멘트
$ ssh-keygen -t ed25519 -C "your_email@example.com"

# SSH 에이전트 실행
$ eval "$(ssh-agent -s)"
# SSH 키를 SSH 에이전트에 등록
$ ssh-add ~/.ssh/id_ed25519

# 공개키 확인
$ cat ~/.ssh/id_ed25519.pub

# GitHub 설정에 공개키 등록

# GitHub 서버와 연결 테스트
$ ssh -T git@github.com
Hi {github-username}! You've successfully authenticated, but GitHub does not provide shell access.
```

### 3. HTTPS와 SSH의 핵심 차이

| 항목 | HTTPS | SSH |
| --- | --- | --- |
| **접속 주소 형태** | `https://github.com/...` | `git@github.com:...` |
| **인증 방식** | 토큰, 자격 증명 저장소 | SSH 키 |
| **초기 설정 난이도** | 쉬움 | 약간 복잡함 |
| **장기 사용 편의성** | 보통 | 매우 편함 |
| **주 사용 환경** | 입문자, 제한된 네트워크 환경 | 개인 개발 환경, 터미널 중심 작업 |

### 4. 어떤 방식을 선택하면 좋은가

**HTTPS가 더 적합한 경우**
- Git과 GitHub를 처음 배우는 단계
- SSH 키 설정이 아직 낯설게 느껴지는 경우
- 회사나 학교 네트워크 정책상 SSH가 제한될 가능성이 있는 경우

**SSH가 더 적합한 경우**
- 개인 로컬 개발 환경에서 Git을 자주 사용하는 경우
- 터미널 기반으로 작업하는 경우
- 여러 GitHub 저장소를 지속적으로 다루는 경우
- 인증 과정을 최대한 간단하게 유지하고 싶은 경우

### 5. 현재 저장소 연결 방식 확인하기

현재 내 로컬 저장소가 HTTPS인지 SSH인지 확인하려면 아래 명령어를 사용하면 됩니다.

```bash
$ git remote -v
```

**HTTPS 예시**
```bash
origin  https://github.com/user/repo.git (fetch)
origin  https://github.com/user/repo.git (push)
```

**SSH 예시**
```bash
origin  git@github.com:user/repo.git (fetch)
origin  git@github.com:user/repo.git (push)
```

### 6. 연결 방식 변경하기

중간에 연결 방식을 바꾸는 것도 가능합니다.

**HTTPS → SSH**
```bash
$ git remote set-url origin git@github.com:user/repo.git
```

**SSH → HTTPS**
```bash
$ git remote set-url origin https://github.com/user/repo.git
```

### 7. 정리

HTTPS와 SSH는 둘 다 GitHub를 사용하는 데 문제가 없는 정상적인 방식입니다. 다만 HTTPS는 시작하기 쉽고, SSH는 한 번 설정하면 장기적으로 더 편리하다는 차이가 있습니다.

개인 개발 환경에서 Git을 자주 사용한다면 보통 SSH 방식이 더 선호되며, 처음 배우는 단계이거나 네트워크 제약이 있다면 HTTPS 방식도 충분히 좋은 선택입니다.
