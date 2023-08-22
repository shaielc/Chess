from enum import Enum

class EventType(Enum):
    BOARD=0
    PROMOTION=1
    MOVE=2

class EventSourceType(Enum):
    UI=0
    AI=1

class Event:
    def __init__(self, event_type:EventType, source: EventSourceType, payload=None) -> None:
        self.event_type = event_type
        self.payload = payload
        self.source = source
