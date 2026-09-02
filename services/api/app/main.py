from datetime import datetime,timezone,timedelta
from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import Base,engine,SessionLocal,get_db,Customer,Card,Transaction,DisputeCase,Audit
from app.agent import run_agent
from app.domain import recent,decide,audit

app=FastAPI(title="CardGuard AI API",version="1.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

class Chat(BaseModel):
    session_id:str
    customer_id:str="cust_maya"
    message:str
class ApprovalDecision(BaseModel):
    approved:bool

@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if not db.get(Customer,"cust_maya"):
            c=Customer(id="cust_maya",name="Maya Shah");card=Card(id="card_4242",customer_id=c.id,last4="4242",status="active")
            now=datetime.now(timezone.utc)
            txs=[
                Transaction(id="tx_1001",card_id=card.id,merchant="Metro Electronics",amount=184.72,occurred_at=now-timedelta(days=2),category="Electronics"),
                Transaction(id="tx_1002",card_id=card.id,merchant="Bean House Coffee",amount=6.45,occurred_at=now-timedelta(days=1),category="Dining"),
                Transaction(id="tx_1003",card_id=card.id,merchant="StreamFlix",amount=17.99,occurred_at=now-timedelta(days=1),category="Subscription"),
            ]
            db.add_all([c,card,*txs]);db.commit()

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/api/customers/{customer_id}/transactions")
def transactions(customer_id:str,db:Session=Depends(get_db)):
    return [{"id":t.id,"merchant":t.merchant,"amount":t.amount,"occurred_at":t.occurred_at,"category":t.category} for t in recent(db,customer_id)]

@app.post("/api/agent/chat")
def chat(x:Chat,db:Session=Depends(get_db)):
    return run_agent(db,x.session_id,x.customer_id,x.message)

@app.post("/api/approvals/{approval_id}/decision")
def approval(approval_id:str,x:ApprovalDecision,db:Session=Depends(get_db)):
    result=decide(db,approval_id,x.approved)
    if result=="not_found":raise HTTPException(404,"Approval not found")
    return {"approval_id":approval_id,"result":result}

@app.get("/api/cases")
def cases(db:Session=Depends(get_db)):
    rows=list(db.scalars(select(DisputeCase).order_by(DisputeCase.created_at.desc())))
    return [{"id":c.id,"transaction_id":c.transaction_id,"reason":c.reason,"status":c.status,"owner":c.owner,
             "agent_confidence":c.agent_confidence,"created_at":c.created_at} for c in rows]

@app.get("/api/audit/{session_id}")
def audit_events(session_id:str,db:Session=Depends(get_db)):
    rows=list(db.scalars(select(Audit).where(Audit.session_id==session_id).order_by(Audit.created_at)))
    return [{"event_type":x.event_type,"detail":x.detail,"created_at":x.created_at} for x in rows]
