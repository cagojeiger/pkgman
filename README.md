# pkgman

onprem 환경을 위한 패키지 관리자 문서 사이트

## 링크

- **문서 사이트**: https://cagojeiger.github.io/pkgman/

## 로컬 개발

```bash
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
