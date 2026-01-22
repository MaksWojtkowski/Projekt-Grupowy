from typing import Optional


class Route:

    def __init__(self, command: str, action_class: str, method: Optional[str] = None):
        self._command = command
        self._action_class = action_class
        self._method = method or 'execute'

    @property
    def command(self) -> str:
        return self._command

    @property
    def action_class(self) -> str:
        return self._action_class

    @property
    def method(self) -> str:
        return self._method

    def matches(self, input_command: str) -> bool:
        return input_command.lower() == self._command.lower()

    def __repr__(self) -> str:
        return f"Route(command='{self._command}', action='{self._action_class}', method='{self._method}')"
