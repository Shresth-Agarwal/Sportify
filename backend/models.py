from datetime import datetime
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from backend.database.db_config import Base


class Auth(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    user = relationship("User", back_populates="auth", uselist=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    sport = Column(String(100))

    @property
    def email(self):
        return self.auth.email if self.auth else None

    auth = relationship("Auth", uselist=False, back_populates="user")
    records = relationship("ExerciseRecord", back_populates="user", cascade="all, delete")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))
    metric_type = Column(String(50))

    # Relationships
    records = relationship("ExerciseRecord", back_populates="exercise")


class ExerciseRecord(Base):
    __tablename__ = "exercise_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)

    sets = Column(Integer)
    reps = Column(Integer)
    metric_value = Column(Float)
    note = Column(String(255))
    details = Column(JSON)
    recorded_at = Column(DateTime, default=datetime.now())

    # Relationships
    user = relationship("User", back_populates="records")
    exercise = relationship("Exercise", back_populates="records")


class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan = Column(JSON, nullable=False)

    user = relationship("User", backref="training_plans")
