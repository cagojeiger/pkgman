# rpmtools

RPM 패키지 번들러 - Rocky Linux용 시스템 패키지 번들

---

## 다운로드

=== "Rocky 9 (Latest)"

    ```bash
    curl -LO https://files.project-jelly.io/packages/rpmtools/9.5/latest/rpmtools-bundle
    chmod +x rpmtools-bundle
    ```

=== "Rocky 8 (Latest)"

    ```bash
    curl -LO https://files.project-jelly.io/packages/rpmtools/8.10/latest/rpmtools-bundle
    chmod +x rpmtools-bundle
    ```

=== "특정 버전"

    ```bash
    VERSION="20250125-2110"
    OS_VER="9.5"  # 또는 8.10
    curl -LO "https://files.project-jelly.io/packages/rpmtools/${OS_VER}/${VERSION}/rpmtools-bundle"
    chmod +x rpmtools-bundle
    ```

---

## 패키지 목록

### Rocky 9

<!-- ROCKY9_PACKAGES_START -->
| Package | Version | Description |
|---------|---------|-------------|
| containerd.io | - | Container runtime |
| docker-ce | - | Docker engine |
| docker-ce-cli | - | Docker CLI |
| docker-buildx-plugin | - | Docker Buildx |
| docker-compose-plugin | - | Docker Compose |
<!-- ROCKY9_PACKAGES_END -->

### Rocky 8

<!-- ROCKY8_PACKAGES_START -->
| Package | Version | Description |
|---------|---------|-------------|
| containerd.io | - | Container runtime |
| docker-ce | - | Docker engine |
| docker-ce-cli | - | Docker CLI |
| docker-buildx-plugin | - | Docker Buildx |
| docker-compose-plugin | - | Docker Compose |
<!-- ROCKY8_PACKAGES_END -->

!!! note "자동 업데이트"
    이 표는 CDN의 metadata.json에서 자동으로 생성됩니다.

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
