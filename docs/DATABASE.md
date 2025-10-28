# 데이터베이스 설계 📊

키움밥상(Growing Table) 프로젝트의 데이터베이스 스키마 및 ERD 문서입니다.

## 📋 목차

- [개요](#개요)
- [ERD (Entity Relationship Diagram)](#erd-entity-relationship-diagram)
- [테이블 상세](#테이블-상세)
- [인덱스 및 제약조건](#인덱스-및-제약조건)
- [쿼리 예제](#쿼리-예제)

---

## 개요

### 데이터베이스 정보
- **DBMS**: PostgreSQL 14+
- **Character Set**: UTF-8
- **Time Zone**: UTC

### 설계 원칙
- 정규화: 제3정규형(3NF) 준수
- 외래키를 통한 참조 무결성 보장
- 인덱스를 통한 쿼리 성능 최적화
- 민감 정보(개인정보) 암호화 고려

---

## ERD (Entity Relationship Diagram)

```
┌─────────────────┐
│     Users       │
├─────────────────┤
│ user_id (PK)    │
│ email           │
│ name            │
│ birth_date      │
│ gender          │
│ user_type       │
│ google_id       │
│ profile_picture │
│ created_at      │
│ updated_at      │
└─────────────────┘
        │
        │ 1:1
        ▼
┌─────────────────┐         ┌─────────────────┐
│    Children     │         │     Meals       │
├─────────────────┤         ├─────────────────┤
│ child_id (PK)   │────────▶│ meal_id (PK)    │
│ user_id (FK)    │   1:N   │ child_id (FK)   │
│ guardian_id(FK) │         │ meal_type       │
│ height          │         │ meal_date       │
│ weight          │         │ meal_time       │
│ bmi             │         │ created_at      │
│ last_updated    │         └─────────────────┘
└─────────────────┘                 │
        ▲                           │ 1:1
        │                           ▼
        │ N:1              ┌─────────────────┐
        │                  │   Nutrition     │
    Guardian              ├─────────────────┤
    (Users)                │ nutrition_id(PK)│
                           │ meal_id (FK)    │
                           │ calories        │
                           │ carbohydrates   │
                           │ protein         │
                           │ fat             │
                           │ sodium          │
                           │ sugar           │
                           │ fiber           │
                           └─────────────────┘

┌─────────────────┐
│     Stores      │
├─────────────────┤
│ store_id (PK)   │
│ store_name      │
│ address         │
│ latitude        │
│ longitude       │
│ category        │
│ phone           │
│ business_hours  │
└─────────────────┘
```

---

## 테이블 상세

### 1. Users (사용자)

사용자 인증 및 기본 정보를 저장하는 테이블입니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| user_id | INTEGER | PK, AUTO_INCREMENT | 사용자 고유 ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | 이메일 주소 |
| name | VARCHAR(100) | NOT NULL | 사용자 이름 |
| birth_date | DATE | NULL | 생년월일 |
| gender | VARCHAR(10) | NULL | 성별 (male, female, other) |
| user_type | ENUM | NOT NULL | 사용자 타입 (child, guardian) |
| google_id | VARCHAR(255) | UNIQUE, NULL | Google OAuth ID |
| profile_picture | VARCHAR(500) | NULL | 프로필 사진 URL |
| created_at | TIMESTAMP | DEFAULT NOW() | 계정 생성 시간 |
| updated_at | TIMESTAMP | ON UPDATE NOW() | 정보 수정 시간 |

**인덱스**:
- PRIMARY KEY: `user_id`
- UNIQUE: `email`, `google_id`
- INDEX: `user_type`

**관계**:
- Children (1:1): user_id → children.user_id
- Children (1:N, as guardian): user_id → children.guardian_id

---

### 2. Children (아동 프로필)

아동의 건강 지표를 저장하는 테이블입니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| child_id | INTEGER | PK, AUTO_INCREMENT | 아동 프로필 고유 ID |
| user_id | INTEGER | FK, UNIQUE, NOT NULL | 사용자 ID (Users 참조) |
| guardian_id | INTEGER | FK, NULL | 보호자 ID (Users 참조) |
| height | FLOAT | NULL | 키 (cm) |
| weight | FLOAT | NULL | 몸무게 (kg) |
| bmi | FLOAT | NULL | 체질량지수 (자동 계산) |
| last_updated | TIMESTAMP | ON UPDATE NOW() | 마지막 업데이트 시간 |

**인덱스**:
- PRIMARY KEY: `child_id`
- UNIQUE: `user_id`
- FOREIGN KEY: `user_id` → `users.user_id`
- FOREIGN KEY: `guardian_id` → `users.user_id`

**관계**:
- Users (N:1): user_id → users.user_id
- Users (N:1, guardian): guardian_id → users.user_id
- Meals (1:N): child_id → meals.child_id

**BMI 계산**:
```sql
bmi = weight / ((height / 100) ^ 2)
```

---

### 3. Meals (식사 기록)

아동의 식사 기록을 저장하는 테이블입니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| meal_id | INTEGER | PK, AUTO_INCREMENT | 식사 기록 고유 ID |
| child_id | INTEGER | FK, NOT NULL | 아동 ID (Children 참조) |
| meal_type | VARCHAR(20) | NOT NULL | 식사 유형 (breakfast, lunch, dinner, snack) |
| meal_date | DATE | NOT NULL | 식사 날짜 |
| meal_time | TIMESTAMP | NOT NULL | 식사 시간 |
| created_at | TIMESTAMP | DEFAULT NOW() | 기록 생성 시간 |

**인덱스**:
- PRIMARY KEY: `meal_id`
- FOREIGN KEY: `child_id` → `children.child_id`
- INDEX: `meal_date`, `child_id`
- COMPOSITE INDEX: `(child_id, meal_date)`

**관계**:
- Children (N:1): child_id → children.child_id
- Nutrition (1:1): meal_id → nutrition.meal_id

**meal_type 값**:
- `breakfast`: 아침
- `lunch`: 점심
- `dinner`: 저녁
- `snack`: 간식

---

### 4. Nutrition (영양소 정보)

식사의 영양소 정보를 저장하는 테이블입니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| nutrition_id | INTEGER | PK, AUTO_INCREMENT | 영양소 정보 고유 ID |
| meal_id | INTEGER | FK, UNIQUE, NOT NULL | 식사 ID (Meals 참조) |
| calories | FLOAT | NULL | 열량 (kcal) |
| carbohydrates | FLOAT | NULL | 탄수화물 (g) |
| protein | FLOAT | NULL | 단백질 (g) |
| fat | FLOAT | NULL | 지방 (g) |
| sodium | FLOAT | NULL | 나트륨 (mg) |
| sugar | FLOAT | NULL | 당류 (g) |
| fiber | FLOAT | NULL | 식이섬유 (g) |

**인덱스**:
- PRIMARY KEY: `nutrition_id`
- UNIQUE: `meal_id`
- FOREIGN KEY: `meal_id` → `meals.meal_id`

**관계**:
- Meals (1:1): meal_id → meals.meal_id

**참고**:
- 향후 비타민, 미네랄 등 추가 영양소 컬럼 확장 가능
- JSON 타입 컬럼 사용 고려 (유연성)

---

### 5. Stores (가맹점)

아동급식카드 사용 가능한 가맹점 정보를 저장하는 테이블입니다.

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|---------|------|
| store_id | INTEGER | PK, AUTO_INCREMENT | 가맹점 고유 ID |
| store_name | VARCHAR(200) | NOT NULL | 가맹점 이름 |
| address | VARCHAR(500) | NOT NULL | 주소 |
| latitude | DECIMAL(10, 8) | NOT NULL | 위도 |
| longitude | DECIMAL(11, 8) | NOT NULL | 경도 |
| category | VARCHAR(50) | NULL | 업종 (restaurant, convenience, cafe) |
| phone | VARCHAR(20) | NULL | 전화번호 |
| business_hours | VARCHAR(200) | NULL | 영업시간 |

**인덱스**:
- PRIMARY KEY: `store_id`
- INDEX: `category`
- SPATIAL INDEX: `(latitude, longitude)` (지리적 검색 최적화)

**category 값**:
- `restaurant`: 음식점
- `convenience`: 편의점
- `cafe`: 카페
- `bakery`: 빵집
- `other`: 기타

---

## 인덱스 및 제약조건

### 주요 인덱스

#### 성능 최적화를 위한 인덱스
```sql
-- 사용자 검색
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_google_id ON users(google_id);

-- 식사 기록 조회 (날짜별, 아동별)
CREATE INDEX idx_meals_child_date ON meals(child_id, meal_date);
CREATE INDEX idx_meals_date ON meals(meal_date);

-- 가맹점 위치 검색
CREATE INDEX idx_stores_location ON stores(latitude, longitude);
CREATE INDEX idx_stores_category ON stores(category);
```

### 외래키 제약조건

```sql
-- Children → Users
ALTER TABLE children
ADD CONSTRAINT fk_child_user
FOREIGN KEY (user_id) REFERENCES users(user_id)
ON DELETE CASCADE;

ALTER TABLE children
ADD CONSTRAINT fk_child_guardian
FOREIGN KEY (guardian_id) REFERENCES users(user_id)
ON DELETE SET NULL;

-- Meals → Children
ALTER TABLE meals
ADD CONSTRAINT fk_meal_child
FOREIGN KEY (child_id) REFERENCES children(child_id)
ON DELETE CASCADE;

-- Nutrition → Meals
ALTER TABLE nutrition
ADD CONSTRAINT fk_nutrition_meal
FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
ON DELETE CASCADE;
```

### Check 제약조건

```sql
-- 키와 몸무게는 양수
ALTER TABLE children
ADD CONSTRAINT chk_height CHECK (height > 0 AND height < 300);

ALTER TABLE children
ADD CONSTRAINT chk_weight CHECK (weight > 0 AND weight < 200);

-- 영양소 값은 음수가 될 수 없음
ALTER TABLE nutrition
ADD CONSTRAINT chk_calories CHECK (calories >= 0);

ALTER TABLE nutrition
ADD CONSTRAINT chk_carbohydrates CHECK (carbohydrates >= 0);
```

---

## 쿼리 예제

### 사용자 및 아동 프로필

#### 1. 새 아동 사용자 등록
```sql
-- 사용자 생성
INSERT INTO users (email, name, birth_date, gender, user_type, google_id)
VALUES ('child@example.com', '김어린이', '2015-05-20', 'male', 'child', 'google_123456');

-- 아동 프로필 생성
INSERT INTO children (user_id, height, weight)
VALUES (1, 145.5, 38.2);
```

#### 2. 아동의 전체 프로필 조회
```sql
SELECT
    u.user_id, u.email, u.name, u.birth_date, u.gender,
    c.child_id, c.height, c.weight, c.bmi,
    g.name AS guardian_name
FROM users u
LEFT JOIN children c ON u.user_id = c.user_id
LEFT JOIN users g ON c.guardian_id = g.user_id
WHERE u.user_id = 1 AND u.user_type = 'child';
```

### 식사 및 영양 분석

#### 3. 식사 기록 추가
```sql
-- 식사 기록
INSERT INTO meals (child_id, meal_type, meal_date, meal_time)
VALUES (1, 'lunch', '2025-01-20', '2025-01-20 12:30:00');

-- 영양소 정보
INSERT INTO nutrition (meal_id, calories, carbohydrates, protein, fat, sodium)
VALUES (1, 650, 85.5, 25.3, 18.2, 950);
```

#### 4. 일일 영양소 합계 조회
```sql
SELECT
    m.meal_date,
    SUM(n.calories) AS total_calories,
    SUM(n.carbohydrates) AS total_carbs,
    SUM(n.protein) AS total_protein,
    SUM(n.fat) AS total_fat,
    SUM(n.sodium) AS total_sodium
FROM meals m
JOIN nutrition n ON m.meal_id = n.meal_id
WHERE m.child_id = 1 AND m.meal_date = '2025-01-20'
GROUP BY m.meal_date;
```

#### 5. 주간 영양소 평균
```sql
SELECT
    DATE_TRUNC('week', m.meal_date) AS week,
    AVG(n.calories) AS avg_calories,
    AVG(n.protein) AS avg_protein,
    AVG(n.carbohydrates) AS avg_carbs
FROM meals m
JOIN nutrition n ON m.meal_id = n.meal_id
WHERE m.child_id = 1
    AND m.meal_date BETWEEN '2025-01-13' AND '2025-01-19'
GROUP BY DATE_TRUNC('week', m.meal_date);
```

### 가맹점 검색

#### 6. 주변 가맹점 검색 (반경 내)
```sql
SELECT
    store_id,
    store_name,
    address,
    category,
    -- 거리 계산 (Haversine formula)
    (
        6371 * acos(
            cos(radians(37.5665)) * cos(radians(latitude)) *
            cos(radians(longitude) - radians(126.9780)) +
            sin(radians(37.5665)) * sin(radians(latitude))
        ) * 1000
    ) AS distance_meters
FROM stores
WHERE (
    6371 * acos(
        cos(radians(37.5665)) * cos(radians(latitude)) *
        cos(radians(longitude) - radians(126.9780)) +
        sin(radians(37.5665)) * sin(radians(latitude))
    ) * 1000
) <= 1000
ORDER BY distance_meters
LIMIT 20;
```

### 성장 추이

#### 7. 아동의 월별 키/몸무게 변화 (히스토리 테이블 필요 시)
```sql
-- 참고: 실제로는 growth_history 테이블을 별도로 만들어 추적하는 것이 좋음
SELECT
    DATE_TRUNC('month', last_updated) AS month,
    AVG(height) AS avg_height,
    AVG(weight) AS avg_weight,
    AVG(bmi) AS avg_bmi
FROM children
WHERE child_id = 1
GROUP BY DATE_TRUNC('month', last_updated)
ORDER BY month;
```

---

## 데이터베이스 마이그레이션

### 테이블 생성 스크립트

전체 데이터베이스 스키마 생성은 SQLAlchemy ORM을 통해 자동으로 수행됩니다:

```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 초기 데이터 (Seed Data)

가맹점 데이터는 별도의 CSV 파일이나 외부 API에서 가져와 적재할 예정입니다.

---

## 향후 확장 계획

### 추가 예정 테이블

1. **growth_history**: 아동의 키/몸무게 변화 이력
2. **rewards**: 칭찬 스티커 및 성취 기록
3. **favorites**: 즐겨찾는 가맹점
4. **notifications**: 알림 기록

### 성능 최적화

- 파티셔닝: meals 테이블을 날짜별로 파티셔닝
- 캐싱: Redis를 활용한 자주 조회되는 데이터 캐싱
- Read Replica: 읽기 전용 복제본 구성

---

데이터베이스 설계에 대한 질문이나 제안사항은 [GitHub Issues](https://github.com/chungheeh/growfarm_kids/issues)에 등록해주세요.
