from ursina import *
app = Ursina()      # Initialising Ursina before the following files is necessary
from CodeBlocks import *
from Platforms import *

camera.orthographic = True
camera.position = (30/2,8)
camera.fov = 16

CodeBlocksEnabled = False
blocksdragging = False
blockoffset = Vec3(0, 0, 0)
def input(key):
    global CodeBlocksEnabled, blockoffset, blocksdragging
    if key == 'space':
        execute()
    if key == 'k':
        CodeBlocksEnabled = not CodeBlocksEnabled
        ToggleCodeBlocks(CodeBlocksEnabled)
    if key == 'scroll up' and CodeBlocksEnabled:
        scrollblock('up')
    if key == 'scroll down' and CodeBlocksEnabled:
        scrollblock('down')
    if key == 'right mouse down' and CodeBlocksEnabled:
        blocksdragging = True
        mouselocalpos = cbpep.get_relative_point(camera.ui, mouse.position)
        blockoffset = (mouselocalpos - cbpe.position)
    if key == 'right mouse up' and CodeBlocksEnabled:
        blocksdragging = False

make_level(load_texture('Levels/platformer_tutorial_level'))

def update():
    for i in ItemCodeBlocks:
        if player.intersects(i).hit and i.Active:
            CreateCodeBlock(i.CBid)
            i.Active = False
            i.enabled = False
    if blocksdragging:
        mouselocalpos = cbpep.get_relative_point(camera.ui, mouse.position)
        cbpe.position = (mouselocalpos - blockoffset)

app.run()