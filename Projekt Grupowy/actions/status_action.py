from typing import Any
from .base_action import BaseAction


class StatusAction(BaseAction):

    def execute(self, *args, **kwargs) -> Any:
        return self._game_engine.get_status()
