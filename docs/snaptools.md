# snaptools

Snap 패키지 번들러 - Ubuntu용 시스템 패키지 번들

---

## 다운로드

=== "Latest"

    ```bash
    curl -LO https://files.project-jelly.io/packages/snaptools/latest/snaptools-bundle
    chmod +x snaptools-bundle
    ```

=== "특정 버전"

    ```bash
    VERSION="20250125-2110"
    curl -LO "https://files.project-jelly.io/packages/snaptools/${VERSION}/snaptools-bundle"
    chmod +x snaptools-bundle
    ```

---

## 패키지 목록

<!-- PACKAGES_TABLE_START -->
| Package | Version | Description |
|---------|---------|-------------|
<!-- PACKAGES_TABLE_END -->

!!! note "자동 업데이트"
    이 표는 CDN의 metadata.json에서 자동으로 생성됩니다.

---

## 사용법

### 설치

```bash
# 기본 설치 (root 필요)
sudo ./snaptools-bundle

# 자동 설치 (확인 없이)
sudo ./snaptools-bundle --yes

# 특정 경로에 압축 해제만
./snaptools-bundle --extract-only --prefix=/tmp/snaps
```

### 옵션

| 옵션 | 설명 |
|------|------|
| `--yes`, `-y` | 확인 없이 설치 |
| `--extract-only` | snap 파일만 추출 |
| `--prefix=PATH` | 추출 경로 지정 |
| `--list` | 포함된 패키지 목록 |
| `--help` | 도움말 |

---

## 지원 OS

| OS 버전 | 아키텍처 | 지원 |
|---------|----------|------|
| Ubuntu 22.04 | x86_64 | :white_check_mark: |
| Ubuntu 22.04 | aarch64 | :white_check_mark: |
| Ubuntu 24.04 | x86_64 | :white_check_mark: |
| Ubuntu 24.04 | aarch64 | :white_check_mark: |
