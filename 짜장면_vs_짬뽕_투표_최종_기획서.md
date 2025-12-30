# 짜장면 vs 짬뽕 실시간 투표 웹서비스 — 최종 기획서 (출시 수준)

> 이 문서는 지금까지 요청하신 PRD/상세 기능 명세/화면 구성·플로우를 통합하여, **“개발자가 바로 구현해서 실제 서비스로 출시할 수 있는 수준”**의 최종 기획서입니다.  
> 기술 스택(프론트: HTML/CSS/JS, 백엔드: Flask, DB: MySQL, 배포: Docker Compose)과 RESTful API(POST 투표, GET 결과조회)를 전제로 합니다.

---

## 0. 한 줄 요약
**짜장면과 짬뽕 중 하나를 선택해 투표하고, 누적 결과를 실시간으로 확인할 수 있는 단일 페이지 투표 웹서비스.**  
서버가 결과를 관리하고 MySQL에 영속 저장하여 재접속/재시작에도 결과가 유지된다.

---

## 1. 배경과 문제 정의

### 1.1 배경
메뉴 선택은 빠른 합의가 필요하지만, 사람마다 취향이 달라 결정을 미루게 된다. “짜장면 vs 짬뽕” 같은 2지선다 주제는 누구나 이해하고 바로 참여할 수 있다.

### 1.2 문제
- 메뉴를 빠르게 정하고 싶은데 의견이 분산되어 합의가 늦다.
- 결과가 즉시 반영되지 않으면 참여/공유 가치가 떨어진다.
- 서버/DB가 관리하지 않으면 새로고침/재접속 시 결과가 사라져 신뢰도가 떨어진다.

### 1.3 해결
- **투표 1탭**으로 참여하게 하고,
- **실시간 결과**를 보여주며,
- 결과는 **서버가 관리**하고 **MySQL 영속 저장**으로 유지한다.

---

## 2. 목표(Goals) & 비목표(Non-goals)

### 2.1 목표(Goals)
- 누구나 30초 안에 투표하고 결과를 확인할 수 있다.
- 결과는 **즉시 갱신**되고(실시간), 재접속해도 유지된다.
- RESTful API로 프론트/백 분리 개발이 가능하다.
- Docker Compose로 로컬/서버에서 일관되게 실행할 수 있다.

### 2.2 비목표(Non-goals) — MVP 범위 밖
- 로그인/회원가입/프로필
- 여러 주제의 투표 생성/관리(현재는 “1개 poll 고정”)
- 완벽한 “1인 1표” 강제(로그인 없는 환경에서는 현실적으로 불가)
- 관리자 페이지(추후 필요 시 추가)

---

## 3. 타겟 사용자 & 사용 맥락

### 3.1 타겟 사용자
- 점심/저녁 메뉴를 고민하는 직장인/학생/가족/친구 모임 사용자

### 3.2 사용 맥락(시나리오)
- “점심 뭐 먹지?” 상황에서 팀/친구들이 투표 링크를 공유 → 즉시 참여 → 결과를 보며 메뉴 확정

---

## 4. 제품 정의(서비스/기능 개요)

### 4.1 서비스 형태
- **단일 페이지(SPA-lite) 웹**: 한 화면에서 투표와 결과 확인을 끝낸다.
- **서버 중심 집계**: 결과는 클라이언트가 계산하지 않고 서버가 반환한다.
- **영속 저장**: MySQL에 `votes` 로그 및 `options.vote_count`를 저장한다.

### 4.2 핵심 가치
- **즉시성**: 투표 → 결과 즉시 반영
- **신뢰성**: 서버/DB가 관리하는 누적 결과
- **단순함**: 로그인/복잡한 흐름 없이 빠르게 참여

---

## 5. UX/UI 기획 (모바일 우선)

### 5.1 전역 원칙
- 들어오자마자 **3초 안에 이해** 가능
- **1탭 투표**: 버튼 클릭만으로 완료
- **즉시 피드백**: 투표 중/완료 상태를 명확히 표시
- **실패 대응**: 오류 안내 + 재시도 제공

### 5.2 주요 화면(1개)
- **홈/투표 페이지** 단일 화면 구성
  - Header: 타이틀 + 상태 배지(LIVE/OFFLINE/UPDATING)
  - Vote 영역: “짜장면” 카드 + “짬뽕” 카드(각각 투표 버튼)
  - Results 영역: 총 투표수, 옵션별 count/percent, progress bar, 마지막 업데이트
  - Footer: 안내 문구, 재시도/새로고침(선택)

### 5.3 화면 상태(state) 정의(공통)
- `loading`: 최초 결과 로딩/재시도 중
- `empty`: totalVotes=0(첫 투표 안내)
- `success`: 정상 결과 표시
- `error`: API 실패(네트워크/서버) → 재시도 UI

### 5.4 실시간 업데이트 UX
- MVP(필수): **폴링**(2~5초 간격)으로 `GET /results` 갱신
- 확장(권장): SSE 스트림 `GET /results/stream` 도입 후 폴링 fallback

---

## 6. 사용자 플로우(User Flow)

### 6.1 정상 플로우
1. 사용자가 페이지 접속 → 로딩 표시
2. `GET /results?pollId=1` 호출 → empty/success 화면 렌더링
3. 사용자가 “짜장면/짬뽕” 중 하나 선택 → `POST /votes`
4. 성공 응답에 포함된 최신 results로 즉시 UI 갱신
5. 폴링(또는 SSE)로 실시간 업데이트 유지
6. 새로고침/재접속 시 DB 기반 결과 재조회

### 6.2 예외 플로우(핵심)
- 초기 결과 조회 실패 → error 화면 + “다시 시도”
- 투표 실패(409/503 등) → 토스트/배너 안내 + 버튼 재활성화 + 재시도 유도
- 폴링 연속 실패 → OFFLINE 표시 + 일정 시간 후 자동 재시도(선택)

---

## 7. 기능 요구사항(요약)

### 7.1 사용자 기능(프론트)
- 결과 자동 로딩
- 투표 버튼(중복 클릭 방지)
- 결과 즉시 갱신
- 실시간 갱신(폴링)
- 오류 표시/재시도

### 7.2 서버 기능(백엔드)
- 결과 조회 API(집계/퍼센트 계산 포함)
- 투표 API(트랜잭션 + 원자적 카운트 증가)
- (선택) SSE 스트림
- (권장) 헬스체크 API

### 7.3 데이터(영속)
- 투표 로그 저장(votes)
- 옵션 카운트 저장(options.vote_count)
- 재시작/재접속 시 유지

---

## 8. 시스템 아키텍처 & 기술 스택

### 8.1 아키텍처
- Frontend: 정적 파일(HTML/CSS/JS)
- Backend: Flask REST API
- Database: MySQL (Docker Compose)
- (선택) Reverse Proxy: Nginx(정적 파일 서빙 + API 프록시)

### 8.2 데이터 흐름
- 페이지 로딩 → GET results → 화면 렌더링
- 투표 클릭 → POST votes → DB 트랜잭션 반영 → 최신 results 응답 → 화면 갱신
- 실시간 → 폴링 GET results 반복

---

## 9. API 설계(RESTful)

### 9.1 공통
- Base: `/api/v1`
- Content-Type: `application/json`
- 응답 표준:
  - `success: boolean`
  - `data: object | null`
  - `error: { code, message, details } | null`

### 9.2 투표 (필수)
#### `POST /api/v1/votes`
- Body:
```json
{ "pollId": 1, "optionId": 10 }
```
- 성공: 200 + 최신 results 포함
- 실패: 400/404/409/503/500 등 표준 에러

### 9.3 결과 조회 (필수)
#### `GET /api/v1/results?pollId=1`
- 성공: 200 + `{ totalVotes, options[], updatedAt }`
- 빈 상태: totalVotes=0 반환(프론트 empty 처리)

### 9.4 실시간 스트림 (선택)
#### `GET /api/v1/results/stream?pollId=1`
- SSE로 results_updated 이벤트 전송
- 프론트는 EventSource로 구독, 끊기면 폴링으로 fallback

### 9.5 헬스체크 (권장)
#### `GET /api/v1/health`
- 서버/DB 상태 확인용

---

## 10. 데이터 모델(최종 초안)

### 10.1 테이블
- `polls`(투표 주제)
- `options`(선택지 + vote_count 캐시)
- `votes`(투표 로그)

### 10.2 집계 전략
- `options.vote_count`를 증가시키는 방식으로 빠른 조회 제공
- 동시에 `votes`에 로그를 남겨 추후 분석/정책(중복 제한 등) 확장 가능

### 10.3 동시성/정합성(핵심)
- 투표 처리 시 트랜잭션으로:
  1) votes insert
  2) options.vote_count = vote_count + 1
- 이 2개가 함께 성공/실패하도록 원자성 보장

---

## 11. 비기능 요구사항(NFR)

### 11.1 성능
- 결과 조회는 빠르게(캐시 컬럼 활용)
- 투표 증가 연산은 원자적 update 사용

### 11.2 안정성
- DB 연결 실패 시 503 반환 + 프론트 에러 처리
- 연속 실패 시 OFFLINE 안내 + 재시도 제공

### 11.3 보안(현실적 수준)
- 입력값 검증(pollId/optionId 타입/존재)
- CORS 제한(운영 도메인만 허용, 개발은 localhost 허용)
- (선택) 남용 방지
  - client_hash 기반 짧은 시간 중복 제한(10초 등)
  - rate limit(IP 기준 분당 제한 등)

### 11.4 관측성
- 요청/응답 상태 코드 및 latency 로그
- 투표 이벤트 로그(개인정보 원문 저장 X)

---

## 12. Docker Compose 운영 설계

### 12.1 구성 요소(최소)
- mysql: MySQL 8.x + volume
- api: Flask + gunicorn(권장)

### 12.2 환경 변수
- MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_ROOT_PASSWORD 등
- APP_PORT 등

### 12.3 DB 초기화
- `docker-entrypoint-initdb.d/`로 schema/seed SQL 적용(권장)

### 12.4 데이터 영속성
- MySQL 데이터를 named volume에 저장해 컨테이너 재시작에도 유지

---

## 13. 구현 계획(개발 순서) — “코파일럿 개발” 최적화

> 목표: 작은 단위로 쪼개서 Copilot로 빠르게 구현/검증 가능하도록 한다.

### 13.1 1단계: DB/인프라 뼈대
1) docker-compose.yml 작성(mysql, api)
2) schema.sql + seed.sql 준비(1 poll + 2 options)
3) MySQL volume 설정 및 init 동작 확인

### 13.2 2단계: 백엔드 API
4) Flask 프로젝트 구조 생성
5) DB 연결 유틸(커넥션 풀/재시도)
6) `GET /api/v1/results` 구현 + percent 계산
7) `POST /api/v1/votes` 구현(트랜잭션/검증/원자적 증가)
8) (권장) `GET /api/v1/health` 구현
9) (선택) SSE stream 구현

### 13.3 3단계: 프론트 구현
10) index.html 레이아웃(모바일 1컬럼)
11) styles.css 반응형 및 컴포넌트 스타일
12) app.js state 머신(loading/empty/success/error)
13) fetchResults / submitVote / polling manager 구현
14) 오류/재시도/토스트 UX 적용
15) (선택) SSE 연결 + fallback

### 13.4 4단계: 품질/문서
16) 동시성 간단 테스트(스크립트로 POST 폭주)
17) README(실행 방법, env, API curl)
18) 운영 배포(서버에서 compose up) 리허설

---

## 14. 테스트/QA 계획(필수)

### 14.1 핵심 시나리오
- 0표 → empty
- 투표 1회 → 즉시 반영 + 새로고침 유지
- 다른 브라우저 → 동일 결과
- 동시 투표 20~100회 → 합계 누락 없음
- DB 재시작 → 결과 유지
- API 다운 → error UI

### 14.2 예외 케이스
- pollId 누락/문자열 → 400
- optionId가 poll에 속하지 않음 → 400
- 존재하지 않는 poll/option → 404
- DB down → 503

---

## 15. 출시 기준(Release Criteria)

- [ ] RESTful API(POST votes, GET results) 정상 동작
- [ ] MySQL 영속 저장 확인(재시작/재접속 유지)
- [ ] 프론트 상태(loading/empty/success/error) 모두 구현
- [ ] 실시간 갱신(최소 폴링) 동작
- [ ] 동시 투표에서 vote_count 누락 없음
- [ ] 기본 오류 메시지/재시도 UX 제공
- [ ] Docker Compose로 원클릭 실행 가능

---

## 16. 확장 로드맵(선택)

### 16.1 단기(운영 개선)
- SSE 도입으로 트래픽/UX 개선
- rate limit / 중복 제한 강화(단, 로그인 없이 한계 명시)
- Nginx 도입(정적 캐싱, gzip, TLS termination)

### 16.2 중기(제품 확장)
- 여러 투표 주제(복수 poll) 지원
- 공유 링크(특정 pollId), 간단한 관리자 기능(투표 리셋/종료)
- 투표 결과 공유 이미지 생성(소셜 공유 강화)

---

## 17. 리스크 & 대응

- **1인 1표 강제 불가**(로그인 없음): “남용 방지” 수준으로 중복 제한/rate limit 적용
- **실시간 방식 선택**: MVP는 폴링로 단순화, 필요 시 SSE로 업그레이드
- **DB 장애**: 503 처리 + 프론트 에러/재시도 UX로 완충

---

## 18. 최종 산출물 목록

- PRD 문서 (이미 작성됨)
- 상세 기능 명세서 (이미 작성됨)
- 화면 구성 & 사용자 플로우 문서 (이미 작성됨)
- **최종 기획서(본 문서)**
- (개발 산출물) docker-compose.yml, schema.sql, Flask API, 정적 프론트 파일, README

---

## 부록 A. 개발자에게 전달할 “핵심 정의”

- 투표는 `POST /api/v1/votes`로만 처리한다.
- 결과 조회는 `GET /api/v1/results`로만 처리한다.
- 결과는 서버에서 계산/반환하며, 프론트는 렌더링만 담당한다.
- DB는 MySQL에 영속 저장하며, compose volume으로 유지한다.
- 프론트는 loading/empty/success/error 상태를 반드시 가진다.
- 실시간은 최소 폴링으로 제공하고, 필요 시 SSE로 확장한다.
