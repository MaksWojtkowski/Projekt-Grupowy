import importlib
import inspect
from typing import List, Optional, Any, Dict, Type
from .route import Route
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exceptions import RouteNotFoundException, ReflectionException


class Router:

    def __init__(self, routes: List[Route], game_engine):
        self._routes = routes
        self._game_engine = game_engine
        self._action_cache: Dict[str, Type] = {}

    def find_route(self, command: str) -> Optional[Route]:
        command_base = command.split()[0] if command else ""

        for route in self._routes:
            if route.matches(command_base):
                return route

        return None

    def dispatch(self, command: str, *args) -> Any:
        route = self.find_route(command)

        if not route:
            raise RouteNotFoundException(command)

        action_class = self._get_action_class(route.action_class)
        action_instance = self._create_instance(action_class)
        result = self._invoke_method(action_instance, route.method, *args)

        return result

    def _get_action_class(self, class_name: str) -> Type:
        if class_name in self._action_cache:
            return self._action_cache[class_name]

        try:
            module = importlib.import_module('actions')

            if hasattr(module, class_name):
                action_class = getattr(module, class_name)
                self._action_cache[class_name] = action_class
                return action_class
            else:
                raise ReflectionException(class_name, "Klasa nie istnieje w module")

        except ImportError as e:
            raise ReflectionException(class_name, str(e))

    def _create_instance(self, action_class: Type) -> Any:
        try:
            signature = inspect.signature(action_class.__init__)
            parameters = list(signature.parameters.keys())

            if 'game_engine' in parameters:
                instance = action_class(self._game_engine)
            else:
                instance = action_class()

            return instance

        except Exception as e:
            raise ReflectionException(action_class.__name__, f"Błąd tworzenia instancji: {e}")

    def _invoke_method(self, instance: Any, method_name: str, *args) -> Any:
        try:
            if not hasattr(instance, method_name):
                raise ReflectionException(
                    instance.__class__.__name__,
                    f"Metoda '{method_name}' nie istnieje"
                )

            method = getattr(instance, method_name)

            if not callable(method):
                raise ReflectionException(
                    instance.__class__.__name__,
                    f"'{method_name}' nie jest metodą"
                )

            if args:
                return method(*args)
            else:
                return method()

        except TypeError as e:
            raise ReflectionException(instance.__class__.__name__, str(e))
        except Exception as e:
            if isinstance(e, ReflectionException):
                raise
            raise ReflectionException(instance.__class__.__name__, method_name)

    def get_class_info(self, class_name: str) -> Dict[str, Any]:
        action_class = self._get_action_class(class_name)

        info = {
            'name': action_class.__name__,
            'module': action_class.__module__,
            'bases': [base.__name__ for base in action_class.__bases__],
            'methods': [],
            'attributes': []
        }

        for name, member in inspect.getmembers(action_class):
            if not name.startswith('_'):
                if inspect.isfunction(member) or inspect.ismethod(member):
                    info['methods'].append(name)
                elif not callable(member):
                    info['attributes'].append(name)

        return info

    def list_routes(self) -> List[str]:
        return [route.command for route in self._routes]
