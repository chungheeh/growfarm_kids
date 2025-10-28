# 개발 환경 설정 가이드 🛠️

키움밥상(Growing Table) 프로젝트의 개발 환경 설정 방법을 안내합니다.

## 📋 목차

- [시스템 요구사항](#시스템-요구사항)
- [사전 준비](#사전-준비)
- [백엔드 설정](#백엔드-설정)
- [프론트엔드 설정](#프론트엔드-설정)
- [데이터베이스 설정](#데이터베이스-설정)
- [외부 API 설정](#외부-api-설정)
- [실행 방법](#실행-방법)
- [트러블슈팅](#트러블슈팅)

---

## 시스템 요구사항

### 필수 소프트웨어
- **Python**: 3.11 이상
- **Node.js**: 18 이상
- **PostgreSQL**: 14 이상
- **Git**: 최신 버전

### 권장 개발 환경
- **OS**: macOS, Linux, Windows 10/11
- **IDE**: VSCode, PyCharm, WebStorm
- **메모리**: 8GB RAM 이상
- **저장공간**: 10GB 이상

---

## 사전 준비

### 1. 저장소 클론

```bash
git clone https://github.com/chungheeh/growfarm_kids.git
cd growfarm_kids
```

### 2. 필수 소프트웨어 설치

#### macOS (Homebrew 사용)
```bash
# Python 설치
brew install python@3.11

# Node.js 설치
brew install node

# PostgreSQL 설치
brew install postgresql@14
brew services start postgresql@14
```

#### Ubuntu/Debian
```bash
# Python 설치
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Node.js 설치
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs

# PostgreSQL 설치
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Windows
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- PostgreSQL: https://www.postgresql.org/download/windows/

---

## 백엔드 설정

### 1. 백엔드 디렉토리로 이동
```bash
cd backend
```

### 2. 가상환경 생성 및 활성화

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일을 편집하여 필요한 값 입력:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/growfarm_kids

# JWT Configuration (랜덤 문자열 생성)
SECRET_KEY=your-super-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/callback

# CORS Configuration
FRONTEND_URL=http://localhost:3000

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

#### SECRET_KEY 생성 방법
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 프론트엔드 설정

### 1. 프론트엔드 디렉토리로 이동
```bash
cd frontend
```

### 2. 패키지 설치
```bash
npm install
# 또는
yarn install
```

### 3. 환경 변수 설정

`.env.local` 파일 생성:

```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

---

## 데이터베이스 설정

### 1. PostgreSQL 데이터베이스 생성

PostgreSQL에 접속:
```bash
# macOS/Linux
psql postgres

# Windows (PostgreSQL bin 디렉토리에서)
psql -U postgres
```

데이터베이스 및 사용자 생성:
```sql
-- 데이터베이스 생성
CREATE DATABASE growfarm_kids;

-- 사용자 생성 (선택사항)
CREATE USER growfarm_user WITH PASSWORD 'your_password';

-- 권한 부여
GRANT ALL PRIVILEGES ON DATABASE growfarm_kids TO growfarm_user;

-- 연결 확인
\c growfarm_kids
\q
```

### 2. 데이터베이스 마이그레이션

백엔드 디렉토리에서 실행:

```bash
# 테이블 생성 (개발 중)
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

---

## 외부 API 설정

### 1. Google OAuth 설정

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. **API 및 서비스 > 사용자 인증 정보** 이동
4. **사용자 인증 정보 만들기 > OAuth 2.0 클라이언트 ID** 선택
5. 애플리케이션 유형: **웹 애플리케이션**
6. 승인된 리디렉션 URI 추가:
   - `http://localhost:3000/auth/callback`
   - `http://localhost:8000/auth/callback`
7. 클라이언트 ID와 클라이언트 보안 비밀번호를 `.env` 파일에 추가

### 2. NAVER CLOVA OCR API 설정

1. [NAVER Cloud Platform](https://www.ncloud.com/) 접속
2. 계정 생성 및 로그인
3. **AI·NAVER API > AI·Application Service > CLOVA OCR** 선택
4. 도메인 등록 및 API Key 발급
5. `.env` 파일에 API Key 추가:
```bash
NAVER_OCR_API_URL=https://your-ocr-api-url
NAVER_OCR_SECRET_KEY=your-ocr-secret-key
```

### 3. Kakao Map API 설정

1. [Kakao Developers](https://developers.kakao.com/) 접속
2. 애플리케이션 추가
3. **설정 > 일반 > 플랫폼 설정**에서 웹 플랫폼 추가
4. 사이트 도메인 등록: `http://localhost:3000`
5. JavaScript 키를 프론트엔드 `.env.local`에 추가:
```bash
REACT_APP_KAKAO_MAP_API_KEY=your-kakao-map-api-key
```

---

## 실행 방법

### 백엔드 서버 실행

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버 실행 확인:
- API 문서: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 프론트엔드 개발 서버 실행

```bash
cd frontend
npm start
# 또는
yarn start
```

브라우저 자동 실행:
- 프론트엔드: http://localhost:3000

### 동시 실행 (개발 모드)

루트 디렉토리에서:

```bash
# 터미널 1: 백엔드
cd backend && source venv/bin/activate && uvicorn main:app --reload

# 터미널 2: 프론트엔드
cd frontend && npm start
```

---

## 트러블슈팅

### 백엔드 관련

#### 문제: `ModuleNotFoundError: No module named 'config'`
**해결**: 가상환경이 활성화되어 있는지 확인하고 패키지를 다시 설치
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### 문제: PostgreSQL 연결 실패
**해결**:
1. PostgreSQL 서비스 실행 확인:
   ```bash
   # macOS
   brew services list

   # Linux
   sudo systemctl status postgresql
   ```
2. `.env` 파일의 `DATABASE_URL` 확인
3. 데이터베이스 및 사용자 권한 확인

#### 문제: `pydantic_settings` import 오류
**해결**: pydantic-settings 패키지 설치
```bash
pip install pydantic-settings
```

### 프론트엔드 관련

#### 문제: `npm install` 실패
**해결**:
```bash
# 캐시 삭제
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### 문제: CORS 오류
**해결**: 백엔드 `.env` 파일의 `FRONTEND_URL`이 올바른지 확인

### 데이터베이스 관련

#### 문제: 테이블 생성 실패
**해결**:
1. 데이터베이스 존재 확인:
   ```bash
   psql postgres -c "\l"
   ```
2. 마이그레이션 다시 실행:
   ```bash
   python -c "from database import Base, engine; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"
   ```

---

## 다음 단계

설정이 완료되었다면:

1. [API.md](./API.md)에서 API 엔드포인트 확인
2. [DATABASE.md](./DATABASE.md)에서 데이터베이스 스키마 이해
3. [ARCHITECTURE.md](./ARCHITECTURE.md)에서 시스템 구조 파악
4. 개발 시작! 🚀

---

문제가 해결되지 않으면 [GitHub Issues](https://github.com/chungheeh/growfarm_kids/issues)에 문의해주세요.
