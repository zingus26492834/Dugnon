from ursina import *
app = Ursina()      # Initialising Ursina before the following files is necessary
from CodeBlocks import *
from Platforms import *
from Player import *
from CodeFunctions import *
from ursina.prefabs.conversation import *

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
executing = False

def input(key):
    global CodeBlocksEnabled, blockoffset, blocksdragging, executing
    # key is a variable handled by Ursina which is set to whichever key is being pressed

    # Toggle Executing code
    if key == 'q':
        executing = not executing       # sets executing boolean to whatever executing isnt
    # Toggle CodeBlocks UI
    if key == 'k':
        CodeBlocksEnabled = not CodeBlocksEnabled       # sets CodeBlocksEnabled boolean to whatever CodeBlocksEnable isnt
        ToggleCodeBlocks(CodeBlocksEnabled)     # Feets boolean into ToggleCodeBlocks function
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
    
    # Debug keys
    if key == 'o':
        player.position = (camera.x, camera.y)
    if key == 'h':
        print(player.position)

    # Toggle Fullscreen    
    if key == 'y':
        window.fullscreen = not window.fullscreen

    # This needs to be here to read keyboard inputs, however does not normally run every frame (check update func)
    if executing:
        execute(key)

    # Tutorial
    global Tutorial2, Tutorial1, Tutorial3
    if key =='k' and Tutorial2:     # If CodeBlocks UI is opened during a certain part of the tutorial
        TutorialGuyConvo2.enabled = True        # Reenable conversation UI
        TutorialGuyConvo2.start_conversation(TutorialGuy2)      # Begin tutorial conversation
        Tutorial2 = False       # Ends second part of the tutorial
        Tutorial3 = True        # Begins third part of the tutorial
        TutorialGuy.position = (20, 8.5, 0)     # Moves TutorialGuy to the second position

################################################################################

# Update loop handled by Ursina automatically
chunkx = 0
chunky = 0
incrementchunk = False
# Update Function, runs every tick
def update():
    global CameraEdges, chunkx, chunky, incrementchunk, executing

    for i in ItemCodeBlocks:        # Checks every CodeBlock pickup
        if player.intersects(i).hit and i.Active:       # If player and pickup intersect
            CreateCodeBlock(i.CBid)     # Creates a CodeBlock in the image of the pickup
            i.Active = False        # Disables pickup code
            i.enabled = False       # Disables pickup
    if blocksdragging:      # If player is panning the blocks
        mouselocalpos = cbpep.get_relative_point(camera.ui, mouse.position)     # Finds accurate position of mouse(can be wildly inaccurate otherwise)
        cbpe.position = (mouselocalpos - blockoffset)       # Moves codeblock parent entity with mouse (pans blocks ui)

    #for e in scene.entities:
    #    if hasattr(e, 'collider') and e.collider:
   #         e.collider.visible = True

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

    # Locked Doors
    global Tutorial4
    for L in LockedDoors:       # Checks every Locked Door
        for K in ExistingKeys:      # Checks every Key
            # If door and key intersect, remove both
            if L.intersects(K):
                L.enabled = False
                K.enabled = False
                # When the first Locked Door is opened and the tutorial has progressed enough, play end of tutorial conversation and end tutorial
                if Tutorial4:
                    TutorialGuyConvo4.enabled = True
                    TutorialGuyConvo4.start_conversation(TutorialGuy4)
                    Tutorial4 = False
                    TutorialGuy.enabled = False
    
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
    
    # Tutorial
    global Tutorial1, Tutorial2, Tutorial3
    # First TutorialGuy position
    if player.intersects(TutorialGuy) and Tutorial1:        # If the player hasn't begun the tutorial and touches TutorialGuy
        TutorialGuyConvo1.enabled = True        # Reenables conversation UI now that its needed
        TutorialGuyConvo1.start_conversation(TutorialGuy1)      # Begins conversation with dialogue defined in variable
        Tutorial1 = False       # Marks the first of 4 parts of the tutorial complete
        Tutorial2 = True        # and moves on to the second part
    # Second TutorialGuy position
    if player.intersects(TutorialGuy) and Tutorial3:        # If the player progressed to the point where TutorialGuy moves and touches TutorialGuy
        TutorialGuyConvo3.enabled = True
        TutorialGuyConvo3.start_conversation(TutorialGuy3)
        Tutorial3 = False
        Tutorial4 = True
    
    # Solves problem of execute not running every frame by called input function every frame regardless of input
    if executing:
        input(None)
    
################################################################################

# Tutorial

# Tutorial Codeblocks
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

# Tutorial Variables and Objects
Tutorial1 = True
Tutorial2 = False
Tutorial3 = False
Tutorial4 = False
TutorialGuyConvo1 = Conversation(variables_object = Empty())        # Creates an object handled by an Ursina prefab to handle conversations
TutorialGuyConvo1.enabled = False       # Conversation template appears on game start otherwise
TutorialGuyConvo2 = Conversation(variables_object = Empty())        # Theoretically I should only need 1 conversation object for all conversations, but in practice that's not how it works
TutorialGuyConvo2.enabled = False
TutorialGuyConvo3 = Conversation(variables_object = Empty())
TutorialGuyConvo3.enabled = False
TutorialGuyConvo4 = Conversation(variables_object = Empty())
TutorialGuyConvo4.enabled = False
TutorialGuy = Entity(position = (16, 2.5, 0),
                     model = 'quad',
                     collider = 'box',
                     scale = (1, 1, 1),
                     playercollision = False,
                     texture = load_texture('Sprites/TutorialGuy'))

# Tutorial Conversations
TutorialGuy1 = dedent('''
                         Hi, I'm TutorialGuy.
                         Press K to view your "CodeBlocks", we will continue our conversation there.
                         ''')
TutorialGuy2 = dedent('''
                         This the menu for your "CodeBlocks".
                         You can move the screen with scroll and right click.
                         Right now you have a "Snippet" that creates a key when you press E.
                         Try replacing the "key" block with the "block" block.
                         Remember, the CodeBlocks will snap into a snippet in order of the last dropped block.
                         This means you have to move the "make" block as well,
                         otherwise the "block" block will snap to the other side of the "make" block.
                         Once your done, press Q to start running your CodeBlocks.
                         I will meet you again at the top of this wall.
                         ''')
TutorialGuy3 = dedent('''
                         Now that you've made it up the wall we have a new problem.
                         There is a locked door blocking our path.
                         Try switching the key and the block one more time and open the door.
                         You may want to press Q again to stop the code from running while you are editing it.
                        ''')
TutorialGuy4 = dedent('''
                         Great job!
                         I will leave you now.
                         Good luck.
                      ''')

# Start game
make_level(load_texture('Levels/platformer_tutorial_level'), 2, 0, 0, 0)        # Creates the tutorial level / starting room
player.y += 2       # Makes sure the player doesn't get stuck in the ground
CameraEdges = GetCameraEdges()      # Finds edges of the starting
app.run()      # Starts the game