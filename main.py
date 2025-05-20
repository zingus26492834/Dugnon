from ursina import *
app = Ursina()      # Initialising Ursina before the following files is necessary
from CodeBlocks import *
from Platforms import *

camera.orthographic = True
camera.position = (30/2,8)
camera.fov = 16

ifblock = CodeBlock('CodeBlocks/if.png', 'if ')
cheese = CodeBlock('CodeBlocks/cheese.png', 'apple:\n    ')
banana = CodeBlock('CodeBlocks/banana.png', 'print("Banana")')
CurrentCodeBlocks = [ifblock, cheese, banana]

CodeBlocksEnabled = False
for c in CurrentCodeBlocks:
    c.Active = False
    c.visible = False

def input(key):
    global CodeBlocksEnabled
    if key == 'space':
        execute(apple=True)
    if key == 'k':
        CodeBlocksEnabled = not CodeBlocksEnabled
        for c in CurrentCodeBlocks:
            if CodeBlocksEnabled:
                c.Active = True
                c.visible = True
            else:
                c.Active = False
                c.visible = False

make_level(load_texture('Levels/platformer_tutorial_level'))

EditorCamera()
app.run()