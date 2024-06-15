import json
from util import ensure_path

class History:
    def __init__(self, history_file: str = "history.json", history_length: int = 10 * 1000):
        self.history: list[dict] = None
        self.history_file = history_file
        self.history_length = history_length


    def connect(self):
        with open(self.history_file, "r") as f:
            self.history = json.load(f)

    def add(self, role, parts):
        self.history.append({"role": role, "parts": parts})

    def clear(self):
        self.history = []

    def get(self):
        return self.history

    def get_last(self):
        return self.history[-1]

    def dump(self):
        return self.history

    def dumpbuffer(self):
        if len(self.history) > self.history_length:
            self.history = self.history[-self.history_length:] # Truncate the history to the last 10,000 messages
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)
