import importlib
import inspect
from typing import Dict, List, Type, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from upgrades import BaseUpgrade, Oven, ChefTraining, IngredientQuality, Marketing, TablesUpgrade
from exceptions import InsufficientFundsException, ReflectionException


class UpgradeShop:

    def __init__(self):
        self._available_upgrades: Dict[str, BaseUpgrade] = {}
        self._load_upgrades()

    def _load_upgrades(self) -> None:
        upgrade_classes = self._discover_upgrade_classes()

        for upgrade_class in upgrade_classes:
            try:
                instance = upgrade_class()
                self._available_upgrades[instance.name] = instance
            except Exception:
                pass

    def _discover_upgrade_classes(self) -> List[Type[BaseUpgrade]]:
        try:
            module = importlib.import_module('upgrades')
            classes = []

            for name in dir(module):
                obj = getattr(module, name)
                if (inspect.isclass(obj) and
                    issubclass(obj, BaseUpgrade) and
                    obj is not BaseUpgrade):
                    classes.append(obj)

            return classes
        except ImportError as e:
            raise ReflectionException("upgrades", str(e))

    def get_upgrades(self) -> Dict[str, BaseUpgrade]:
        return self._available_upgrades.copy()

    def get_upgrade(self, name: str) -> BaseUpgrade:
        for upgrade_name, upgrade in self._available_upgrades.items():
            if upgrade_name.lower() == name.lower():
                return upgrade
        return None

    def get_upgrade_by_index(self, index: int) -> BaseUpgrade:
        upgrades = list(self._available_upgrades.values())
        if 0 <= index < len(upgrades):
            return upgrades[index]
        return None

    def purchase_upgrade(self, upgrade_name: str, current_money: float) -> tuple:
        upgrade = self.get_upgrade(upgrade_name)

        if upgrade is None:
            return (False, 0.0, "Ulepszenie nie istnieje")

        if not upgrade.can_upgrade():
            return (False, 0.0, f"{upgrade.name} osiągnęło maksymalny poziom")

        cost = upgrade.get_upgrade_cost()

        if current_money < cost:
            raise InsufficientFundsException(cost, current_money)

        upgrade.upgrade()
        return (True, cost, f"\n{'='*40}\n✓ ULEPSZENIE ZOSTAŁO ZAKUPIONE!\n{'='*40}\n{upgrade.name} → Poziom {upgrade.get_level()}\nKoszt: {cost:.2f} zł")

    def display_shop(self, current_money: float) -> str:
        lines = [
            f"\n{'='*50}",
            "SKLEP ULEPSZEŃ",
            f"Dostępne środki: {current_money:.2f} zł",
            f"{'='*50}"
        ]

        for i, (name, upgrade) in enumerate(self._available_upgrades.items(), 1):
            if upgrade.can_upgrade():
                cost = upgrade.get_upgrade_cost()
                affordable = "✓" if current_money >= cost else "✗"
                lines.append(f"{i}. {upgrade.name} (Poz. {upgrade.get_level()}) - {cost:.2f} zł [{affordable}]")
                lines.append(f"   {upgrade.get_effect_description()}")
            else:
                lines.append(f"{i}. {upgrade.name} - MAKSYMALNY POZIOM")

        lines.append(f"{'='*50}")
        lines.append("Wpisz numer ulepszenia lub 'wyjdz' aby wyjść")

        return "\n".join(lines)
