# API 문서 (warp-fastapi-demo-ai)

프론트엔드에서 사용하는 주요 API 엔드포인트를 정리한 문서입니다.

- Base URL (로컬 개발 기준): `http://127.0.0.1:8000`
- 응답 포맷: `application/json`
- 인증 방식: **Bearer Token (JWT)**

---

## 1. 헬스/루트 API

### `GET /`

애플리케이션이 정상 동작하는지 확인하는 간단한 헬스 체크/루트 엔드포인트입니다.

- **Request**
  - Method: `GET`
  - Path: `/`
  - Headers: 없음

- **Response (200)**
  ```json
  {
    "message": "Hello from warp-fastapi-demo-ai"
  }
  ```

---

## 2. 인증 / 로그인

### `POST /auth/token`

폼 데이터로 `username`, `password`를 보내면 JWT access token 을 발급합니다.
프론트엔드는 이 토큰을 이후 요청의 `Authorization` 헤더에 `Bearer <token>` 형태로 포함해야 합니다.

- **Request**
  - Method: `POST`
  - Path: `/auth/token`
  - Headers:
    - `Content-Type: application/x-www-form-urlencoded`
  - Body (x-www-form-urlencoded):
    - `username`: `string` (필수)
    - `password`: `string` (필수)

- **Sample Request (curl)**
  ```bash
  curl -X POST "http://127.0.0.1:8000/auth/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test&password=test1234"
  ```

- **Response (200)**
  - Body
    ```json
    {
      "access_token": "<JWT 문자열>",
      "token_type": "bearer"
    }
    ```

- **Response (401 - 인증 실패)**
  - Body
    ```json
    {
      "detail": "Incorrect username or password"
    }
    ```

- **프론트엔드 처리 가이드**
  - 로그인 성공 시:
    - `access_token` 값을 로컬 스토리지/메모리 등에 저장
    - 이후 API 호출 시 `Authorization: Bearer <access_token>` 헤더를 항상 포함
  - 실패 시:
    - `detail` 메시지를 UI 에러로 표시

---

## 3. 내 정보 조회

### `GET /users/me`

현재 로그인된 유저의 정보를 반환하는 보호된 엔드포인트입니다.
반드시 `Authorization` 헤더에 유효한 JWT 토큰이 있어야 합니다.

- **Request**
  - Method: `GET`
  - Path: `/users/me`
  - Headers:
    - `Authorization: Bearer <access_token>`

- **Response (200)**
  - Body 예시
    ```json
    {
      "username": "test",
      "full_name": "Test User",
      "disabled": false
    }
    ```

- **Response (401 - 인증 실패)**
  - 토큰이 없거나, 잘못되었거나, 만료된 경우
  - Body
    ```json
    {
      "detail": "Could not validate credentials"
    }
    ```

- **Response (400 - 비활성 유저)**
  - disabled 유저인 경우
  - Body
    ```json
    {
      "detail": "Inactive user"
    }
    ```

- **프론트엔드 처리 가이드**
  - 401 응답 시:
    - 토큰 만료 또는 인증 실패로 간주 → 로그인 페이지로 리다이렉트
  - 400 & "Inactive user" 시:
    - 계정 비활성화 안내 메시지 노출

---

## 4. 에러 처리 공통 규칙

FastAPI 기본 에러 포맷을 사용합니다.

- 예) 422 Validation Error
  ```json
  {
    "detail": [
      {
        "loc": ["body", "username"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

프론트엔드는 아래를 기준으로 처리하면 됩니다.

- 2xx: 정상 응답 → body 를 그대로 사용
- 4xx: 클라이언트 입력/인증 문제 → 메시지(`detail` 또는 각 필드 오류)를 사용자에게 보여줌
- 5xx: 서버 오류 → "일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요" 등 공통 에러 메시지 사용

---

## 5. Swagger / OpenAPI 참고 (개발용)

백엔드가 실행 중일 때, 브라우저에서 다음 URL로 접속하면 자동 생성된 API 문서를 볼 수 있습니다.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

프론트엔드 개발 시, 상세 스키마나 추가 필드는 Swagger UI를 참고하면 됩니다.
