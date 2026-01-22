from typing import Any
from .base_action import BaseAction


class QuitAction(BaseAction):

    def execute(self, *args, **kwargs) -> Any:
        return "__QUIT__"
