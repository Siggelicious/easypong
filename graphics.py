from sdl2 import *
from settings import *

class Graphics:
    def __init__(self, title, size):
        SDL_Init(SDL_INIT_VIDEO)
        self.window = SDL_CreateWindow(
                title.encode(), 
                SDL_WINDOWPOS_CENTERED,
                SDL_WINDOWPOS_CENTERED,
                *size,
                SDL_WINDOW_SHOWN
                )
        self.renderer = SDL_CreateRenderer(
            self.window,
            -1, 
            SDL_RENDERER_ACCELERATED
            )

    def __del__(self):
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        SDL_Quit()

    def fill_rect(self, rect, color):
        SDL_SetRenderDrawColor(self.renderer, *color)
        SDL_RenderFillRect(self.renderer, SDL_Rect(*rect))

    def present(self):
        SDL_RenderPresent(self.renderer)
