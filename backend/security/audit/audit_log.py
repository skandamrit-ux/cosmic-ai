
import time

_events = []

def record(event, details=None):
    item = {
        "timestamp": time.time(),
        "event": event,
        "details": details or {}
    }
    _events.append(item)
    return item

def recent(limit=100):
    return _events[-limit:]
