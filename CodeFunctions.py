from ursina import *
from Player import *

ExistingBlocks = []
def FireableBlock(modification, **kwargs):
    extraargs = {**kwargs}
    if modification == 'make':
        Block = Entity(position=(player.x, player.y - 1), 
                model='cube', 
                scale = (1, 1, 1),
                collider='box', 
                visible=True,
                texture=load_texture('brick'),
                **extraargs)
        ExistingBlocks.append(Block)
        return Block
    if modification =='shoot':
        Block = Entity(position=(player.x + 1, player.y), 
                model='cube', 
                scale = (1, 1, 1),
                collider='box', 
                visible=True,
                texture=load_texture('brick'),
                shooting = True,
                speed = 15,
                spawntime = time.time(),
                **extraargs)
        Block.ignore_list = [player, Block]
        ExistingBlocks.append(Block)
        return Block

ExistingFire = []
def FireableFire(modification, **kwargs):
    if modification == 'make':
        Fire = Entity(position = (player.x, player.y),
                      playercollision = False,
                      visible = True,
                      collider = 'box',
                      scale = (1, 1, 1),
                      spawntime = time.time()
                      )
        fireanimation = CreateAnimation('fire')
        fireanimation.parent = Fire
        ExistingFire.append(Fire)
        return Fire
    if modification == 'shoot':
        Fire = Entity(position = (player.x, player.y),
                      playercollision = False,
                      visible = True,
                      collider = 'box',
                      scale = (1, 1, 1),
                      spawntime = time.time(),
                      shooting = True,
                      speed = 15)
        fireanimation = CreateAnimation('fire')
        fireanimation.parent = Fire
        ExistingFire.append(Fire)
        return Fire

ExistingKeys = []
def FireableKey(modification, **kwargs):
    if modification == 'make':
        Key = Entity(position = (player.x + 1, player.y),
                     playercollision = False,
                     visible = True,
                     model = 'quad',
                     collider = 'box',
                     scale = (1, 1, 1),
                     texture = load_texture('Sprites/Key.png'),
                     spawntime = time.time())
        ExistingKeys.append(Key)
        return Key
    if modification == 'shoot':
        Key = Entity(position = (player.x + 1, player.y),
                     playercollision = False,
                     visible = True,
                     model = 'quad',
                     collider = 'box',
                     scale = (1, 1, 1),
                     texture = load_texture('Sprites/Key.png'),
                     spawntime = time.time(),
                     shooting = True,
                     speed = 10)
        ExistingKeys.append(Key)
        return Key
        
    

def CreateAnimation(type):
    if type == 'fire':
        fireanimation = SpriteSheetAnimation('Sprites/Fire/Firesheet.png', tileset_size=(3,1), fps = 6, animations={'burn' : ((0, 0), (2, 0))})
        fireanimation.scale = 2
        fireanimation.play_animation('burn')
        return fireanimation