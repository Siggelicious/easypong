class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class CollisionData:
    def __init__(self, time, a, b, normal_a, normal_b):
        self.time = time
        self.a = a
        self.b = b
        self.normal_a = normal_a
        self.normal_b = normal_b

class Box:
    def __init__(self, size, speed, pos, vel):
        self.size = size
        self.speed = speed
        self.pos = pos
        self.vel = vel

    def apply_velocity(self, dt):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
