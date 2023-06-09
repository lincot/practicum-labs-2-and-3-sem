from random import randint
from tkinter import *
import time
from enum import Enum, auto


TINY_N = 300
SMALL_N = 200
LARGE_N = 100
SCREEN_SIZE = 700


class RaindropSize(Enum):
    TINY = auto()
    SMALL = auto()
    LARGE = auto()


class Raindrop:
    def __init__(self, size):
        self.x = randint(0, SCREEN_SIZE)
        self.y = randint(-100, SCREEN_SIZE)
        match size:
            case RaindropSize.TINY:
                self.height = randint(1, 10)
                self.speed = randint(3, 5)
                self.color = "MidnightBlue"
            case RaindropSize.SMALL:
                self.height = randint(11, 25)
                self.speed = randint(9, 12)
                self.color = "MediumSlateBlue"
            case RaindropSize.LARGE:
                self.height = randint(26, 50)
                self.speed = randint(15, 25)
                self.color = "LightSteelBlue"


def main():
    c = Canvas(Tk(), width=SCREEN_SIZE, height=SCREEN_SIZE, background="black")
    c.pack()

    raindrops = (
        [Raindrop(RaindropSize.TINY) for _ in range(TINY_N)]
        + [Raindrop(RaindropSize.SMALL) for _ in range(SMALL_N)]
        + [Raindrop(RaindropSize.LARGE) for _ in range(LARGE_N)]
    )

    while True:
        figures = []
        for raindrop in raindrops:
            figures.append(
                c.create_oval(
                    raindrop.x,
                    raindrop.y,
                    raindrop.x + 8 * raindrop.height / 50,
                    raindrop.y + raindrop.height,
                    fill=raindrop.color,
                )
            )
            raindrop.y += raindrop.speed
            if raindrop.y >= SCREEN_SIZE:
                raindrop.y = -raindrop.height

        c.update()
        time.sleep(1 / 60)
        for figure in figures:
            c.delete(figure)


if __name__ == "__main__":
    main()
