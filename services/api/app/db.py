from sqlalchemy import create_engine, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from datetime import datetime, timezone
from app.core import settings

def utcnow(): return datetime.now(timezone.utc)
class Base(DeclarativeBase): pass

class Customer(Base):
    __tablename__="customers"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    name: Mapped[str]=mapped_column(String)

class Card(Base):
    __tablename__="cards"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    customer_id: Mapped[str]=mapped_column(ForeignKey("customers.id"))
    last4: Mapped[str]=mapped_column(String)
    status: Mapped[str]=mapped_column(String, default="active")

class Transaction(Base):
    __tablename__="transactions"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    card_id: Mapped[str]=mapped_column(ForeignKey("cards.id"))
    merchant: Mapped[str]=mapped_column(String)
    amount: Mapped[float]=mapped_column(Float)
    occurred_at: Mapped[datetime]=mapped_column(DateTime(timezone=True))
    category: Mapped[str]=mapped_column(String)

class DisputeCase(Base):
    __tablename__="dispute_cases"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    customer_id: Mapped[str]=mapped_column(String)
    transaction_id: Mapped[str]=mapped_column(String)
    reason: Mapped[str]=mapped_column(Text)
    status: Mapped[str]=mapped_column(String, default="open")
    owner: Mapped[str]=mapped_column(String, default="Fraud Operations")
    agent_confidence: Mapped[float]=mapped_column(Float)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)

class Approval(Base):
    __tablename__="approvals"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    session_id: Mapped[str]=mapped_column(String)
    action: Mapped[str]=mapped_column(String)
    resource_id: Mapped[str]=mapped_column(String)
    status: Mapped[str]=mapped_column(String, default="pending")
    reason: Mapped[str]=mapped_column(Text)

class Audit(Base):
    __tablename__="audit"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    session_id: Mapped[str]=mapped_column(String)
    event_type: Mapped[str]=mapped_column(String)
    detail: Mapped[str]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)

cfg=settings()
args={"check_same_thread":False} if cfg.database_url.startswith("sqlite") else {}
engine=create_engine(cfg.database_url, connect_args=args, pool_pre_ping=True)
SessionLocal=sessionmaker(bind=engine, autoflush=False)

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
