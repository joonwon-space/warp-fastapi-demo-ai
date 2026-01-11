# Devlog 기록 가이드

각 커밋마다, 커밋 날짜 기준으로 devlog 파일을 하나씩 생성합니다.

## 파일명 규칙 예시

- `YYYY-MM-DD-<short-hash>.md`
- 예: `2026-01-11-a1b2c3d.md`

## 문서 예시 구조

```markdown
# 2026-01-11 a1b2c3d

- Author: YOUR_NAME
- Commit: a1b2c3d
- Date: 2026-01-11
- Subject: Initial FastAPI project setup

## 변경 요약
- FastAPI 기본 앱 생성 (`app/main.py`)
- 의존성 정의 (`requirements.txt`)
- README 초안 작성

## 세부 변경 사항
- 엔드포인트 목록
  - `GET /health`: 헬스 체크
  - ...

## 테스트
- [ ] 로컬에서 `uvicorn app.main:app --reload` 로 서버 실행 확인
- [ ] 주요 엔드포인트 수동 호출 및 동작 확인

## 메모
- 이후 TODO 및 개선 아이디어 기록
```

이 템플릿을 복사해서 각 커밋에 대한 devlog를 `docs/devlog` 아래에 추가하면 됩니다.
