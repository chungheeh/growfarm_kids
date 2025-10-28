# API 문서 📡

키움밥상(Growing Table) 프로젝트의 REST API 엔드포인트 문서입니다.

## 📋 목차

- [개요](#개요)
- [인증](#인증)
- [API 엔드포인트](#api-엔드포인트)
  - [인증 (Authentication)](#인증-authentication)
  - [사용자 (Users)](#사용자-users)
  - [아동 프로필 (Child Profiles)](#아동-프로필-child-profiles)
  - [식사 기록 (Meals)](#식사-기록-meals)
  - [영양 분석 (Nutrition)](#영양-분석-nutrition)
  - [가맹점 (Stores)](#가맹점-stores)
  - [OCR](#ocr)
- [에러 코드](#에러-코드)

---

## 개요

### Base URL
```
http://localhost:8000
```

### Content Type
모든 요청과 응답은 `application/json` 형식입니다.

### API 문서
FastAPI 자동 생성 문서:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 인증

### JWT 토큰 인증

대부분의 API는 JWT 토큰 인증이 필요합니다.

#### 헤더 형식
```http
Authorization: Bearer <access_token>
```

#### 토큰 만료
- Access Token: 30분 (기본값)

---

## API 엔드포인트

### 인증 (Authentication)

#### 1. Google OAuth 로그인 시작
Google OAuth 로그인 페이지로 리디렉션합니다.

```http
GET /auth/google/login
```

**Response**: 302 Redirect to Google OAuth

---

#### 2. Google OAuth 콜백
Google OAuth 인증 후 콜백을 처리합니다.

```http
POST /auth/google/callback
```

**Request Body**:
```json
{
  "code": "google-authorization-code"
}
```

**Response**: 200 OK
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "user_id": 1,
    "email": "user@example.com",
    "name": "홍길동",
    "user_type": "child",
    "profile_picture": "https://...",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

---

#### 3. 로그아웃
현재 세션을 종료합니다.

```http
POST /auth/logout
```

**Headers**: `Authorization: Bearer <token>`

**Response**: 200 OK
```json
{
  "message": "로그아웃 성공"
}
```

---

### 사용자 (Users)

#### 1. 내 프로필 조회
현재 로그인한 사용자의 프로필을 조회합니다.

```http
GET /users/me
```

**Headers**: `Authorization: Bearer <token>`

**Response**: 200 OK
```json
{
  "user_id": 1,
  "email": "child@example.com",
  "name": "김어린이",
  "user_type": "child",
  "birth_date": "2015-05-20",
  "gender": "male",
  "profile_picture": "https://...",
  "created_at": "2025-01-15T10:30:00Z",
  "child_profile": {
    "child_id": 1,
    "user_id": 1,
    "guardian_id": 2,
    "height": 145.5,
    "weight": 38.2,
    "bmi": 18.1,
    "last_updated": "2025-01-20T09:00:00Z"
  }
}
```

---

#### 2. 사용자 정보 수정
사용자 기본 정보를 수정합니다.

```http
PATCH /users/me
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "name": "김어린이",
  "birth_date": "2015-05-20",
  "gender": "male"
}
```

**Response**: 200 OK
```json
{
  "user_id": 1,
  "email": "child@example.com",
  "name": "김어린이",
  "user_type": "child",
  "birth_date": "2015-05-20",
  "gender": "male",
  "profile_picture": "https://...",
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

### 아동 프로필 (Child Profiles)

#### 1. 아동 프로필 생성
새로운 아동 프로필을 생성합니다 (아동 사용자만).

```http
POST /children/profile
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "height": 145.5,
  "weight": 38.2,
  "guardian_id": 2
}
```

**Response**: 201 Created
```json
{
  "child_id": 1,
  "user_id": 1,
  "guardian_id": 2,
  "height": 145.5,
  "weight": 38.2,
  "bmi": 18.1,
  "last_updated": "2025-01-20T09:00:00Z"
}
```

---

#### 2. 아동 프로필 수정 (키/몸무게 업데이트)
아동의 키와 몸무게를 업데이트합니다.

```http
PATCH /children/profile
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "height": 146.0,
  "weight": 38.5
}
```

**Response**: 200 OK
```json
{
  "child_id": 1,
  "user_id": 1,
  "guardian_id": 2,
  "height": 146.0,
  "weight": 38.5,
  "bmi": 18.1,
  "last_updated": "2025-01-25T10:00:00Z"
}
```

---

#### 3. BMI 백분위수 조회
아동의 BMI 백분위수와 성장 상태를 조회합니다.

```http
GET /children/bmi
```

**Headers**: `Authorization: Bearer <token>`

**Response**: 200 OK
```json
{
  "bmi": 18.1,
  "percentile": 65.3,
  "status": "정상",
  "comparison": {
    "average_bmi": 17.8,
    "message": "또래 평균보다 약간 높아요"
  }
}
```

---

### 식사 기록 (Meals)

#### 1. 식사 기록 추가
새로운 식사를 기록합니다.

```http
POST /meals
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "meal_type": "lunch",
  "meal_date": "2025-01-20",
  "meal_time": "2025-01-20T12:30:00Z",
  "nutrition": {
    "calories": 650,
    "carbohydrates": 85.5,
    "protein": 25.3,
    "fat": 18.2,
    "sodium": 950,
    "sugar": 12.5,
    "fiber": 8.0
  }
}
```

**Response**: 201 Created
```json
{
  "meal_id": 123,
  "child_id": 1,
  "meal_type": "lunch",
  "meal_date": "2025-01-20",
  "meal_time": "2025-01-20T12:30:00Z",
  "created_at": "2025-01-20T12:35:00Z",
  "nutrition": {
    "nutrition_id": 456,
    "meal_id": 123,
    "calories": 650,
    "carbohydrates": 85.5,
    "protein": 25.3,
    "fat": 18.2,
    "sodium": 950,
    "sugar": 12.5,
    "fiber": 8.0
  }
}
```

---

#### 2. 식사 기록 목록 조회
특정 기간의 식사 기록을 조회합니다.

```http
GET /meals?start_date=2025-01-01&end_date=2025-01-31
```

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `start_date` (optional): 시작 날짜 (YYYY-MM-DD)
- `end_date` (optional): 종료 날짜 (YYYY-MM-DD)
- `meal_type` (optional): 식사 유형 (breakfast, lunch, dinner, snack)

**Response**: 200 OK
```json
{
  "total": 45,
  "meals": [
    {
      "meal_id": 123,
      "meal_type": "lunch",
      "meal_date": "2025-01-20",
      "meal_time": "2025-01-20T12:30:00Z",
      "nutrition": {
        "calories": 650,
        "carbohydrates": 85.5,
        "protein": 25.3,
        "fat": 18.2
      }
    }
  ]
}
```

---

#### 3. 식사 기록 상세 조회
특정 식사의 상세 정보를 조회합니다.

```http
GET /meals/{meal_id}
```

**Headers**: `Authorization: Bearer <token>`

**Response**: 200 OK
```json
{
  "meal_id": 123,
  "child_id": 1,
  "meal_type": "lunch",
  "meal_date": "2025-01-20",
  "meal_time": "2025-01-20T12:30:00Z",
  "created_at": "2025-01-20T12:35:00Z",
  "nutrition": {
    "nutrition_id": 456,
    "calories": 650,
    "carbohydrates": 85.5,
    "protein": 25.3,
    "fat": 18.2,
    "sodium": 950,
    "sugar": 12.5,
    "fiber": 8.0
  }
}
```

---

#### 4. 식사 기록 삭제
식사 기록을 삭제합니다.

```http
DELETE /meals/{meal_id}
```

**Headers**: `Authorization: Bearer <token>`

**Response**: 204 No Content

---

### 영양 분석 (Nutrition)

#### 1. 일일 영양소 분석
특정 날짜의 영양소 섭취 현황을 분석합니다.

```http
GET /nutrition/daily?date=2025-01-20
```

**Headers**: `Authorization: Bearer <token>`

**Response**: 200 OK
```json
{
  "date": "2025-01-20",
  "total_nutrition": {
    "calories": 1850,
    "carbohydrates": 245.5,
    "protein": 68.3,
    "fat": 52.8,
    "sodium": 2100,
    "sugar": 35.2,
    "fiber": 18.5
  },
  "recommended": {
    "calories": 2000,
    "carbohydrates": 300,
    "protein": 60,
    "fat": 55,
    "sodium": 2000,
    "sugar": 50,
    "fiber": 25
  },
  "percentage": {
    "calories": 92.5,
    "carbohydrates": 81.8,
    "protein": 113.8,
    "fat": 96.0,
    "sodium": 105.0,
    "sugar": 70.4,
    "fiber": 74.0
  },
  "status": {
    "calories": "적정",
    "protein": "충분",
    "sodium": "주의",
    "fiber": "부족"
  },
  "recommendations": [
    "나트륨 섭취가 권장량을 초과했어요. 짠 음식을 줄여보세요.",
    "식이섬유가 부족해요. 채소나 과일을 더 먹으면 좋아요."
  ]
}
```

---

#### 2. 주간 영양소 추이
주간 영양소 섭취 추이를 조회합니다.

```http
GET /nutrition/weekly?start_date=2025-01-13
```

**Headers**: `Authorization: Bearer <token>`

**Response**: 200 OK
```json
{
  "period": {
    "start_date": "2025-01-13",
    "end_date": "2025-01-19"
  },
  "daily_data": [
    {
      "date": "2025-01-13",
      "calories": 1920,
      "protein": 65.2,
      "carbohydrates": 255.0,
      "fat": 58.3
    }
  ],
  "weekly_average": {
    "calories": 1885,
    "protein": 66.8,
    "carbohydrates": 248.5,
    "fat": 54.2
  }
}
```

---

### 가맹점 (Stores)

#### 1. 주변 가맹점 검색
현재 위치 기반으로 주변 가맹점을 검색합니다.

```http
GET /stores/nearby?latitude=37.5665&longitude=126.9780&radius=1000
```

**Query Parameters**:
- `latitude`: 위도 (필수)
- `longitude`: 경도 (필수)
- `radius`: 검색 반경 (미터, 기본값: 1000)
- `category`: 업종 (optional: restaurant, convenience, cafe)

**Response**: 200 OK
```json
{
  "total": 15,
  "stores": [
    {
      "store_id": 1,
      "store_name": "맛있는식당",
      "address": "서울특별시 종로구 세종대로 123",
      "latitude": 37.5670,
      "longitude": 126.9782,
      "category": "restaurant",
      "phone": "02-1234-5678",
      "business_hours": "11:00-22:00",
      "distance": 85.3
    }
  ]
}
```

---

#### 2. 가맹점 상세 정보
특정 가맹점의 상세 정보를 조회합니다.

```http
GET /stores/{store_id}
```

**Response**: 200 OK
```json
{
  "store_id": 1,
  "store_name": "맛있는식당",
  "address": "서울특별시 종로구 세종대로 123",
  "latitude": 37.5670,
  "longitude": 126.9782,
  "category": "restaurant",
  "phone": "02-1234-5678",
  "business_hours": "11:00-22:00"
}
```

---

### OCR

#### 1. 영양성분표 이미지 인식
영양성분표 이미지를 업로드하여 텍스트를 추출합니다.

```http
POST /ocr/nutrition-label
```

**Headers**:
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Request Body** (form-data):
- `image`: 이미지 파일 (jpg, png)

**Response**: 200 OK
```json
{
  "success": true,
  "extracted_data": {
    "calories": 250,
    "carbohydrates": 35.5,
    "protein": 8.2,
    "fat": 9.5,
    "sodium": 450,
    "sugar": 12.0
  },
  "confidence": 0.95,
  "raw_text": "열량 250kcal\n탄수화물 35.5g\n..."
}
```

---

## 에러 코드

### HTTP 상태 코드

| 코드 | 설명 |
|------|------|
| 200 | 요청 성공 |
| 201 | 리소스 생성 성공 |
| 204 | 요청 성공 (응답 본문 없음) |
| 400 | 잘못된 요청 |
| 401 | 인증 실패 |
| 403 | 권한 없음 |
| 404 | 리소스를 찾을 수 없음 |
| 422 | 유효성 검증 실패 |
| 500 | 서버 내부 오류 |

### 에러 응답 형식

```json
{
  "detail": "에러 메시지",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-01-20T12:00:00Z"
}
```

### 주요 에러 코드

| 에러 코드 | 설명 |
|-----------|------|
| `INVALID_TOKEN` | 유효하지 않은 토큰 |
| `EXPIRED_TOKEN` | 만료된 토큰 |
| `USER_NOT_FOUND` | 사용자를 찾을 수 없음 |
| `INVALID_CREDENTIALS` | 잘못된 인증 정보 |
| `DUPLICATE_EMAIL` | 이미 존재하는 이메일 |
| `INSUFFICIENT_PERMISSION` | 권한 부족 |
| `RESOURCE_NOT_FOUND` | 리소스를 찾을 수 없음 |
| `VALIDATION_ERROR` | 유효성 검증 실패 |
| `OCR_FAILED` | OCR 처리 실패 |

---

## 추가 정보

- 모든 날짜는 ISO 8601 형식 (YYYY-MM-DD)
- 모든 시간은 ISO 8601 형식 (YYYY-MM-DDTHH:MM:SSZ)
- 페이지네이션은 `limit`와 `offset` 파라미터 사용
- Rate Limiting: 분당 100 요청

---

API에 대한 질문이나 문제가 있으면 [GitHub Issues](https://github.com/chungheeh/growfarm_kids/issues)에 등록해주세요.
