from ursina import *

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(model = 'quad', 
                         texture = load_texture('white_cube'),
                         scale = (1,1,1),
                         collider = 'box'
                         )
        self.velocity = 0
        self.gravity = 1
        self.grounded = True
        self.speed = 10
        self.jumpheight = 0.8

    def update(self):
        self.y += self.velocity
        self.velocity -= (self.gravity / 10)
        collideright = raycast(self.world_position,
                               Vec3(1, 0, 0),
                               distance = 0.6,
                               ignore = (self,)).hit
        collideleft = raycast(self.world_position,
                              Vec3(-1, 0 ,0),
                              distance = 0.6,
                              ignore = (self,)).hit


        if held_keys['d'] and not collideright:
            self.x += time.dt * self.speed
        if held_keys['a'] and not collideleft:
            self.x -= time.dt * self.speed
        if self.intersects().hit:
            self.velocity = 0
            if held_keys['space']:
                self.velocity = self.jumpheight
        

player = Player()