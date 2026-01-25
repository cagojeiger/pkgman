# pkgman

에어갭 환경을 위한 패키지 관리자 문서 사이트

## 링크

- **문서 사이트**: https://cagojeiger.github.io/pkgman/
- **CDN**: https://files.project-jelly.io/packages/

## 로컬 개발

```bash
# 의존성 설치
pip install mkdocs-material

# 메타데이터에서 문서 생성
python scripts/generate-docs.py

# 로컬 서버 실행
mkdocs serve
```

## 구조

```
pkgman/
├── docs/
│   ├── index.md        # 홈 페이지
│   ├── bintools.md     # bintools 문서
│   └── rpmtools.md     # rpmtools 문서
├── scripts/
│   └── generate-docs.py  # 메타데이터 변환 스크립트
├── mkdocs.yml          # MkDocs 설정
└── .github/
    └── workflows/
        └── deploy.yml  # GitHub Pages 배포
```

## 문서 업데이트

수동으로 워크플로우를 실행하여 CDN의 `metadata.json`에서 문서를 업데이트합니다.

```bash
gh workflow run deploy.yml
```

## 라이선스

MIT
