class Vec2:
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

class Box:
    def __init__(self, size = Vec2(), speed = 0.0, pos = Vec2(), vel = Vec2()):
        self.size = size
        self.speed = speed
        self.pos = pos
        self.vel = vel
