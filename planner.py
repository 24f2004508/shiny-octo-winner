import uuid
from models import Diagnosis, Dispatch

def plan_diagnosis(req):
    # Simplified: pick first allowed root cause and two evidence IDs
    root = req.incident["allowedRootCauses"][0]
    evidence = ["ev_1", "ev_2"]

    diagnosis = Diagnosis(rootCause=root, evidence=evidence)

    dispatches = [
        Dispatch(
            actionId=str(uuid.uuid4()),
            callId=str(uuid.uuid4()),
            phase="diagnostic",
            toolName="query_metrics",
            arguments={"service": req.incident["service"]},
            evidence=[evidence[0]],
            attempt=1,
            traceparent="00-"+uuid.uuid4().hex+"-"+uuid.uuid4().hex+"-01"
        )
    ]
    return diagnosis, dispatches
