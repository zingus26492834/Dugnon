from ursina import *
from CodeBlocks import *
from Player import *

quad = load_model('quad', use_deepcopy=True)
level_parent = Entity(model=Mesh(vertices=[], uvs=[]), texture='white_cube')
ItemCodeBlocks = []

def make_level(texture):
    for y in range(texture.height):
        collider = None
        for x in range(texture.width):
            col = texture.get_pixel(x,y)


            if col == color.black:
                level_parent.model.vertices += [Vec3(*e) + Vec3(x+.5,y+.5,0) for e in quad.generated_vertices]
                level_parent.model.uvs += quad.uvs
                if not collider:
                    collider = Entity(parent=level_parent, 
                                      position=(x,y), 
                                      model='cube', 
                                      origin=(-.5,-.5), 
                                      collider='box', 
                                      visible=False)
                else:
                    collider.scale_x += 1
            else:
                collider = None

            if col == color.green:
                player.start_position = (x, y)
                player.position = player.start_position
            
            if col == color.red:
                ItemCodeBlocks.append(GenerateCodeBlock(RandomCodeBlock(), (x + 0.5), (y + 0.5)))

    level_parent.model.generate()