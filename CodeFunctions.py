# Imports
from ursina import *
from Player import *
from math import *

# Default codefunctions audio
CodeFunctionsAudios = []
CodeFunctionAudio = Audio('Audio/CodeFunction.mp3', loop = False, autoplay = False, volume = 0.3)
CodeFunctionsAudios.append(CodeFunctionAudio)

ExistingBlocks = []     # Blocks list
# Block codefunction
def FireableBlock(modification, colour = 'default', damage = 0, speed = 0, scale = 1, **kwargs):
    extraargs = {**kwargs}      # I added **kwargs to everything with plans to use it for something but it eventually became more of a habit, this does nothing, but I'll leave it here to explain that **kwargs is keyword arguments and lets you add more arguments than listed, **args also works idk the difference
    if colour != 'default':     # Makes sure colour is not default (note the spelling, "color" is handled by ursina "colour" is not)
        if colour == 'blue':        # Set color to blue if colour is blue
            r = 0
            g = 0
            b = 255
        elif colour == 'red':       # Set color to red if colour is red
            r = 255
            g = 0
            b = 0
    else:           # 255,255,255 is default color
        r = 255
        g = 255
        b = 255
    if damage != 0:     # If damage has been set
        damageoverride = damage     # Override damage
    else:
        damageoverride = 0      # Don't override damage
    if speed != 0:      # If speed has been set
        speedoverride = speed       # Override speed
    else:
        speedoverride = 0       # Don't override speed
    if scale != 1:      # etc. etc.
        scaleoverride = scale
    else:
        scaleoverride = 0

    velocity = player.scale_x       # Velocity is the player's scale, player's scale is determined by velocity but never 0 so this works
    Block = Entity(position=(0, 0), 
                   model='cube', 
                   scale = (1, 1, 1),
                   collider='box', 
                   visible=True,
                   velocity = velocity,
                   texture=load_texture('Sprites/CodeFuncBlock.png'),
                   spawntime = time.time(),
                   color = color.rgb(r, g, b),
                   **extraargs)     # Everything else is handled but you could set block jumpheight or health I guess??
    if player.grounded:     # If player is grounded place block to the side
        Block.position = (player.x + velocity, player.y)
    elif not player.jumping:        # If player is in the air but not jumping place block below
        Block.position = (player.x, player.y - 1)
    else:
        Block.position = (player.x + player.velocity, player.y - 1)     # If the player is jumping place block to the side
    Block.ignore_list = [Block, player]     # Ingore self and player, used for raycast that stops shooting block at collision
    if modification == 'shoot':     # If moodification is set to shoot
        Block.shooting = True       # Allows update loop to handle this as a moving projectile
        Block.speed = 15        # Adds speed to handle movement
        Block.position = (player.x + velocity, player.y)        # Ignores above movement and places block to the side
    elif modification == 'aiming':      # If modification is aiming
        Block.aiming = True     # Allows update loop to handle this as a moving projectile that isn't horizontally moving
        Block.destination = mouse.world_point       # Sets destination of aim to the cursor
        Block.position = (player.x, player.y + 2)
        if distance(Block.destination, player.position) < 3:        # If aim is too close to the player, reverts to make modification, prevents player from placing block inside themself
            Block.aiming = False
            Block.position = (player.x + velocity, player.y)
    
    # Damage and speed override
    if damageoverride != 0:
        Block.speed = damageoverride
    if speedoverride != 0:
        Block.damage = speedoverride
    if scaleoverride != 0:
        Block.scale = scaleoverride

    ExistingBlocks.append(Block)    # Add block to existing blocks
    CodeFunctionAudio.play()        # Play codefunction default audio
    return Block        # Return audio

ExistingFire = []
# Fire Codefunction
FireAudio = Audio('Audio/Fire.mp3', loop = False, autoplay = False, volume = 0.3)       # Fire audio
CodeFunctionsAudios.append(FireAudio)
def FireableFire(modification, colour = 'default', damage = 0, speed = 0, scale = 1, **kwargs):
    if colour != 'default':
        if colour == 'blue':
            r = 0
            g = 0
            b = 255
        elif colour == 'red':
            r = 255
            g = 0
            b = 0
    else:
        r = 255
        g = 255
        b = 255
    if damage != 0:
        damageoverride = damage
    else:
        damageoverride = 0
    if speed != 0:
        speedoverride = speed
    else:
        speedoverride = 0
    if scale != 1:
        scaleoverride = scale
    else:
        scaleoverride = 0

    velocity = player.scale_x
    Fire = Entity(position = (player.x, player.y),
                  playercollision = False,
                  visible = True,
                  collider = 'box',
                  velocity = velocity,
                  color = color.rgba(0, 0, 0, 0),       # Invisible, setting visible to false makes children and therefore animation invisible
                  scale = (1, 1, 1),
                  spawntime = time.time())
    fireanimation = CreateAnimation('fire')     # Makes animation for fire
    fireanimation.color = color.rgb(r, g, b)
    fireanimation.parent = Fire
    if modification == 'shoot':
        Fire.shooting = True
        Fire.speed = 15
        Fire.damage = 10
    elif modification == 'aiming':
        Fire.aiming = True
        Fire.speed = 10
        Fire.damage = 10
        mousepos = mouse.world_point
        dx = mousepos.x - player.x
        dy = mousepos.y - player.y
        Fire.angle = atan2(dy, dx)

    if damageoverride != 0:
        Fire.damage = damageoverride
    if speedoverride != 0:
        Fire.speed = speedoverride
    if scaleoverride != 0:
        Fire.scale = scaleoverride

    ExistingFire.append(Fire)
    FireAudio.play()
    return Fire

ExistingLasers = []
LaserAudio = Audio('Audio/Laser.mp3', loop = False, autoplay = False, volume = 0.3)     # Laser audio
CodeFunctionsAudios.append(LaserAudio)
# Laser codefunction
def FireableLaser(modification, colour = 'default', damage = 0, scale = 1, **kwargs):
    if colour != 'default':
        if colour == 'blue':
            r = 0
            g = 0
            b = 255
        elif colour == 'red':
            r = 255
            g = 0
            b = 0
    else:
        r = 255
        g = 255
        b = 255
    if damage != 0:
        damageoverride = damage
    else:
        damageoverride = 0
    if scale != 1:
        scaleoverride = scale
    else:
        scaleoverride = 0

    velocity = player.scale_x
    Laser = Entity(position = (player.x, player.y),
                  playercollision = False,
                  visible = True,
                  model = 'quad',
                  collider = 'box',
                  velocity = velocity,
                  origin = (-0.5 * velocity, 0),
                  damage = 20,
                  texture = load_texture('Sprites/laser.png'),
                  scale = (10, 1, 1),
                  spawntime = time.time(),
                  double_sided = True)      # Ursina normmally culls backsides of sprites
    if modification == 'shoot':
        Laser.damage = 30
    elif modification == 'aiming':
        Laser.origin = (-0.5, 0)
        Laser.damage = 20
        mousepos = mouse.world_point
        dx = mousepos.x - player.x
        dy = mousepos.y - player.y
        Laser.angle = atan2(-dy, dx)
        Laser.rotation_z = degrees(Laser.angle)
    if damageoverride != 0:
        Laser.damage = damageoverride
    if scaleoverride != 0:
        Laser.scale = (10 * scaleoverride, 1 * scaleoverride)
    ExistingLasers.append(Laser)
    LaserAudio.play()
    return Laser


ExistingKeys = []
# Key codefunction
def FireableKey(modification, colour = 'regular', damage = 0, speed = 0, scale = 1, **kwargs):
    if colour != 'regular':     # Colour matters more for keys so this is regular not default
        if colour == 'blue':
            r = 0
            g = 0
            b = 255
        elif colour == 'red':
            r = 255
            g = 0
            b = 0
    else:
        r = 255
        g = 255
        b = 255
    if damage != 0:
        damageoverride = damage
    else:
        damageoverride = 0
    if speed != 0:
        speedoverride = speed
    else:
        speedoverride = 0
    if scale != 1:
        scaleoverride = scale
    else:
        scaleoverride = 0

    velocity = player.scale_x
    Key = Entity(position = (player.x + velocity, player.y),
                 playercollision = False,
                 visible = True,
                 model = 'quad',
                 collider = 'box',
                 scale = (1, 0.8, 1),
                 texture = load_texture('Sprites/Key.png'),
                 spawntime = time.time(),
                 velocity = velocity,
                 colour = colour,
                 color = color.rgb(r, g, b),
                 double_sided = True)
    if Key.velocity == -1:
            Key.scale_x = -1
    if modification == 'shoot':
        Key.shooting = True
        Key.speed = 10
    elif modification == 'aiming':
        Key.aiming = True
        Key.speed = 5
        Key.position = player.x, player.y
        mousepos = mouse.world_point
        dx = mousepos.x - player.x
        dy = mousepos.y - player.y
        Key.angle = atan2(dy, dx)
        Key.rotation_z = degrees(atan2(dx, dy)) - 90
        if mousepos.x < player.x:
            Key.scale_x = -1
            Key.rotation_z = degrees(atan2(dx, dy)) + 90
        else:
            Key.scale_x = 1

    if damageoverride != 0:
        Key.damage = damageoverride
    if speedoverride != 0:
        Key.speed = speedoverride
    if scaleoverride != 0:
        Key.scale = (1 * scaleoverride, 0.8 * scaleoverride)
    ExistingKeys.append(Key)
    CodeFunctionAudio.play()
    return Key

ExistingJospeps = []
# Jospep codefunction
def Jospep(modification, colour = 'default', damage = 0, speed = 0, scale = 1, **kwargs):
    if colour != 'default':
        if colour == 'blue':
            r = 0
            g = 0
            b = 255
        elif colour == 'red':
            r = 255
            g = 0
            b = 0
    else:
        r = 255
        g = 255
        b = 255
    if damage != 0:
        damageoverride = damage
    else:
        damageoverride = 0
    if speed != 0:
        speedoverride = speed
    else:
        speedoverride = 0
    if scale != 1:
        scaleoverride = scale
    else:
        scaleoverride = 0

    velocity = player.scale_x
    Jospep = Entity(position = (player.x + velocity, player.y),
                    playercollision = False,
                    visible = True,
                    model = 'quad',
                    collider = 'box',
                    scale = (1, 1, 1),
                    color = color.rgba(0, 0, 0, 0),
                    velocity = velocity,
                    spawntime = time.time(),
                    damage = 20,
                    speed = 15)
    jospepanimation = CreateAnimation('jospep')
    jospepanimation.color = color.rgb(r, g, b)
    jospepanimation.parent = Jospep
    if Jospep.velocity == -1:
        Jospep.scale_x = -1
    if modification == 'shoot':
        Jospep.damage = 40
        Jospep.speed = 30
    elif modification == 'aiming':
        Jospep.aiming = True
        Jospep.speed = 20
        Jospep.position = player.x, player.y
        mousepos = mouse.world_point
        dx = mousepos.x - player.x
        dy = mousepos.y - player.y
        Jospep.angle = atan2(dy, dx)
        Jospep.rotation_z = degrees(atan2(dx, dy)) - 90
        if mousepos.x < player.x:
            Jospep.scale_x = -1
            Jospep.rotation_z = degrees(atan2(dx, dy)) + 90
        else:
            Jospep.scale_x = 1
    
    if damageoverride != 0:
        Jospep.damage = damageoverride
    if speedoverride != 0:
        Jospep.speed = speedoverride
    if scaleoverride != 0:
        Jospep.scale = scaleoverride

    ExistingJospeps.append(Jospep)
    return Jospep

# Boiled One concept by Doctor Nowhere
HiredOnes = []
# HiredOne codefunction
def HiredOne(modification, colour = 'default', damage = 0, speed = 0, scale = 1, **kwargs):
    if colour != 'default':
        if colour == 'blue':
            r = 0
            g = 0
            b = 255
        elif colour == 'red':
            r = 255
            g = 0
            b = 0
    else:
        r = 255
        g = 255
        b = 255
    if damage != 0:
        damageoverride = damage
    else:
        damageoverride = 0
    if speed != 0:
        speedoverride = speed
    else:
        speedoverride = 0
    if scale != 1:
        scaleoverride = scale
    else:
        scaleoverride = 0

    velocity = player.scale_x
    HiredOne = Entity(position = (player.x + velocity, player.y),
                    playercollision = False,
                    visible = True,
                    model = 'quad',
                    collider = 'box',
                    scale = (1, 1, 1),
                    texture = load_texture('Sprites/BoiledOne.png'),
                    velocity = velocity,
                    spawntime = time.time(),
                    damage = 100,
                    double_sided = True,
                    speed = 15)
    if HiredOne.velocity == -1:
        HiredOne.scale_x = -1
    if modification == 'shoot':
        HiredOne.damage = 150
        HiredOne.speed = 30
    elif modification == 'aiming':
        HiredOne.aiming = True
        HiredOne.speed = 15
        HiredOne.position = player.x, player.y
        mousepos = mouse.world_point
        dx = mousepos.x - player.x
        dy = mousepos.y - player.y
        HiredOne.angle = atan2(dy, dx)
        HiredOne.rotation_z = degrees(atan2(dx, dy)) - 90
        if mousepos.x < player.x:
            HiredOne.scale_x = -1
            HiredOne.rotation_z = degrees(atan2(dx, dy)) + 90
        else:
            HiredOne.scale_x = 1
    
    if damageoverride != 0:
        HiredOne.damage = damageoverride
    if speedoverride != 0:
        HiredOne.speed = speedoverride
    if scaleoverride != 0:
        HiredOne.scale = scaleoverride
    HiredOnes.append(HiredOne)
    return HiredOne

EntryPortals = []
ExitPortals = []
# Portals codefunction and also just portals generatoin code
def SummonPortal(x, y, chunkx, chunky, colour = 'default', scale = 1, **kwargs):
     if colour != 'default':
        if colour == 'blue':
            r = 0
            g = 0
            b = 255
        elif colour == 'red':
            r = 255
            g = 0
            b = 0
     else:
        r = 255
        g = 255
        b = 255
     if scale != 1:
        scaleoverride = scale
     else:
        scaleoverride = 0

     ExitLocationX = random.randint(10000, 1000000)     # Randomly determines exit location far from portal
     ExitLocationY = random.randint(10000, 1000000)
     ExitChunkX = random.randint(10000, 1000000)        # Randomly determines chunk coords far from portal
     ExitChunkY = random.randint(10000, 1000000)
     EntryPortal = Entity(position = (x, y),
                     model = 'quad',
                     scale = (2, 2),
                     playercollision = False,
                     despawnable = True,
                     color = color.rgba(0, 0, 0, 0),
                     chunkx = ExitChunkX,
                     chunky = ExitChunkY,
                     collider = 'box',
                     Generated = False,
                     GenerateCoordX = ExitLocationX,
                     GenerateCoordY = ExitLocationY)
     entryportalanimation = CreateAnimation('portal')
     entryportalanimation.color = color.rgb(r, g, b)
     entryportalanimation.parent = EntryPortal
     entryportalanimation.z += 0.05     # Pushes sprite behind other sprites to prevent z fighting
     ExitPortal = Entity(position = (ExitLocationX + 13, ExitLocationY + 10),
                         model = 'quad',
                         scale = (2, 2),
                         playercollision = False,
                         color = color.rgba(0, 0, 0, 0),
                         despawnable = True,
                         chunkx = chunkx,
                         chunky = chunky,
                         collider = 'box')
     exitportalanimation = CreateAnimation('portal')
     exitportalanimation.color = color.rgb(r, g, b)
     exitportalanimation.parent = ExitPortal
     exitportalanimation.z == 0.05
     EntryPortal.destination = ExitPortal.position      # portal destinations are set to each other
     ExitPortal.destination = EntryPortal.position
     if scaleoverride != 0:
         ExitPortal.scale = scaleoverride * 2
         EntryPortal.scale = scaleoverride * 2
     ExitPortals.append(ExitPortal)
     EntryPortals.append(EntryPortal)
     return EntryPortal, ExitPortal

# Animations
def CreateAnimation(type):
    if type == 'fire':
        fireanimation = SpriteSheetAnimation('Sprites/Fire/Firesheet.png', tileset_size=(3,1), fps = 6, animations={'burn' : ((0, 0), (2, 0))}, doublesided = True)
        fireanimation.scale = 2
        fireanimation.play_animation('burn')
        return fireanimation
    elif type == 'jospep':
        jospepanimation = SpriteSheetAnimation('Sprites/Jospep/JospepSheet.png', tileset_size=(11,1), fps = 15, animations={'run' : ((0, 0), (10, 0))}, double_sided = True)
        jospepanimation.scale = 2
        jospepanimation.play_animation('run')
        return jospepanimation
    elif type == 'portal':
          portalanimation = SpriteSheetAnimation('Sprites/Portal/PortalSheet.png', tileset_size=(5,1), fps = 10, animations={'spin' : ((0, 0), (4, 0))})
          portalanimation.scale = 3
          portalanimation.play_animation('spin')
          return portalanimation