from graphics import Graphics
from arena import Arena
from sdl2 import *
import sys
from settings import *
from easytypes import Vec2

def main():
    SDL_Init(SDL_INIT_EVERYTHING)
    graphics = Graphics("Easy Pong", WINDOW_SIZE)
    arena = Arena(Vec2(*ARENA_SIZE), graphics)
    arena.play()

if __name__ == "__main__":
    sys.exit(main())
