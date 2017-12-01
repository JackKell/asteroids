from abc import ABC, abstractmethod
from typing import Tuple

import pygame
from pygame import display, Surface
from pygame.time import Clock


class Game(ABC):
    def __init__(self, screenSize: Tuple[int, int], framesPerSecond: int):
        self.screenSize: Tuple[int, int] = screenSize
        self.screen: Surface = display.set_mode(screenSize)
        self.framesPerSecond: int = framesPerSecond
        self.clock: Clock = Clock()
        self.isRunning: bool = False
        pygame.init()

    def tick(self) -> float:
        return self.clock.tick(self.framesPerSecond) / 1000

    @abstractmethod
    def stop(self):
        ...

    @abstractmethod
    def start(self):
        ...

