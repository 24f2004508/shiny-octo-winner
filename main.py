from fastapi import FastAPI, Request, HTTPException
from models import IncidentRequest, ReceiptRequest, IncidentState
from state import StateStore
from planner import plan_diagnosis
from trace import build_trace

app = FastAPI()
store = StateStore()

@app.post("/v2/incidents")
async def create_incident(req: IncidentRequest):
    if req.profile != "ga5-incident-agent/v2":
        raise HTTPException(status_code=400, detail="Unsupported profile")

    # run diagnosis
    diagnosis, dispatches = plan_diagnosis(req)

    state = IncidentState(
        runId=req.runId,
        status="waiting",
        diagnosis=diagnosis,
        dispatches=dispatches,
        approvals=[],
        actionLog=dispatches,
        receiptLog=[],
        otlp=build_trace(req.runId, req.publicMarker, diagnosis, dispatches)
    )
    store.save(req.runId, state)
    return state.dict()

@app.post("/v2/incidents/{runId}/receipts")
async def post_receipt(runId: str, req: ReceiptRequest):
    state = store.load(runId)
    if not state:
        raise HTTPException(status_code=404, detail="Run not found")

    # update state with receipt outcomes
    state.apply_receipt(req)
    store.save(runId, state)
    return state.dict()

@app.get("/v2/incidents/{runId}")
async def get_incident(runId: str):
    state = store.load(runId)
    if not state:
        raise HTTPException(status_code=404, detail="Run not found")
    return state.dict()
