# pkgman

에어갭 환경을 위한 패키지 관리자 문서 사이트

## 링크

- **문서 사이트**: https://cagojeiger.github.io/pkgman/

## 로컬 개발

```bash
# packages.json 생성
BINTOOLS_VERSION="20260125-1217" \
SNAPTOOLS_VERSION="20260125-1430" \
RPMTOOLS_DATA='{"9.2":"20260125-1218"}' \
python scripts/generate-index.py

# 로컬 서버 실행
python -m http.server 8000 -d docs

# 브라우저에서 확인
open http://localhost:8000
```

## 구조

```
pkgman/
├── docs/
│   ├── index.html          # 메인 페이지 (Tailwind CSS)
│   └── data/
│       └── packages.json   # 패키지 데이터
├── scripts/
│   └── generate-index.py   # packages.json 생성 스크립트
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Pages 배포
```

## 배포

`docs/` 폴더 변경 시 자동 배포됩니다.

```bash
# 수동 배포
gh workflow run deploy.yml
```

## 라이선스

MIT
