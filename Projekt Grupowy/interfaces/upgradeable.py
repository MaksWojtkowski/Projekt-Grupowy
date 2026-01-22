from abc import ABC, abstractmethod


class IUpgradeable(ABC):

    @abstractmethod
    def upgrade(self) -> None:
        pass

    @abstractmethod
    def get_upgrade_cost(self) -> float:
        pass

    @abstractmethod
    def get_level(self) -> int:
        pass
