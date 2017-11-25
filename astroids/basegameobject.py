from abc import ABC, abstractmethod
from typing import Tuple

from numpy import ndarray, array
from pygame.surface import Surface


class BaseGameObject(ABC):
    def __init__(self, position: Tuple[int, int]):
        self.position: ndarray = array(position)

    def setPosition(self, x, y):
        self.position = array([x, y])

    @abstractmethod
    def update(self, deltaTime: float) -> None:
        ...

    @abstractmethod
    def draw(self, surface: Surface) -> None:
        ...
