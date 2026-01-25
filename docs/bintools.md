# bintools

Go 바이너리 패키지 관리자 - DevOps CLI 도구 번들

---

## 다운로드

=== "Latest"

    ```bash
    curl -LO https://files.project-jelly.io/packages/bintools/latest/bintools
    chmod +x bintools
    ```

=== "특정 버전"

    ```bash
    VERSION="20250125-2110"
    curl -LO "https://files.project-jelly.io/packages/bintools/${VERSION}/bintools-${VERSION}"
    chmod +x "bintools-${VERSION}"
    ```

---

## 패키지 목록

<!-- PACKAGES_TABLE_START -->
| Package | Version | Description |
|---------|---------|-------------|
| kubectl | - | Kubernetes CLI |
| helm | - | Kubernetes package manager |
| terraform | - | Infrastructure as Code |
| argocd | - | GitOps CD for Kubernetes |
| k9s | - | Kubernetes TUI |
| yq | - | YAML processor |
| jq | - | JSON processor |
| aws-cli | - | AWS CLI v2 |
| kustomize | - | Kubernetes configuration |
| kind | - | Kubernetes in Docker |
| skopeo | - | Container image tool |
<!-- PACKAGES_TABLE_END -->

!!! note "자동 업데이트"
    이 표는 CDN의 metadata.json에서 자동으로 생성됩니다.

---

## 사용법

### 패키지 설치

```bash
# 단일 패키지 설치
./bintools install kubectl

# 여러 패키지 설치
./bintools install kubectl helm terraform

# 특정 경로에 설치
./bintools install kubectl --prefix=/opt/bin
```

### 패키지 목록 확인

```bash
# 포함된 패키지 목록
./bintools ls

# 상세 정보
./bintools ls -l
```

### 패키지 정보

```bash
# 패키지 버전 확인
./bintools info kubectl
```

---

## 지원 아키텍처

| 아키텍처 | 지원 |
|----------|------|
| linux/amd64 | :white_check_mark: |
| linux/arm64 | :white_check_mark: |
| darwin/amd64 | :white_check_mark: |
| darwin/arm64 | :white_check_mark: |
