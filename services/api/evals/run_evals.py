import json
from pathlib import Path
from app.guardrails import injection
from app.model import heuristic
cases=json.loads((Path(__file__).parent/'golden_dataset.json').read_text())
passed=0
for c in cases:
    pred='blocked' if injection(c['input']) else heuristic(c['input'])['intent']
    ok=pred==c['expected'];passed+=int(ok)
    print(('PASS' if ok else 'FAIL'),c['input'],'->',pred)
print(f'{passed}/{len(cases)} passed')
raise SystemExit(0 if passed==len(cases) else 1)
