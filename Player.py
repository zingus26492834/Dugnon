# Imports
from ursina import *
from CodeBlocks import *
from Tutorial import *

# Player class, ursina has a prefab for one but all the prefabs kinda suck, this takes a lot from that prefab but I can edit this one
class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(model = 'quad', 
                         color = color.rgba(0, 0, 0, 0),
                         scale = (1,1,1),
                         collider = 'box')
        self.velocity = 0       # Velocity is movement direction, 1 is left, -1 is right
        self.gravity = 1        # Controls speed player is pulled down
        self.grounded = True    # Certain things only happen while player is grounded
        self.speed = 10         # Player movement speed
        self.jumpheight = 4     # Player jump height
        self.traverse_target = scene        # Not entirely sure how this works but setting it to scene means it can interact with the scene
        self.walking = False        # I think I took this from the prefab and did nothing with it but I'm not deleting it just incase
        self.jumping = False        # Checks whether the player is jumping (as opposed to falling when in air)
        self.air_time = 0       # Took this name from the prefab, it controls fall speeds, but I think also goes up when jumping and then gets reset and goes up again when falling for some reason?
        self.ignore_list = [self]       # Ignores own hitboxes for movement
        self.jumpcooldown = 0       # Cooldown for jumping
        self.stuckcheck = time.time() + 5       # Checks every 5 seconds if player is stuck
        self.aescape = 0        # Counter for a button presses, resets every 5 seconds
        self.descape = 0        # Counter for d button presses, resets every 5 seconds
        self.spaceescape = 0    # Counter for space button presses, resets every 5 seconds
        self.stuckpos = 0       # Checks position every 5 seconds, player is stuck if it matches
        self.health = 100       # Player health
        self.dh = 0         # Difference in health
        self.flingvel = 0       # Velocity for flinging
        self.hitwall = False    # Checks if player hit a wall
        self.hitceiling = False     # Checks if player hit a ceiling
        self.flingdir = self.velocity       # Direction for flinging
        self.dead = False       # Checks if player is dead
        self.deadaudio = Audio('Audio/Death.mp3', loop = False, autoplay = False, volume = 0.5)     # Audio for death
        self.hurtaudio = Audio('Audio/Hurt.mp3', loop = False, autoplay = False, volume = 0.3)      # Audio for being hurt
        self.dy = 0     # Difference in y coord
        self.animationplaying = ''      # Current animation playing
        self.jumpaudio = Audio('Audio/Jump.mp3', loop = False, autoplay = False, volume = 0.2)      # Jump audio
        self.healthbar = Entity(model = 'quad', color = color.red, parent = camera.ui, scale = (0.5, 0.02), origin = (0.5, 0), position = (0.9, 0.3, 0.05), visible = False)
        self.healthbackground = Entity(model = 'quad', color = color.black, parent = camera.ui, scale = (0.5, 0.02), origin = (0.5, 0), position = (0.9, 0.3, 0.1), visible = False)
        # Not sure why this is here but i don't want to remove it and find out the hard way
        ray = raycast(self.world_position, 
                      self.down, 
                      distance = 10, 
                      ignore = (self, ), 
                      traverse_target = self.traverse_target)
        if ray.hit:
            self.y = ray.world_point[1] + 0.01

        self.playeranimation = self.Animation()     # Sets animation controller to animator entity made by function
        self.playeranimation.parent = self
        self.playeranimation.y += 0.5       # Fixes location of animation entity

    def update(self):
        if self.dead:       # Prevents updates if player is dead
            return
        
        self.ignore_list = [self] + [e for e in scene.entities if hasattr(e, 'playercollision')]    # Add all entities that has playercollision attribute to ignore list (meaning if they have the attribute they will NOT be collided with)     # Updates ignore list to include entities made after the player, and ignores entities that have playercollision attribute
        # Boxcast returns boolean when touching a collider, false if not touching, true if touching
        if not boxcast(
            self.position,
            direction=Vec3(self.velocity,self.scale_y / 2,0),
            distance=abs(self.scale_x / 2),
            ignore=self.ignore_list,
            traverse_target=self.traverse_target,
            thickness=(self.scale_x*.99, self.scale_y*.9)).hit:

            self.x += self.velocity * time.dt * self.speed      # Move player
            self.hitwall = False        # Player is not hitting wall if not boxcast.hit
        else:
            self.hitwall = True     # Player is hitting wall if boxcast.hit

        self.walking = held_keys['a'] + held_keys['d'] > 0 and self.grounded        # No idea, from the prefab, I think held_keys[] returns 1 if held and 0 if not, so pretty much if a or d are being pressed and player is on ground, walking is True, but I don't think it actually changes anything

        ray_origin = self.world_position - Vec3(0, self.scale_y / 2, 0)     # More accurate origin(rather position, origin in ursina is different as I discovered since making this) for the rays
        # raycast is like boxcast, but boxcast is a box and raycast is a line, raycast is better at checking hits in a certain direction
        ray = raycast(ray_origin + Vec3(0,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)
        left_ray = raycast(ray_origin + Vec3(-self.scale_x*.49,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)
        right_ray = raycast(ray_origin + Vec3(self.scale_x*.49,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)

        if any((ray.hit, left_ray.hit, right_ray.hit)):     # checks if any of the above raycasts hit something, since they are all facing down, essentially checks if player is touching the ground
            if not self.grounded:       # If player is not already grounded
                self.air_time = 0       # Sets player air time to 0 since player is not in air
                self.grounded = True    # Makes player grounded
            self.y = max((r.world_point.y for r in (ray, left_ray, right_ray) if r.hit)) + self.scale_y / 2     # Sets y to ground
        else:
            self.grounded = False       # If raycasts are not hitting / player is not touching ground, grounded = fasle
        
        # If not grounded or jumping, move downward
        if not self.grounded and not self.jumping:
            self.y -= min(self.air_time * self.gravity, ray.distance - 0.1)     # Y is decreased by air time * gravity, not going below ray distance -0.1 so that it doesnt go so fast the ray misses the ground
            self.air_time += time.dt * 4 * self.gravity         # Increase air time by gravity

        # Raycasts to check for ceiling
        hit_above = raycast(self.world_position+Vec3(0,(self.scale_y/2)-0.5,0), self.up, distance=0.8, traverse_target=self.traverse_target, ignore=self.ignore_list)
        hit_above_left = raycast(self.world_position+Vec3(-self.scale_x*.49,(self.scale_y/2)-0.5,0), self.up, distance=0.8, traverse_target=self.traverse_target, ignore=self.ignore_list)
        hit_above_right = raycast(self.world_position+Vec3(self.scale_x*.49,(self.scale_y/2)-0.5,0), self.up, distance=0.8, traverse_target=self.traverse_target, ignore=self.ignore_list)
        if any((hit_above.hit, hit_above_left.hit, hit_above_right.hit)):
             if self.jumping:
                self.y = min(min((r.world_point.y for r in (hit_above, hit_above_left, hit_above_right) if r.hit)), self.y)     # Move player below ceiling rather than letting momentum carry them through the ceiling
                self.jumping = False        # Player is no longer rising
                self.air_time = 0       # Reset air velocity
             if hasattr(self, 'y_animator'):        # Kill the jump animator so it doesn't keep rising
                 self.y_animator.kill()
             self.hitceiling = True     # Player has hit the ceiling
        else:
             self.hitceiling = False    # Player has not hit the ceiling
        
        # Resets stuck checkers every 5 seconds
        if self.stuckcheck <= time.time():
            self.stuckcheck += 5        # Check every 5 seconds
            self.stuckpos = self.position       # If this position doesn't change, tries to move player out of wall
            self.aescape = 0        # Resets a presses
            self.descape = 0        # Resets d presses
            self.spaceescape = 0    # Resets space presses
        
        # flings player if fling velocity is above 0
        if self.flingvel > 0:
            self.fling()
        else:
            self.flingflipready = True      # Ready to flip direction, makes player not constantly flip when flung

        # If fling velocity is higher than 0 and ready to flip, flip player sprite, and reset flip ready
        if self.flingvel > 0 and self.flingflipready:
            self.scale_x *= -1
            self.flingflipready = False

        # If player heatlh < 0, player is dead
        if self.health <= 0:
            self.dead = True
            self.deadaudio.play()       # Play death audio
        
        # If player loses health / if player health is lower than last frame, play hurt audio
        if self.dh > self.health:
            self.hurtaudio.play()       # play hurt audio
        self.dh = self.health

        self.healthbar.scale_x = self.health / 100 * 0.5

        # Updates animations
        self.Animate()

    # Player inputs
    def input(self, key):
        # Don't move if Nosed One is speaking
        if TutorialGuy.IsSpeaking:
            return
        # Don't move if player is dead
        if self.dead:
            return
        # Jump if space/w is pressed
        if key == 'space':
            self.jump()
            self.spaceescape += 1       # Increment space/w presses for stuckcheck
        elif key == 'w':
            self.jump()
            self.spaceescape += 1       # Increment space/w presses for stuckchekc
        # If A is pressed, move left. If D is pressed, move right
        if key == 'a':
            self.velocity = -1
            self.aescape += 1       # Increment A presses for stuckcheck
        if key == 'd':
            self.velocity = 1
            self.descape += 1       # Increment D presses for stuckcheck
        if key == 'a up':
            self.velocity = held_keys['d']      # By using held_keys[] rather than 0, it doesn't stop movement if d is still being pressed
        if key == 'd up':
            self.velocity = -held_keys['a']

    # Jump function
    def jump(self):
        # Don't jump if not touching ground
        if not self.grounded:
            return
        # Don't jump if jump on cooldown
        if self.jumpcooldown > time.time():
            return
        
        # Increase jump cooldown
        self.jumpcooldown = time.time() + 0.3

        # Player is jumping and not grounded
        self.jumping = True
        self.grounded = False

        self.jumpaudio.play()       # Play jump audio
        self.target_y = self.y + self.jumpheight        # sets target position for jump to release as player y + jumpheight
        self.animate_y(self.target_y, 0.2, resolution = 30, curve = curve.out_expo)     # Slides player towards target_y, this one line of code has caused many many problems but for some reason every time I try to rewrite the jump code it refuses to work. Basically if the animator is not killed in time, the animator WILL move to the target_y, ignoring anything inbetween. You can still clip through ceilings if you're close enough to the bottom of it, it was too hard to completely fix
        self._start_fall_sequence = invoke(self.start_fall, delay = 0.2)        # After 0.2 seconds, set jumping to false and therefore start falling
    
    # Sets jump to false, kinda just here because I don't know a way around making it a function to fit in the above function
    def start_fall(self):
        self.jumping = False
    
    # Fling player
    def fling(self):
        self.flingvel = min(self.flingvel, 150)     # Fling velocity is set to either fling velocity or 150, whichever is smaller
        if self.flingdir == 0:      # If no fling direction
            self.flingdir = -1      # Fling direction is left
        if self.hitwall:        # If player hits wall
            self.flingdir *= -1     # Flip fling direction
            self.x += time.dt * 50 * self.flingdir      # Increase speed after bounce 
        else:
            self.x += time.dt * self.flingvel * self.flingdir       # If doesnt hit wall, keep moving based on fling velocity
        if not self.hitceiling:     # If player doesn't hit ceiling
            self.y += time.dt * self.flingvel / 2       # Move y based on fling velocity
        self.flingvel *= 0.8        # Decrease fling velocity
        if self.flingvel < 0.1:     # If fling velocity is small enough
            self.flingvel = 0       # Fling velocity is 0
        
    # Creates player animations
    def Animation(self):
        animation = SpriteSheetAnimation('Sprites/Player/PlayerSheet.png', tileset_size=(9,1), fps = 10, animations={'idle' : ((0, 0), (1, 0)), 'jump' : ((1, 0), (2,0)), 'rising' : ((2, 0), (2, 0)), 'stalling' : ((3, 0), (3, 0)), 'fall' : ((3, 0), (4, 0)), 'falling' : ((4, 0), (4, 0)), 'walking' : ((5, 0), (8, 0))}, double_sided = True)
        animation.scale = 2
        animation.play_animation('idle')
        animation.z -= 0.01     # Helps prevent z fighting
        return animation
    
    # Controls player animations  
    def Animate(self):
        animationdecided = False        # Animation not yet decided
        if self.velocity != 0:      # If player velocity isn't 0
            self.scale_x = self.velocity        # Set player width to velocity

        if self.velocity != 0 and self.grounded:        # If player velocity isn't 0 and player is on the ground
            if self.animationplaying != 'walking':      # If player isn't already walking
                self.playeranimation.play_animation('walking')      # Play walking animation
            self.animationplaying = 'walking'       # Set playing animation to walking
            animationdecided = True     # Animation has been decided

        vel_y = self.y - self.dy        # Y velocity = y - last frame y
        if vel_y > 0.1 and not self.grounded:       # If y velocity is above 0.1
            self.playeranimation.play_animation('rising')       # Play rising animation
            self.animationplaying = 'rising'        # Set playing animation to rising
            animationdecided = True     # Animation has been decided
        elif vel_y < 0.1 and not self.grounded:     # If y velocity is below -0.1
            self.playeranimation.play_animation('falling')      # Play falling animation
            self.animationplaying = 'falling'       # Set playing animation to falling
            animationdecided = True     # Animation has been decided
        
        # Stalling does not happen, i accidentally made value above 0.1 not -0.1, but upon realizing i changed it back and decided I liked it more before
        elif not self.grounded:     # If velocity is beteween -0.1 and 0.1 and player isnt on the gorund
            self.playeranimation.play_animation('stalling')     # Play stalling animation
            self.animationplaying = 'stalling'      # Set playing animation to stalling
            animationdecided = True     # Animation has been decided
        self.dy = self.y        # Update y difference

        if not animationdecided:        # If animation has not yet been decided
            if self.animationplaying != 'idle':     # If idle animation isn't playing
                self.playeranimation.play_animation('idle')     # Play idle animation
            self.animationplaying = 'idle'      # Set playing animation to idle

player = Player()       # Create object for player class