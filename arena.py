import time
import math
from easytypes import Box, CollisionData
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

def set_box_velocity_from_angle(box, angle):
    box.vel.x = box.speed * math.cos(angle)
    box.vel.y = box.speed * math.sin(angle) 

def player_collision_callback(player, _, normal):
    if not normal.y == 0.0:
        player.vel.y = 0.0

def ball_collision_callback(ball, box, normal):
    if not normal.y == 0.0:
        ball.vel.y = abs(ball.vel.y) * -normal.y
    
    else:
        dist_from_center = (box.pos.y + box.size.y / 2.0) - (ball.pos.y + ball.size.y / 2.0)
        angle_origin = (math.pi / 2.0) * (1.0 + normal.x)
        angle_difference = (math.pi / 3.0) * (dist_from_center / ((box.size.y + ball.size.y) / 2.0))
        angle_adjusted = angle_origin + normal.x * angle_difference
        set_box_velocity_from_angle(ball, angle_adjusted)

class Arena:
    def __init__(self, size, graphics):
        self.size = size
        self.graphics = graphics
        random.seed(time.time())
        self.players = [Box(Vec2(*PLAYER_SIZE), PLAYER_SPEED, Vec2(0.0, 0.0), Vec2(0.0, 0.0)) for _ in range(0,2)]
        self.ball = Box(Vec2(*BALL_SIZE), BALL_SPEED, Vec2(0.0, 0.0), Vec2(0.0, 0.0))
        self.walls = [
            Box(Vec2(self.size.x, 10.0), 0.0, Vec2(0.0, -10.0), Vec2(0.0, 0.0)),
            Box(Vec2(self.size.x, 10.0), 0.0, Vec2(0.0, self.size.y), Vec2(0., 0.0)),
        ]
        self.boxes = []
        self.boxes.extend(self.players)
        self.boxes.extend(self.walls)
        self.boxes.append(self.ball)
        self.call_backs = {}

        for player in self.players:
            self.call_backs[player] = player_collision_callback

        self.call_backs[self.ball] = ball_collision_callback
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
        set_box_velocity_from_angle(self.ball, angle)

    def test_for_collision(self, a, b, dt):
        resulting_velocity = Vec2(
                    a.vel.x - b.vel.x,
                    a.vel.y - b.vel.y
                )
        normal = Vec2(0.0, 0.0)

        if resulting_velocity.x == 0.0 and resulting_velocity.y == 0.0:
            return False, 0.0, normal

        dist_near = Vec2(
                    b.pos.x - (a.pos.x + a.size.x),
                    b.pos.y - (a.pos.y + a.size.y)
                )
        dist_far = Vec2(
                    b.pos.x + b.size.x - a.pos.x,
                    b.pos.y + b.size.y - a.pos.y
                )
        time_near = Vec2(0.0, 0.0)
        time_far = Vec2(0.0, 0.0)

        if resulting_velocity.x == 0:
            time_near.x = math.inf * (-1.0 if dist_near.x == 0.0 else dist_near.x / abs(dist_near.x))
            time_far.x = math.inf * (1.0 if dist_far.x == 0.0 else dist_far.x / abs(dist_far.x))

        else: 
            time_near.x = dist_near.x / resulting_velocity.x
            time_far.x = dist_far.x / resulting_velocity.x

        if resulting_velocity.y == 0:
            time_near.y = math.inf * (-1.0 if dist_near.y == 0.0 else dist_near.y / abs(dist_near.y))
            time_far.y = math.inf * (1.0 if dist_far.y == 0.0 else dist_far.y / abs(dist_far.y))

        else: 
            time_near.y = dist_near.y / resulting_velocity.y
            time_far.y = dist_far.y / resulting_velocity.y

        if time_near.x > time_far.x:
            time_near.x, time_far.x = time_far.x, time_near.x

        if time_near.y > time_far.y:
            time_near.y, time_far.y = time_far.y, time_near.y

        time_near_real = max(time_near.x, time_near.y)
        time_far_real = min(time_far.x, time_far.y)

        if time_near.x > time_far.y or time_near.y > time_far.x or time_near_real < 0.0 or time_far_real < 0.0 or time_near_real > dt:
            return False, 0.0, normal

        if time_near.x > time_near.y:
            normal.x = abs(resulting_velocity.x) / resulting_velocity.x
        
        else:
            normal.y = abs(resulting_velocity.y) / resulting_velocity.y

        return True, time_near_real, normal

    def resolve_collisions(self, dt):
        collisions = []
        num = len(self.boxes)
        
        for i in range(num):
            for j in range(i + 1, num):
                a, b = self.boxes[i], self.boxes[j]
                occurred, time_of_collision, normal = self.test_for_collision(a, b, dt)         

                if occurred:
                    normal_a = normal
                    normal_b = Vec2(normal.x * -1.0, normal.y * -1.0)
                    collision_data = CollisionData(time_of_collision, a, b, normal_a, normal_b)
                    collisions.append(collision_data)

        if len(collisions) == 0:
            for box in self.boxes:
                box.apply_velocity(dt)

            return 0.0

        collision = min(collisions, key=lambda c: c.time)
        
        for box in self.boxes:
            box.apply_velocity(collision.time)

        if collision.a in self.call_backs: 
            self.call_backs[collision.a](collision.a, collision.b, collision.normal_a)

        if collision.b in self.call_backs:
            self.call_backs[collision.b](collision.b, collision.a, collision.normal_b)

        return dt - collision.time

    def update_positions(self, dt):
        while dt > 0.0: 
            dt = self.resolve_collisions(dt)

    def render(self):
        self.graphics.fill_rect((0, 0, *WINDOW_SIZE), (0, 0, 0, 255))

        for box in self.boxes:
            self.graphics.fill_rect(
                        (round(box.pos.x), round(box.pos.y), round(box.size.x), round(box.size.y)), 
                        (255, 255, 255, 255)
                    )

        self.graphics.render_text(str(self.score[0]), (round(self.size.x / 4.0) - 50, 10, 100, 100), (255, 255, 255, 255))
        self.graphics.render_text(str(self.score[1]), (round(self.size.x / 4.0 * 3.0) - 50, 10, 100, 100), (255, 255, 255, 255))
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
                self.score[1] += 1
                self.serve(0.0)

            elif self.ball.pos.x > self.size.x:
                self.score[0] += 1
                self.serve(math.pi)

            self.render()

