from typing import Tuple

from pygame import display, event, QUIT

from asteroids.colors import Colors
from asteroids.game import Game
from asteroids.ship import Ship


class AsteroidsGame(Game):
    def __init__(self, screenSize: Tuple[int, int], framesPerSecond: int):
        super().__init__(screenSize, framesPerSecond)

    def stop(self):
        self.isRunning = False

    def start(self):
        self.isRunning = True
        ship: Ship = Ship((200, 200), Colors.BLUE500.value)

        while self.isRunning:
            deltaTime = self.tick()

            # Update Game Objects
            ship.update(deltaTime)

            # Draw Game Objects
            self.screen.fill(Colors.BLACK.value)
            ship.draw(self.screen)
            display.update()

            for currentEvent in event.get():
                if currentEvent.type == QUIT:
                    self.stop()
