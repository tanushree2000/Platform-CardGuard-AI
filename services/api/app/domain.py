import uuid, json
from sqlalchemy import select
from app.db import Card, Transaction, DisputeCase, Approval, Audit

def recent(db, customer_id):
    return list(db.scalars(select(Transaction).join(Card).where(Card.customer_id==customer_id).order_by(Transaction.occurred_at.desc())))

def find_tx(db, customer_id, q):
    q=q.lower(); out=[]
    for t in recent(db,customer_id):
        if t.merchant.lower() in q or any(w in q for w in t.merchant.lower().split()) or f"{t.amount:.2f}" in q:
            out.append(t)
    return out

def create_case(db,customer_id,tx_id,confidence):
    existing=db.scalar(select(DisputeCase).where(DisputeCase.transaction_id==tx_id,DisputeCase.status!="closed"))
    if existing:return existing
    c=DisputeCase(id="FRD-"+uuid.uuid4().hex[:8].upper(),customer_id=customer_id,transaction_id=tx_id,
                  reason="Cardholder reports transaction as unrecognized",status="open",owner="Fraud Operations",
                  agent_confidence=confidence)
    db.add(c);db.commit();db.refresh(c);return c

def request_approval(db,session_id,resource_id,reason):
    a=Approval(id="APR-"+uuid.uuid4().hex[:8].upper(),session_id=session_id,action="lock_card",
               resource_id=resource_id,status="pending",reason=reason)
    db.add(a);db.commit();db.refresh(a);return a

def audit(db,session_id,event_type,detail):
    a=Audit(id="AUD-"+uuid.uuid4().hex[:10].upper(),session_id=session_id,event_type=event_type,detail=json.dumps(detail,default=str))
    db.add(a);db.commit()

def decide(db,approval_id,approved):
    a=db.get(Approval,approval_id)
    if not a:return "not_found"
    if a.status!="pending":return "already_decided"
    if not approved:
        a.status="declined";db.commit();return "declined"
    if a.action=="lock_card":
        card=db.get(Card,a.resource_id)
        if not card:return "resource_not_found"
        card.status="locked";a.status="approved";db.commit();return "approved"
    return "unsupported"
