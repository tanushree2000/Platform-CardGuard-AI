import re
PATTERNS=[
    r"ignore (all|your|previous).*(instructions|rules|controls)",
    r"reveal.*(system prompt|full card|cvv|password|secret)",
    r"bypass.*(approval|guardrail|policy|control)"
]
def injection(text:str)->bool:
    return any(re.search(p,text.lower()) for p in PATTERNS)
def redact(text:str)->str:
    return re.sub(r"\b(?:\d[ -]*?){13,19}\b","[REDACTED_CARD]",text)
