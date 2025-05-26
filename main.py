from ursina import *
app = Ursina()      # Initialising Ursina before the following files is necessary
from CodeBlocks import *
from Platforms import *

camera.orthographic = True
camera.position = (30/2,8)
camera.fov = 16

CodeBlocksEnabled = False
def input(key):
    global CodeBlocksEnabled
    if key == 'space':
        execute()
    if key == 'k':
        CodeBlocksEnabled = not CodeBlocksEnabled
        ToggleCodeBlocks(CodeBlocksEnabled)

make_level(load_texture('Levels/platformer_tutorial_level'))

EditorCamera()
def update():
    for i in ItemCodeBlocks:
        if player.intersects(i).hit and i.Active:
            CreateCodeBlock(i.CBid)
            i.Active = False
            i.enabled = False
    
    if mouse.scroll.y != 0:
        .scale += mouse.scroll.y * 0.1

app.run()