from typing import Any
from .base_action import BaseAction


class StartDayAction(BaseAction):

    def execute(self, *args, **kwargs) -> Any:
        return self._game_engine.start_day()
