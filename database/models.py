from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    language_code = Column(String(10), default='en')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)

class SupportRequest(Base):
    __tablename__ = 'support_requests'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # telegram_id
    message_text = Column(Text, nullable=False)
    request_type = Column(String(50), nullable=True)  # deposit, withdraw, bonus, etc.
    status = Column(String(20), default='open')  # open, closed, escalated
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

class BotStats(Base):
    __tablename__ = 'bot_stats'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_users = Column(Integer, default=0)
    daily_requests = Column(Integer, default=0)
    resolved_requests = Column(Integer, default=0)
    escalated_requests = Column(Integer, default=0)

# Создание движка базы данных
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Создание всех таблиц в базе данных"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Получение сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
