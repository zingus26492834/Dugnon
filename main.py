from ursina import *
app = Ursina()      # Initialising Ursina before the following files is necessary
from CodeBlocks import *
from Platforms import *
from Player import *

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
CameraEdges = GetCameraEdges()

EditorCamera()
for e in scene.entities:
    if hasattr(e, 'collider') and e.collider:
        e.collider.visible = True

def update():
    global CameraEdges
    for i in ItemCodeBlocks:
        if player.intersects(i).hit and i.Active:
            CreateCodeBlock(i.CBid)
            i.Active = False
            i.enabled = False
    if blocksdragging:
        mouselocalpos = cbpep.get_relative_point(camera.ui, mouse.position)
        cbpe.position = (mouselocalpos - blockoffset)

    cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges
    if player.position.x >= cright_edge:
        newcamerapos = cright_edge + width
        player.velocity = 0
        player.gravity = 0
        if camera.x < newcamerapos - (width / 2):
            camera.x += time.dt * 40
        else:
            camera.x = newcamerapos - (width / 2)
            player.position.x = cright_edge
            CameraEdges = GetCameraEdges()
            player.gravity = 1
    if player.position.y >= ctop_edge:
        newcamerapos = ctop_edge + height
        player.velocity = 0
        player.gravity = 0
        if camera.y < newcamerapos - (height / 2):
            camera.y += time.dt * 40
        else:
            camera.y = newcamerapos - (height / 2)
            player.position.y = ctop_edge
            CameraEdges = GetCameraEdges()
            player.gravity = 1
    if player.position.x <= cleft_edge:
        newcamerapos = cleft_edge - width
        player.velocity = 0
        player.gravity = 0
        if camera.x > newcamerapos + (width / 2):
            camera.x -= time.dt * 40
        else:
            camera.x = newcamerapos + (width / 2)
            player.position.x = cleft_edge
            CameraEdges = GetCameraEdges()
            player.gravity = 1
    if player.position.y <= cbottom_edge:
        newcamerapos = cbottom_edge - height
        player.velocity = 0
        player.gravity = 0
        if camera.y > newcamerapos + (height / 2):
            camera.y -= time.dt * 40
        else:
            camera.y = newcamerapos + (height / 2)
            player.position.y = cbottom_edge
            CameraEdges = GetCameraEdges()
            player.gravity = 1

app.run()