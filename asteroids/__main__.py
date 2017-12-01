from asteroids.asteroidsgame import AsteroidsGame


def main():
    framesPerSecond: int = 60
    screenWidth: int = 1000
    screenHeight: int = 1000
    screenSize = (screenWidth, screenHeight)

    game: AsteroidsGame = AsteroidsGame(screenSize, framesPerSecond)
    game.start()


if __name__ == "__main__":
    main()
