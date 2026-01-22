from typing import Any
from .base_action import BaseAction


class ShopAction(BaseAction):

    def execute(self, *args, **kwargs) -> Any:
        return self._game_engine.open_shop()

    def purchase(self, choice: str) -> Any:
        return self._game_engine.purchase_upgrade(choice)
