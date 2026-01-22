from typing import Any
from .base_action import BaseAction


class HelpAction(BaseAction):

    def execute(self, *args, **kwargs) -> Any:
        return self._game_engine.display_service.display_help()
