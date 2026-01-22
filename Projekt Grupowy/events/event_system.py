import random
from typing import List, Type
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from events.sanitary_inspection import SanitaryInspection
from events.oven_breakdown import OvenBreakdown


class EventSystem:

    def __init__(self):
        self._event_classes: List[Type] = [
            SanitaryInspection,
            OvenBreakdown
        ]
        self._active_events: List = []

    def trigger_random_event(self, game_engine) -> str:
        messages = []
        for event_class in self._event_classes:
            event = event_class()
            if random.random() < event.occurrence_chance:
                self._active_events.append(event)
                messages.append(event.trigger(game_engine))

        return "\n".join(messages) if messages else ""

    def remove_expired_events(self, game_engine) -> None:
        for event in self._active_events:
            event.remove_effect(game_engine)
        self._active_events = []

    def get_active_events(self) -> List:
        return self._active_events.copy()

    def has_active_events(self) -> bool:
        return len(self._active_events) > 0
