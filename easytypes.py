class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Box:
    def __init__(self, size, speed, pos, vel):
        self.size = size
        self.speed = speed
        self.pos = pos
        self.vel = vel

    def apply_velocity(self, dt):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
