import pygame as pg

from game.run_game import Game

pg.init()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()