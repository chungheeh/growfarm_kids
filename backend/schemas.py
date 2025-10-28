from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional
from models import UserType


# 인증 스키마
class Token(BaseModel):
    """JWT 토큰 응답."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """JWT 토큰에 저장되는 데이터."""
    email: Optional[str] = None
    user_id: Optional[int] = None


class GoogleAuthRequest(BaseModel):
    """Google OAuth 인증 코드."""
    code: str


# 사용자 스키마
class UserBase(BaseModel):
    """기본 사용자 스키마."""
    email: EmailStr
    name: str
    user_type: UserType


class UserCreate(UserBase):
    """사용자 생성 스키마."""
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    google_id: Optional[str] = None
    profile_picture: Optional[str] = None


class UserUpdate(BaseModel):
    """사용자 수정 스키마."""
    name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None


class UserResponse(UserBase):
    """사용자 응답 스키마."""
    user_id: int
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# 아동 프로필 스키마
class ChildProfileBase(BaseModel):
    """기본 아동 프로필 스키마."""
    height: Optional[float] = Field(None, description="키 (cm)")
    weight: Optional[float] = Field(None, description="몸무게 (kg)")


class ChildProfileCreate(ChildProfileBase):
    """아동 프로필 생성 스키마."""
    guardian_id: Optional[int] = None


class ChildProfileUpdate(ChildProfileBase):
    """아동 프로필 수정 스키마."""
    pass


class ChildProfileResponse(ChildProfileBase):
    """아동 프로필 응답 스키마."""
    child_id: int
    user_id: int
    guardian_id: Optional[int] = None
    bmi: Optional[float] = None
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


# 전체 사용자 프로필
class UserProfileResponse(UserResponse):
    """아동 데이터를 포함한 전체 사용자 프로필."""
    child_profile: Optional[ChildProfileResponse] = None

    class Config:
        from_attributes = True
