from sdl2 import *
from sdl2.sdlttf import *
from settings import *

class Graphics:
    def __init__(self, title, size):
        SDL_Init(SDL_INIT_VIDEO)
        TTF_Init()
        self.font = TTF_OpenFont(b"8bit16.ttf", 24)
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
        SDL_Quit()

    def render_text(self, text, rect, color):
        text_surface = TTF_RenderText_Solid(self.font, text.encode(), SDL_Color(*color))
        text_texture = SDL_CreateTextureFromSurface(self.renderer, text_surface)
        SDL_RenderCopy(self.renderer, text_texture, None, SDL_Rect(*rect)) 

    def fill_rect(self, rect, color):
        SDL_SetRenderDrawColor(self.renderer, *color)
        SDL_RenderFillRect(self.renderer, SDL_Rect(*rect))

    def present(self):
        SDL_RenderPresent(self.renderer)
