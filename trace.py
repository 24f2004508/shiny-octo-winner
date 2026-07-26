import uuid
def build_trace(runId, marker, diagnosis, dispatches):
    trace_id = uuid.uuid4().hex
    spans = []

    def make_attr(key, val):
        return {"key": key, "value": {"stringValue": val}}

    # SERVER span
    spans.append({
        "name": "POST /v2/incidents",
        "kind": 2,
        "traceId": trace_id,
        "spanId": uuid.uuid4().hex,
        "attributes": [
            make_attr("ga5.run.id", runId),
            make_attr("ga5.public.marker", marker)
        ]
    })

    # CLIENT chat incident-plan
    spans.append({
        "name": "chat incident-plan",
        "kind": 3,
        "traceId": trace_id,
        "spanId": uuid.uuid4().hex,
        "attributes": [
            make_attr("ga5.run.id", runId),
            make_attr("ga5.public.marker", marker),
            make_attr("gen_ai.operation.name", "chat"),
            make_attr("gen_ai.request.model", "dummy-model")
        ]
    })

    # tool spans
    for d in dispatches:
        spans.append({
            "name": "execute_tool " + d.toolName,
            "kind": 1,
            "traceId": trace_id,
            "spanId": uuid.uuid4().hex,
            "attributes": [
                make_attr("ga5.run.id", runId),
                make_attr("ga5.public.marker", marker),
                make_attr("ga5.action.id", d.actionId),
                make_attr("gen_ai.tool.name", d.toolName),
                make_attr("gen_ai.tool.call.id", d.callId),
                make_attr("gen_ai.operation.name", "execute_tool")
            ]
        })

    return {"resourceSpans": [{"scopeSpans": [{"spans": spans}]}]}
