# Imports
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
camera.position = (15,8)
camera.fov = 16
height = camera.fov
ratio = window.aspect_ratio
width = height * ratio

# Audio
bgm = Audio('Audio/Main.mp3', loop = True, autoplay = True, volume = 0)
bosstheme = Audio('Audio/Boss.mp3', loop = True, autoplay = True, volume = 0)
JospepAudio = Audio('Audio/Jospep.mp3', loop = True, autoplay = True, volume = 0)
HiredOneAudio = Audio('Audio/HiredOne.mp3', loop = True, autoplay = True, volume = 0)

# Function to find Edges of the Camera
def GetCameraEdges():
    cright_edge = camera.x + (width / 2)        # Camera.x is the center of the screen, width / 2 is half the screen, so camera.x + width / 2 is the center of the screen + half the screen resulting in the right side of the screen, similar logic applies for others
    ctop_edge = camera.y + (height / 2)
    cleft_edge = camera.x - (width / 2)
    cbottom_edge = camera.y - (height / 2)
    return cright_edge, ctop_edge, cleft_edge, cbottom_edge

# Scores
with open ('scores.txt', 'r') as scores:        # Read scores txt file
    scoreslist = []     # Empty scores list
    for line in scores:     # For every line in the txt file
        scoreslist.append(line)     # Add the line to scoreslist
    HighScoreDamage = int(scoreslist[0])        # HighScore damage is the 1st line
    HighScoreRooms = int(scoreslist[1])     # HighScore rooms is the 2nd line
HighestRunDamage = 0        # Highest damage this run
HighestRunRooms = 0     # Highest rooms this run

# Variables for input
CodeBlocksEnabled = False
blocksdragging = False
blockoffset = Vec3(0, 0, 0)
titlescreen = True
executing = False
warpcooldown = 0
warping = False
# Function to check inputs, built in to run every time a key is pressed by Ursina
def input(key):
    global titlescreen
    global CodeBlocksEnabled, blockoffset, blocksdragging, executing
    # key is a variable handled by Ursina which is set to whichever key is being pressed

    if TutorialGuy.IsSpeaking:      # Don't progress if NosedOne is speaking
        return

    # Toggle Executing code
    if key == 'q':
        executing = not executing       # sets executing boolean to whatever executing isnt
    # Toggle CodeBlocks UI
    if key == 'k':
        CodeBlocksEnabled = not CodeBlocksEnabled       # sets CodeBlocksEnabled boolean to whatever CodeBlocksEnable isnt
        ToggleCodeBlocks(CodeBlocksEnabled)     # Feeds boolean into ToggleCodeBlocks function
    # Controlling CodeBlocks UI
    if key == 'scroll up' and CodeBlocksEnabled:        # If scrolling up and codeblocks ui is open
        scrollblock('up')       # Zoom in codeblocks ui
    if key == 'scroll down' and CodeBlocksEnabled:      # If scrolling down and codeblocks ui is open
        scrollblock('down')     # Zoom out codeblocks ui
    if key == 'right mouse down' and CodeBlocksEnabled:     # If right mouse held down
        blocksdragging = True       # Blocks are being dragged
        mouselocalpos = cbpep.get_relative_point(camera.ui, mouse.position)     # Convert mouse position to relative point in ui space
        blockoffset = (mouselocalpos - cbpe.position)       # Move codeblocks ui with mouse
    if key == 'right mouse up':       # If rightmouse isnt being held
        blocksdragging = False      # Stop dragging blocks
    
    # Open CodeBlocks Guide
    if key == 'p':
        if CodeBlocksEnabled:       # If codeblocks ui is open
            CodeBlocksGuide.visible = not CodeBlocksGuide.visible       # CodeBlocks Guide is toggled

    # This needs to be here to read keyboard inputs, however does not normally run every frame (check update func)
    if executing:
        execute(key)

    # Interactions
    for B in BossSpawners:
        if player.intersects(B) and not B.spawned and key == 'z':       # If player is touching boss spawner and presses z
            B.enabled = False       # Disable spawner
            B.despawnable = False       # Make spawner not despawnable
            B.spawned = True        # Boss is spawned
            choice = random.randint(1, 3)       # Choose random 1-3 number
            if choice == 1:     # If choice rolled 1, spawn default boss
                BossEnemy(position = (B.x, B.y + 2), spawntime = time.time())
            elif choice == 2:       # If choice rolled 2, spawn stationary boss
                StationaryBossEnemy(position = (B.x, B.y + 2), spawntime = time.time())
            elif choice == 3:       # If choice rolled 3, spawn floating boss
                FloatingBoss(position = (B.x, B.y + 2), spawntime = time.time())

    if player.intersects(TutorialEntity) and TutorialEntity.enabled and key == 'z':     # If player is touching NosedOne and presses z
        TutorialGuy.visible = True

    global warpcooldown, warping, cright_edge, ctop_edge, cleft_edge, cbottom_edge, CameraEdges
    for portal in EntryPortals:
        if player.intersects(portal) and warpcooldown < time.time() and key == 'z':     # If player is touching portal and presses z
            warping = True
            if not portal.Generated:        # If level hasn't already been generated
                CheckChunk(portal.chunkx, portal.chunky)        # Chunk has been loaded
                RandomLevel('down', portal.GenerateCoordX, portal.GenerateCoordY, portal.chunkx, portal.chunky, portals = False)        # Create Random level on other side of portal
                portal.Generated = True
            player.position = portal.destination        # Move player to other side of portal
            camera.position = (portal.destination.x, portal.destination.y - 2)      # Move camera to other side of portal
            if hasattr(player, 'y_animator'):       # Kill y animator if player is jumping
                 player.y_animator.kill()
            CameraEdges = GetCameraEdges()      # Reset camera edges
            cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges
            chunkx = portal.chunkx      # Set chunkx to portal's chunkx
            chunky = portal.chunky      # Set chunky to portal's chunky
            warpcooldown = time.time() + 5
    for portal in ExitPortals:
        if player.intersects(portal) and warpcooldown < time.time() and key == 'z':
            warping = True
            player.position = portal.destination
            camera.position = (portal.destination.x, portal.destination.y - 2)
            if hasattr(player, 'y_animator'):
                 player.y_animator.kill()
            CameraEdges = GetCameraEdges()
            CheckChunk(portal.chunkx, portal.chunky)
            cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges
            chunkx = portal.chunkx
            chunky = portal.chunky
            warpcooldown = time.time() + 5


################################################################################

# Update variables
chunkx = 0
chunky = 0
incrementchunk = False
keynotification = False
hired = False
alreadyhired = False
blackouttimer = 0
keycolour = 'regular'
CodeBlockPickup = Audio('Audio/CodeBlock.mp3', loop = False, autoplay = False, volume = 0.3)
keymessage = Text(text = f'You need a {keycolour} key to open this door', origin = (0, -3), scale = 2, visible = False, parent = camera.ui)
MouseCheck = Entity(model = 'quad', scale = (100, 100, 0.1), position = (0, 0), color = color.rgba(0, 0, 0, 0), z = 2, collider = 'box', playercollision = False)
# Update Function, runs every tick
def update():
    global titlescreen, warping, HighestRunDamage, HighestRunRooms
    if titlescreen:
        return      # Skip update loop if on titlescreen
    
    global CameraEdges, chunkx, chunky, incrementchunk, executing
    # Item Code Blocks
    for i in ItemCodeBlocks:        # Checks every CodeBlock pickup
        if player.intersects(i).hit and i.Active:       # If player and pickup intersect
            if hasattr(i, 'rare'):      # If Codeblock is Rare
                CreateRareCodeBlock(i.CBid)     # Create from Rare list
            else:
                CreateCodeBlock(i.CBid)     # Creates a CodeBlock in the image of the pickup
            i.Active = False        # Disables pickup code
            i.despawnable = False
            i.enabled = False       # Disables pickup
            CodeBlockPickup.play()      # Play codeblock item pickup sound
    if blocksdragging:      # If player is panning the blocks
        mouselocalpos = cbpep.get_relative_point(camera.ui, mouse.position)     # Finds accurate position of mouse(can be wildly inaccurate otherwise)
        cbpe.position = (mouselocalpos - blockoffset)       # Moves codeblock parent entity with mouse (pans blocks ui)

    # Creates variable for every camera edge
    cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges

    # Check every edge, create new levels, and screen transitions handling
    # Right edge
    if player.position.x >= cright_edge and not warping:        # If player moves beyond the right side of the screen
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
            HighestRunRooms += 1        # Increase HighestRunRooms
        # Until camera has reached the new position, slide it towards that point
        if camera.x < newcamerapos - (width / 2):
            camera.x += time.dt * 40
        else:
            camera.x = newcamerapos - (width / 2)       # Snap camera to the new position, in case it moved too far
            player.position.x = cright_edge + 2     # Places the player on the new screen
            CameraEdges = GetCameraEdges()      # Checks new Camera Edges
            player.gravity = 1      # Reenables gravity for the player
            incrementchunk = False      # Sets up for next chunk to be loaded

    # Top edge
    if player.position.y >= ctop_edge and not warping:       # If player moves above the top of the screen
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
            HighestRunRooms += 1        # Increase HighestRunRooms
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
    if player.position.x <= cleft_edge and not warping:     # If player moves beyond the left side of the screen
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
            HighestRunRooms += 1        # Increase HighestRunRooms
        # Until camera has reached the new position, slide it towards that point
        if camera.x > newcamerapos + (width / 2):
            camera.x -= time.dt * 40
        else:
            camera.x = newcamerapos + (width / 2)       # Snap camera to the new position, in case it moved too far
            player.position.x = cleft_edge - 2      # Places the player on the new screen
            CameraEdges = GetCameraEdges()      # Checks new Camera Edges
            player.gravity = 1      # Reenables gravity for the player
            incrementchunk = False      # Sets up for next chunk to be loaded
    # Bottom edge
    if player.position.y <= cbottom_edge and not warping:       # If player moves below the bottom of the screen
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
            HighestRunRooms += 1        # Increase HighestRunRooms
        # Until camera has reached the new position, slide it towards that point
        if camera.y > newcamerapos + (height / 2):
            camera.y -= time.dt * 40
        else:
            camera.y = newcamerapos + (height / 2)      # Snap camera to the new position, in case it moved too far
            player.position.y = cbottom_edge - 8        # Places the player on the new screen
            CameraEdges = GetCameraEdges()      # Checks new Camera Edges
            player.gravity = 1      # Reenables gravity for the player
            incrementchunk = False      # Sets up for next chunk to be loaded

    # Unstuck player if spam a w d, more context in player.py
    if player.spaceescape >= 5 and player.aescape >= 5 and player.descape >= 5 and player.position == player.stuckpos:
            player.x += 1
            player.y += 1

    # Locked Doors
    global keycolour, starttime, keynotification
    for L in LockedDoors:       # Checks every Locked Door
        for K in ExistingKeys:      # Checks every Key
            # If door and key intersect, remove both
            if L.intersects(K):
                if K.colour == L.colour:        # Makes sure key and door colours match first
                    L.despawnable = False
                    L.enabled = False
                    K.enabled = False
        if L.intersects(player) and L.enabled:      # If player and door touch
            keynotification = True      # Notify player that they need a certain coloured key to open it
            starttime = time.time()
            keycolour = L.colour

    # If keynotification is true, show key notification
    if keynotification:
        keymessage.visible = True
        if keycolour != 'regular':      # If door colour is 'regular', make text colour yellow, otherwise make the colour the door colour
            keymessage.color = getattr(color, keycolour)
        else:
            keymessage.color = color.yellow
        keymessage.text = f'You need a {keycolour} key to open this door'       # Update text to display what colour key is needed
        if time.time() - starttime > 1:     # Message goes away after 1 second
            keymessage.visible = False
            keynotification = False
    
    # CodeFunctions
    currenttime = time.time()       # Necessary to create a variable with this value rather than just calling time.time()
    for b in ExistingBlocks:        # Checks every block from CodeFunctions.py
        ray_origin = b.world_position - Vec3(0, b.scale_y / 2, 0)       # Creates a more accurate start point for raycasts
        if hasattr(b, 'shooting'):      # Checks if the block was made with shooting modification
            b.x += time.dt * b.speed * b.velocity        # Moves block horizontally every frame
            # Raycasts to check collision
            topray = raycast(ray_origin + Vec3(b.scale_x*.49 * b.velocity,b.scale_y,0), b.right, distance=max(.15,  0.15), ignore=b.ignore_list, traverse_target=scene)
            middleray = raycast(ray_origin + Vec3(b.scale_x*.49 * b.velocity, b.scale_y / 2, 0), b.right, distance=max(.15, 0.15), ignore=b.ignore_list, traverse_target=scene)
            bottomray = raycast(ray_origin + Vec3(b.scale_x*.49 * b.velocity,.1,0), b.right, distance=max(.15,  0.15), ignore=b.ignore_list, traverse_target=scene)
            if any((topray.hit, middleray, bottomray.hit)):     # If any of the raycasts collide with an Entity that isn't the player or itself
                delattr(b, 'shooting')      # Ends the loop, therefore stopping movement
            # Also end the loop and stop movement after half a second if no collision
            elif currenttime - b.spawntime > 0.5:
                delattr(b, 'shooting')
        elif hasattr(b, 'aiming') and b.aiming:     # If modification is aiming
            b.animate_y(b.destination.y, 0.2, resolution = 30, curve = curve.out_expo)      # Animate towards specified location
            b.animate_x(b.destination.x, 0.2, resolution = 30, curve = curve.out_expo)      
        if currenttime - b.spawntime > 5:       # Despawn after 5 seconds
            b.enabled = False
            b.collider = None
            ExistingBlocks.remove(b)        # Remove from list to make sure it doesn't check this again
    for f in ExistingFire:      # Checks every fire entity from CodeFunctions.py
        # Delete the fire after 2 seconds
        if currenttime - f.spawntime > 2:
            f.enabled = False
            f.collider = None
            ExistingFire.remove(f)      # Makes sure loop isn't checking nonexistant fire entities
        # If shooting modification, move the fire horizontally
        if hasattr(f, 'shooting'):
            f.x += time.dt * f.speed * f.velocity
        elif hasattr(f, 'aiming'):      # If aiming modification, move at an angle
            f.x += cos(f.angle) * time.dt * f.speed
            f.y += sin(f.angle) * time.dt * f.speed
    # Checks every key from CodeFunctions.py
    for k in ExistingKeys:
        # Delete the key after 2 seconds
        if currenttime - k.spawntime > 2:
            k.enabled = False
            k.collider = None
            ExistingKeys.remove(k)      # Makes sure loop isn't checking nonexistant key entities
        # If shooting modification, move key horizontally
        if hasattr(k, 'shooting'):
            k.x += time.dt * k.speed * k.velocity
        # If aiming modification, move key at an angle
        elif hasattr(k, 'aiming'):
            k.x += cos(k.angle) * time.dt * k.speed
            k.y += sin(k.angle) * time.dt * k.speed
    JospepAudio.volume = 0      # Resets Jospep audio
    for j in ExistingJospeps:
        JospepAudio.volume += 0.5       # Increase volume by 0.5 for every Jospep currently existing
        if currenttime - j.spawntime > 1.5:     # Despawn after 1.5 seconds
            j.enabled = False
            j.collider = None
            ExistingJospeps.remove(j)
        if hasattr(j, 'aiming'):        # If aiming modification, move at an angle
            j.x += cos(j.angle) * time.dt * j.speed
            j.y += sin(j.angle) * time.dt * j.speed
        else:       # If no aiming modification, move horizontally
            j.x += time.dt * j.speed * j.velocity
    HiredOneAudio.volume = 0        # Resets HiredOne audio
    for h in HiredOnes:
        NearestOne = distance(h, player)        # Checks distance to HiredOne
        NearestVolume = max(1 - NearestOne / 20, 0.2)       # Checks if HiredOne is the nearest to the player
        if NearestVolume > HiredOneAudio.volume:        # Set volume based on distance to the nearest HiredOne, or 0.2 minimum
            HiredOneAudio.volume = NearestVolume

        if currenttime - h.spawntime > 1.5:     # Despawn after 1.5 seconds
            h.enabled = False
            h.collider = None
            HiredOnes.remove(h)
        if hasattr(h, 'aiming'):        # If aiming modification, move at an angle
            h.x += cos(h.angle) * time.dt * h.speed
            h.y += sin(h.angle) * time.dt * h.speed
        else:       # If no aiming modification, move horizontally
            h.x += time.dt * h.speed * h.velocity
    for l in ExistingLasers:
        # Delete the laser after 1 second
        if currenttime - l.spawntime > 1:
            l.enabled = False
            l.collider = None
            ExistingLasers.remove(l)      # Makes sure loop isn't checking nonexistant key entities

    global hired
    for e in [e for e in scene.entities if hasattr(e, 'Enemy') and e.enabled]:      # For every entity if entity is an enemy and is enabled
        for a in [a for a in ExecutedEntities if hasattr(a, 'damage')]:     # For every executed entity if entity has damage
            if a.intersects(e) and time.time() - e.hurtcooldown > 0:        # If enemy intersects executed entity and enemy hurtcooldown has passed
                e.health -= a.damage        # subtract executed entity damage from enemy health
                e.hurtcooldown = time.time() + 0.5      # add 0.5 seconds to enemy hurt cooldown
                a.spawntime -= 100      # executed entity spawntime - 100 (basically a force despawn but cleaner)
                if a.damage > HighestRunDamage:     # If executed entity's damage is the highest so far in the run
                    HighestRunDamage = a.damage     # Damage is the new run's highest
                if a.damage > 100000:       # If executed entity's damage is above 100k
                    hired = True        # Hired

    # Solves problem of execute not running every frame by called input function every frame regrdless of input
    if executing:
        input(None)

    global HighScoreDamage, HighScoreRooms
    # If player is dead, display high scores, death splash, restart button
    if player.dead:
        DeathSplash.enabled = True
        ReturnButton.enabled = True
        HighestDamageDisplay.enabled = True
        HighScoreDamageDisplay.enabled = True
        HighestRoomsDisplay.enabled = True
        HighScoreRoomsDisplay.enabled = True
        if HighestRunDamage > HighScoreDamage:      # If highest run damage is higher than the high score
            NewHighDamage.enabled = True        # Player got the high score
            HighScoreDamage = HighestRunDamage      # Update high score
        if HighestRunRooms > HighScoreRooms:        # If highest run rooms is higher than the high score
            NewHighRooms.enabled = True     # Player got the high score
            HighScoreRooms = HighestRunRooms        # Update high score
        with open ('scores.txt', 'w') as scores:        # Open scores.txt in write mode
            scores.write(f'{HighScoreDamage}\n{HighScoreRooms}')        # update high scores
        # Update Score displays
        HighestDamageDisplay.text = f'Highest Damage: {HighestRunDamage}'
        HighScoreDamageDisplay.text = f'Damage High Score: {HighScoreDamage}'
        HighestRoomsDisplay.text = f'Rooms Travelled: {HighestRunRooms}'
        HighScoreRoomsDisplay.text = f'Rooms High Score: {HighScoreRooms}'
    
    for e in scene.entities:        # For every entity in the scene
        if hasattr(e, 'despawnable') and e.despawnable:     # If despawnable
            if distance(player, e) > 100:       # If far enough away from the player
                e.enabled = False       # Disable entity
            else:
                e.enabled = True        # Otherwise enable entity if close enough again

    # Tutorial
    if TutorialGuy.IsSpeaking:      # If NosedOne is speaking
        player.velocity = 0     # Stop player horizontal movement
        if TutorialGuy.SecretTutorial:      # If player found secret tutorial
            bgm.volume = 0      # Cut music while NosedOne is speaking
    if TutorialGuy.SecretObtained:      # If player obtained the secret, add secret codeblock
        CurrentCodeBlocks.append(CodeBlock(texture = 'CodeBlocks/Jospep.png', code = "ExecutedEntities.append(Jospep(", visible = False))
        TutorialGuy.SecretObtained = False      # Don't give more than one secret codeblock
    
    from Enemy import LockRoom      # Global LockRoom only counts for this file, so reimporting Lockroom here is necessary
    # If room is locked, create borders on the room that prevent player from leaving, else remove them
    if LockRoom:
        BottomLockCollider.enabled = True
        RightLockCollider.enabled = True
        LeftLockCollider.enabled = True
        TopLockCollider.enabled = True
        BottomLockCollider.position = (cright_edge, cbottom_edge)
        RightLockCollider.position = (cright_edge, cbottom_edge + 1)
        LeftLockCollider.position = (cleft_edge, cbottom_edge + 1)
        TopLockCollider.position = (cright_edge, ctop_edge)
        if bgm.volume > 0:      # If bgm is playing, lower volume until 0
            bgm.volume -= 0.02
        if bosstheme.volume < 0.4:      # If boss theme is not playing, rise volume until 0.4
            bosstheme.volume += 0.02
    else:
        BottomLockCollider.enabled = False
        RightLockCollider.enabled = False
        LeftLockCollider.enabled = False
        TopLockCollider.enabled = False
        if bgm.volume < 0.3:        # If bgm is not playing, rise volume until 0.3
            bgm.volume += 0.01
        if bosstheme.volume > 0:        # If boss theme is playing, lower volume until 0
            bosstheme.volume -= 0.02

    # Mousecheck stay on screen, mousecheck is an invisible entity behind everything that makes sure the mouse always has something behind it, mouse.world_point is technically a hit, therefore needs to be touching a collider
    MouseCheck.x = player.x
    MouseCheck.y = player.y
    
    # Vignette centers on player
    Vignette.x = player.x
    Vignette.y = player.y
    global scary
    # If scary is disabled, remove vignette
    if not scary:
        Vignette.enabled = False
    else:
        Vignette.enabled = True
    
    # Disable player movement while warping
    if warping:
        player.velocity = 0
        player.gravity = 0
        # Add cooldown before warping again
        if warpcooldown - 4 < time.time():
            warping = False
            player.gravity = 1


    global blackouttimer, alreadyhired
    # Hired
    if hired:
        if not alreadyhired:        # Makes sure it only happens once
            if blackouttimer == 0:      # Set blackouttimer
                blackouttimer = time.time()
            if not time.time() - blackouttimer > 5:     # until 5 seconds have passed
                blackout.enabled = True     # blackout screen
                blackout.position = player.position     # Move blackout to player
                HiredOneAudio.volume = 2        # Play HiredOne audio
                bgm.volume = 0      # Cut bgm
                bosstheme.volume = 0        # Cut bosstheme
                DMan.enabled = True     # Enable DMan, I've never played half life but someone told me to add GMan so this is probably close enough
                DMan.position = (camera.scale_x / 2 + camera.x, camera.scale_y / 2 + camera.y - 3)      # Move DMan to center of the screen
                DmanMessage.enabled = True      # Enable DMan message
                player.velocity = 0     # Stop player movement
                player.gravity = 0      # Stop player gravity
                player.health = 100     # Make player unkillable temporarily, also heals player to full but thats fine
                player.flingvel = 0     # Stops player from being flung
            elif not time.time() - blackouttimer > 5.2:     # Disable blackout and message slightly before disabling everything else
                blackout.enabled = False
                DmanMessage.enabled = False
            else:
                DMan.enabled = False
                alreadyhired = True     # Has already been hired
                HiredOneAudio.volume = 0        # Turn off HiredOne volume
                player.gravity = 1
                CurrentCodeBlocks.append(CodeBlock(texture = 'CodeBlocks/HiredOne.png', code = "ExecutedEntities.append(HiredOne(", visible = False))       # Add HiredOne Block


################################################################################

CameraEdges = GetCameraEdges()      # Finds edges of the starting screen
cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges

# Load Tutorial and initial variables
def start():
    global CameraEdges, titlescreen
    titlescreen = False
    TitleBackground.visible = False
    ScaryButton.enabled = False
    Vignette.visible = True
    player.enabled = True
    player.health = 100
    player.dead = False
    # Start game / Load tutorial levels, load tutorial codeblock items
    make_level(load_texture('Levels/platformer_tutorial_level'), 2, 0, 0, 0, randomdoors = False)        # Creates the tutorial level / starting room
    player.y += 2       # Makes sure the player doesn't get stuck in the ground
    CameraEdges = GetCameraEdges()      # Finds edges of the starting screen
    cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges
    # Make first 3 levels after start room non random
    make_level(load_texture('Levels/intersection'), cright_edge, cbottom_edge, 1, 0, randomdoors = False, bossdisable = True)
    make_level(load_texture('Levels/trisection4'), cright_edge + width, cbottom_edge, 2, 0, randomdoors = False, bossdisable = True, disableenemy= True)
    make_level(load_texture('Levels/trisection1'), cright_edge + width, ctop_edge, 2, 1, bossguarentee = True)
    # Generate extra codeblock items for tutorial
    ItemCodeBlocks.append(GenerateCodeBlock(0, 62, 1.5))
    ItemCodeBlocks.append(GenerateRareCodeBlock(3, 64, 1.5))
    ItemCodeBlocks.append(GenerateCodeBlock(1, 66, 1.5))
    ItemCodeBlocks.append(GenerateCodeBlock(13, 70, 1.5))
    # Tell platforms code the tutorial levels already exist and don't need to be created again
    CheckChunk(0, 0)
    CheckChunk(1, 0)
    CheckChunk(2, 0)
    CheckChunk(2, 1)
    # Starting Codeblocks
    StartIf = CreateCodeBlock(0)
    StartIf.position += (-0.7, 0.3)     # Moves CodeBlocks to create a default Snippet, gives player an example/template of what Snippets should look like
    StartKeyE = CreateRareCodeBlock(2)
    StartKeyE.position += (-0.5, 0.3)
    StartColon = CreateCodeBlock(1)
    StartColon.position += (-0.3, 0.3)
    StartKey = CreateCodeBlock(14)
    StartKey.position += (-0.1, 0.3)
    StartMake = CreateCodeBlock(13)
    StartMake.position += (0.1, 0.3)
    StartBlock = CreateCodeBlock(11)
    StartBlock.position += (-0.1, 0.1)
    # Disable TitleScreen
    TitleSplash.enabled = False
    StartButton.enabled = False
    # Create TutorialGuy
    TutorialEntity.enabled = True
    # Create Tutorial Messages
    MoveTutorial.enabled = True
    JumpTutorial.enabled = True
    InteractTutorial.enabled = True
    # BGM
    global bgm, bosstheme
    if not scary:       # Change bgm if not scary
        bgm = Audio('nonscaryMain.mp3', loop = True, autoplay = True)
        bosstheme = Audio('nonscaryBoss.mp3', loop = True, autoplay = True, volume = 0)
    bgm.volume = 0.3
    TitleTheme.volume = 0       # Disable title music

import sys, os
def reset():
    os.execv(sys.executable, ['python'] + sys.argv)

# Scary toggle buttons
ScaryButton = Button(text = 'Toggle Scary', scale = (0.2, 0.1), position = (0, -0.3), color = color.green)
ScaryButton.text_entity.color = color.black
# Check Scary setting
with open ('settings.txt', 'r') as scarysetting:
    global scary
    scary = scarysetting.read() == 'True'       # scarysetting.read() is a string not a boolean, scarysetting.read() == 'True' is a statement checking if the string is literally 'True', resulting in a boolean
if scary:
    ScaryButton.color = color.green     # Change button colour to green if scarymode enabled
    ScaryButton.highlight_color = color.green       # Highlight colour is different to button colour, need to set both
else:
    ScaryButton.color = color.gray      # Change button colour to grey if scarymode dsabled
    ScaryButton.highlight_color = color.gray
# toggle ScarySetting
def ScaryToggle():
    global scary
    with open ('settings.txt', 'w') as scarysetting:
        scarysetting.write(f'{not scary}')
        scary = not scary
        if scary:
            ScaryButton.color = color.green
            ScaryButton.highlight_color = color.green
        else:
            ScaryButton.color = color.gray
            ScaryButton.highlight_color = color.gray
ScaryButton.on_click = ScaryToggle      # Set ScaryButton to run ScaryToggle when clickeds

# Title screen
TitleTheme = Audio('Audio/Title.mp3', loop = True, autoplay= True)
TitleSplash = Text(text = 'Dugnon', color = color.black, origin = (0,0), scale = 3, position = (0, 0.3))
TitleBackground = Entity(model = 'quad', position = (15, 8), scale = (28, 17), texture = load_texture('Sprites/titlescreen.png'))
StartButton = Button(text = 'Start', scale = (0.2, 0.1), position = (0, -0.1), color = color.blue)

StartButton.on_click = start
ReturnButton = Button(text='Return to Title', scale = (0.2, 0.1), position = (0, -0.1), color = color.azure)
DeathSplash = Text(text = 'You Dieded', origin = (0, 0), scale = 3, position = (0,0.3), color = color.red)

# Scores display
HighestDamageDisplay = Text(text = f'Highest Damage: {HighestRunDamage}', origin = (0, 0), scale = 2, position = (0, 0), color = color.white)
HighScoreDamageDisplay = Text(text = f'Damage High Score: {HighScoreDamage}', origin = (0, 0), scale = 2, position = (0, -0.1), color = color.white)
HighestRoomsDisplay = Text(text = f'Rooms Travelled: {HighestRunRooms}', origin = (0, 0), scale = 2, position = (0, -0.3), color = color.white)
HighScoreRoomsDisplay = Text(text = f'Rooms High Score: {HighScoreRooms}', origin = (0, 0), scale = 2, position = (0, -0.4), color = color.white)
NewHighDamage = Text(text = 'High Score!', origin = (0, 0), scale = 2, position = (-0.5, 0), color = color.yellow)
NewHighRooms = Text(text = 'High Score!', origin = (0, 0), scale = 2, position = (-0.5, -0.3), color = color.yellow)

HighestDamageDisplay.enabled = False
HighScoreDamageDisplay.enabled = False
HighestRoomsDisplay.enabled = False
HighScoreRoomsDisplay.enabled = False
NewHighDamage.enabled = False
NewHighRooms.enabled = False
DeathSplash.enabled = False
ReturnButton.enabled = False
ReturnButton.on_click = reset

# Tutorial Messages
JumpTutorial = Entity(model = 'quad', texture = load_texture('Sprites/JumpTutorial.png'), position = (14, 10), scale = (4, 3.5), enabled = False)
MoveTutorial = Entity(model = 'quad', texture = load_texture('Sprites/MoveTutorial.png'), position = (6, 6), scale = (4, 3.5), enabled = False)
InteractTutorial = Entity(model = 'quad', texture = load_texture('Sprites/InteractTutorial.png'), position = (14, 4), scale = (4, 3.5), enabled = False)

# Locks (note this code is a mess there are so many seemingly unecessary things but removing them breaks things)
BottomLockCollider = Entity(model = 'quad', collider = 'box', position = (cright_edge, cbottom_edge), scale = (55, 1.7, 4), color = color.black, enabled = False)
RightLockCollider = Entity(model = 'quad', collider = 'box', position = (cright_edge, camera.scale_y / 2), scale = (1.7, 30, 4), color = color.black, enabled = False)
LeftLockCollider = Entity(model = 'quad', collider = 'box', position = (cleft_edge, camera.scale_y / 2), scale = (1.7, 30, 4), color = color.black, enabled = False)
TopLockCollider = Entity(model = 'quad', collider = 'box', position = (cright_edge, ctop_edge), scale = (55, 1.7, 4), color = color.black, enabled = False)
BottomLock = Entity(model = 'quad', texture = 'white_cube', color = color.black, position = (cright_edge, cbottom_edge), scale = (55, 1.7, 4), z = -0.01, parent = BottomLockCollider, enabled = False)
RightLock = Entity(model = 'quad', texture = 'white_cube',  color = color.black, position = (cright_edge, camera.scale_y / 2), scale = (1.7, 30, 4), z = -0.01, parent = RightLockCollider, enabled = False)
LeftLock = Entity(model = 'quad', texture = 'white_cube',  color = color.black, position = (cleft_edge, camera.scale_y / 2), scale = (1.7, 30, 4), z = -0.01, parent = LeftLockCollider, enabled = False)
TopLock = Entity(model = 'quad', texture = 'white_cube',  color = color.black, position = (cright_edge, ctop_edge), scale = (55, 1.7, 4), z = -0.01, parent = TopLockCollider, enabled = False)

# Miscellaneous Entities
Vignette = Entity(model = 'quad', texture = 'Sprites/vignette.png', position = (0, 0, -1), scale = 50, visible = False)
blackout = Entity(model = 'quad', color = color.black, position = (0, 0, -1), scale = 100)
DMan = Entity(model = 'quad', texture = load_texture('Sprites/BoiledOne.png'), scale = 8)
DmanMessage = Text(text = 'YOU ARE HIRED!!\n\nOR I AM HIRED???', scale = 2, position = (0, 0.3), color = color.red)
DMan.enabled = False
DmanMessage.enabled = False
blackout.enabled = False

app.run()      # Starts the game