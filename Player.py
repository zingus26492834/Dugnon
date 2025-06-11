from ursina import *
from CodeBlocks import *

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(model = 'quad', 
                         texture = load_texture('Sprites/PlayerTemp'),
                         scale = (1,1,1),
                         collider = 'box'
                         )
        self.velocity = 0
        self.gravity = 1
        self.grounded = True
        self.speed = 10
        self.jumpheight = 4
        self.traverse_target = scene
        self.grounded = True
        self.walking = False
        self.jumping = False
        self.air_time = 0
        self.animator = Animator({'idle' : None, 'walk' : None, 'jump' : None})
        self.ignore_list = [self]
        self.jumpcooldown = 0
        self.stuckcheck = time.time() + 5
        self.aescape = 0
        self.descape = 0
        self.spaceescape = 0
        self.stuckpos = 0

        ray = raycast(self.world_position, 
                      self.down, 
                      distance = 10, 
                      ignore = (self, ), 
                      traverse_target = self.traverse_target)
        if ray.hit:
            self.y = ray.world_point[1] + 0.01

    def update(self):
        self.ignore_list = [self] + [e for e in scene.entities if hasattr(e, 'playercollision')]        # Updates ignore list to include entities made after the player, and ignores entities that have playercollision attribute
        if not boxcast(
            self.position,
            direction=Vec3(self.velocity,self.scale_y / 2,0),
            distance=abs(self.scale_x / 2),
            ignore=self.ignore_list,
            traverse_target=self.traverse_target,
            thickness=(self.scale_x*.99, self.scale_y*.9)).hit:

            self.x += self.velocity * time.dt * self.speed

        self.walking = held_keys['a'] + held_keys['d'] > 0 and self.grounded

        ray_origin = self.world_position - Vec3(0, self.scale_y / 2, 0)
        ray = raycast(ray_origin + Vec3(0,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)
        left_ray = raycast(ray_origin + Vec3(-self.scale_x*.49,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)
        right_ray = raycast(ray_origin + Vec3(self.scale_x*.49,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)

        if any((ray.hit, left_ray.hit, right_ray.hit)):
            if not self.grounded:
                self.air_time = 0
                self.grounded = True
            self.y = max((r.world_point.y for r in (ray, left_ray, right_ray) if r.hit)) + self.scale_y / 2
        else:
            self.grounded = False
        
        if not self.grounded and not self.jumping:
            self.y -= min(self.air_time * self.gravity, ray.distance - 0.1)
            self.air_time += time.dt * 4 * self.gravity    

        hit_above = raycast(self.world_position+Vec3(0,(self.scale_y/2)-0.5,0), self.up, distance=0.8, traverse_target=self.traverse_target, ignore=self.ignore_list)
        hit_above_left = raycast(self.world_position+Vec3(-self.scale_x*.49,(self.scale_y/2)-0.5,0), self.up, distance=0.8, traverse_target=self.traverse_target, ignore=self.ignore_list)
        hit_above_right = raycast(self.world_position+Vec3(self.scale_x*.49,(self.scale_y/2)-0.5,0), self.up, distance=0.8, traverse_target=self.traverse_target, ignore=self.ignore_list)
        if any((hit_above.hit, hit_above_left.hit, hit_above_right.hit)):
             if self.jumping:
                self.y = min(min((r.world_point.y for r in (hit_above, hit_above_left, hit_above_right) if r.hit)), self.y)
                self.jumping = False
                self.air_time = 0
             if hasattr(self, 'y_animator'):
                 self.y_animator.kill()
        
        if self.stuckcheck <= time.time():
            self.stuckcheck += 5
            self.stuckpos = self.position
            self.aescape = 0
            self.descape = 0
            self.spaceescape = 0

    def input(self, key):
        if key == 'space':
            self.jump()
            self.spaceescape += 1
        elif key == 'w':
            self.jump()
            self.spaceescape += 1
        if key == 'a':
            self.velocity = -1
            self.aescape += 1
        if key == 'd':
            self.velocity = 1
            self.descape += 1
        if key == 'a up':
            self.velocity = held_keys['d']
        if key == 'd up':
            self.velocity = -held_keys['a']

    def jump(self):
        if not self.grounded:
            return
        if self.jumpcooldown > time.time():
            return
        
        self.jumpcooldown = time.time() + 1

        self.jumping = True
        self.grounded = False

        self.target_y = self.y + self.jumpheight
        self.animate_y(self.target_y, 0.5, resolution = 30, curve = curve.out_expo)
        self._start_fall_sequence = invoke(self.start_fall, delay = 0.5)
    
    def start_fall(self):
        self.jumping = False
        

player = Player()