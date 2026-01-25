# rpmtools

RPM 패키지 번들러 - Rocky Linux용 시스템 패키지 번들

---

## 다운로드

<!-- CONTENT_START -->
_Loading..._
<!-- CONTENT_END -->

!!! note "자동 업데이트"
    이 내용은 CDN의 metadata.json에서 자동으로 생성됩니다.

---

## 사용법

### 설치

```bash
# 기본 설치 (root 필요)
sudo ./rpmtools-bundle

# 자동 설치 (확인 없이)
sudo ./rpmtools-bundle --yes

# 특정 경로에 압축 해제만
./rpmtools-bundle --extract-only --prefix=/tmp/rpms
```

### 옵션

| 옵션 | 설명 |
|------|------|
| `--yes`, `-y` | 확인 없이 설치 |
| `--extract-only` | RPM 파일만 추출 |
| `--prefix=PATH` | 추출 경로 지정 |
| `--list` | 포함된 패키지 목록 |
| `--help` | 도움말 |

---

## 지원 OS

| OS 버전 | 아키텍처 | 지원 |
|---------|----------|------|
| Rocky Linux 9 | x86_64 | :white_check_mark: |
| Rocky Linux 9 | aarch64 | :white_check_mark: |
| Rocky Linux 8 | x86_64 | :white_check_mark: |
| Rocky Linux 8 | aarch64 | :white_check_mark: |

---

## 호환성

!!! warning "RHEL 호환성"
    rpmtools 번들은 Rocky Linux를 기반으로 빌드되었습니다.
    RHEL, CentOS Stream, AlmaLinux에서의 호환성은 [호환성 가이드](https://github.com/project-jelly/pkgman-core/blob/main/docs/compatibility.md)를 참조하세요.
