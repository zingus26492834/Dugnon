from ursina import *
from Player import *

ExistingBlocks = []
def FireableBlock(modification, **kwargs):
    extraargs = {**kwargs}
    Block = Entity(position=(player.x, player.y - 1), 
                   model='cube', 
                   scale = (1, 1, 1),
                   collider='box', 
                   visible=True,
                   texture=load_texture('brick'),
                   spawntime = time.time(),
                   **extraargs)
    Block.ignore_list = [Block,]
    if modification == 'shoot':
        Block.shooting = True
        Block.speed = 15
    ExistingBlocks.append(Block)
    return Block

ExistingFire = []
def FireableFire(modification, **kwargs):
    Fire = Entity(position = (player.x, player.y),
                  playercollision = False,
                  visible = True,
                  collider = 'box',
                  scale = (1, 1, 1),
                  spawntime = time.time())
    fireanimation = CreateAnimation('fire')
    fireanimation.parent = Fire
    if modification == 'shoot':
        Fire.shooting = True
        Fire.speed = 15
        Fire.damage = 10
    ExistingFire.append(Fire)
    return Fire

ExistingKeys = []
def FireableKey(modification, colour = 'regular', **kwargs):
    Key = Entity(position = (player.x + 1, player.y),
                 playercollision = False,
                 visible = True,
                 model = 'quad',
                 collider = 'box',
                 scale = (1, 1, 1),
                 texture = load_texture('Sprites/Key.png'),
                 spawntime = time.time(),
                 colour = colour)
    if modification == 'shoot':
        Key.shooting = True
        Key.speed = 10
    ExistingKeys.append(Key)
    return Key

ExistingJospeps = []
def Jospep(modification, **kwargs):
    Jospep = Entity(position = (player.x + 1, player.y),
                    playercollision = False,
                    visible = True,
                    model = 'quad',
                    collider = 'box',
                    scale = (1, 1, 1),
                    spawntime = time.time(),
                    damage = 20,
                    color = color.rgba(0, 0, 0, 0),
                    speed = 15)
    jospepanimation = CreateAnimation('jospep')
    jospepanimation.parent = Jospep
    if modification == 'shoot':
        Jospep.damage = 40
        Jospep.speed = 30
    ExistingJospeps.append(Jospep)
    return Jospep
    

def CreateAnimation(type):
    if type == 'fire':
        fireanimation = SpriteSheetAnimation('Sprites/Fire/Firesheet.png', tileset_size=(3,1), fps = 6, animations={'burn' : ((0, 0), (2, 0))})
        fireanimation.scale = 2
        fireanimation.play_animation('burn')
        return fireanimation
    elif type == 'jospep':
        jospepanimation = SpriteSheetAnimation('Sprites/Jospep/JospepSheet.png', tileset_size=(11,1), fps = 15, animations={'run' : ((0, 0), (10, 0))})
        jospepanimation.scale = 2
        jospepanimation.play_animation('run')
        return jospepanimation