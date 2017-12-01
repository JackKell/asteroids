from typing import Tuple

import numpy
from numpy import clip, array
from pygame import draw
from pygame.surface import Surface

from asteroids.basegameobject import BaseGameObject
from asteroids.types import Point


# noinspection PyAttributeOutsideInit
class Meter(BaseGameObject):
    def __init__(self, position: Point, size: Point, backgroundColor: Tuple[int, int, int],
                 progressColor: Tuple[int, int, int], minValue: float = 0, maxValue: float = 1, value: float = 0,
                 startValue: float = 0):
        super().__init__(position)
        self.size: Point = size
        self.backgroundColor: Tuple[int, int, int] = backgroundColor
        self.valueColor: Tuple[int, int, int] = progressColor
        self.minValue: float = minValue
        self.maxValue: float = maxValue
        self.value: float = value
        self.startValue: float = startValue

    def _getPercentage(self, value):
        return (value - self.minValue) / (self.maxValue - self.minValue)

    def _getPosition(self, value):
        percentage: float = self._getPercentage(value)
        return array((self.position[0] + self.size[0] * percentage, self.position[1])).round()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = clip(value, self.minValue, self.maxValue)

    def draw(self, surface: Surface) -> None:
        # Draw Background Meter
        draw.line(
            surface,
            self.backgroundColor,
            self.position,
            self._getPosition(self.maxValue),
            self.size[1])
        # Draw Progress Meter
        startValuePosition = self._getPosition(self.startValue)
        currentValuePosition = self._getPosition(self.value)
        if not numpy.allclose(startValuePosition, currentValuePosition, atol=1.e-2, rtol=1.e-2):
            draw.line(
                surface,
                self.valueColor,
                self._getPosition(self.startValue),
                self._getPosition(self.value),
                self.size[1])

    def update(self, deltaTime: float) -> None:
        pass
