import json, os
from models import IncidentState

class StateStore:
    def __init__(self, path="state.json"):
        self.path = path
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({}, f)

    def save(self, runId, state: IncidentState):
        data = self._load_all()
        data[runId] = state.dict()
        with open(self.path, "w") as f:
            json.dump(data, f)

    def load(self, runId):
        data = self._load_all()
        if runId in data:
            return IncidentState(**data[runId])
        return None

    def _load_all(self):
        with open(self.path) as f:
            return json.load(f)
