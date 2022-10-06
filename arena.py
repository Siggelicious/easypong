import time
import math
from easytypes import Box
from sdl2 import *
import random
from settings import *
from easytypes import Vec2

MAPS = [
    {
        1 : SDL_SCANCODE_W,
        -1 : SDL_SCANCODE_S
    },
    {
        1 : SDL_SCANCODE_I,
        -1 : SDL_SCANCODE_K
    }
]

class Arena:
    def __init__(self, size, graphics):
        self.size = size
        self.graphics = graphics
        random.seed(time.time())
        self.players = [Box(Vec2(*PLAYER_SIZE), PLAYER_SPEED)] * 2
        self.ball = Box(Vec2(*BALL_SIZE), BALL_SPEED)
        self.score = [ 0, 0 ]

    def handle_player_input(self):
        kb_state = SDL_GetKeyboardState(None)
        
        for i in range(2):
            move = 0
            player = self.players[i]

            for k, v in MAPS[i].items():
                if kb_state[v]:
                    move += k;      

            player.vel.y = move * player.speed 

    def prepare(self, angle):
        player1 = self.players[0]
        player2 = self.players[1]
        player1.pos.x = MARGIN
        player1.pos.y = self.size.y / 2.0
        player2.pos.x = self.size.x - MARGIN - player2.size.x  
        player2.pos.y = self.size.y / 2.0
        print(str(player1.pos.x) + " " + str(player1.pos.y))
        self.ball.pos.x = self.size.x / 2.0
        self.ball.pos.y = self.size.y / 2.0
        self.ball.vel.x = self.ball.speed * math.cos(angle)
        self.ball.vel.y = self.ball.speed * math.sin(angle)

    def render(self):
        self.graphics.fill_rect((0, 0, *WINDOW_SIZE), (0, 0, 0, 255))

        for player in self.players:
            self.graphics.fill_rect((round(player.pos.x), round(player.pos.y), round(player.size.x), round(player.size.y)), (255, 255, 255, 255))
        
        self.graphics.fill_rect((round(self.ball.pos.x), round(self.ball.pos.y), round(self.ball.size.x), round(self.ball.size.y)), (255, 255, 255, 255))
        self.graphics.present()

    def play(self):
        quit = False
        self.prepare(random.randint(0, 1) * math.pi)
        event = SDL_Event()
        
        while not quit:
            while SDL_PollEvent(event) != 0:
                if event.type == SDL_QUIT:
                    quit = True

            self.handle_player_input()
            self.render()
