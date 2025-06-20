from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from menu.navigator import Navigator

class Command(ABC):
    @abstractmethod
    def execute(self, navigator: "Navigator") -> None:
        pass
