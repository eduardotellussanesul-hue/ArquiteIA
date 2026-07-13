import numpy as np
from pathlib import Path

def generate_gemm_cases(sizes=(128, 256, 512, 1024), tiles=(4,8,16,32), out_dir='data'):
    p = Path(out_dir)
    p.mkdir(parents=True, exist_ok=True)
    rows = []
    for N in sizes:
        for t in tiles:
            # placeholder features: N, tile
            rows.append({'N': int(N), 'tile': int(t)})
    import json
    (p / 'cases.json').write_text(json.dumps(rows, indent=2))
    return rows

if __name__ == '__main__':
    print('Generating sample GEMM cases...')
    print(generate_gemm_cases())
