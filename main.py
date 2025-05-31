from ursina import *
app = Ursina()      # Initialising Ursina before the following files is necessary
from CodeBlocks import *
from Platforms import *
from Player import *
from CodeFunctions import *

camera.orthographic = True
camera.position = (30/2,8)
camera.fov = 16
height = camera.fov
ratio = window.aspect_ratio
width = height * ratio

def GetCameraEdges():
    cright_edge = camera.x + (width / 2)
    ctop_edge = camera.y + (height / 2)
    cleft_edge = camera.x - (width / 2)
    cbottom_edge = camera.y - (height / 2)
    return cright_edge, ctop_edge, cleft_edge, cbottom_edge

CodeBlocksEnabled = False
blocksdragging = False
blockoffset = Vec3(0, 0, 0)
executing = False
def input(key):
    global CodeBlocksEnabled, blockoffset, blocksdragging, executing
    if key == 'q':
        executing = not executing
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
    if key == 'o':
        player.position = (camera.x, camera.y)

    if executing:
        execute(key)

make_level(load_texture('Levels/platformer_tutorial_level'), 0, 0, 0, 0)
CameraEdges = GetCameraEdges()

chunkx = 0
chunky = 0
incrementchunk = False
def update():
    global CameraEdges, chunkx, chunky, incrementchunk, executing
    for i in ItemCodeBlocks:
        if player.intersects(i).hit and i.Active:
            CreateCodeBlock(i.CBid)
            i.Active = False
            i.enabled = False
    if blocksdragging:
        mouselocalpos = cbpep.get_relative_point(camera.ui, mouse.position)
        cbpe.position = (mouselocalpos - blockoffset)

    #for e in scene.entities:
     #   if hasattr(e, 'collider') and e.collider:
      #      e.collider.visible = True

    cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges

    # Right edge
    if player.position.x >= cright_edge:
        newcamerapos = cright_edge + width
        player.velocity = 0
        player.gravity = 0
        if not incrementchunk:
            chunkx += 1
            incrementchunk = True
        if not CheckChunk(chunkx, chunky):
            RandomLevel('right', cright_edge, cbottom_edge, chunkx, chunky)
        if camera.x < newcamerapos - (width / 2):
            camera.x += time.dt * 40
        else:
            camera.x = newcamerapos - (width / 2)
            player.position.x = cright_edge
            CameraEdges = GetCameraEdges()
            player.gravity = 1
            incrementchunk = False

    # Top edge
    if player.position.y >= ctop_edge:
        newcamerapos = ctop_edge + height
        player.velocity = 0
        player.gravity = 0
        if not incrementchunk:
            chunky += 1
            incrementchunk = True
        if not CheckChunk(chunkx, chunky):
            RandomLevel('up', cleft_edge, ctop_edge, chunkx, chunky)
        if camera.y < newcamerapos - (height / 2):
            camera.y += time.dt * 40
        else:
            camera.y = newcamerapos - (height / 2)
            player.position.y = ctop_edge
            CameraEdges = GetCameraEdges()
            player.gravity = 1
            incrementchunk = False

    # Left edge
    if player.position.x <= cleft_edge:
        newcamerapos = cleft_edge - width
        player.velocity = 0
        player.gravity = 0
        if not incrementchunk:
            chunkx -= 1
            incrementchunk = True
        if not CheckChunk(chunkx, chunky):
            RandomLevel('left', cleft_edge - width, cbottom_edge, chunkx, chunky)
        if camera.x > newcamerapos + (width / 2):
            camera.x -= time.dt * 40
        else:
            camera.x = newcamerapos + (width / 2)
            player.position.x = cleft_edge
            CameraEdges = GetCameraEdges()
            player.gravity = 1
            incrementchunk = False
    # Bottom edge
    if player.position.y <= cbottom_edge:
        newcamerapos = cbottom_edge - height
        player.velocity = 0
        player.gravity = 0
        if not incrementchunk:
            chunky -= 1
            incrementchunk = True
        if not CheckChunk(chunkx, chunky):
            RandomLevel('down', cleft_edge, cbottom_edge - height, chunkx, chunky)
        if camera.y > newcamerapos + (height / 2):
            camera.y -= time.dt * 40
        else:
            camera.y = newcamerapos + (height / 2)
            player.position.y = cbottom_edge
            CameraEdges = GetCameraEdges()
            player.gravity = 1
            incrementchunk = False

CreateCodeBlock(15)
CreateCodeBlock(13)
CreateCodeBlock(1)
CreateCodeBlock(4)
CreateCodeBlock(0)
CreateCodeBlock(17)
for i in range(10):
    CreateCodeBlock(9)
app.run()