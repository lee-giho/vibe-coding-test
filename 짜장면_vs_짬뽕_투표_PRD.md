# 짜장면 vs 짬뽕 투표 웹페이지 PRD (Flask + MySQL + Docker Compose)

> 목적: 사용자가 **짜장면**과 **짬뽕** 중 하나를 선택해 투표하고, **현재까지의 결과를 실시간으로 확인**할 수 있는 웹서비스를 만든다.  
> 결과는 **서버가 관리**하며, 데이터는 **MySQL에 영속 저장**되어 재접속/재배포 후에도 결과가 유지된다.  
> 프론트는 **HTML/CSS/JavaScript**, 백엔드는 **Flask**, DB는 **Docker Compose 기반 MySQL 컨테이너**를 사용한다.

---

## 1. 문제 정의 & 목표

### 1.1 배경
식사 메뉴를 고를 때 “짜장면 vs 짬뽕”처럼 2지선다 투표로 주변의 선택을 빠르게 확인하고 싶어한다. 단순하지만 **즉시성(실시간 결과)**과 **신뢰성(서버/DB가 관리)**이 중요하다.

### 1.2 성공 기준(측정 가능한 목표)
- 사용자가 **30초 이내**에 투표를 완료하고 결과를 확인할 수 있다.
- 동시 접속 100명 수준에서 결과가 정상 반영되고 UI가 깨지지 않는다.
- 서버/DB 재시작 이후에도 누적 결과가 **정확히 유지**된다.
- 투표 API 평균 응답시간 p95 < 300ms (로컬/개발 기준, 프로덕션은 별도 모니터링)

---

## 2. 타겟 사용자 & 페르소나

### 타겟
- 점심/저녁 메뉴를 고민하는 사람들(직장인/학생/가족/친구 모임 등)

### 페르소나 예시
- **직장인 A(29)**: 점심 때 동료들과 “뭐 먹지?”를 빠르게 정하고 싶다. 투표 결과가 바로 반영되는 게 중요.
- **학생 B(22)**: 친구들 취향을 보고 메뉴를 정한다. 휴대폰으로 사용하며, UI가 단순해야 한다.

---

## 3. 범위(Scope)

### 3.1 이번 버전(MVP, 출시 가능 수준)
- 투표 페이지(짜장면/짬뽕 2개 옵션)
- 투표 생성(POST) 및 결과 조회(GET)
- 결과 실시간 반영(기본: 폴링, 옵션: SSE 스트림)
- MySQL 영속 저장
- Docker Compose로 로컬/서버에서 손쉽게 기동
- 기본 보안/운영 요소(입력 검증, CORS 정책, 로깅, 간단한 악용 방지)

### 3.2 제외(추후 고려)
- 로그인/회원 시스템
- 여러 주제/여러 투표 생성 기능(지금은 1개 고정 주제)
- 관리자 페이지(추후 운영 필요 시 추가)
- 다국어/테마 커스터마이징

---

## 4. 핵심 사용자 시나리오(유저 스토리)

1) **사용자**는 페이지에 접속하면 현재 투표 결과를 즉시 확인한다.  
2) **사용자**는 “짜장면” 또는 “짬뽕” 버튼을 누르고 투표한다.  
3) 투표 후 **결과가 즉시 업데이트**되며(실시간), 새로고침해도 결과는 유지된다.  
4) 네트워크 오류가 발생하면 사용자에게 안내하고 재시도를 유도한다.

---

## 5. UX/UI 요구사항

### 5.1 페이지 구성(단일 페이지)
- 상단: 서비스 타이틀(예: “오늘 뭐 먹지?”)
- 중앙: 선택 카드 2개
  - 짜장면 카드: 이미지(선택), 버튼
  - 짬뽕 카드: 이미지(선택), 버튼
- 하단: 현재 집계 결과
  - 각 항목별 득표수, 퍼센트, 막대 그래프
  - 마지막 업데이트 시각(서버 기준)

### 5.2 상태 정의(화면 공통 상태)
- **Loading**: 최초 결과 로딩 중 스켈레톤/로딩 표시
- **Success**: 정상 렌더링
- **Error**: API 실패(네트워크/서버 오류) → “다시 시도” 버튼
- **Empty**: 투표 수 0일 때(“첫 투표를 해보세요!”)

### 5.3 실시간 업데이트 방식
- **기본(필수)**: 클라이언트가 2~5초 간격으로 `GET /api/v1/results` 폴링
- **옵션(권장)**: `GET /api/v1/results/stream` **SSE(Server-Sent Events)**로 서버가 변경사항 푸시  
  - 프론트는 `EventSource`로 구독
  - 네트워크 불안정 시 자동 재연결 처리

> “실제 서비스” 관점에서 트래픽이 커지면 SSE/WS가 유리하지만, MVP는 폴링만으로도 충분히 출시 가능하다(서버 비용/복잡도 감소).

---

## 6. 시스템 요구사항

## 6.1 아키텍처 개요
- **Frontend**: HTML/CSS/Vanilla JS (정적 파일)
- **Backend**: Flask REST API (+ 선택적으로 SSE)
- **DB**: MySQL (Docker Compose)
- (선택) Reverse Proxy: Nginx (프로덕션 배포 시 추천)

### 6.2 데이터 영속성
- 결과/투표 로그는 MySQL에 저장
- Docker Compose에서 MySQL volume을 사용해 컨테이너 재시작에도 데이터 유지

---

## 7. 데이터 모델(초안)

### 7.1 테이블: `polls`
- `id` (PK, INT, AI)
- `title` (VARCHAR) — 예: “짜장면 vs 짬뽕”
- `is_active` (TINYINT) — 현재는 1개 고정이지만 확장 대비
- `created_at` (DATETIME)

### 7.2 테이블: `options`
- `id` (PK, INT, AI)
- `poll_id` (FK -> polls.id)
- `label` (VARCHAR) — “짜장면”, “짬뽕”
- `vote_count` (INT, DEFAULT 0) — 빠른 집계를 위한 캐시 컬럼(서버에서 업데이트)
- `created_at` (DATETIME)

### 7.3 테이블: `votes`
- `id` (PK, BIGINT, AI)
- `poll_id` (FK)
- `option_id` (FK)
- `created_at` (DATETIME)
- `client_hash` (CHAR(64), NULL) — (선택) IP+UA 기반 해시 등 악용 방지용 (원문 저장 X)

> 운영 관점 권장: `votes`에 투표 로그를 남기고, `options.vote_count`는 **트랜잭션**으로 증가시켜 집계와 로그를 동시에 보장한다.

---

## 8. API 설계 (RESTful)

### 공통
- Base URL: `/api/v1`
- Content-Type: `application/json`
- 응답 공통 필드(권장):
  - `success` (bool)
  - `data` (object | null)
  - `error` (object | null): `{ code, message, details }`

---

### 8.1 투표하기
#### `POST /api/v1/votes`
사용자가 특정 옵션에 투표한다.

**Request Body**
```json
{
  "pollId": 1,
  "optionId": 10
}
```

**Validation**
- `pollId`는 존재해야 함
- `optionId`는 해당 poll에 속해야 함
- poll이 활성 상태여야 함(`is_active=1`)

**Response 200**
```json
{
  "success": true,
  "data": {
    "pollId": 1,
    "optionId": 10,
    "results": {
      "totalVotes": 123,
      "options": [
        { "optionId": 10, "label": "짜장면", "count": 70, "percent": 56.91 },
        { "optionId": 11, "label": "짬뽕",   "count": 53, "percent": 43.09 }
      ],
      "updatedAt": "2025-12-30T14:00:00+09:00"
    }
  },
  "error": null
}
```

**Error Cases**
- 400: 잘못된 payload(필드 누락/타입 오류)
- 404: poll/option 없음
- 409: (선택) 동일 사용자 반복 투표 제한 정책 위반
- 500: 서버 내부 오류

---

### 8.2 결과 조회
#### `GET /api/v1/results?pollId=1`
현재 결과를 조회한다.

**Response 200**
```json
{
  "success": true,
  "data": {
    "pollId": 1,
    "title": "짜장면 vs 짬뽕",
    "totalVotes": 123,
    "options": [
      { "optionId": 10, "label": "짜장면", "count": 70, "percent": 56.91 },
      { "optionId": 11, "label": "짬뽕",   "count": 53, "percent": 43.09 }
    ],
    "updatedAt": "2025-12-30T14:00:00+09:00"
  },
  "error": null
}
```

**Empty 처리**
- totalVotes=0이면 `options[].percent=0`으로 반환
- 프론트는 “첫 투표를 해보세요!” 안내 표시

---

### 8.3 (옵션) 실시간 스트림(SSE)
#### `GET /api/v1/results/stream?pollId=1`
- Server-Sent Events 형식으로 결과 변경 이벤트를 푸시
- 이벤트 예시:
  - `event: results_updated`
  - `data: {...results json...}`

**프론트 예시 정책**
- SSE 연결 성공 시 폴링 중단
- SSE 끊기면 폴링로 fallback

> 이 엔드포인트도 “조회”이므로 GET을 사용하며, RESTful 제약에 위배되지 않는다.

---

## 9. 비기능 요구사항(NFR)

### 9.1 성능/확장
- 결과 조회는 빠르게(캐시 컬럼 사용)
- 투표 증가(update count)는 원자적으로 처리(트랜잭션 + `vote_count = vote_count + 1`)

### 9.2 보안
- CORS: 운영 도메인만 허용(개발 환경은 localhost 허용)
- 입력 검증(숫자 타입/존재 여부)
- (선택) 간단한 악용 방지:
  - 동일 client_hash(예: IP+UA 해시) 기준 일정 시간(예: 10초) 내 중복 투표 제한
  - Rate Limit(예: IP당 분당 60회) — Flask-Limiter 등 적용 가능

### 9.3 관측/로깅
- 요청/응답 상태코드 로그
- 투표 요청은 optionId, pollId, latency, 결과 반영 여부 기록(개인정보 저장 X)

### 9.4 가용성/복구
- DB 연결 실패 시 503 반환 및 안내
- MySQL 컨테이너 재기동 후에도 volume 기반으로 데이터 유지

---

## 10. Docker Compose 요구사항

### 10.1 구성 요소
- `mysql` 서비스
- `api`(Flask) 서비스
- (선택) `nginx` 서비스(정적 파일/리버스 프록시)

### 10.2 환경 변수(예시)
- `MYSQL_HOST=mysql`
- `MYSQL_PORT=3306`
- `MYSQL_DATABASE=poll_db`
- `MYSQL_USER=poll_user`
- `MYSQL_PASSWORD=...`
- `MYSQL_ROOT_PASSWORD=...`

### 10.3 데이터 보존
- MySQL 데이터 디렉토리를 named volume으로 마운트

---

## 11. 기능 상세 명세(개발자가 바로 구현 가능한 수준)

## 11.1 프론트엔드

### 11.1.1 최초 로딩
- 동작
  - 페이지 진입 시 `GET /api/v1/results?pollId=1`
- 상태
  - Loading → Success/Empty/Error
- 예외
  - 5xx/네트워크 오류 시 Error UI + 재시도 버튼

### 11.1.2 투표 동작
- 입력
  - 사용자의 클릭(짜장면 또는 짬뽕)
- 처리
  - 버튼 비활성화(중복 클릭 방지)
  - `POST /api/v1/votes` 호출
  - 성공 시 결과 UI 즉시 갱신
- 예외
  - 409(중복 제한) → “잠시 후 다시 시도” 토스트
  - 400/404 → “잘못된 요청” 메시지
  - 500 → “서버 오류” 메시지

### 11.1.3 실시간 갱신
- 기본
  - 2~5초 간격 폴링으로 결과 갱신
- 옵션(SSE)
  - SSE 구독 성공 시 폴링 중단
  - 연결 끊김 시 폴링 재개

---

## 11.2 백엔드(Flask)

### 11.2.1 `POST /votes`
- 트랜잭션 처리(권장)
  1) poll, option 유효성 검사
  2) `votes` insert (로그 저장)
  3) `options.vote_count = options.vote_count + 1` update
  4) commit
  5) 최신 결과 계산 후 반환

### 11.2.2 `GET /results`
- `options`에서 `vote_count` 기반으로 집계
- percent 계산:
  - `percent = count / totalVotes * 100` (totalVotes=0이면 0)
- 응답에 `updatedAt` 포함(서버 시각)

### 11.2.3 에러 표준(권장)
- 400: `VALIDATION_ERROR`
- 404: `NOT_FOUND`
- 409: `VOTE_LIMITED`
- 503: `DB_UNAVAILABLE`
- 500: `INTERNAL_ERROR`

---

## 12. 테스트 시나리오(핵심)

1) 결과 0표 상태에서 첫 화면 로딩 → Empty UI 정상
2) 짜장면 1표 투표 → 결과 즉시 반영, totalVotes=1
3) 다른 브라우저에서 접속 → 동일 결과 확인(영속)
4) 동시 20명 투표 → 카운트 누락 없이 합계 일치
5) MySQL 컨테이너 재시작 → 결과 유지 확인
6) API 다운(Flask 중단) → 프론트 Error 상태 표시
7) (선택) 중복 제한 정책 동작 확인(409)

---

## 13. 배포(운영) 가이드 초안

- Flask는 개발 서버 대신 **gunicorn** 사용 권장
- (선택) Nginx로 정적 파일 캐싱 및 API reverse proxy
- 환경변수는 `.env`로 관리하고, 비밀값은 배포 환경의 Secret로 주입
- DB 백업 정책(예: 주 1회 dump, 또는 볼륨 스냅샷)

---

## 14. 오픈 이슈 / 의사결정 포인트

- “1인 1표”를 어디까지 강제할지?
  - 로그인 없음 기준에서는 완벽한 제약이 불가능(브라우저/네트워크 변경 가능)
  - 현실적 대안: **짧은 시간 중복 제한 + rate limiting**
- 실시간 방식 선택
  - MVP: 폴링(구현 단순)
  - 트래픽/UX 강화: SSE(권장), 또는 WebSocket(양방향 필요할 때)

---

## 15. 구현 체크리스트(코파일럿 개발용)

- [ ] DB 스키마 작성 및 초기 데이터(poll 1개 + option 2개) 시드
- [ ] Flask: DB 연결/헬스 체크 엔드포인트(선택)
- [ ] Flask: `POST /api/v1/votes` 구현(트랜잭션/검증/표준 에러)
- [ ] Flask: `GET /api/v1/results` 구현(percent 계산)
- [ ] (선택) Flask: `GET /api/v1/results/stream` SSE 구현
- [ ] Front: 상태(loading/empty/error/success) UI 구현
- [ ] Front: 투표 POST, 결과 렌더링, 폴링(or SSE) 구현
- [ ] Docker Compose: mysql + api 구성, volume 적용
- [ ] README: 실행 방법, 환경변수, API 예시(curl) 문서화

---

## 부록 A. 예시 응답 데이터(퍼센트 계산 규칙)
- totalVotes = 0 → 모든 percent = 0
- 소수점 처리: 프론트 표시용으로 소수점 2자리 반올림(서버에서 계산/프론트에서 포맷 둘 중 택1)

---

## 부록 B. API 예시 호출(curl)

```bash
# 결과 조회
curl "http://localhost:5000/api/v1/results?pollId=1"

# 투표
curl -X POST "http://localhost:5000/api/v1/votes" \
  -H "Content-Type: application/json" \
  -d '{"pollId":1,"optionId":10}'
```
