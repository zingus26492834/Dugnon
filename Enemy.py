# Imports
from ursina import *
from Player import *
from math import *
from CodeBlocks import *
from CodeFunctions import *

# Variables
LockRoom = False        # If True, Prevent player from leaving the room
TennaMode = False       # If scarymode is off, this becomes true, and turns all enemies into Tenna from Deltarune Chapter 3

# Default Enemy
class DefaultEnemy(Entity):     # Extends Entity
    def __init__(self, position, **kwargs):     # Variables set at creation of object
        super().__init__(model = 'quad',        # Variables for Entity that is being extended
                         scale = (1, 1),
                         position = position,
                         color = color.rgba(0, 0, 0, 0),        # Invisible
                         collider = 'box',
                         **kwargs)
        self.Enemy = True       # It is in fact, an enemy
        self.health = 50       # Has 50 health
        self.hurtcooldown = time.time()     # Variable controlling amt of time that needs to pass before it can take damage again
        self.playercollision = False        # Cannot stop player's movement (as terrain)
        self.despawnable = True     # It is despawnable
        self.speed = 3      # It's speed is 3
        self.velocity = 1       # Velocity is movement direction, 1 is right, -1 is left
        EnemyAnimation = self.EnemyAnim()       # Child Entity controlling animations
        EnemyAnimation.parent = self        # This entity is a child of DefaultEnemy

    # Object specific update loop    
    def update(self):
        # Don't run code from this loop if it's disabled
        if not self.enabled or not self.visible:
            return

        # Since deleting the entity is impossible, it needs to be disabled and hidden instead
        if self.health <= 0:
            self.enabled = False
            self.collider = None        # Collider doesn't get disabled normally since checks for collider exist in main.py
            self.visible = False

        # Wall Collision, raycasts are straight lines that return booleans, True if touching another collider, otherwise False
        wall = raycast(self.world_position, direction = (self.velocity, 0), distance = 0.3, ignore = (self, player))
        front_x = self.x + self.velocity * 0.5      # Raycasts are set to whichever direction the Enemy is moving toward
        edge = raycast (origin = (front_x, self.y - 0.5), direction = (0, -1), distance = 0.1, ignore = (self,))
        if wall.hit or not edge.hit:        # If it hits the wall or if about to move off a ledge (edge checks the floor in front of enemy)
            self.velocity *= -1     # Flips velocity and therefore movement direction
        else:
            self.x += time.dt * self.speed * self.velocity      # Move forward if none of the above
        if self.intersects(player) and time.time() - self.hurtcooldown > 0:     # If cooldown has passed and enemy touched player
            player.health -= 20     # player loses 20 health
            self.hurtcooldown = time.time() + 1     # Hurting player goes on cooldown for 1 second
            player.flingdir = player.velocity * -1      # Flings player away from Enemy
            player.flingvel += 50       # Increases fling velocity (so it increases more if player is hit again during fling)

    # Animation creator
    def EnemyAnim(self):
        TennaCheck()        # Updates TennaMode boolean
        if random.randint(1, 200) == 1 or TennaMode:        # 0.5% chance, 100% if TennaMode is True
            TennaDance = SpriteSheetAnimation('Sprites/Tenna/TennaSheet.png', tileset_size=(24,1), fps = 30, animations={'dance' : ((0, 0), (23, 0))})
            TennaDance.scale = 1
            TennaDance.play_animation('dance')      # Need to call this func to have the animation actually animate
            return TennaDance       # Sends animation back (technically a kind of entity)
        else:
            EnemyAnimation = SpriteSheetAnimation('Sprites/Enemy/SlimeThing/SlimeSheet.png', tileset_size=(7,1), fps = 10, animations={'blob' : ((0, 0), (6, 0))})
            EnemyAnimation.scale = 1
            EnemyAnimation.play_animation('blob')
            return EnemyAnimation
        
# Rotating Enemy        
class RotateEnemy(Entity):
    def __init__(self, position, **kwargs):
        super().__init__(model = 'quad',
                         color = color.rgba(0, 0, 0, 0),
                         position = position,
                         **kwargs)
        self.Enemy = True
        self.hurtcooldown = time.time()
        self.health = 20
        self.playercollision = False
        self.hurtcooldown = 0
        self.despawnable = True
        self.speed = 200        # Rotation speed is calculated differently
        # Entity that fights the rotation of self to make the sprite stay upright
        self.RotationControl = Entity(model = 'quad',
                                      despawnable = True,
                                      parent = self,
                                      color = color.rgba(0, 0, 0, 0),
                                      position = (4, 0),
                                      playercollision = False)
        # Actual Enemy, so basically since this is a child of self, rotating self moves this enemy too, in retrospect I should have just moved the origin instead of making another entity
        self.Enemy = Entity(model = 'quad', 
                            texture = load_texture('Sprites/Enemy/Eyenemy.png'),
                            scale = (2, 2),
                            despawnable = True,
                            playercollision = False,
                            position = (0, 0),
                            parent = self.RotationControl,
                            collider = 'box')
        self.TennaJumpscare()
        
        
    def update(self):
        if not self.enabled or not self.visible:
            return
        
        if self.health <= 0:
            self.enabled = False
            self.visible = False
            self.collider = None

        self.Rotate()       # Calls Rotate every frame
        if self.Enemy.intersects(player) and time.time() - self.hurtcooldown > 0:       # Self.Enemy rather than self because self.Enemy has the hitbox I want to track
            player.health -= 20
            self.hurtcooldown = time.time() + 1
            player.flingdir = player.velocity * -1
            player.flingvel += 50

    # Rotation controller
    def Rotate(self):
        self.rotation_z += time.dt * self.speed     # Since ursina is technically always in 3D, I need to spin the Z axis
        direction = player.world_position - self.Enemy.world_position       # Finds angle of player to enemy
        angle = degrees(atan2(direction.x, direction.y))        # Maths for calculating the angle and also converts it to degrees, notably it should be (y, x) not (x, y) but sometimes flipping it fixes things, like here. Not sure why
        self.RotationControl.rotation_z = -self.rotation_z      # Rotation control spins in opposition to self, resulting in rotation control staying upright
        self.Enemy.rotation_z = angle       # Enemy rotates to look at player

    def TennaJumpscare(self):
            TennaCheck()
            if random.randint(1, 200) == 1 or TennaMode:
                TennaDance = SpriteSheetAnimation('Sprites/Tenna/TennaSheet.png', tileset_size=(24,1), fps = 30, animations={'dance' : ((0, 0), (23, 0))})
                TennaDance.scale = 2
                TennaDance.play_animation('dance')
                self.Enemy.visible = False
                TennaDance.parent = self.RotationControl

# Stationary Shooting Enemy
class ShootEnemy(Entity):
    def __init__(self, position, **kwargs):
        super().__init__(model = 'quad',
                         texture = load_texture('Sprites/BoiledOne.png'),       # Sprite by Joseph
                         collider = 'box',
                         scale = 2,
                         position = position,
                         **kwargs)
        self.Enemy = True
        self.y += 0.5       # Gets self out of the ground
        self.hurtcooldown = time.time()
        self.health = 50
        self.playercollision = False
        self.hurtcooldown = 0
        self.despawnable = True
        self.shootcooldown = 0      # Cooldown for making another projectile
        self.TennaJumpscare()
        self.currentprojectiles = []        # List to store projectiles for updating
        
        
    def update(self):
        if not self.enabled or not self.visible:
            return
        
        if self.health <= 0:
            self.enabled = False
            self.visible = False
            self.collider = None
            self.enabled = False
            for p in self.currentprojectiles:       # Iterates through every existing projectile
                p.visible = False       # Makes projectile in visible
                p.enabled = False       # Disables projectile
                p.collider = None       # Removes projectile's collider
            return

        if self.intersects(player) and time.time() - self.hurtcooldown > 0:
            player.health -= 20
            self.hurtcooldown = time.time() + 1
            player.flingdir = player.velocity * -1
            player.flingvel += 50

        if self.shootcooldown < time.time():        # If shoot cooldown has ended, shoot again
            projectile = Entity(model = 'quad',
                                texture = load_texture('Sprites/RedOrb.png'),
                                collider = 'box',
                                damage = 20,
                                scale = (1, 1),
                                speed = 5,
                                spawntime = time.time(),
                                playercollision = False,
                                position = self.position)
            # Calculate angle of player and self and shoot in that direction
            projectile.dx = player.world_position.x - self.world_position.x
            projectile.dy = player.world_position.y - self.world_position.y
            projectile.angle = atan2(projectile.dy, projectile.dx)
            projectile.rotation_z = degrees(-projectile.angle)      # Rotate sprite to match
            self.currentprojectiles.append(projectile)      # Add projectile to list
            self.shootcooldown = time.time() + 2        # Sets cooldown to 2 seconds
        
        # Updates all existing projectiles
        for p in self.currentprojectiles:
            if time.time() - p.spawntime > 4:       # If 4 seconds have passed since spawning
                self.currentprojectiles.remove(p)       # Remove it from the list so it doesn't get checked again
                p.enabled = False       # And Disable it
            # Player also gets hurt if touched by projectiles
            if p.intersects(player) and time.time() - self.hurtcooldown > 0:
                self.hurtcooldown = time.time() + 1
                player.health -= 20
                player.flingdir = player.velocity * -1
                player.flingvel += 50
            p.x += cos(p.angle) * time.dt * p.speed     # Move in the direction it was initially fired
            p.y += sin(p.angle) * time.dt * p.speed
    
    def TennaJumpscare(self):
            TennaCheck()
            if random.randint(1, 200) == 1 or TennaMode:
                TennaDance = SpriteSheetAnimation('Sprites/Tenna/TennaSheet.png', tileset_size=(24,1), fps = 30, animations={'dance' : ((0, 0), (23, 0))})
                TennaDance.scale = 1
                TennaDance.play_animation('dance')
                TennaDance.parent = self
                self.color = color.rgba(0, 0, 0, 0)


# Default Boss
class BossEnemy(Entity):
    def __init__(self, position, spawntime, **kwargs):
        super().__init__(model = 'quad',
                         scale = (5, 5),
                         position = position,
                         collider = 'box',
                         texture = load_texture('Sprites/Enemy/Awesme.png'),        # Texture by Joseph
                         **kwargs)
        self.health = 300
        self.Enemy = True
        self.playercollision = False
        self.hurtcooldown = 0
        self.despawnable = True
        self.speed = 5
        self.velocity = 1
        self.gravity = 0        # Gravity / Fall speed, set to 0 initially to give player time to move
        self.jumping = False        # Makes sure it doesn't behave as if it's on the ground whlie jumping
        self.dead = False       # Checks if it's dead, used for boss drops etc. which is why other enemies don't have it
        self.spawntime = spawntime      # Boss waits 2 seconds after spawning, this is used to check that
        self.healthbar = Entity(model = 'quad',     # Healthbar for boss fights
                                color = color.red,
                                scale = (self.health / 300, 0.07),
                                parent = camera.ui,     # Camera.ui is used for all ui, exists by default in ursina
                                position = (0, 0.4))
        self.TennaJumpscare()
    
    def update(self):
        global LockRoom
        if not self.enabled or not self.visible:
            return
        if self.dead:
            self.visible = False
            self.enabled = False
            self.despawnable = False
            LockRoom = False        # Unlocks room when dead
            self.healthbar.enabled = False
            return
        else:
            LockRoom = True     # Locks room if alive
        
        self.ignore_list = [self,] + [e for e in ExecutedEntities]      # CodeFunctions won't act as terrain for the boss / CodeFunctions won't make boss turn around as if it hit a wall (except blocks)


        if time.time() - self.spawntime <= 2:       # Waits 2 seconds before attacking after spawning
            return
        # If raycast doesn't hit, it's in the air and gravity applies, otherwise its grounded and walks
        if not raycast(self.world_position + Vec3(0, (-self.scale_y / 2) - 0.2, 0), direction = (0, -1), distance = 0.3, ignore = (self, player)).hit and not self.jumping:
            self.gravity -= max(1, self.gravity * 1.2)  # Gravity increases the longer its in the air
            self.grounded = False
        elif not self.jumping:      # Makes sure it doesnt get stuck to the ground instead of jumping
            self.grounded = True
            self.gravity = 0        # No gravity because it's not fallinng
        self.y += time.dt * self.gravity # Moves downward based on gravity

        # Checks for walls and turns around, 1/3 chance to jump and turn around instead
        wall = raycast(self.world_position, direction = (self.velocity, 0), distance = 0.3, ignore = (self, player))
        wallbottom = raycast(self.world_position + Vec3(0, -self.scale_y / 2, 0), direction = (self.velocity, 0), distance = 1, ignore = (self, player))
        if wall.hit or wallbottom.hit:
            if random.choice([True, False, False]):
                if self.grounded:
                    self.gravity = 300      # the number is positive so it moves up, needs to be a high number to counteract the rapid decreasing of gravity when its in the air
                    self.speed += 15     # Speed increases when it jumps
                    self.jumping = True
            self.velocity *= -1
        else:
            self.x += time.dt * self.speed * self.velocity      # Move forward
        if self.intersects(player) and time.time() - self.hurtcooldown > 0:
            player.health -= 20
            self.hurtcooldown = time.time() + 1
            player.flingdir = player.velocity * -1
            player.flingvel += 50
        
        if self.jumping:        # If boss is jumping
            self.gravity /= 2       # Lower gravity (fall faster)
            if self.gravity < 0.2:      # If gravity is low enough
                self.jumping = False        # End jump
        
        if self.speed > 5:      # If speed if above 5
            self.speed * 0.8        # Lower speed
            if self.speed < 5:     # If speed is below 5
                self.speed = 5      # make speed 5
        
        # If health below 0, boss dies, drops codeblocks, summons portal, unlocks room
        if self.health <= 0:
            self.dead = True
            self.healthbar.enabled = False
            ItemCodeBlocks.append(GenerateRareCodeBlock(RandomRareCodeBlock(), (self.world_x) + 0.5, (self.world_y + 0.5)))
            ItemCodeBlocks.append(GenerateRareCodeBlock(RandomRareCodeBlock(), (self.world_x) + 1.5, (self.world_y + 0.5)))
            ItemCodeBlocks.append(GenerateCodeBlock(RandomCodeBlock(), (self.world_x) + 1, (self.world_y + 1)))
            SummonPortal(x = (camera.x + camera.scale_x / 2 - 0.5), y = (camera.y + camera.scale_y / 2 + 1.5), chunkx = (random.randint(5000, 500000)), chunky = (random.randint(5000, 500000)))
            self.LockRoom = False
            self.collider = None
        

        self.healthbar.scale_x = self.health / 100      # Healthbar length is scaled with self health

        # If boss is far enough from screen, start doing damage, makes sure the boss doesnt softlock player by glitching out of the level
        if self.y < camera.world_position.y - 15 or self.y > camera.world_position.y + 15 or self.x < camera.world_position.x - 30 or self.x > camera.world_position.x + 30:
            self.health -= 10

    def TennaJumpscare(self):
        TennaCheck()
        if random.randint(1, 200) == 1 or TennaMode:
            TennaDance = SpriteSheetAnimation('Sprites/Tenna/TennaSheet.png', tileset_size=(24,1), fps = 30, animations={'dance' : ((0, 0), (23, 0))})
            TennaDance.scale = 1
            TennaDance.play_animation('dance')
            TennaDance.parent = self
            self.color = color.rgba(0, 0, 0, 0)

# Stationary Shooting Boss
class StationaryBossEnemy(Entity):
    def __init__(self, position, spawntime, **kwargs):
        super().__init__(model = 'quad',
                         scale = (3, 3),
                         position = position,
                         collider = 'box',
                         texture = load_texture('Sprites/Enemy/StationaryBoss.png'),
                         **kwargs)
        self.health = 200
        self.Enemy = True
        self.playercollision = False
        self.hurtcooldown = 0
        self.despawnable = True
        self.angle = 0      # I think this is useless but I don't want to find out the hard way
        self.dead = False
        self.TennaJumpscare()
        self.spawntime = spawntime
        self.healthbar = Entity(model = 'quad',
                                color = color.red,
                                scale = (self.health / 100, 0.07),
                                parent = camera.ui,
                                position = (0, 0.4))
        self.shootcooldown = 0
        self.currentprojectiles = []
    
    def update(self):
        global LockRoom
        if not self.enabled or not self.visible:
            return
        if self.dead:
            self.visible = False
            self.enabled = False
            self.despawnable = False
            LockRoom = False
            for p in self.currentprojectiles:
                p.visible = False
                p.enabled = False
                p.collider = None
            self.healthbar.enabled = False
            return
        else:
            LockRoom = True

        if self.shootcooldown < time.time():
            projectile = Entity(model = 'quad',
                                texture = load_texture('Sprites/Arrow.png'),
                                collider = 'box',
                                damage = 20,
                                scale = (1, 0.5),
                                speed = 5,
                                spawntime = time.time(),
                                playercollision = False,
                                position = self.position)
            projectile.dx = player.world_position.x - self.world_position.x + random.uniform(-5, 5)
            projectile.dy = player.world_position.y - self.world_position.y + random.uniform(-5, 5)
            projectile.angle = atan2(projectile.dy, projectile.dx)
            projectile.rotation_z = degrees(-projectile.angle)
            self.currentprojectiles.append(projectile)
            self.shootcooldown = time.time() + 0.5

        for p in self.currentprojectiles:
            if time.time() - p.spawntime > 10:
                self.currentprojectiles.remove(p)
                p.enabled = False
            if p.intersects(player) and time.time() - self.hurtcooldown > 0:
                self.hurtcooldown = time.time() + 1
                player.health -= 20
                player.flingdir = player.velocity * -1
                player.flingvel += 50
            p.x += cos(p.angle) * time.dt * p.speed
            p.y += sin(p.angle) * time.dt * p.speed

        if time.time() - self.spawntime <= 2:
            return

        if self.intersects(player) and time.time() - self.hurtcooldown > 0:
            player.health -= 20
            self.hurtcooldown = time.time() + 1
            player.flingdir = player.velocity * -1
            player.flingvel += 50
        
        if self.health <= 0:
            self.dead = True
            self.healthbar.enabled = False
            ItemCodeBlocks.append(GenerateRareCodeBlock(RandomRareCodeBlock(), (self.world_x) + 0.5, (self.world_y + 0.5)))
            ItemCodeBlocks.append(GenerateRareCodeBlock(RandomRareCodeBlock(), (self.world_x) + 1.5, (self.world_y + 0.5)))
            ItemCodeBlocks.append(GenerateCodeBlock(RandomCodeBlock(), (self.world_x) + 1, (self.world_y + 1)))
            SummonPortal(x = (camera.x + camera.scale_x / 2 - 0.5), y = (camera.y + camera.scale_y / 2 + 1.5), chunkx = (random.randint(5000, 500000)), chunky = (random.randint(5000, 500000)))
            self.LockRoom = False
            self.collider = None
        

        self.healthbar.scale_x = self.health / 100
        if self.y < camera.world_position.y - 15 or self.y > camera.world_position.y + 15 or self.x < camera.world_position.x - 30 or self.x > camera.world_position.x + 30:
            self.health -= 10

    def TennaJumpscare(self):
            TennaCheck()
            if random.randint(1, 200) == 1 or TennaMode:
                TennaDance = SpriteSheetAnimation('Sprites/Tenna/TennaSheet.png', tileset_size=(24,1), fps = 30, animations={'dance' : ((0, 0), (23, 0))})
                TennaDance.scale = 1
                TennaDance.play_animation('dance')
                TennaDance.parent = self
                self.color = color.rgba(0, 0, 0, 0)

# Floating Boss
class FloatingBoss(Entity):
    def __init__(self, position, spawntime, **kwargs):
        super().__init__(model = 'quad',
                         scale = (5, 5),
                         position = position,
                         collider = 'box',
                         texture = load_texture('Sprites/Enemy/SkullBoss.png'),
                         **kwargs)
        self.health = 100
        self.dh = 0         # Difference in health
        self.Enemy = True
        self.playercollision = False
        self.hurtcooldown = 0
        self.despawnable = True
        self.dead = False
        self.speed = 5
        self.LockRoom = True
        self.spawntime = spawntime
        self.healthbar = Entity(model = 'quad',
                                color = color.red,
                                scale = (self.health / 100, 0.07),
                                parent = camera.ui,
                                position = (0, 0.4))
        # Eye that looks at player
        self.Eye = Entity(model = 'quad',
                          position = (0.2, 0),
                          scale = (0.2, 0.2),
                          parent = self,
                          texture = load_texture('Sprites/eye.png'),
                          z = -0.1)
        self.xaccel = 0     # Horizontal acceleration
        self.yaccel = 0     # Vertical acceleration
        self.TennaJumpscare()
    
    def update(self):
        global LockRoom
        if not self.enabled:
            return
        if self.dead:
            self.visible = False
            self.enabled = False
            self.despawnable = False
            LockRoom = False
            self.healthbar.enabled = False
            return
        else:
            LockRoom = True

        # Calculate direction to player and move that way
        self.dx = player.world_position.x - self.world_position.x
        self.dy = player.world_position.y - self.world_position.y
        angle = atan2(self.dy, self.dx)
        self.x += cos(angle) * time.dt * self.speed
        self.y += sin(angle) * time.dt * self.speed

        # Calculate direction to player and rotate eye that way
        edx = player.world_position.x - self.world_position.x
        edy = player.world_position.y - self.world_position.y
        eyeangle = atan2(edy, edx)
        self.Eye.rotation_z = degrees(-eyeangle)

        if time.time() - self.spawntime <= 2:
            return

        if self.intersects(player) and time.time() - self.hurtcooldown > 0:
            player.health -= 20
            self.hurtcooldown = time.time() + 1
            player.flingdir = player.velocity * -1
            player.flingvel += 50
            self.speed *= -1        # Reverse speed (bounces backward when hit player)
        
        if self.health <= 0:
            self.dead = True
            self.healthbar.enabled = False
            ItemCodeBlocks.append(GenerateRareCodeBlock(RandomRareCodeBlock(), (self.world_x) + 0.5, (self.world_y + 0.5)))
            ItemCodeBlocks.append(GenerateRareCodeBlock(RandomRareCodeBlock(), (self.world_x) + 1.5, (self.world_y + 0.5)))
            ItemCodeBlocks.append(GenerateCodeBlock(RandomCodeBlock(), (self.world_x) + 1, (self.world_y + 1)))
            SummonPortal(x = (camera.x + camera.scale_x / 2 - 0.5), y = (camera.y + camera.scale_y / 2 + 1.5), chunkx = (random.randint(5000, 500000)), chunky = (random.randint(5000, 500000)))
            self.LockRoom = False
            self.collider = None
        
        # Acceleration
        da = abs((self.xaccel - cos(angle)) + (self.yaccel - sin(angle)))       # Checks the difference in angles from last tick
        self.speed -= da * 2        # Lowers speed based on the difference; deccelerates when turning
        # Accelerate if angle is small
        if da < 0.25:
            self.speed += 0.2
        if self.speed < 0:
            self.speed += 0.2
        # Cap speed at 8
        if self.speed > 8:
            self.speed = 8
        self.xaccel = cos(angle)        # Actually not sure if these 2 do anything
        self.yaccel = sin(angle)

        self.healthbar.scale_x = self.health / 100
        if self.y < camera.world_position.y - 15 or self.y > camera.world_position.y + 15 or self.x < camera.world_position.x - 30 or self.x > camera.world_position.x + 30:
            self.health -= 10

        if self.dh > self.health:       # If health lowered this tick
            self.speed *= -1        # Reverse Speed (bounces backward when take damage)
        self.dh = self.health       # Updates health difference for next loop
    
    def TennaJumpscare(self):
            TennaCheck()
            if random.randint(1, 10) == 1 or TennaMode:
                TennaDance = SpriteSheetAnimation('Sprites/Tenna/TennaSheet.png', tileset_size=(24,1), fps = 30, animations={'dance' : ((0, 0), (23, 0))})
                TennaDance.scale = 1
                TennaDance.play_animation('dance')
                TennaDance.parent = self
                self.Eye.visible = False
                self.color = color.rgba(0, 0, 0, 0)

FirstEncounter = True        # First encounter check
# Create random enemy
def RandomEnemy(position):
    global FirstEncounter
    # If this is the first enemy being created, create a rotating enemy
    if FirstEncounter:
        FirstEncounter = False
        return RotateEnemy(position)
    randomenemy = random.randint(1, 3)      # Choose randomly from 1-3
    if random.choice([True, False]):        # 50% chance to not generate an enemy instead
        return
    if randomenemy == 1:        # If randomenemy rolled 1, create rotating enemy
        ChosenEnemy = RotateEnemy(position)
    elif randomenemy == 2:      # If randomenemy rolled 2, create default enemy
        ChosenEnemy = DefaultEnemy(position)
    elif randomenemy == 3:      # If randomenemy rolled 3, create shooting enemy
        ChosenEnemy = ShootEnemy(position)
    return ChosenEnemy      # Return the enemy that was chosen

# Check scary
def TennaCheck():
    global TennaMode
    with open ('settings.txt', 'r') as scary:       # Open settings file
        TennaMode = scary.read() == 'False'     # If scary is True, TennaMode is False, and vice versa