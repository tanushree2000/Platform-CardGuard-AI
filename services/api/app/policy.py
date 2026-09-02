from pathlib import Path
import re
FILE=Path(__file__).resolve().parents[1]/"data"/"fraud_policy.md"
def retrieve(query:str):
    sections=[x.strip() for x in FILE.read_text().split("## ") if x.strip()]
    q=set(re.findall(r"[A-Za-z]+",query.lower()))
    scored=sorted(((len(q & set(re.findall(r"[A-Za-z]+",s.lower()))),s) for s in sections), reverse=True)
    return [s for score,s in scored[:2] if score>0] or sections[:1]
