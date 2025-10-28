# 키움밥상 (Growing Table) 🍚

> 아동급식카드를 사용하는 어린이들의 건강한 성장을 위한 영양 관리 및 성장 모니터링 플랫폼

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)

## 📖 프로젝트 소개

키움밥상은 아동급식카드를 사용하는 결식우려아동의 영양 관리와 성장 모니터링을 지원하는 웹 기반 플랫폼입니다. 어린이가 직접 식사 정보를 입력하고, 자신의 영양 상태와 키·몸무게 성장 추이를 쉽고 재미있게 확인할 수 있도록 설계되었습니다.

### 🎯 프로젝트 목표

현재 결식아동의 70% 이상이 편의점에서 끼니를 해결하며 영양 불균형 문제를 겪고 있습니다. 키움밥상은 다음과 같은 목표를 가지고 있습니다:

- **아동 맞춤형 성장 지원**: 영양소 섭취 현황과 BMI 기반 성장 추이 모니터링
- **보호자 직관적 관리**: 아동의 발달 상태 실시간 확인 및 식습관 관리
- **데이터 기반 정책 활용**: 지역별 아동 급식 현황 파악 및 정책 개선 근거 제공

### ✨ 주요 기능

#### 1. 영양 분석 📊
- 하루 영양소 섭취량 확인 (탄수화물, 단백질, 지방, 비타민, 미네랄)
- 연령별 권장 섭취량(DRI) 대비 실제 섭취량 비교
- 일별/주별/월별 영양소 섭취 추이 그래프
- 부족한 영양소 알림 및 개선 제안
- 게임화된 영양 목표 달성 시스템 (칭찬 스티커)

#### 2. 성장 기록 📈
- 소아청소년 BMI 백분위수 계산
- 성장 곡선 그래프 시각화
- 또래 평균 대비 비교 (익명화된 데이터)
- 월별 성장 추이 모니터링

#### 3. OCR 영양표 인식 📸
- NAVER CLOVA OCR API를 통한 영양성분표 자동 인식
- 칼로리, 탄수화물, 단백질, 지방 등 자동 입력
- 인식 결과 수정 기능
- 수동 입력 대비 입력 시간 70% 단축

#### 4. 가맹점 조회 🗺️
- 카카오맵 API 기반 주변 아동급식카드 가맹점 검색
- 현재 위치 기반 가까운 가게 표시
- 업종별 필터링 (음식점, 편의점, 카페 등)
- 가게 상세 정보 및 즐겨찾기 기능

### 👥 타겟 사용자

- **Primary**: 만 6-15세 어린이 (아동급식카드 사용자)
- **Secondary**: 보호자 (부모, 후견인, 사회복지사)
- **Tertiary**: 지자체 및 정책 입안자

### 🛠 기술 스택

- **Frontend**: React.js + TypeScript + TailwindCSS
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **Authentication**: Google OAuth 2.0 + JWT
- **External APIs**: NAVER CLOVA OCR, Kakao Map API

### 📊 현재 상태

**프로젝트 진행률**: 기획 완료 (45%)

**완료된 작업**:
- ✅ 프로젝트 기획 및 PRD 작성
- ✅ 백엔드 기본 구조 설계
- ✅ 데이터베이스 모델 설계
- ✅ 인증 시스템 스키마 정의

**진행 중인 작업**:
- 🔄 Google OAuth 인증 구현
- 🔄 FastAPI 엔드포인트 개발
- 🔄 React 프론트엔드 초기화

### 🚀 빠른 시작

자세한 설치 및 실행 방법은 [SETUP.md](./SETUP.md)를 참고해주세요.

```bash
# 저장소 클론
git clone https://github.com/chungheeh/growfarm_kids.git
cd growfarm_kids

# 백엔드 설정
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 필요한 값 입력

# 서버 실행
uvicorn main:app --reload
```

### 📚 문서

- [SETUP.md](./SETUP.md) - 개발 환경 설정 가이드
- [API.md](./API.md) - API 엔드포인트 문서
- [DATABASE.md](./DATABASE.md) - 데이터베이스 스키마 및 ERD
- [ARCHITECTURE.md](./ARCHITECTURE.md) - 시스템 아키텍처 설계
- [prd.md](./prd.md) - 프로덕트 요구사항 문서

### 👨‍👩‍👧‍👦 팀

**Team 2**: 양가윤, 강윤선, 한충희, 곽기명
**프로젝트 기간**: 2025학년도 2학기

### 📄 라이선스

This project is licensed under the MIT License.

### 🤝 기여하기

이슈와 풀 리퀘스트는 언제나 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📞 문의

프로젝트에 대한 문의사항은 이슈를 통해 남겨주세요.

---

**키움밥상**으로 어린이들의 건강한 성장을 함께 응원해주세요! 🌱
