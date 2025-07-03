from ursina import *
from Player import *
from math import *
from CodeBlocks import *

LockRoom = False

class DefaultEnemy(Entity):
    def __init__(self, position, **kwargs):
        super().__init__(model = 'quad',
                         scale = (1, 1),
                         color = color.rgba(0, 0, 0, 0),
                         position = position,
                         collider = 'box',
                         **kwargs)
        self.Enemy = True
        self.health = 100
        self.hurtcooldown = time.time()
        self.playercollision = False
        self.hurtcooldown = 0
        self.despawnable = True
        self.speed = 5
        self.velocity = 1
        EnemyAnimation = self.EnemyAnim()
        EnemyAnimation.parent = self
        
    def update(self):
        if not self.enabled:
            return
    
        if self.health <= 100:
            self.enabled = False

        wall = raycast(self.world_position, direction = (self.velocity, 0), distance = 0.3, ignore = (self, player))
        front_x = self.x + self.velocity * 0.5
        edge = raycast (origin = (front_x, self.y - 0.5), direction = (0, -1), distance = 0.1, ignore = (self,))
        if wall.hit or not edge.hit:
            self.velocity *= -1
        else:
            self.x += time.dt * self.speed * self.velocity
        if self.intersects(player) and time.time() - self.hurtcooldown > 0:
            player.health -= 20
            self.hurtcooldown = time.time() + 1
            player.flingdir = player.velocity * -1
            player.flingvel += 50
    
    def EnemyAnim(self):
        EnemyAnimation = SpriteSheetAnimation('Sprites/Enemy/SlimeThing/SlimeSheet.png', tileset_size=(7,1), fps = 6, animations={'blob' : ((0, 0), (6, 0))})
        EnemyAnimation.scale = 1
        EnemyAnimation.play_animation('blob')
        return EnemyAnimation
        

class RotateEnemy(Entity):
    def __init__(self, position, **kwargs):
        super().__init__(model = 'quad',
                         color = color.rgba(0, 0, 0, 0),
                         position = position,
                         **kwargs)
        self.Enemy = True
        self.hurtcooldown = time.time()
        self.health = 100
        self.playercollision = False
        self.hurtcooldown = 0
        self.despawnable = True
        self.speed = 200
        self.RotationControl = Entity(model = 'quad',
                                      despawnable = True,
                                      parent = self,
                                      color = color.rgba(0, 0, 0, 0),
                                      position = (4, 0),
                                      playercollision = False)
        self.Enemy = Entity(model = 'quad', 
                            texture = load_texture('Sprites/Enemy/Eyenemy.png'),
                            scale = (2, 2),
                            despawnable = True,
                            playercollision = False,
                            position = (0, 0),
                            parent = self.RotationControl,
                            collider = 'box')
        
        
    def update(self):
        if not self.enabled:
            return
        
        if self.health <= 0:
            self.enabled = False

        self.Rotate()
        if self.Enemy.intersects(player) and time.time() - self.hurtcooldown > 0:
            player.health -= 20
            self.hurtcooldown = time.time() + 1
            player.flingdir = player.velocity * -1
            player.flingvel += 50

    def Rotate(self):
        self.rotation_z += time.dt * self.speed
        direction = player.world_position - self.Enemy.world_position
        angle = degrees(atan2(direction.x, direction.y))
        self.RotationControl.rotation_z = -self.rotation_z
        self.Enemy.rotation_z = angle

class BossEnemy(Entity):
    def __init__(self, position, spawntime, **kwargs):
        super().__init__(model = 'quad',
                         scale = (5, 5),
                         position = position,
                         collider = 'box',
                         texture = load_texture('Sprites/Enemy/Awesme.png'),
                         **kwargs)
        self.health = 100
        self.Enemy = True
        self.hurtcooldown = time.time()
        self.playercollision = False
        self.hurtcooldown = 0
        self.despawnable = True
        self.speed = 5
        self.spawnheight = self.y
        self.velocity = 1
        self.gravity = 0
        self.jumping = False
        self.dead = False
        self.spawntime = spawntime
        self.healthbar = Entity(model = 'quad',
                                color = color.red,
                                scale = (self.health / 100, 0.07),
                                parent = camera.ui,
                                position = (0, 0.4))
    
    def update(self):
        global LockRoom
        if not self.enabled:
            return
        if self.dead:
            self.visible = False
            return
        
        self.ignore_list = [self,] + [e for e in ExecutedEntities]


        if time.time() - self.spawntime <= 2:
            return
        if not raycast(self.world_position + Vec3(0, (-self.scale_y / 2) - 0.2, 0), direction = (0, -1), distance = 0.3, ignore = (self, player)).hit and not self.jumping:
            self.gravity -= max(1, self.gravity * 1.2)
            self.grounded = False
        elif not self.jumping:
            self.grounded = True
            self.gravity = 0
        self.y += time.dt * self.gravity

        wall = raycast(self.world_position, direction = (self.velocity, 0), distance = 0.3, ignore = (self, player))
        wallbottom = raycast(self.world_position + Vec3(0, -self.scale_y / 2, 0), direction = (self.velocity, 0), distance = 1, ignore = (self, player))
        if wall.hit or wallbottom.hit:
            if random.choice([True, False, False]):
                if self.grounded:
                    self.gravity = 300
                    self.speed = 15
                    self.jumping = True
            self.velocity *= -1
        else:
            self.x += time.dt * self.speed * self.velocity
        if self.intersects(player) and time.time() - self.hurtcooldown > 0:
            player.health -= 20
            self.hurtcooldown = time.time() + 1
            player.flingdir = player.velocity * -1
            player.flingvel += 50
        
        if self.jumping:
            self.gravity /= 2
            if self.gravity < 0.2:
                self.jumping = False
        
        if self.speed > 5:
            self.speed * 0.8
            if self.speed <= 5:
                self.speed = 5
        
        if self.health <= 0:
            self.enabled = False
            self.dead = True
            self.healthbar.enabled = False
            ItemCodeBlocks.append(GenerateRareCodeBlock(RandomRareCodeBlock(), (self.world_x) + 0.5, (self.world_y + 0.5)))
            LockRoom = False
        

        self.healthbar.scale_x = self.health / 100

FirstEncounter = True
def RandomEnemy(position):
    global FirstEncounter
    if FirstEncounter:
        FirstEncounter = False
        return RotateEnemy(position)
    if random.choice([True, False]):
        return
    ChosenEnemy = random.choice([DefaultEnemy, RotateEnemy])
    return ChosenEnemy(position)