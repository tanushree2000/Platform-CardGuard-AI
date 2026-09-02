from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from app.guardrails import injection, redact
from app.model import classify
from app.policy import retrieve
from app.domain import find_tx,recent,create_case,request_approval,audit
from app.db import Card

class State(TypedDict,total=False):
    session_id:str;customer_id:str;message:str;intent:str;confidence:float
    response:str;transaction_id:str;case_id:str;approval_id:str;escalated:bool;trace:list

def run_agent(db,session_id,customer_id,message):
    def safety(s):
        if injection(s["message"]):
            audit(db,s["session_id"],"guardrail_block",{"reason":"prompt_injection"})
            return {**s,"message":redact(s["message"]),"intent":"blocked","confidence":1.0,
                    "response":"I can’t bypass account controls or reveal protected payment data.",
                    "trace":[{"step":"guardrail","result":"blocked"}]}
        return {**s,"message":redact(s["message"]),"trace":[{"step":"guardrail","result":"pass"}]}

    def route(s):
        if s.get("intent")=="blocked":return s
        r=classify(s["message"]);audit(db,s["session_id"],"intent",r)
        return {**s,**r,"trace":s["trace"]+[{"step":"intent",**r}]}

    def act(s):
        if s.get("intent")=="blocked":return s
        intent=s["intent"];conf=float(s["confidence"])
        if conf<.60:
            return {**s,"escalated":True,"response":"I’m not confident enough to automate this. I’m routing it to Fraud Operations.",
                    "trace":s["trace"]+[{"step":"escalate","reason":"low_confidence"}]}
        if intent=="greeting":
            return {**s,"response":"Hi. I can help review an unfamiliar transaction or request a card lock through an approval step."}
        if intent=="policy_question":
            p=retrieve(s["message"])[0]
            return {**s,"response":"Based on the governed demo policy: "+" ".join(p.splitlines()[:4]),
                    "trace":s["trace"]+[{"step":"policy_retrieval"}]}
        if intent=="lock_card":
            tx=recent(db,s["customer_id"])[0]; card=db.get(Card,tx.card_id)
            a=request_approval(db,s["session_id"],card.id,"Card state change requires explicit approval")
            return {**s,"approval_id":a.id,"response":"I prepared a synthetic card-lock request. It cannot execute until you approve it.",
                    "trace":s["trace"]+[{"step":"approval_gate","approval_id":a.id}]}
        if intent=="unrecognized_transaction":
            matches=find_tx(db,s["customer_id"],s["message"])
            if len(matches)!=1:
                lines="; ".join(f"{t.merchant} ${t.amount:.2f}" for t in recent(db,s["customer_id"])[:5])
                return {**s,"response":"I couldn't identify one transaction confidently. Recent synthetic transactions: "+lines}
            tx=matches[0]; case=create_case(db,s["customer_id"],tx.id,conf); card=db.get(Card,tx.card_id)
            a=request_approval(db,s["session_id"],card.id,f"Unrecognized transaction {tx.merchant} ${tx.amount:.2f}")
            audit(db,s["session_id"],"case_created",{"case_id":case.id})
            trace=s["trace"]+[{"step":"transaction_lookup","transaction_id":tx.id},{"step":"policy_retrieval"},
                              {"step":"case_created","case_id":case.id},{"step":"approval_gate","approval_id":a.id}]
            return {**s,"transaction_id":tx.id,"case_id":case.id,"approval_id":a.id,"trace":trace,
                    "response":f"I found {tx.merchant} for ${tx.amount:.2f}. I created synthetic dispute case {case.id}. A card-lock request is ready, but it requires your approval."}
        return {**s,"escalated":True,"response":"That request is outside the automated scope. I’m routing it to Fraud Operations."}

    g=StateGraph(State);g.add_node("safety",safety);g.add_node("route",route);g.add_node("act",act)
    g.add_edge(START,"safety");g.add_edge("safety","route");g.add_edge("route","act");g.add_edge("act",END)
    return g.compile().invoke({"session_id":session_id,"customer_id":customer_id,"message":message,"trace":[],"escalated":False})
