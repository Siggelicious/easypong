import time
import math
from easytypes import Box
from sdl2 import *
import random
from settings import *
from easytypes import Vec2

MAPS = [
    {
        -1 : SDL_SCANCODE_W,
        1 : SDL_SCANCODE_S
    },
    {
        -1 : SDL_SCANCODE_I,
        1 : SDL_SCANCODE_K
    }
]

class Arena:
    def __init__(self, size, graphics):
        self.size = size
        self.graphics = graphics
        random.seed(time.time())
        self.players = [Box(Vec2(*PLAYER_SIZE), PLAYER_SPEED, Vec2(0.0, 0.0), Vec2(0.0, 0.0)) for _ in range(0,2)]
        self.ball = Box(Vec2(*BALL_SIZE), BALL_SPEED, Vec2(0.0, 0.0), Vec2(0.0, 0.0))
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

    def serve(self, angle):
        player1, player2 = self.players[0], self.players[1]
        player1.pos.x, player1.pos.y = MARGIN, (self.size.y - player1.size.y) / 2.0 
        player2.pos.x, player2.pos.y = self.size.x - MARGIN - player2.size.x, (self.size.y - player2.size.y) / 2.0 
        self.ball.pos.x, self.ball.pos.y = (self.size.x - self.ball.size.x) / 2.0, (self.size.y - self.ball.size.y) / 2.0
        self.set_ball_velocity_from_angle(angle)

    def test_for_collision(self, player, dt):
        dist_short = Vec2(
                    player.pos.x + player.size.x - self.ball.pos.x,
                    player.pos.y + player.size.y - self.ball.pos.y,
                )
        dist_long = Vec2(
                    player.pos.x - (self.ball.pos.x + self.ball.size.x),
                    player.pos.y - (self.ball.pos.y + self.ball.size.y)
                )

        if abs(dist_short.x) > abs(dist_long.x):
            dist_short.x, dist_long.x = dist_long.x, dist_short.x

        if abs(dist_short.y) > abs(dist_long.y):
            dist_short.y, dist_long.y = dist_long.y, dist_short.y

        entry_time = Vec2(0.0, 0.0)
        exit_time = Vec2(0.0, 0.0)

        if self.ball.vel.x == 0.0:
            entry_time.x = -math.inf
            exit_time.x = math.inf

        else:
            entry_time.x = dist_short.x / self.ball.vel.x
            exit_time.x = dist_long.x / self.ball.vel.x

        if self.ball.vel.y == 0.0:
            entry_time.y = -math.inf
            exit_time.y = math.inf

        else:
            entry_time.y = dist_short.y / self.ball.vel.y
            exit_time.y = dist_long.y / self.ball.vel.y
        
        entry_time_real = max(entry_time.x, entry_time.y)
        exit_time_real = min(exit_time.y, exit_time.y)
        normal = Vec2(0.0, 0.0)

        if (entry_time_real > exit_time_real or (entry_time.x <= 0.0 and entry_time.y <= 0.0) or entry_time.x > dt or entry_time.y > dt):
            return False, 0.0, normal 

        else:
            if entry_time.x > entry_time.y:
                normal.x = -1.0 if dist_short.x < 0.0 else 1.0

            else:
                normal.y = -1.0 if dist_short.y < 0.0 else 1.0

        return True, entry_time_real, normal 

    def update_ball_position(self, dt):
        self.ball.pos.x += self.ball.vel.x * dt
        self.ball.pos.y += self.ball.vel.y * dt

    def set_ball_velocity_from_angle(self, angle):
        self.ball.vel.x = self.ball.speed * math.cos(angle)
        self.ball.vel.y = self.ball.speed * math.sin(angle) 

    def resolve_ball_position(self, dt):
        for player in self.players:
            occurred, time_of_collision, normal = self.test_for_collision(player, dt)
            
            if occurred:
                print("Collision happened")
                print(str(time_of_collision))
                self.update_ball_position(time_of_collision)

                if not normal.y == 0.0:
                    print("y normal")
                    self.ball.vel.y *= -1.0

                elif not normal.x == 0.0:
                    print("x normal")
                    dist_from_center = (player.pos.y + player.size.y / 2.0) - (self.ball.pos.y + self.ball.size.y / 2.0)
                    angle_origin = (math.pi / 2.0) * (1.0 + normal.x)
                    angle_difference = (math.pi / 3.0) * (dist_from_center / ((player.size.y + self.ball.size.y) / 2.0))
                    angle_adjusted = angle_origin + normal.x * angle_difference
                    self.set_ball_velocity_from_angle(angle_adjusted)

                return dt - time_of_collision
        
        if self.ball.pos.y + self.ball.vel.y * dt < 0.0:
            time_of_collision = abs(self.ball.pos.y / self.ball.vel.y)
            self.update_ball_position(time_of_collision)
            self.ball.vel.y *= -1.0
            return dt - time_of_collision
        
        elif self.ball.pos.y + self.ball.size.y + self.ball.vel.y * dt > self.size.y:
            time_of_collision = abs((self.size.y - (self.ball.pos.y + self.ball.size.y)) / self.ball.vel.y)
            self.update_ball_position(time_of_collision)
            self.ball.vel.y *= -1.0
            return dt - time_of_collision

        self.update_ball_position(dt)
        return 0.0

    def update_positions(self, dt):
        for player in self.players:
            floor = self.size.y - player.size.y
            new_pos = player.pos.y + player.vel.y * dt
            new_pos = 0 if new_pos < 0 else floor if new_pos > floor else new_pos
            player.pos.y = new_pos
                    
        while dt > 0.0: 
            dt = self.resolve_ball_position(dt)

    def render(self):
        self.graphics.fill_rect((0, 0, *WINDOW_SIZE), (0, 0, 0, 255))

        for player in self.players:
            self.graphics.fill_rect(
                        (round(player.pos.x), round(player.pos.y), round(player.size.x), round(player.size.y)), 
                        (255, 255, 255, 255)
                    )
        
        self.graphics.fill_rect(
                    (round(self.ball.pos.x), round(self.ball.pos.y), round(self.ball.size.x), round(self.ball.size.y)), 
                    (255, 0, 0, 255)
                )
        self.graphics.present()

    def play(self):
        quit = False
        self.serve(random.randint(0, 1) * math.pi)
        event = SDL_Event()
        old_time = new_time = time.process_time_ns()

        while not quit:
            while SDL_PollEvent(event) != 0:
                if event.type == SDL_QUIT:
                    quit = True

            self.handle_player_input()
            new_time = time.process_time_ns()
            dt = (new_time - old_time) / 1000000000
            old_time = new_time
            self.update_positions(dt)

            if (self.ball.pos.x + self.ball.size.x) < 0.0:
                self.serve(0.0)

            elif self.ball.pos.x > self.size.x:
                self.serve(math.pi)

            self.render()

