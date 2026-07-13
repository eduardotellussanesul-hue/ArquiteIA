from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import dependencies

app = FastAPI(title='ArquiteIA Orchestrator')

class GemmRequest(BaseModel):
    N: int
    tile: int

@app.post('/estimate')
def estimate(req: GemmRequest):
    backend = dependencies.get_backend()
    if backend is None:
        raise HTTPException(status_code=500, detail='Backend not available')
    res = backend.estimate_gemm_cache(req.N, req.tile)
    return {'cache_misses': res.cache_misses, 'accesses': res.accesses}
