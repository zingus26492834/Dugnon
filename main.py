from ursina import *
app = Ursina()      # Initialising Ursina before the following files is necessary
from CodeBlocks import *
from Platforms import *
from Player import *
from CodeFunctions import *
from Enemy import *
from Tutorial import *

# Camera Settings
camera.orthographic = True
camera.position = (30/2,8)
camera.fov = 16
height = camera.fov
ratio = window.aspect_ratio
width = height * ratio

# Function to find Edges of the Camera
def GetCameraEdges():
    cright_edge = camera.x + (width / 2)
    ctop_edge = camera.y + (height / 2)
    cleft_edge = camera.x - (width / 2)
    cbottom_edge = camera.y - (height / 2)
    return cright_edge, ctop_edge, cleft_edge, cbottom_edge

# Function to check inputs, built in to run every time a key is pressed by Ursina
CodeBlocksEnabled = False
blocksdragging = False
blockoffset = Vec3(0, 0, 0)
titlescreen = True
executing = False
def input(key):
    global titlescreen
    global CodeBlocksEnabled, blockoffset, blocksdragging, executing
    # key is a variable handled by Ursina which is set to whichever key is being pressed

    # Toggle Fullscreen    
    if key == 'y':
        window.fullscreen = not window.fullscreen

    if TutorialGuy.IsSpeaking:
        return

    # Toggle Executing code
    if key == 'q':
        executing = not executing       # sets executing boolean to whatever executing isnt
    # Toggle CodeBlocks UI
    if key == 'k':
        CodeBlocksEnabled = not CodeBlocksEnabled       # sets CodeBlocksEnabled boolean to whatever CodeBlocksEnable isnt
        ToggleCodeBlocks(CodeBlocksEnabled)     # Feeds boolean into ToggleCodeBlocks function
    # Controlling CodeBlocks UI
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
    
    # Open CodeBlocks Guide
    if key == 'p':
        if CodeBlocksEnabled:
            CodeBlocksGuide.visible = not CodeBlocksGuide.visible
    
    # Debug keys
    if key == 'o':
        player.position = (camera.x, camera.y)
    if key == 'h':
        print(player.position)
    if key == 'g':
        BossLevel(player.x + 4, player.y + 1)

    # This needs to be here to read keyboard inputs, however does not normally run every frame (check update func)
    if executing:
        execute(key)

    # Boss Spawners
    global LockRoom
    for B in BossSpawners:
        if player.intersects(B) and not B.spawned and key == 'space':
            B.enabled = False
            B.despawnable = False
            B.spawned = True
            LockRoom = True
            BossEnemy(position = (B.x, B.y + 2), spawntime = time.time())


################################################################################

# Update loop handled by Ursina automatically
chunkx = 0
chunky = 0
incrementchunk = False
keynotification = False
keycolour = 'regular'
keymessage = Text(text = f'You need a {keycolour} key to open this door', origin = (0, -3), scale = 2, visible = False, parent = camera.ui)
# Update Function, runs every tick
def update():
    global titlescreen
    if titlescreen:
        return
    
    global CameraEdges, chunkx, chunky, incrementchunk, executing
    for i in ItemCodeBlocks:        # Checks every CodeBlock pickup
        if player.intersects(i).hit and i.Active:       # If player and pickup intersect
            if hasattr(i, 'rare'):
                CreateRareCodeBlock(i.CBid)
            else:
                CreateCodeBlock(i.CBid)     # Creates a CodeBlock in the image of the pickup
            i.Active = False        # Disables pickup code
            i.despawnable = False
            i.enabled = False       # Disables pickup
    if blocksdragging:      # If player is panning the blocks
        mouselocalpos = cbpep.get_relative_point(camera.ui, mouse.position)     # Finds accurate position of mouse(can be wildly inaccurate otherwise)
        cbpe.position = (mouselocalpos - blockoffset)       # Moves codeblock parent entity with mouse (pans blocks ui)

    # Creates variable for every camera edge
    cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges

    # Check every edge, create new levels, and screen transitions handling
    # Right edge
    if player.position.x >= cright_edge:        # If player moves beyond the right side of the screen
        newcamerapos = cright_edge + width      # New camera position is 1 screen to the right
        player.velocity = 0     # Stops the player's horizonal movement
        player.gravity = 0      # Stops the player's vertical movement
        # On the first frame the chunk is being loaded, update coordinates of new chunk
        if not incrementchunk:
            chunkx += 1
            incrementchunk = True
        # If there is no Level loaded in the chunk, create a level there
        if not CheckChunk(chunkx, chunky):
            RandomLevel('right', cright_edge, cbottom_edge, chunkx, chunky)
        # Until camera has reached the new position, slide it towards that point
        if camera.x < newcamerapos - (width / 2):
            camera.x += time.dt * 40
        else:
            camera.x = newcamerapos - (width / 2)       # Snap camera to the new position, in case it moved too far
            player.position.x = cright_edge + 1     # Places the player on the new screen
            CameraEdges = GetCameraEdges()      # Checks new Camera Edges
            player.gravity = 1      # Reenables gravity for the player
            incrementchunk = False      # Sets up for next chunk to be loaded

    # Top edge
    if player.position.y >= ctop_edge:       # If player moves above the top of the screen
        newcamerapos = ctop_edge + height       # New camera position is 1 screen above
        player.velocity = 0     # Stops the player's horizonal movement
        player.gravity = 0      # Stops the player's vertical movement
        # On the first frame the chunk is being loaded, update coordinates of new chunk
        if not incrementchunk:
            chunky += 1
            incrementchunk = True
        # If there is no Level loaded in the chunk, create a level there
        if not CheckChunk(chunkx, chunky):
            RandomLevel('up', cleft_edge, ctop_edge, chunkx, chunky)
        # Until camera has reached the new position, slide it towards that point
        if camera.y < newcamerapos - (height / 2):
            camera.y += time.dt * 40
        else:
            camera.y = newcamerapos - (height / 2)      # Snap camera to the new position, in case it moved too far
            player.position.y = ctop_edge + 15       # Places the player on the new screen
            CameraEdges = GetCameraEdges()      # Checks new Camera Edges
            player.gravity = 1      # Reenables gravity for the player
            incrementchunk = False      # Sets up for next chunk to be loaded
                

    # Left edge
    if player.position.x <= cleft_edge:     # If player moves beyond the left side of the screen
        newcamerapos = cleft_edge - width       # New camera position is 1 screen to the left
        player.velocity = 0     # Stops the player's horizonal movement
        player.gravity = 0      # Stops the player's vertical movement
        # On the first frame the chunk is being loaded, update coordinates of new chunk
        if not incrementchunk:
            chunkx -= 1
            incrementchunk = True
        # If there is no Level loaded in the chunk, create a level there    
        if not CheckChunk(chunkx, chunky):
            RandomLevel('left', cleft_edge - width, cbottom_edge, chunkx, chunky)
        # Until camera has reached the new position, slide it towards that point
        if camera.x > newcamerapos + (width / 2):
            camera.x -= time.dt * 40
        else:
            camera.x = newcamerapos + (width / 2)       # Snap camera to the new position, in case it moved too far
            player.position.x = cleft_edge - 1      # Places the player on the new screen
            CameraEdges = GetCameraEdges()      # Checks new Camera Edges
            player.gravity = 1      # Reenables gravity for the player
            incrementchunk = False      # Sets up for next chunk to be loaded
    # Bottom edge
    if player.position.y <= cbottom_edge:       # If player moves below the bottom of the screen
        newcamerapos = cbottom_edge - height        # New camera position is 1 screen below
        player.velocity = 0     # Stops the player's horizonal movement
        player.gravity = 0      # Stops the player's vertical movement
        # On the first frame the chunk is being loaded, update coordinates of new chunk
        if not incrementchunk:
            chunky -= 1
            incrementchunk = True
        # If there is no Level loaded in the chunk, create a level there
        if not CheckChunk(chunkx, chunky):
            RandomLevel('down', cleft_edge, cbottom_edge - height, chunkx, chunky)
        # Until camera has reached the new position, slide it towards that point
        if camera.y > newcamerapos + (height / 2):
            camera.y -= time.dt * 40
        else:
            camera.y = newcamerapos + (height / 2)      # Snap camera to the new position, in case it moved too far
            player.position.y = cbottom_edge - 8        # Places the player on the new screen
            CameraEdges = GetCameraEdges()      # Checks new Camera Edges
            player.gravity = 1      # Reenables gravity for the player
            incrementchunk = False      # Sets up for next chunk to be loaded

    # Unstuck player if spam a w d
    if player.spaceescape >= 5 and player.aescape >= 5 and player.descape >= 5 and player.position == player.stuckpos:
            player.x += 1
            player.y += 1

    # Locked Doors
    global keycolour, starttime, keynotification
    for L in LockedDoors:       # Checks every Locked Door
        for K in ExistingKeys:      # Checks every Key
            # If door and key intersect, remove both
            if L.intersects(K):
                L.despawnable = False
                L.enabled = False
                K.enabled = False
        if L.intersects(player) and L.enabled:
            keynotification = True
            starttime = time.time()
            keycolour = L.colour

    if keynotification:
        keymessage.visible = True
        if keycolour != 'regular':
            keymessage.color = getattr(color, keycolour)
        else:
            keymessage.color = color.yellow
        keymessage.text = f'You need a {keycolour} key to open this door'
        if time.time() - starttime > 3:
            keymessage.visible = False
            keynotification = False
    
    # CodeFunctions
    currenttime = time.time()       # Necessary to create a variable with this value rather than just calling time.time()
    for b in ExistingBlocks:        # Checks every block from CodeFunctions.py
        if hasattr(b, 'shooting'):      # Checks if the block was made with shooting modification
            b.x += time.dt * b.speed        # Moves block horizontally every frame
            ray_origin = b.world_position - Vec3(0, b.scale_y / 2, 0)       # Creates a more accurate start point for raycasts
            # Raycasts to check collision
            topray = raycast(ray_origin + Vec3(b.scale_x*.49,b.scale_y,0), b.right, distance=max(.15,  0.15), ignore=b.ignore_list, traverse_target=scene)
            middleray = raycast(ray_origin + Vec3(b.scale_x*.49, b.scale_y / 2, 0), b.right, distance=max(.15, 0.15), ignore=b.ignore_list, traverse_target=scene)
            bottomray = raycast(ray_origin + Vec3(b.scale_x*.49,.1,0), b.right, distance=max(.15,  0.15), ignore=b.ignore_list, traverse_target=scene)
            if any((topray.hit, middleray, bottomray.hit)):     # If any of the raycasts collide with an Entity that isn't the player or itself
                delattr(b, 'shooting')      # Ends the loop, therefore stopping movement
            # Also end the loop and stop movement after half a second if no collision
            elif currenttime - b.spawntime > 0.5:
                delattr(b, 'shooting')
            if currenttime - b.spawntime > 5.5:
                b.enabled = False
                ExistingBlocks.remove(b)
        elif currenttime - b.spawntime > 5:
            b.enabled = False
            ExistingBlocks.remove(b)
    for f in ExistingFire:      # Checks every fire entity from CodeFunctions.py
        # Delete the fire after 2 seconds
        if currenttime - f.spawntime > 2:
            f.enabled = False
            ExistingFire.remove(f)      # Makes sure loop isn't checking nonexistant fire entities
        # If shooting modification, move the fire horizontally
        if hasattr(f, 'shooting'):
            f.x += time.dt * f.speed
    # Checks every key from CodeFunctions.py
    for k in ExistingKeys:
        # Delete the key after 2 seconds
        if currenttime - k.spawntime > 2:
            k.enabled = False
            ExistingKeys.remove(k)      # Makes sure loop isn't checking nonexistant key entities
        # If shooting modification, move key horizontally
        if hasattr(k, 'shooting'):
            k.x += time.dt * k.speed
    for j in ExistingJospeps:
        if currenttime - j.spawntime > 1.5:
            j.enabled = False
            ExistingJospeps.remove(j)
        j.x += time.dt * j.speed

    for e in [e for e in scene.entities if hasattr(e, 'Enemy') and e.enabled]:
        for a in [a for a in ExecutedEntities if hasattr(a, 'damage')]:
            if a.intersects(e) and e.hurtcooldown - time.time() <= 0:
                e.health -= a.damage
                e.hurtcooldown = time.time() + 0.5
                a.spawntime -= 20

    # Solves problem of execute not running every frame by called input function every frame regrdless of input
    if executing:
        input(None)

    if player.dead:
        DeathSplash.enabled = True
        ReturnButton.enabled = True
    
    for e in scene.entities:
        if hasattr(e, 'despawnable') and e.despawnable:
            if distance(player, e) > 100:
                e.enabled = False
                #e.visible = False
            else:
                e.enabled = True
                #e.visible = True

    # Tutorial
    if player.intersects(TutorialEntity) and TutorialEntity.enabled:
        TutorialGuy.visible = True
    if TutorialGuy.IsSpeaking:
        player.velocity = 0
    if TutorialGuy.SecretObtained:
        CurrentCodeBlocks.append(CodeBlock(texture = 'CodeBlocks/Jospep.png', code = "ExecutedEntities.append(Jospep(", visible = False))
        TutorialGuy.SecretObtained = False
    
    if LockRoom:
        TopLockCollider.enabled = True
        BottomLockCollider.enabled = True
        RightLockCollider.enabled = True
        LeftLockCollider.enabled = True
        TopLockCollider.position = (cright_edge, ctop_edge)
        BottomLockCollider.position = (cright_edge, cbottom_edge)
        RightLockCollider.position = (cright_edge, cbottom_edge + 1)
        LeftLockCollider.position = (cleft_edge, cbottom_edge + 1)
    else:
        TopLockCollider.enabled = False
        BottomLockCollider.enabled = False
        RightLockCollider.enabled = False
        LeftLockCollider.enabled = False

################################################################################

CameraEdges = GetCameraEdges()      # Finds edges of the starting screen
cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges

def start():
    global CameraEdges, titlescreen
    titlescreen = False
    player.enabled = True
    player.health = 100
    player.dead = False
    # Start game / Load tutorial levels, load tutorial codeblock items
    make_level(load_texture('Levels/platformer_tutorial_level'), 2, 0, 0, 0, randomdoors = False)        # Creates the tutorial level / starting room
    player.y += 2       # Makes sure the player doesn't get stuck in the ground
    CameraEdges = GetCameraEdges()      # Finds edges of the starting screen
    cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges
    # Make first 3 levels after start room non random
    make_level(load_texture('Levels/intersection'), cright_edge, cbottom_edge, 1, 0, randomdoors = False, bossdisable = False)
    make_level(load_texture('Levels/trisection4'), cright_edge + width, cbottom_edge, 2, 0, randomdoors = False)
    make_level(load_texture('Levels/trisection1'), cright_edge + width, ctop_edge, 2, 1, bossguarentee = True)
    # Generate extra codeblock items for tutorial
    ItemCodeBlocks.append(GenerateCodeBlock(0, 62, 1.5))
    ItemCodeBlocks.append(GenerateCodeBlock(16, 64, 1.5))
    ItemCodeBlocks.append(GenerateCodeBlock(1, 66, 1.5))
    ItemCodeBlocks.append(GenerateCodeBlock(17, 70, 1.5))
    # Tell platforms code the tutorial levels already exist and don't need to be created again
    CheckChunk(0, 0)
    CheckChunk(1, 0)
    CheckChunk(2, 0)
    CheckChunk(2, 1)
    # Starting Codeblocks
    StartIf = CreateCodeBlock(0)
    StartIf.position += (-0.7, 0.3)     # Moves CodeBlocks to create a default Snippet, gives player an example/template of what Snippets should look like
    StartKeyE = CreateCodeBlock(15)
    StartKeyE.position += (-0.5, 0.3)
    StartColon = CreateCodeBlock(1)
    StartColon.position += (-0.3, 0.3)
    StartKey = CreateCodeBlock(19)
    StartKey.position += (-0.1, 0.3)
    StartMake = CreateCodeBlock(17)
    StartMake.position += (0.1, 0.3)
    StartBlock = CreateCodeBlock(13)
    StartBlock.position += (-0.1, 0.1)
    # Disable TitleScreen
    TitleSplash.enabled = False
    StartButton.enabled = False
    # Create TutorialGuy
    TutorialEntity.enabled = True
    # Create Tutorial Messages
    MoveTutorial.enabled = True
    JumpTutorial.enabled = True
    FireBlock = CreateCodeBlock(18)
    ShootBlock = CreateCodeBlock(20)


import sys, os
def reset():
    os.execv(sys.executable, ['python'] + sys.argv)

TitleSplash = Text(text = 'Dugnon', origin = (0,0), scale = 3, position = (0, 0.3))
StartButton = Button(text = 'Start', scale = (0.2, 0.1), position = (0, -0.1), color = color.red)
StartButton.on_click = start
ReturnButton = Button(text='Return to Title', scale = (0.2, 0.1), position = (0, -0.1), color = color.azure)
DeathSplash = Text(text = 'You Dieded', origin = (0, 0), scale = 3, position = (0,0.3), color = color.red)
DeathSplash.enabled = False
ReturnButton.enabled = False
ReturnButton.on_click = reset
JumpTutorial = Entity(model = 'quad', texture = load_texture('Sprites/JumpTutorial.png'), position = (9, 8), scale = (4, 3.5), enabled = False)
MoveTutorial = Entity(model = 'quad', texture = load_texture('Sprites/MoveTutorial.png'), position = (7, 11), scale = (4, 3.5), enabled = False)
# Locks (note this code is a mess there are so many seemingly unecessary things but removing them breaks things)
BottomLockCollider = Entity(model = 'quad', collider = 'box', position = (cright_edge, cbottom_edge), scale = (55, 1.7, 4), color = color.black, enabled = False)
RightLockCollider = Entity(model = 'quad', collider = 'box', position = (cright_edge, camera.scale_y / 2), scale = (1.7, 30, 4), color = color.black, enabled = False)
LeftLockCollider = Entity(model = 'quad', collider = 'box', position = (cleft_edge, camera.scale_y / 2), scale = (1.7, 30, 4), color = color.black, enabled = False)
TopLockCollider = Entity(model = 'quad', collider = 'box', position = (cright_edge, ctop_edge), scale = (55, 1.7, 4), color = color.black, enabled = False)
BottomLock = Entity(model = 'quad', texture = 'white_cube', color = color.black, position = (cright_edge, cbottom_edge), scale = (55, 1.7, 4), z = -0.01, parent = BottomLockCollider, enabled = False)
RightLock = Entity(model = 'quad', texture = 'white_cube',  color = color.black, position = (cright_edge, camera.scale_y / 2), scale = (1.7, 30, 4), z = -0.01, parent = RightLockCollider, enabled = False)
LeftLock = Entity(model = 'quad', texture = 'white_cube',  color = color.black, position = (cleft_edge, camera.scale_y / 2), scale = (1.7, 30, 4), z = -0.01, parent = LeftLockCollider, enabled = False)
TopLock = Entity(model = 'quad', texture = 'white_cube',  color = color.black, position = (cright_edge, ctop_edge), scale = (55, 1.7, 4), z = -0.01, parent = TopLockCollider, enabled = False)

app.run()      # Starts the game