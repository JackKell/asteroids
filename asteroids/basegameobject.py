from abc import ABC, abstractmethod
from typing import Tuple

from numpy import ndarray, array
from pygame.surface import Surface


class BaseGameObject(ABC):
    def __init__(self, position: Tuple[int, int]):
        self.position: ndarray = array(position)

    def setPosition(self, x, y):
        self.position[0] = x
        self.position[1] = y

    @abstractmethod
    def update(self, deltaTime: float) -> None:
        pass

    @abstractmethod
    def draw(self, surface: Surface) -> None:
        pass
