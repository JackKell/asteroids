import math
from typing import Tuple, List

import numpy
import pygame
from numpy import ndarray, array
from numpy.linalg import norm
from pygame import draw
from pygame.surface import Surface

from asteroids.basegameobject import BaseGameObject
from asteroids.colors import Colors
from asteroids.meter import Meter
from asteroids.utility import getPointFromPolarCoordinate, drawArrow, getMagnitude


class Ship(BaseGameObject):
    def __init__(self, position: Tuple[int, int], color: Colors, size: int = 50):
        super().__init__(position)
        self.color: Colors = color
        self.velocity: array = array([0, 0])
        self.maxSpeed: float = 500
        self.acceleration: float = 0
        self.maxAcceleration: float = 100
        self.rotation: float = 0
        self.rotationalVelocity: float = 0
        self.maxRotationalVelocity: float = 360
        self.rotationalAcceleration: float = 0
        self.maxRotationalAcceleration: float = 360
        self.size: float = size
        self.rotationVelocityMeter: Meter = Meter((20, 20), (500, 19), Colors.GRAY50.value, Colors.RED500.value,
                                                  -1 * self.maxRotationalVelocity, self.maxRotationalVelocity,
                                                  self.rotationalVelocity)
        self.speedMeter: Meter = Meter((20, 40), (500, 19), Colors.GRAY50.value, Colors.WHITE.value, 0, self.maxSpeed,
                                       self.speed)

    @property
    def speed(self):
        return math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

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
    def heading(self):
        return array(getPointFromPolarCoordinate((0, 0), 1, math.radians(self.rotation)))

    def move(self, deltaMovement: ndarray) -> None:
        self.position = self.position + deltaMovement

    def rotate(self, deltaRotation: float) -> None:
        self.rotation = (self.rotation + deltaRotation) % 360

    def accelerate(self, deltaVelocity: float) -> None:
        self.velocity = self.velocity + self.heading * deltaVelocity
        if self.speed > self.maxSpeed:
            self.velocity = self.velocity / norm(self.velocity) * self.maxSpeed

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
        # TODO: pass keys down instead of getting them here
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.acceleration = self.maxAcceleration
        elif keys[pygame.K_DOWN]:
            self.acceleration = -1 * self.maxAcceleration
        else:
            self.acceleration = 0

        if keys[pygame.K_LEFT]:
            self.rotationalAcceleration = -1 * self.maxRotationalAcceleration
        elif keys[pygame.K_RIGHT]:
            self.rotationalAcceleration = self.maxRotationalAcceleration
        else:
            self.rotationalAcceleration = 0

        print(self.acceleration, self.rotationalAcceleration, self.velocity, self.rotationalVelocity)
        self._updateVelocity(deltaTime)
        self._updateRotationalVelocity(deltaTime)
        self._updatePosition(deltaTime)
        self._updateRotation(deltaTime)
        self.rotationVelocityMeter.value = self.rotationalVelocity
        self.speedMeter.value = self.speed

    def _drawShip(self, surface: Surface) -> None:
        draw.polygon(surface, self.color, self.shipPoints)

    def _drawFire(self, surface: Surface) -> None:
        backOfShip = getPointFromPolarCoordinate(self.position, self.size // 4, math.radians(180 + self.rotation))
        fireSize = self.size
        points: List = [
            backOfShip,
            getPointFromPolarCoordinate(backOfShip, fireSize, math.radians(145 + self.rotation)),
            getPointFromPolarCoordinate(backOfShip, fireSize // 2, math.radians(165 + self.rotation)),
            getPointFromPolarCoordinate(backOfShip, fireSize, math.radians(180 + self.rotation)),
            getPointFromPolarCoordinate(backOfShip, fireSize // 2, math.radians(195 + self.rotation)),
            getPointFromPolarCoordinate(backOfShip, fireSize, math.radians(215 + self.rotation)),
        ]
        draw.polygon(surface, Colors.RED500.value, points)

    def draw(self, surface: Surface) -> None:
        super().draw(surface)
        if self.acceleration != 0:
            self._drawFire(surface)
        self._drawShip(surface)
        self.rotationVelocityMeter.draw(surface)
        self.speedMeter.draw(surface)

