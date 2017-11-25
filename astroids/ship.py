import math
from typing import Tuple, List

import numpy
import pygame
from numpy import ndarray, array
from pygame import draw
from pygame.surface import Surface

from astroids.basegameobject import BaseGameObject
from astroids.colors import Colors
from astroids.utility import getPointFromPolarCoordinate, drawArrow


# TODO: fix movement, it feels a little bit off right now. I don't know what is wrong
class Ship(BaseGameObject):
    def __init__(self, position: Tuple[int, int], color: Colors, size: int = 50):
        super().__init__(position)
        self.color: Colors = color
        self.velocity: ndarray = array([0, 0])
        self.maxVelocity = 200
        self.acceleration = 0
        self.maxAcceleration = 500
        self.rotation = 45
        self.rotationalVelocity = 0
        self.maxRotationalVelocity = 100
        self.rotationalAcceleration = 0
        self.maxRotationalAcceleration = 360
        self.size = size

    @property
    def shipPoints(self):
        points: List = [
            getPointFromPolarCoordinate(self.position, self.size, math.radians(self.rotation)),
            getPointFromPolarCoordinate(self.position, self.size, math.radians(225 + self.rotation)),
            getPointFromPolarCoordinate(self.position, self.size // 4, math.radians(180 + self.rotation)),
            getPointFromPolarCoordinate(self.position, self.size, math.radians(135 + self.rotation))
        ]
        return points

    @property
    def direction(self):
        return array(getPointFromPolarCoordinate((0, 0), 1, math.radians(self.rotation)))

    def move(self, deltaMovement: ndarray) -> None:
        self.position = self.position + deltaMovement

    def rotate(self, deltaRotation: float) -> None:
        self.rotation = (self.rotation + deltaRotation) % 360

    def accelerate(self, deltaVelocity: float) -> None:
        self.velocity = self.velocity + self.direction * deltaVelocity
        self.velocity = numpy.clip(self.velocity, self.maxVelocity * -1, self.maxVelocity)

    def rotationallyAccelerate(self, deltaRotationalVelocity: float) -> None:
        self.rotationalVelocity = self.rotationalVelocity + deltaRotationalVelocity
        self.rotationalVelocity = numpy.clip(self.rotationalVelocity,
                                             self.maxRotationalVelocity * -1,
                                             self.maxRotationalVelocity)

    def _updateVelocity(self, deltaTime: float) -> None:
        deltaVelocity: float = self.acceleration * deltaTime
        self.accelerate(deltaVelocity)

    def _updatePosition(self, deltaTime: float) -> None:
        deltaMovement: ndarray = self.velocity * deltaTime
        self.move(deltaMovement)

    def _updateRotation(self, deltaTime: float):
        deltaRotation: float = self.rotationalVelocity * deltaTime
        self.rotate(deltaRotation)

    def _updateRotationalVelocity(self, deltaTime: float):
        deltaRotationalVelocity: float = self.rotationalAcceleration * deltaTime
        self.rotationallyAccelerate(deltaRotationalVelocity)

    def update(self, deltaTime: float) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.acceleration = self.maxAcceleration
                elif event.key == pygame.K_DOWN:
                    self.acceleration = self.maxAcceleration * -1
                if event.key == pygame.K_LEFT:
                    self.rotationalAcceleration = self.maxRotationalAcceleration * -1
                elif event.key == pygame.K_RIGHT:
                    self.rotationalAcceleration = self.maxRotationalAcceleration
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.acceleration = 0
                elif event.key == pygame.K_DOWN:
                    self.acceleration = 0
                if event.key == pygame.K_LEFT:
                    self.rotationalAcceleration = 0
                elif event.key == pygame.K_RIGHT:
                    self.rotationalAcceleration = 0
        print(self.acceleration, self.rotationalAcceleration, self.velocity, self.rotationalVelocity)
        self._updateVelocity(deltaTime)
        self._updateRotationalVelocity(deltaTime)
        self._updatePosition(deltaTime)
        self._updateRotation(deltaTime)

    def _drawShip(self, surface: Surface) -> None:
        draw.polygon(surface, self.color, self.shipPoints)

    # TODO: Move this progress bar to its own class
    def _drawSpeedBar(self, surface: Surface, startPoint, height, width):
        rotationSpeedRatio = abs(self.rotationalVelocity / self.maxRotationalVelocity)
        draw.line(surface,
                  Colors.GRAY500.value,
                  startPoint,
                  (startPoint[0] + width, startPoint[1]),
                  height)
        draw.line(surface,
                  Colors.GREEN500.value,
                  startPoint,
                  ((startPoint[0] + width) * rotationSpeedRatio, startPoint[1]),
                  height)

    def draw(self, surface: Surface) -> None:
        self._drawShip(surface)
        drawArrow(surface, Colors.RED500.value, self.position, self.position + self.velocity, (5, 7))
        self._drawSpeedBar(surface, (20, 20), 20, 700)

