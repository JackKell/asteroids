import pygame
from pygame.time import Clock
from pygame import display, Surface, event, QUIT
from typing import Tuple


from astroids.colors import Colors
from astroids.ship import Ship
from astroids.utility import getRectangle


class Game(object):
    def __init__(self, screenSize: Tuple[int, int], framesPerSecond: int):
        self.screenSize: Tuple[int, int] = screenSize
        self.screen: Surface = display.set_mode(screenSize)
        self.framesPerSecond: int = framesPerSecond
        self.clock: Clock = Clock()
        self.isRunning: bool = False
        pygame.init()

    def tick(self):
        return self.clock.tick(self.framesPerSecond) / 1000

    def start(self):
        self.isRunning = True
        ship: Ship = Ship((50, 50), Colors.BLUE500.value)

        rotationRate = 15
        rotation = 0

        while self.isRunning:
            deltaTime = self.tick()
            rotation += rotationRate * deltaTime
            rotation %= 360

            # Update Game Objects
            ship.update(deltaTime)

            # Draw Game Objects
            self.screen.fill(Colors.BLACK.value)
            ship.draw(self.screen)
            rectanglePoints = getRectangle((200, 200), rotation, (100, 100))
            # polygonPoints = getRegularPolygon((400, 200), 6, 100, 0)
            pygame.draw.polygon(self.screen, Colors.BLUE500.value, rectanglePoints)
            # pygame.draw.polygon(self.screen, Colors.BLUE500.value, polygonPoints)
            display.update()

            for currentEvent in event.get():
                if currentEvent.type == QUIT:
                    self.stop()

    def stop(self):
        self.isRunning = False
