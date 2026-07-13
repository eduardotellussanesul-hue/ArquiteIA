import json
import random
from pathlib import Path

def simple_search(cases_file='data/cases.json'):
    p = Path(cases_file)
    if not p.exists():
        print('No cases.json found, run dataset_generator')
        return
    cases = json.loads(p.read_text())
    # trivial heuristic: prefer largest tile that divides N
    results = []
    for c in cases:
        N = c['N']; t = c['tile']
        score = 0
        if N % t == 0:
            score = random.random() * 0.1
        else:
            score = 1.0 + random.random()
        results.append({'N':N,'tile':t,'score':score})
    results.sort(key=lambda x: x['score'])
    out = Path('results.json')
    out.write_text(json.dumps(results, indent=2))
    print('Wrote results.json')

if __name__ == '__main__':
    simple_search()
