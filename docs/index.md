# pkgman

**에어갭 환경을 위한 패키지 관리자**

폐쇄망 환경에서 DevOps 도구를 쉽게 배포할 수 있도록 단일 자체 추출 실행 파일을 생성합니다.

---

## 도구 선택

<div class="grid cards" markdown>

-   :material-console:{ .lg .middle } **bintools**

    ---

    Go 바이너리 패키지 관리자
    kubectl, helm, terraform 등 DevOps CLI 도구

    [:octicons-arrow-right-24: bintools 보기](bintools.md)

-   :material-package-variant:{ .lg .middle } **rpmtools**

    ---

    RPM 패키지 번들러
    Rocky Linux용 시스템 패키지 번들

    [:octicons-arrow-right-24: rpmtools 보기](rpmtools.md)

</div>

---

## 빠른 시작

### bintools

```bash
# 다운로드
curl -LO https://files.project-jelly.io/packages/bintools/latest/bintools

# 실행 권한 부여
chmod +x bintools

# 패키지 설치
./bintools install kubectl helm
```

### rpmtools

```bash
# Rocky 9용 번들 다운로드
curl -LO https://files.project-jelly.io/packages/rpmtools/rocky9/latest/rpmtools-bundle

# 실행 권한 부여
chmod +x rpmtools-bundle

# 설치 (root 필요)
sudo ./rpmtools-bundle
```

---

## 특징

- **단일 실행 파일**: 의존성 없이 하나의 파일로 배포
- **오프라인 지원**: 인터넷 연결 없이 사용 가능
- **자동 아키텍처 감지**: amd64/arm64 자동 선택
- **버전 관리**: 특정 버전 다운로드 및 관리
