from astroids.game import Game


def main():
    framesPerSecond = 60
    screenWidth: int = 1000
    screenHeight: int = 1000
    screenSize = (screenWidth, screenHeight)

    game: Game = Game(screenSize, framesPerSecond)
    game.start()


if __name__ == "__main__":
    main()
