from pydantic import BaseModel
from typing import List, Dict, Any

class IncidentRequest(BaseModel):
    profile: str
    runId: str
    agentName: str
    publicMarker: str
    sensitive: Dict[str, Any]
    incident: Dict[str, Any]
    toolCatalog: List[Dict[str, Any]]
    policy: Dict[str, Any]

class Diagnosis(BaseModel):
    rootCause: str
    evidence: List[str]

class Dispatch(BaseModel):
    actionId: str
    callId: str
    phase: str
    toolName: str
    arguments: Dict[str, Any]
    evidence: List[str]
    attempt: int
    traceparent: str

class Approval(BaseModel):
    approvalId: str
    actionId: str
    toolName: str
    argumentsDigest: str

class ReceiptRequest(BaseModel):
    receiptId: str
    outcomes: List[Dict[str, Any]] = []
    approvals: List[Dict[str, Any]] = []

class IncidentState(BaseModel):
    runId: str
    status: str
    diagnosis: Diagnosis
    dispatches: List[Dispatch]
    approvals: List[Approval]
    actionLog: List[Any]
    receiptLog: List[Any]
    otlp: Dict[str, Any]

    def apply_receipt(self, receipt: ReceiptRequest):
        self.receiptLog.append(receipt.dict())
        # update status/dispatches depending on outcomes
