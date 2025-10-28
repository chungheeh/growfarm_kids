# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# 중요 설정
  항상 답변은 한국말로 해주세요.
  변경사항을 항상 깃 허브 에 이슈를 넣어주세요.
  항상 ultrathink 해 주세요.

## Project Overview

키움밥상 (Growing Table)은 아동급식카드를 사용하는 어린이들이 스스로 영양 관리와 성장을 기록할 수 있는 웹 기반 플랫폼입니다. 어린이가 직접 식사 정보를 입력하고, 자신의 영양 상태와 키·몸무게 성장 추이를 쉽고 재미있게 확인할 수 있도록 설계되었습니다.

**현재 상태:** 기획 단계 (PRD 기준 45% 완료). 아직 구현은 시작되지 않았습니다.

**타겟 사용자:** 만 6-15세 어린이 (아동급식카드 사용자)

## Tech Stack (Planned)

### Frontend
- **React.js with TypeScript**: Component-based UI development
- **TailwindCSS**: Fast styling and responsive design

### Backend
- **Python**: Data analysis and API server
- **Framework**: FastAPI or Django (to be decided)

### Database
- **PostgreSQL**: Relational database for complex queries and data integrity

### External APIs
- **NAVER CLOVA OCR API**: Nutrition label image recognition
- **Kakao Map API**: Store location mapping

## 핵심 기능

### 1. 영양 분석 (내가 먹은 음식 확인하기)
- 하루에 먹은 영양소를 쉽게 확인 (탄수화물, 단백질, 지방, 비타민, 미네랄)
- 내 나이에 필요한 영양과 비교해서 보여주기
- 일별/주별/월별로 내가 먹은 음식을 그림으로 보여주기
- 더 먹으면 좋은 음식 알려주기
- 게임처럼 영양 목표 달성하면 칭찬 스티커 받기

### 2. 성장 기록 (키와 몸무게 체크)
- 내 나이 친구들과 비교해서 키와 몸무게가 잘 자라고 있는지 확인
- 성장 그래프로 내가 얼마나 자랐는지 한눈에 보기
- 매달 키와 몸무게 변화 기록하기
- 잘 자라고 있으면 칭찬 메시지 받기

### 3. 사진으로 영양표 읽기 (OCR)
- 음식 포장지의 영양 정보를 사진으로 찍으면 자동으로 읽어주기
- 네이버 CLOVA OCR API 사용
- 칼로리, 탄수화물, 단백질, 지방 등을 자동으로 입력
- 잘못 읽힌 부분은 직접 수정 가능
- 사진 찍으면 식사 기록에 자동 저장

### 4. 아동급식카드 쓸 수 있는 가게 찾기
- 카카오맵 API로 근처 아동급식카드 사용 가능한 가게 찾기
- 내 위치에서 가까운 가게 보여주기
- 음식점, 편의점, 카페 등 종류별로 찾기
- 가게 정보 보기 (주소, 전화번호, 영업시간)
- 자주 가는 가게 즐겨찾기 기능

## 데이터 모델 (계획)

### 주요 테이블
- **Users (사용자)**: user_id, email, name, birth_date, gender, height, weight, bmi
- **Meals (식사 기록)**: meal_id, user_id, meal_type, meal_date, meal_time
- **Nutrition (영양 정보)**: nutrition_id, meal_id, calories, carbohydrates, protein, fat, vitamins (JSON), minerals (JSON)
- **Stores (가게 정보)**: store_id, store_name, address, latitude, longitude, category, phone, business_hours
- **Rewards (칭찬 스티커)**: reward_id, user_id, reward_type, earned_date, description

## 사용자

**어린이 (만 6-15세)**: 아동급식카드를 사용하는 어린이가 직접 서비스를 이용합니다.

## 개발 가이드라인

### 프론트엔드 개발
- React 함수형 컴포넌트와 TypeScript 사용
- TailwindCSS로 모바일 우선 반응형 디자인 구현
- **어린이 친화적 UI/UX 원칙:**
  - 큰 버튼과 터치하기 쉬운 인터페이스
  - 밝고 친근한 색상 팔레트 (파스텔톤, 원색 조합)
  - 캐릭터와 일러스트로 재미있게 표현
  - 읽기 쉬운 글꼴과 큰 글자 크기
  - 복잡한 그래프 대신 직관적인 시각화 (게이지, 이모지, 색깔)
  - 성취감을 주는 애니메이션과 효과음
  - 간단한 단어와 짧은 문장 사용
- 주요 화면:
  - 회원가입/로그인 (Google OAuth, 간소화)
  - 메인 대시보드 (오늘 먹은 음식, 영양 상태, 성장 기록)
  - 식사 추가 화면 (직접 입력 + 사진으로 찍기)
  - 분석 화면 (내가 먹은 음식 그림, 성장 그래프)
  - 가게 찾기 지도 (카카오맵 연동)
  - 내 정보 (프로필, 키·몸무게 업데이트, 칭찬 스티커 모음)

### 백엔드 개발
- Python 사용 (데이터 분석 기능)
- FastAPI (비동기, 현대적) 또는 Django (풀스택) 중 선택
- Google OAuth로 간편 로그인 구현 (어린이 친화적으로 단순화)
- RESTful API 설계: 식사 기록, 영양 분석, 성장 계산, 칭찬 스티커
- 네이버 CLOVA OCR API 연동 (사진 인식)
- 카카오맵 API 연동 (가게 찾기)

### 데이터베이스 스키마
- PostgreSQL 사용 (복잡한 쿼리와 데이터 무결성)
- Users, Meals, Nutrition, Stores, Rewards 테이블 간 관계 설정
- 비타민과 미네랄은 JSON으로 유연하게 저장
- 자주 조회하는 필드 인덱싱 (user_id, meal_date)

## 주요 고려사항

### 개인정보 보호 및 보안
- 어린이의 건강 데이터는 민감 정보 - 적절한 접근 제어 필수
- GDPR/개인정보보호법(PIPA) 준수
- 어린이가 스스로 계정을 안전하게 관리할 수 있도록 간소화된 인증
- 비밀번호 대신 Google OAuth 등 간편 인증 권장

### 영양 분석
- 한국인 영양섭취기준(DRI) 사용
- 나이, 성별, 활동량에 따라 권장량 조정
- 불완전한 영양 데이터도 유연하게 처리
- **어린이가 이해하기 쉬운 표현 사용** (예: "단백질이 부족해요" 대신 "고기나 생선을 더 먹으면 좋아요")

### 성장 계산 (BMI)
- 소아청소년용 BMI 백분위수 사용 (성인 BMI와 다름)
- 한국 소아청소년 성장도표 기준
- 개월 수까지 고려한 정확한 백분위수 계산
- **긍정적인 피드백 중심** (부정적 표현 최소화)

### OCR 연동
- OCR 결과를 저장하기 전에 검증
- 잘못 인식된 정보는 직접 수정 가능
- 다양한 영양표 형식 처리 (편의점, 음식점 등)
- **어린이가 쉽게 사진을 찍고 확인할 수 있도록 UI 단순화**

## External API Requirements

### NAVER CLOVA OCR
- API key required
- Rate limits and quota management needed
- Handle image preprocessing for better accuracy

### Kakao Map API
- API key required
- Implement geocoding for address searches
- Handle map markers for multiple stores efficiently

## 성공 지표

- 영양 분석 정확도: 95% 이상
- OCR 인식 정확도: 90% 이상
- 사진 촬영으로 입력 시간 70% 단축 (직접 입력 대비)
- 전국 가게 데이터베이스 커버리지: 95% 이상
- 일일 활성 사용자의 70% 이상이 영양 분석 기능 사용
- 매달 키·몸무게를 기록하는 어린이: 80% 이상
- 어린이 사용자 만족도: 4.5/5.0 이상
- 칭찬 스티커 획득률: 60% 이상 (목표 달성 동기 부여)

## Team

**Team 2**: Yang Gayun, Kang Yunseon, Han Chunghee, Kwak Gimyeong
**Project Period**: 2025 Academic Year, Semester 2
