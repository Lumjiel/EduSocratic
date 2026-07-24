from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    open_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))
    grade: Mapped[int] = mapped_column(Integer)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    bitable_token: Mapped[str] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StudentClass(Base):
    __tablename__ = "student_classes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    topic: Mapped[str] = mapped_column(String(256))
    response: Mapped[str] = mapped_column(Text)
    scores: Mapped[dict] = mapped_column(JSON)
    weighted_score: Mapped[float] = mapped_column(Float)
    reasoning: Mapped[str] = mapped_column(Text)
    highlights: Mapped[str] = mapped_column(Text)
    suggestions: Mapped[str] = mapped_column(Text)
    overall_comment: Mapped[str] = mapped_column(Text)
    from_cache: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    original_scores: Mapped[dict] = mapped_column(JSON)
    corrected_scores: Mapped[dict] = mapped_column(JSON)
    differences: Mapped[dict] = mapped_column(JSON)
    max_disagreement_dimension: Mapped[str] = mapped_column(String(32))
    max_disagreement_value: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    doc_url: Mapped[str] = mapped_column(String(256))
    period_start: Mapped[datetime] = mapped_column(DateTime)
    period_end: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
