import uuid

def build_trace(runId, marker, diagnosis, dispatches):
    trace_id = uuid.uuid4().hex
    spans = []

    # SERVER span
    spans.append({
        "name":"POST /v2/incidents",
        "kind":2,
        "traceId":trace_id,
        "spanId":uuid.uuid4().hex,
        "attributes":{"ga5.run.id":runId,"ga5.public.marker":marker}
    })

    # CLIENT chat incident-plan
    spans.append({
        "name":"chat incident-plan",
        "kind":3,
        "traceId":trace_id,
        "spanId":uuid.uuid4().hex,
        "attributes":{
            "ga5.run.id":runId,
            "ga5.public.marker":marker,
            "gen_ai.operation.name":"chat",
            "gen_ai.request.model":"dummy-model"
        }
    })

    # tool spans
    for d in dispatches:
        spans.append({
            "name":"execute_tool "+d.toolName,
            "kind":1,
            "traceId":trace_id,
            "spanId":uuid.uuid4().hex,
            "attributes":{
                "ga5.run.id":runId,
                "ga5.public.marker":marker,
                "ga5.action.id":d.actionId,
                "gen_ai.tool.name":d.toolName,
                "gen_ai.tool.call.id":d.callId,
                "gen_ai.operation.name":"execute_tool"
            }
        })

    return {"resourceSpans":[{"scopeSpans":[{"spans":spans}]}]}
