from ursina import *
from Player import *

def FireableBlock(modification, **kwargs):
    extraargs = {**kwargs}
    if modification == 'make':
        Block = Entity(position=(player.x, player.y - 1), 
                model='cube', 
                origin=(-.5,-.5), 
                scale = (1, 1, 1),
                collider='box', 
                visible=True,
                texture=load_texture('brick'),
                **extraargs)
        return Block