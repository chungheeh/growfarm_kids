from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class UserType(str, enum.Enum):
    """사용자 타입 열거형."""
    CHILD = "child"
    GUARDIAN = "guardian"


class User(Base):
    """인증을 위한 메인 사용자 테이블."""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    user_type = Column(SQLEnum(UserType), nullable=False)
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    profile_picture = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계
    child_profile = relationship("Child", back_populates="user", uselist=False)
    guardian_children = relationship("Child", foreign_keys="Child.guardian_id", back_populates="guardian")


class Child(Base):
    """건강 지표를 포함한 아동 프로필."""
    __tablename__ = "children"

    child_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    guardian_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    height = Column(Float, nullable=True)  # cm 단위
    weight = Column(Float, nullable=True)  # kg 단위
    bmi = Column(Float, nullable=True)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계
    user = relationship("User", foreign_keys=[user_id], back_populates="child_profile")
    guardian = relationship("User", foreign_keys=[guardian_id], back_populates="guardian_children")
    meals = relationship("Meal", back_populates="child")


class Meal(Base):
    """식사 기록."""
    __tablename__ = "meals"

    meal_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.child_id"), nullable=False)
    meal_type = Column(String(20), nullable=False)  # 아침/점심/저녁/간식
    meal_date = Column(Date, nullable=False, index=True)
    meal_time = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계
    child = relationship("Child", back_populates="meals")
    nutrition = relationship("Nutrition", back_populates="meal", uselist=False)


class Nutrition(Base):
    """영양 정보."""
    __tablename__ = "nutrition"

    nutrition_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    meal_id = Column(Integer, ForeignKey("meals.meal_id"), unique=True, nullable=False)
    calories = Column(Float, nullable=True)
    carbohydrates = Column(Float, nullable=True)  # g
    protein = Column(Float, nullable=True)  # g
    fat = Column(Float, nullable=True)  # g
    sodium = Column(Float, nullable=True)  # mg
    sugar = Column(Float, nullable=True)  # g
    fiber = Column(Float, nullable=True)  # g

    # 관계
    meal = relationship("Meal", back_populates="nutrition")
