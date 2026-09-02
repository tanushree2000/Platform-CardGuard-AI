import json
from app.core import settings

ALLOWED={"unrecognized_transaction","recognized_transaction","lock_card","policy_question","greeting","other"}

def heuristic(text:str):
    low=text.lower()
    if any(x in low for x in ["don't recognize","do not recognize","not mine","unknown charge","unauthorized","fraud"]):
        return {"intent":"unrecognized_transaction","confidence":0.94}
    if any(x in low for x in ["lock my card","freeze my card","block my card"]):
        return {"intent":"lock_card","confidence":0.96}
    if any(x in low for x in ["dispute policy","what is your policy","eligible","liability","how long"]):
        return {"intent":"policy_question","confidence":0.84}
    if low.strip() in {"hi","hello","hey"}:
        return {"intent":"greeting","confidence":0.96}
    return {"intent":"other","confidence":0.55}

def classify(text:str):
    cfg=settings()
    if not cfg.openai_api_key:
        return heuristic(text)
    try:
        from openai import OpenAI
        client=OpenAI(api_key=cfg.openai_api_key)
        prompt=("Classify this credit-card support message. Return only JSON with intent and confidence. "
                f"Allowed intents: {sorted(ALLOWED)}. Message: {text}")
        r=client.responses.create(model=cfg.openai_model,input=prompt)
        data=json.loads(r.output_text)
        return data if data.get("intent") in ALLOWED else heuristic(text)
    except Exception:
        return heuristic(text)
