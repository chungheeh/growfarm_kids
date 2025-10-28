# 시스템 아키텍처 📐

키움밥상(Growing Table) 프로젝트의 전체 시스템 아키텍처 설계 문서입니다.

## 📋 목차

- [시스템 개요](#시스템-개요)
- [아키텍처 다이어그램](#아키텍처-다이어그램)
- [컴포넌트 설명](#컴포넌트-설명)
- [데이터 흐름](#데이터-흐름)
- [보안 구조](#보안-구조)
- [배포 아키텍처](#배포-아키텍처)
- [확장성 및 성능](#확장성-및-성능)

---

## 시스템 개요

### 아키텍처 스타일
- **패턴**: 3-Tier Architecture (Presentation - Business - Data)
- **통신**: RESTful API
- **인증**: OAuth 2.0 + JWT

### 기술 스택 요약

| 계층 | 기술 |
|------|------|
| Frontend | React 18+, TypeScript, TailwindCSS |
| Backend | Python 3.11+, FastAPI |
| Database | PostgreSQL 14+ |
| Authentication | Google OAuth 2.0, JWT |
| External APIs | NAVER CLOVA OCR, Kakao Map API |
| Deployment | Docker, AWS/GCP (예정) |

---

## 아키텍처 다이어그램

### 전체 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Web Browser (React + TypeScript)                  │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │  어린이 UI  │  │  보호자 UI  │  │  지도 뷰   │         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            │ HTTPS/REST API                      │
│                            ▼                                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend Server                       │  │
│  │                                                            │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐     │  │
│  │  │  Auth API   │  │  Meals API   │  │  Store API  │     │  │
│  │  └─────────────┘  └──────────────┘  └─────────────┘     │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐     │  │
│  │  │  Users API  │  │Nutrition API │  │   OCR API   │     │  │
│  │  └─────────────┘  └──────────────┘  └─────────────┘     │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │           Business Logic Layer                    │    │  │
│  │  │  - 영양소 분석  - BMI 계산  - 권장량 비교        │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Data Layer                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              PostgreSQL Database                          │  │
│  │  ┌──────┐  ┌──────────┐  ┌───────┐  ┌───────────┐       │  │
│  │  │Users │  │ Children │  │ Meals │  │ Nutrition │       │  │
│  │  └──────┘  └──────────┘  └───────┘  └───────────┘       │  │
│  │  ┌────────┐                                               │  │
│  │  │ Stores │                                               │  │
│  │  └────────┘                                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      External Services                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Google OAuth    │  │  NAVER CLOVA OCR │  │  Kakao Map   │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 컴포넌트 설명

### Frontend (React + TypeScript)

#### 주요 컴포넌트 구조
```
frontend/
├── src/
│   ├── components/           # 재사용 가능한 UI 컴포넌트
│   │   ├── common/          # 공통 컴포넌트 (Button, Input 등)
│   │   ├── auth/            # 인증 관련 컴포넌트
│   │   ├── meal/            # 식사 기록 컴포넌트
│   │   ├── nutrition/       # 영양 분석 컴포넌트
│   │   ├── growth/          # 성장 기록 컴포넌트
│   │   └── map/             # 지도 컴포넌트
│   ├── pages/               # 페이지 컴포넌트
│   │   ├── LoginPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── MealPage.tsx
│   │   ├── AnalysisPage.tsx
│   │   └── MapPage.tsx
│   ├── hooks/               # Custom React Hooks
│   ├── services/            # API 통신 서비스
│   ├── context/             # React Context (상태 관리)
│   ├── utils/               # 유틸리티 함수
│   └── types/               # TypeScript 타입 정의
```

#### 주요 기능
- **어린이 친화적 UI**: 큰 버튼, 밝은 색상, 직관적 인터페이스
- **반응형 디자인**: 모바일 우선 설계 (TailwindCSS)
- **상태 관리**: React Context API / Zustand (예정)
- **라우팅**: React Router v6

---

### Backend (FastAPI + Python)

#### 프로젝트 구조
```
backend/
├── main.py                  # FastAPI 애플리케이션 엔트리포인트
├── config.py                # 환경 설정
├── database.py              # 데이터베이스 연결
├── models.py                # SQLAlchemy ORM 모델
├── schemas.py               # Pydantic 스키마
├── routers/                 # API 라우터
│   ├── auth.py             # 인증 API
│   ├── users.py            # 사용자 API
│   ├── children.py         # 아동 프로필 API
│   ├── meals.py            # 식사 기록 API
│   ├── nutrition.py        # 영양 분석 API
│   ├── stores.py           # 가맹점 API
│   └── ocr.py              # OCR API
├── services/                # 비즈니스 로직
│   ├── auth_service.py     # 인증 서비스
│   ├── nutrition_service.py # 영양 분석 서비스
│   ├── bmi_service.py      # BMI 계산 서비스
│   └── ocr_service.py      # OCR 서비스
├── utils/                   # 유틸리티 함수
│   ├── jwt.py              # JWT 토큰 관리
│   ├── security.py         # 보안 관련
│   └── validators.py       # 데이터 검증
└── tests/                   # 테스트 코드
```

#### 주요 기능
- **RESTful API**: 표준 REST 원칙 준수
- **자동 문서화**: OpenAPI (Swagger UI)
- **비동기 처리**: async/await 패턴
- **데이터 검증**: Pydantic 모델
- **ORM**: SQLAlchemy 2.0

---

### Database (PostgreSQL)

#### 데이터베이스 설계 원칙
- **정규화**: 제3정규형(3NF) 준수
- **인덱싱**: 자주 조회되는 컬럼에 인덱스
- **외래키**: 참조 무결성 보장
- **트랜잭션**: ACID 속성 보장

자세한 스키마는 [DATABASE.md](./DATABASE.md) 참조

---

## 데이터 흐름

### 1. 사용자 로그인 플로우

```
[브라우저] → [프론트엔드] → [백엔드] → [Google OAuth] → [백엔드] → [DB] → [프론트엔드]

1. 사용자가 "Google 로그인" 버튼 클릭
2. 프론트엔드에서 /auth/google/login 요청
3. 백엔드가 Google OAuth URL로 리디렉션
4. 사용자가 Google에서 인증
5. Google이 인증 코드와 함께 콜백 URL 호출
6. 백엔드가 인증 코드로 Google에서 사용자 정보 가져옴
7. 백엔드가 사용자 정보를 DB에 저장/업데이트
8. 백엔드가 JWT 토큰 생성
9. 프론트엔드에 토큰 반환
10. 프론트엔드가 토큰을 localStorage에 저장
```

### 2. 식사 기록 추가 플로우

```
[사용자 입력] → [프론트엔드] → [백엔드] → [DB]

직접 입력:
1. 사용자가 식사 정보 입력
2. 프론트엔드에서 POST /meals 요청 (+ 영양소 데이터)
3. 백엔드가 JWT 토큰 검증
4. 백엔드가 데이터 유효성 검증
5. 백엔드가 DB에 Meals + Nutrition 레코드 생성
6. 성공 응답 반환

OCR 입력:
1. 사용자가 영양성분표 사진 촬영
2. 프론트엔드에서 POST /ocr/nutrition-label 요청 (이미지)
3. 백엔드가 NAVER CLOVA OCR API 호출
4. OCR 결과를 파싱하여 영양소 데이터 추출
5. 프론트엔드에 추출된 데이터 반환
6. 사용자가 데이터 확인/수정
7. POST /meals 요청으로 저장
```

### 3. 영양 분석 플로우

```
[프론트엔드] → [백엔드] → [DB] → [비즈니스 로직] → [프론트엔드]

1. 프론트엔드에서 GET /nutrition/daily?date=YYYY-MM-DD 요청
2. 백엔드가 해당 날짜의 모든 식사 기록 조회
3. 영양소 합계 계산
4. 연령/성별 기반 권장 섭취량(DRI) 조회
5. 실제 섭취량과 권장량 비교
6. 부족/과다 영양소 분석
7. 개선 제안 생성
8. 프론트엔드에 분석 결과 반환
9. 프론트엔드가 그래프 및 메시지로 시각화
```

---

## 보안 구조

### 1. 인증 및 인가

#### OAuth 2.0 + JWT
```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │ 1. Google Login
       ▼
┌──────────────┐      2. Redirect to Google
│   Backend    ├─────────────────────────────┐
└──────┬───────┘                              │
       │ 4. Get User Info                     │
       │ 5. Generate JWT                      ▼
       ▼                                ┌──────────────┐
┌──────────────┐                       │Google OAuth  │
│  Database    │                       └──────────────┘
└──────────────┘                             │
       ▲                                      │
       │ 6. Save/Update User                 │
       └──────────────────────────────────────┘
                3. Authorization Code
```

#### JWT 토큰 구조
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": 1,
    "email": "user@example.com",
    "user_type": "child",
    "exp": 1737890400
  },
  "signature": "..."
}
```

### 2. API 보안

- **HTTPS**: 모든 통신 암호화
- **CORS**: 허용된 도메인만 접근 가능
- **Rate Limiting**: API 요청 제한 (분당 100회)
- **Input Validation**: Pydantic 스키마로 입력 검증
- **SQL Injection 방지**: SQLAlchemy ORM 사용

### 3. 데이터 보호

- **민감 정보 암호화**: 개인정보 암호화 저장 (예정)
- **환경 변수**: Secret Key 등 환경 변수로 관리
- **GDPR 준수**: 개인정보 처리 방침 준수
- **접근 제어**: 사용자는 본인 데이터만 접근 가능

---

## 배포 아키텍처

### Docker 컨테이너 구조

```
┌─────────────────────────────────────────────────────┐
│                  Docker Compose                      │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   Frontend   │  │   Backend    │  │ PostgreSQL│ │
│  │   (Nginx +   │  │   (FastAPI)  │  │           │ │
│  │    React)    │  │              │  │           │ │
│  │   Port 3000  │  │  Port 8000   │  │ Port 5432 │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│                                                       │
└─────────────────────────────────────────────────────┘
```

### 클라우드 배포 (예정)

```
                    ┌─────────────────┐
                    │   CloudFlare    │
                    │   (CDN + SSL)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Load Balancer  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
  ┌─────▼─────┐        ┌─────▼─────┐       ┌─────▼─────┐
  │  Frontend │        │  Backend  │       │  Backend  │
  │  (Vercel) │        │  (AWS EC2)│       │  (AWS EC2)│
  └───────────┘        └─────┬─────┘       └─────┬─────┘
                             │                    │
                    ┌────────▼────────────────────┘
                    │
              ┌─────▼──────┐         ┌──────────────┐
              │ PostgreSQL │         │  Redis Cache │
              │  (AWS RDS) │         │  (Optional)  │
              └────────────┘         └──────────────┘
```

---

## 확장성 및 성능

### 1. 수평 확장 (Horizontal Scaling)

- **Backend**: 여러 인스턴스 실행 + 로드 밸런서
- **Database**: Read Replica 구성 (읽기 부하 분산)
- **Caching**: Redis를 통한 자주 조회되는 데이터 캐싱

### 2. 성능 최적화

#### 프론트엔드
- Code Splitting (React.lazy)
- Image Optimization (WebP, lazy loading)
- Bundle Size 최소화

#### 백엔드
- Database Connection Pooling
- Query Optimization (인덱스 활용)
- 비동기 처리 (async/await)
- API Response Caching

#### 데이터베이스
- 인덱스 최적화
- 파티셔닝 (날짜별)
- Query 성능 모니터링

### 3. 모니터링 및 로깅

- **Application Monitoring**: Sentry (에러 추적)
- **Performance Monitoring**: New Relic / DataDog (예정)
- **Logging**: 구조화된 JSON 로그 (Python logging)
- **Health Check**: /health 엔드포인트

---

## 개발 및 배포 프로세스

### CI/CD 파이프라인 (예정)

```
[GitHub Push]
     │
     ▼
[GitHub Actions]
     │
     ├─ Run Tests
     ├─ Linting
     ├─ Build Docker Images
     │
     ▼
[Staging Environment]
     │
     ├─ Integration Tests
     ├─ Manual QA
     │
     ▼
[Production Deployment]
     │
     └─ Health Check
```

### 환경 분리

- **Development**: 로컬 개발 환경
- **Staging**: 테스트 환경 (프로덕션과 동일한 구성)
- **Production**: 실제 서비스 환경

---

## 참고 자료

- [SETUP.md](./SETUP.md) - 개발 환경 설정
- [API.md](./API.md) - API 문서
- [DATABASE.md](./DATABASE.md) - 데이터베이스 스키마

---

아키텍처에 대한 질문이나 개선 제안은 [GitHub Issues](https://github.com/chungheeh/growfarm_kids/issues)에 등록해주세요.
