# 🍜 짜장면 vs 짬뽕 투표 웹페이지

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)

Flask + MySQL + Docker Compose 기반 실시간 투표 서비스

## 📋 프로젝트 개요

사용자가 **짜장면**과 **짬뽕** 중 하나를 선택해 투표하고, 현재까지의 결과를 **실시간**으로 확인할 수 있는 웹 서비스입니다.

### 주요 특징
- 🔄 **실시간 업데이트**: 3초마다 자동으로 결과 갱신
- 💾 **영속성 보장**: MySQL에 데이터 저장, 재시작 후에도 유지
- 📱 **반응형 디자인**: 모바일/데스크톱 모두 지원
- 🐳 **쉬운 배포**: Docker Compose로 원클릭 실행
- 🔌 **RESTful API**: 프론트엔드와 백엔드 분리

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Flask (Python 3.11), Gunicorn |
| **Database** | MySQL 8.0 |
| **Infrastructure** | Docker, Docker Compose |
| **API** | RESTful API |

## 📁 프로젝트 구조

```
vibe-coding-test/
├── docker-compose.yml          # Docker Compose 설정
├── .env                         # 환경 변수
├── docker/
│   └── mysql/
│       └── init/
│           ├── 01-schema.sql   # DB 스키마
│           └── 02-seed.sql     # 초기 데이터
├── backend/                     # Flask 애플리케이션
│   ├── app.py                  # Flask 메인 앱
│   ├── config.py               # 설정
│   ├── db.py                   # DB 연결
│   ├── requirements.txt        # Python 패키지
│   ├── Dockerfile              # Backend 이미지
│   ├── services/
│   │   └── poll_service.py     # 투표 비즈니스 로직
│   └── utils/
│       └── responses.py        # API 응답 유틸
└── frontend/                    # 정적 파일
    ├── index.html              # 메인 페이지
    ├── styles.css              # 스타일
    └── app.js                  # 프론트 로직
```

## 🚀 빠른 시작 (Quick Start)

### 사전 요구사항

시작하기 전에 다음 프로그램이 설치되어 있어야 합니다:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Docker Engine + Docker Compose 포함)

> **💡 Tip**: Docker Desktop을 설치하면 Docker와 Docker Compose가 함께 설치됩니다.

### 1️⃣ 프로젝트 클론

터미널을 열고 다음 명령어를 실행하세요:

```bash
# 저장소 클론
git clone https://github.com/lee-giho/vibe-coding-test.git

# 프로젝트 디렉토리로 이동
cd vibe-coding-test
```

### 2️⃣ 환경 변수 설정 (선택사항)

`.env` 파일이 이미 생성되어 있으므로 **바로 실행 가능**합니다.  
필요하다면 비밀번호를 변경할 수 있습니다:

```bash
# .env 파일 편집 (선택)
nano .env
# 또는
vim .env
```

기본 설정:
```env
MYSQL_DATABASE=poll_db
MYSQL_USER=poll_user
MYSQL_PASSWORD=poll_password_2025
MYSQL_ROOT_PASSWORD=root_password_2025
APP_PORT=5001
FLASK_ENV=development
```

### 3️⃣ Docker Compose 실행

**한 번의 명령어로 전체 시스템을 실행**할 수 있습니다:

```bash
# 백그라운드에서 모든 서비스 실행
docker-compose up -d
```

**출력 예시:**
```
[+] Running 4/4
 ✔ Network vibe-coding-test_poll_network  Created
 ✔ Volume "vibe-coding-test_mysql_data"   Created
 ✔ Container poll_mysql                   Healthy
 ✔ Container poll_api                     Started
```

> **⏱ 소요 시간**: 최초 실행 시 Docker 이미지 다운로드 및 빌드로 약 2-3분 소요됩니다.

### 4️⃣ 실행 확인

#### 컨테이너 상태 확인
```bash
docker-compose ps
```

**정상 실행 시 출력:**
```
NAME         IMAGE                  STATUS         PORTS
poll_api     vibe-coding-test-api   Up 10 seconds  0.0.0.0:5001->5000/tcp
poll_mysql   mysql:8.0              Up 10 seconds  0.0.0.0:3306->3306/tcp
```

#### 로그 확인
```bash
# 전체 로그 확인
docker-compose logs

# 실시간 로그 확인
docker-compose logs -f

# 특정 서비스만 확인
docker-compose logs api
docker-compose logs mysql
```

### 5️⃣ 웹 브라우저에서 접속

브라우저를 열고 다음 주소로 접속하세요:

```
http://localhost:5001
```

**🎉 성공!** 짜장면 vs 짬뽕 투표 페이지가 표시됩니다.

---

## 🖥️ 사용 방법

### 웹 페이지 사용

1. **브라우저 접속**: `http://localhost:5001`
2. **투표하기**: 짜장면 또는 짬뽕 버튼 클릭
3. **결과 확인**: 실시간으로 업데이트되는 득표 현황 확인
4. **여러 번 투표**: 새로고침하거나 다른 브라우저에서도 투표 가능

### API 직접 호출

#### 헬스체크
```bash
curl http://localhost:5001/api/v1/health
```

#### 현재 결과 조회
```bash
curl "http://localhost:5001/api/v1/results?pollId=1"
```

#### 투표하기 (짜장면)
```bash
curl -X POST "http://localhost:5001/api/v1/votes" \
  -H "Content-Type: application/json" \
  -d '{"pollId":1,"optionId":1}'
```

#### 투표하기 (짬뽕)
```bash
curl -X POST "http://localhost:5001/api/v1/votes" \
  -H "Content-Type: application/json" \
  -d '{"pollId":1,"optionId":2}'
```

---

## 🛑 서비스 중지 및 삭제

### 컨테이너 중지
```bash
docker-compose stop
```

### 컨테이너 중지 및 삭제
```bash
docker-compose down
```

### 데이터베이스 포함 완전 삭제
```bash
# ⚠️ 주의: 모든 투표 데이터가 삭제됩니다!
docker-compose down -v
```

### 재시작
```bash
# 중지 후 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart api
```

---

## 🔧 문제 해결 (Troubleshooting)

### 포트 충돌 오류

**오류 메시지:**
```
Error: bind: address already in use
```

**해결 방법 1**: 다른 포트 사용
```bash
# .env 파일에서 APP_PORT 변경
# APP_PORT=5001 -> APP_PORT=8080
```

**해결 방법 2**: 기존 프로세스 종료
```bash
# 5001 포트 사용 중인 프로세스 확인
lsof -ti:5001

# 프로세스 종료
kill -9 $(lsof -ti:5001)
```

### Docker가 실행되지 않음

**오류 메시지:**
```
Cannot connect to the Docker daemon
```

**해결 방법:**
1. Docker Desktop 실행
2. Docker Desktop이 완전히 시작될 때까지 대기 (상태 표시줄 확인)
3. 다시 시도

### 데이터베이스 연결 실패

**해결 방법:**
```bash
# MySQL 컨테이너 상태 확인
docker-compose logs mysql

# 컨테이너 재시작
docker-compose restart mysql api
```

### 데이터 초기화

```bash
# 1. 모든 컨테이너 및 볼륨 삭제
docker-compose down -v

# 2. 다시 시작
docker-compose up -d
```

---

## 📡 API 문서

### Base URL
```
http://localhost:5001/api/v1
```

### 엔드포인트 목록

#### 1. 헬스체크
서버와 데이터베이스 상태를 확인합니다.

**요청:**
```http
GET /api/v1/health
```

**응답 (성공):**
```json
{
  "success": true,
  "data": {
    "status": "ok",
    "db": "ok"
  },
  "error": null
}
```

#### 2. 투표 결과 조회
현재 투표 결과를 조회합니다.

**요청:**
```http
GET /api/v1/results?pollId=1
```

**쿼리 파라미터:**
- `pollId` (required): 투표 ID (현재는 1 고정)

**응답 (성공):**
```json
{
  "success": true,
  "data": {
    "pollId": 1,
    "title": "짜장면 vs 짬뽕",
    "totalVotes": 15,
    "options": [
      {
        "optionId": 1,
        "label": "짜장면",
        "count": 10,
        "percent": 66.67
      },
      {
        "optionId": 2,
        "label": "짬뽕",
        "count": 5,
        "percent": 33.33
      }
    ],
    "updatedAt": "2025-12-30T14:00:00+09:00"
  },
  "error": null
}
```

**응답 (빈 상태):**
```json
{
  "success": true,
  "data": {
    "pollId": 1,
    "title": "짜장면 vs 짬뽕",
    "totalVotes": 0,
    "options": [
      {
        "optionId": 1,
        "label": "짜장면",
        "count": 0,
        "percent": 0.0
      },
      {
        "optionId": 2,
        "label": "짬뽕",
        "count": 0,
        "percent": 0.0
      }
    ],
    "updatedAt": "2025-12-30T14:00:00+09:00"
  },
  "error": null
}
```

#### 3. 투표 제출
새로운 투표를 제출합니다.

**요청:**
```http
POST /api/v1/votes
Content-Type: application/json

{
  "pollId": 1,
  "optionId": 1
}
```

**요청 본문:**
- `pollId` (required): 투표 ID (현재는 1)
- `optionId` (required): 선택한 옵션 ID (1: 짜장면, 2: 짬뽕)

**응답 (성공):**
```json
{
  "success": true,
  "data": {
    "pollId": 1,
    "optionId": 1,
    "results": {
      "pollId": 1,
      "title": "짜장면 vs 짬뽕",
      "totalVotes": 16,
      "options": [
        {
          "optionId": 1,
          "label": "짜장면",
          "count": 11,
          "percent": 68.75
        },
        {
          "optionId": 2,
          "label": "짬뽕",
          "count": 5,
          "percent": 31.25
        }
      ],
      "updatedAt": "2025-12-30T14:01:00+09:00"
    }
  },
  "error": null
}
```

**에러 응답 예시:**
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "optionId is required",
    "details": {
      "field": "optionId"
    }
  }
}
```

### 에러 코드
| 코드 | 설명 |
|------|------|
| `VALIDATION_ERROR` | 요청 파라미터 검증 실패 |
| `NOT_FOUND` | 투표 또는 옵션을 찾을 수 없음 |
| `POLL_INACTIVE` | 비활성화된 투표 |
| `DB_UNAVAILABLE` | 데이터베이스 연결 실패 |
| `INTERNAL_ERROR` | 서버 내부 오류 |

---

## 🧪 테스트

### curl로 API 테스트

#### 전체 플로우 테스트
```bash
# 1. 헬스체크
curl http://localhost:5001/api/v1/health

# 2. 현재 결과 확인
curl "http://localhost:5001/api/v1/results?pollId=1"

# 3. 짜장면에 투표
curl -X POST "http://localhost:5001/api/v1/votes" \
  -H "Content-Type: application/json" \
  -d '{"pollId":1,"optionId":1}'

# 4. 짬뽕에 투표
curl -X POST "http://localhost:5001/api/v1/votes" \
  -H "Content-Type: application/json" \
  -d '{"pollId":1,"optionId":2}'

# 5. 결과 다시 확인
curl "http://localhost:5001/api/v1/results?pollId=1"
```

#### 여러 번 투표하기 (반복 테스트)
```bash
# 짜장면에 10번 투표
for i in {1..10}; do
  curl -X POST "http://localhost:5001/api/v1/votes" \
    -H "Content-Type: application/json" \
    -d '{"pollId":1,"optionId":1}' \
    -s > /dev/null
  echo "투표 $i 완료"
done

# 결과 확인
curl "http://localhost:5001/api/v1/results?pollId=1"
```

### MySQL 직접 접속

데이터베이스에 직접 접속하여 데이터를 확인할 수 있습니다.

#### MySQL 컨테이너 접속
```bash
docker-compose exec mysql mysql -u poll_user -ppoll_password_2025 poll_db
```

#### SQL 쿼리 실행
```sql
-- 모든 테이블 확인
SHOW TABLES;

-- 투표 주제 확인
SELECT * FROM polls;

-- 옵션 및 득표수 확인
SELECT * FROM options;

-- 투표 로그 확인 (최근 10개)
SELECT * FROM votes ORDER BY created_at DESC LIMIT 10;

-- 득표수 집계 확인
SELECT 
    o.label as '선택지',
    o.vote_count as '득표수',
    COUNT(v.id) as '실제_투표수'
FROM options o
LEFT JOIN votes v ON o.id = v.option_id
WHERE o.poll_id = 1
GROUP BY o.id, o.label, o.vote_count;
```

#### MySQL 쉘에서 나가기
```sql
exit;
```

#### 원라이너로 SQL 실행
```bash
# 현재 득표 현황 확인
docker-compose exec mysql mysql -u poll_user -ppoll_password_2025 poll_db \
  -e "SELECT label, vote_count FROM options WHERE poll_id=1;"

# 총 투표수 확인
docker-compose exec mysql mysql -u poll_user -ppoll_password_2025 poll_db \
  -e "SELECT COUNT(*) as total_votes FROM votes;"
```

---

## 🛑 서비스 중지 및 삭제

### 서비스 관리 명령어

#### 컨테이너 중지
서비스를 중지하되 컨테이너는 유지합니다.
```bash
docker-compose stop
```

#### 컨테이너 재시작
```bash
# 모든 서비스 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart api
docker-compose restart mysql
```

#### 컨테이너 중지 및 삭제
컨테이너를 삭제하지만 데이터(볼륨)는 유지합니다.
```bash
docker-compose down
```

#### 데이터 포함 완전 삭제
```bash
# ⚠️ 주의: 모든 투표 데이터가 영구적으로 삭제됩니다!
docker-compose down -v
```

#### 이미지까지 모두 삭제
```bash
# 컨테이너, 볼륨, 이미지 모두 삭제
docker-compose down -v --rmi all
```

### 재시작 플로우
```bash
# 1. 모든 것을 삭제하고
docker-compose down -v

# 2. 다시 시작 (새로 빌드)
docker-compose up -d --build

# 3. 로그 확인
docker-compose logs -f
```

---

## 🔧 문제 해결 (Troubleshooting)

### 1. 포트 충돌 오류

**증상:**
```
Error: bind: address already in use
```

**원인:** 5001 포트를 다른 프로그램이 사용 중

**해결 방법 A - 포트 변경:**
```bash
# .env 파일 수정
sed -i '' 's/APP_PORT=5001/APP_PORT=8080/g' .env

# 재시작
docker-compose down
docker-compose up -d
```

**해결 방법 B - 기존 프로세스 종료:**
```bash
# macOS/Linux
lsof -ti:5001 | xargs kill -9

# 다시 시도
docker-compose up -d
```

### 2. Docker가 실행되지 않음

**증상:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**해결 방법:**
1. Docker Desktop을 실행합니다
2. Docker Desktop 아이콘이 초록색이 될 때까지 대기
3. 터미널에서 다시 시도:
```bash
docker ps
docker-compose up -d
```

### 3. 데이터베이스 연결 실패

**증상:**
- API 접속 시 503 에러
- "database unavailable" 메시지

**해결 방법:**
```bash
# 1. MySQL 로그 확인
docker-compose logs mysql

# 2. MySQL 컨테이너 상태 확인
docker-compose ps mysql

# 3. 서비스 재시작
docker-compose restart mysql
sleep 5  # MySQL 시작 대기
docker-compose restart api

# 4. 헬스체크
curl http://localhost:5001/api/v1/health
```

### 4. 웹 페이지가 로드되지 않음

**확인 사항:**

1. **컨테이너 실행 확인:**
```bash
docker-compose ps
```
모든 서비스가 "Up" 상태여야 합니다.

2. **API 서버 로그 확인:**
```bash
docker-compose logs api
```

3. **API 직접 테스트:**
```bash
curl http://localhost:5001/api/v1/health
```

4. **브라우저 캐시 삭제:**
- `Ctrl+Shift+R` (Windows/Linux)
- `Cmd+Shift+R` (macOS)

### 5. 데이터 초기화 필요 시

**전체 데이터 초기화:**
```bash
# 1. 모든 컨테이너와 데이터 삭제
docker-compose down -v

# 2. 이미지도 삭제 (선택)
docker-compose down -v --rmi all

# 3. 처음부터 다시 시작
docker-compose up -d --build

# 4. 로그 확인
docker-compose logs -f
```

### 6. 빌드 오류 발생 시

**증상:**
```
ERROR: failed to solve...
```

**해결 방법:**
```bash
# 1. 빌드 캐시 삭제
docker builder prune -a

# 2. 다시 빌드
docker-compose build --no-cache

# 3. 실행
docker-compose up -d
```

### 7. 로그 확인 방법

```bash
# 모든 로그 (한 번)
docker-compose logs

# 실시간 로그 (계속 출력)
docker-compose logs -f

# 최근 50줄만 확인
docker-compose logs --tail=50

# 특정 서비스만
docker-compose logs api
docker-compose logs mysql

# 타임스탬프 포함
docker-compose logs -t
```

---

## ✨ 주요 기능

### 사용자 기능
- ✅ **원클릭 투표**: 버튼 클릭 한 번으로 즉시 투표
- ✅ **실시간 업데이트**: 3초마다 자동으로 결과 갱신
- ✅ **반응형 디자인**: 모바일/태블릿/데스크톱 모든 기기 지원
- ✅ **시각적 결과**: 프로그레스 바와 퍼센트로 직관적 표시
- ✅ **상태 표시**: LIVE/OFFLINE 상태 실시간 확인

### 기술적 특징
- ✅ **데이터 영속성**: MySQL 볼륨으로 재시작 후에도 데이터 유지
- ✅ **트랜잭션 보장**: 투표 데이터의 정합성 보장
- ✅ **에러 처리**: 네트워크 오류 시 자동 재시도
- ✅ **RESTful API**: 표준 HTTP 메서드와 상태 코드 사용
- ✅ **Docker 기반**: 환경 독립적인 배포

---

## 📱 화면 구성

### 1. Header (헤더)
- 서비스 타이틀: "오늘 뭐 먹지?"
- 서브 타이틀: "짜장면 vs 짬뽕, 당신의 선택은?"
- 상태 배지: `LIVE` (정상) / `OFFLINE` (오류) / `UPDATING...` (투표 중)

### 2. Vote Section (투표 영역)
두 개의 선택 카드로 구성:
- **짜장면 카드** 🍜
  - 이모지
  - 선택지 이름
  - "달달한 짜장!" 설명
  - "이걸로 투표" 버튼
- **짬뽕 카드** 🍲
  - 이모지
  - 선택지 이름
  - "칼칼한 짬뽕!" 설명
  - "이걸로 투표" 버튼

### 3. Results Section (결과 영역)
- 총 투표수 표시
- 각 선택지별:
  - 득표수 (예: 10표)
  - 득표율 (예: 66.67%)
  - 프로그레스 바 (시각적 표현)
- 마지막 업데이트 시간

### 4. 상태별 화면

#### Loading (로딩 중)
- 스피너 애니메이션
- "결과를 불러오는 중..." 메시지

#### Empty (빈 상태)
- "🎉 첫 투표를 해보세요!" 메시지
- 투표 버튼 활성화

#### Success (정상)
- 투표 카드와 결과 모두 표시
- 실시간 업데이트 진행

#### Error (오류)
- "😥 오류가 발생했습니다" 메시지
- 오류 내용 표시
- "다시 시도" 버튼

---

## 🔧 개발 정보

### 프로젝트 구조
```
vibe-coding-test/
├── 📄 docker-compose.yml          # Docker Compose 설정
├── 📄 .env                         # 환경 변수
├── 📄 .gitignore                   # Git 제외 파일
├── 📄 README.md                    # 프로젝트 문서
├── 📁 docker/                      # Docker 관련 파일
│   └── 📁 mysql/
│       └── 📁 init/
│           ├── 📄 01-schema.sql   # DB 스키마 정의
│           └── 📄 02-seed.sql     # 초기 데이터
├── 📁 backend/                     # Flask 애플리케이션
│   ├── 📄 app.py                  # Flask 메인 앱 & 라우트
│   ├── 📄 config.py               # 환경설정
│   ├── 📄 db.py                   # MySQL 연결 관리
│   ├── 📄 requirements.txt        # Python 패키지 목록
│   ├── 📄 Dockerfile              # Backend 이미지 빌드
│   ├── 📁 services/
│   │   └── 📄 poll_service.py     # 투표 비즈니스 로직
│   └── 📁 utils/
│       └── 📄 responses.py        # 표준 API 응답
└── 📁 frontend/                    # 정적 파일
    ├── 📄 index.html              # 메인 HTML
    ├── 📄 styles.css              # CSS 스타일
    └── 📄 app.js                  # JavaScript 로직
```

### 데이터베이스 스키마

#### polls (투표 주제)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INT (PK) | 투표 ID |
| title | VARCHAR(100) | 투표 제목 |
| is_active | TINYINT(1) | 활성 여부 |
| created_at | DATETIME | 생성 시각 |

#### options (선택지)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INT (PK) | 옵션 ID |
| poll_id | INT (FK) | 투표 ID |
| label | VARCHAR(50) | 선택지 이름 |
| vote_count | INT | 득표수 (캐시) |
| created_at | DATETIME | 생성 시각 |

#### votes (투표 로그)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | BIGINT (PK) | 투표 로그 ID |
| poll_id | INT (FK) | 투표 ID |
| option_id | INT (FK) | 선택한 옵션 ID |
| client_hash | CHAR(64) | 클라이언트 해시 |
| created_at | DATETIME | 투표 시각 |

### 백엔드 구조

#### app.py
- Flask 애플리케이션 초기화
- 라우트 정의 (/, /api/v1/*)
- 정적 파일 서빙
- CORS 설정

#### db.py
- MySQL 연결 생성 및 관리
- 컨텍스트 매니저로 안전한 연결 처리
- 헬스체크 기능

#### services/poll_service.py
- `get_results()`: 투표 결과 조회 및 퍼센트 계산
- `submit_vote()`: 투표 제출 (트랜잭션 처리)
  - 투표 로그 삽입 (votes)
  - 옵션 카운트 증가 (options.vote_count)

#### utils/responses.py
- 표준 API 응답 형식
- 에러 응답 생성

### 프론트엔드 구조

#### index.html
- 시맨틱 HTML5
- 상태별 UI 컨테이너
- 투표 카드 및 결과 영역

#### styles.css
- CSS 변수로 테마 관리
- 모바일 우선 반응형 디자인
- Flexbox & Grid 레이아웃
- 애니메이션 (스피너, 프로그레스 바)

#### app.js
- **상태 관리**: loading/empty/success/error
- **API 통신**: fetch API 사용
- **폴링**: 3초 간격 자동 업데이트
- **이벤트 처리**: 투표 버튼 클릭, 재시도
- **탭 최적화**: visibilitychange 이벤트로 폴링 제어

---

## 🚀 향후 개발 계획

### v2.0 (예정)
- [ ] SSE (Server-Sent Events)로 실시간 업데이트 개선
- [ ] 여러 투표 주제 지원
- [ ] 투표 생성 기능
- [ ] 관리자 페이지

### v2.1 (예정)
- [ ] 사용자 인증 (로그인)
- [ ] 1인 1표 제한
- [ ] Rate Limiting
- [ ] 투표 결과 공유 기능

### v2.2 (예정)
- [ ] Nginx 리버스 프록시
- [ ] Redis 캐싱
- [ ] 투표 히스토리
- [ ] 통계 대시보드

---

## � 개발 팁

### 로컬 개발 환경 설정

#### Python 가상환경으로 개발 (선택)
Docker 없이 로컬에서 개발하려면:

```bash
# MySQL만 Docker로 실행
docker-compose up -d mysql

# Python 가상환경 생성
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# Flask 개발 서버 실행
python app.py

# 새 터미널에서 프론트엔드 확인
# http://localhost:5000
```

#### 코드 변경 시 자동 재시작

**방법 1: Docker Compose 개발 모드**
```bash
# docker-compose.yml에 볼륨 마운트 추가 (이미 설정됨)
# 코드 변경 시 자동 반영
docker-compose up
```

**방법 2: Flask 디버그 모드**
```bash
# .env 파일에서
FLASK_ENV=development  # 이미 설정됨

# Flask는 파일 변경 시 자동으로 재시작됩니다
```

### 디버깅

#### 컨테이너 내부 접속
```bash
# API 컨테이너
docker-compose exec api bash

# MySQL 컨테이너
docker-compose exec mysql bash
```

#### Python 디버거 사용
```python
# backend/app.py에 추가
import pdb; pdb.set_trace()
```

#### 로그 레벨 조정
```python
# backend/app.py에서
logging.basicConfig(level=logging.DEBUG)
```

---

## 🤝 기여하기 (Contributing)

기여를 환영합니다! 다음 절차를 따라주세요:

### 1. Fork & Clone
```bash
# 1. GitHub에서 Fork 버튼 클릭

# 2. 본인의 저장소를 클론
git clone https://github.com/your-username/vibe-coding-test.git
cd vibe-coding-test

# 3. 원본 저장소를 upstream으로 추가
git remote add upstream https://github.com/lee-giho/vibe-coding-test.git
```

### 2. 브랜치 생성
```bash
# 기능별로 브랜치 생성
git checkout -b feature/amazing-feature

# 또는 버그 수정
git checkout -b fix/bug-description
```

### 3. 개발 및 테스트
```bash
# 코드 작성

# 로컬에서 테스트
docker-compose up -d
curl http://localhost:5001/api/v1/health

# 커밋
git add .
git commit -m "feat: Add amazing feature"
```

### 4. Push & Pull Request
```bash
# 브랜치 푸시
git push origin feature/amazing-feature

# GitHub에서 Pull Request 생성
```

### 커밋 메시지 컨벤션
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 코드
chore: 빌드/설정 변경
```

---

## 📞 문의 및 지원

### 이슈 제기
버그나 기능 요청은 [GitHub Issues](https://github.com/lee-giho/vibe-coding-test/issues)에 등록해주세요.

### 질문하기
- **버그 리포트**: [Bug Report Template](https://github.com/lee-giho/vibe-coding-test/issues/new?template=bug_report.md)
- **기능 요청**: [Feature Request Template](https://github.com/lee-giho/vibe-coding-test/issues/new?template=feature_request.md)

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자유롭게 사용, 수정, 배포할 수 있습니다.

```
MIT License

Copyright (c) 2025 lee-giho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트들을 사용합니다:
- [Flask](https://flask.palletsprojects.com/) - 웹 프레임워크
- [MySQL](https://www.mysql.com/) - 데이터베이스
- [Docker](https://www.docker.com/) - 컨테이너화
- [PyMySQL](https://github.com/PyMySQL/PyMySQL) - MySQL 드라이버

---

## 📚 참고 자료

- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [MySQL 8.0 문서](https://dev.mysql.com/doc/refman/8.0/en/)
- [Docker Compose 문서](https://docs.docker.com/compose/)
- [RESTful API 설계 가이드](https://restfulapi.net/)

---

<div align="center">

**Made with ❤️ by [lee-giho](https://github.com/lee-giho)**

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!

</div>
```
