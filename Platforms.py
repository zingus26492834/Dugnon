# Imports
from ursina import *
from CodeBlocks import *
from Player import *
from Enemy import *
from CodeFunctions import *
     
# Variables
quad = load_model('quad', use_deepcopy=True)      # Quad is made by ursina by default but this is included in the sample and I'd rather not remove it just in case
level_parent = Entity(model=Mesh(vertices=[], uvs=[]), texture = load_texture('Sprites/block.png'))      # Model that spreads over level rather than individual entity on each pixel (I think??)
loaded_chunks = {}       # Empty Loaded Chunks list
LockedDoors = []         # Empty Locked Doors list

# Create level
def make_level(texture, offset_x, offset_y, chunkx, chunky, randomdoors = True, bossdisable = False, bossguarentee = False, disableenemy = False):
    for y in range(texture.height):          # Check every row of image
        collider = None       # Sets collider default None
        for x in range(texture.width):       # Check every column of image
            col = texture.get_pixel(x,y)          # Get each pixel in image
            
            world_x = x + offset_x      # Finds real location of pixel
            world_y = y + offset_y

            # Create ground at black pixel
            if col == color.black:      # If pixel is black
                level_parent.model.vertices += [Vec3(*e) + Vec3(world_x+.5,world_y+.5,0) for e in quad.generated_vertices]        # No idea I just trust the ursina sample, my guess is it adds vertices to the level parent rather than making a new entity at the pixel
                level_parent.model.uvs += quad.uvs
                if not collider:        # If no collider at pixel
                    collider = Entity(parent=level_parent,       # Add collider
                                      position=(world_x,world_y), 
                                      model='cube', 
                                      origin=(-.5,-.5), 
                                      collider='box',
                                      despawnable = True, 
                                      visible=False)
                else:
                    collider.scale_x += 1         # Increase collider scale
            else:
                collider = None         # If not black pixel, no collider

            # Spawn player at green pixel
            if col == color.green:      # If pixel is green
                player.start_position = (world_x, world_y)       # Set player start position to pixel
                player.position = player.start_position
            
            # Create Item CodeBlock at red pixels
            if col == color.red:        # If pixel is red
                if random.randint(1, 5) == 5:          # 1/5 chance for rare codeblock
                     ItemCodeBlocks.append(GenerateRareCodeBlock(RandomRareCodeBlock(), (world_x) + 0.5, (world_y + 0.5)))
                else:
                     ItemCodeBlocks.append(GenerateCodeBlock(RandomCodeBlock(), (world_x + 0.5), (world_y + 0.5)))
            
            # Create Locked door at blue pixxel
            if col == color.blue:       # If pixel is blue
                 if x > (texture.width / 2) + 5 or x < (texture.width / 2) - 5:      # If pixel is on the left or right side of the screen
                    CreateLockedDoorV(world_x, world_y, randomdoors)       # Create Vertical door
                 elif y > (texture.height / 2) + 5 or y < (texture.height / 2) - 5:       # If pixel is on top or bottom of the screen
                    CreateLockedDoorH(world_x, world_y, randomdoors)       # Create Horizontal door

            # Create enemies at yellow pixels
            if col == color.yellow:          # If pixel is yellow
                 if not disableenemy:        # If enemies aren't disabled
                    if bossguarentee:        # If boss is guarenteed
                         BossLevel(world_x, world_y)        # Create boss at enemy location
                    elif bossdisable:        # If boss is disabled
                         RandomEnemy((world_x, world_y + 0.5))        # Create a random enemy
                    elif random.randint(1, 20) == 1:        # 1/20 chance to create boss
                         BossLevel(world_x, world_y)
                    else:
                         RandomEnemy((world_x, world_y + 0.5))        # Create random enemy if nothing else
            entrances = GetEntrances(texture.name)          # Get entrances for level
            loaded_chunks[(chunkx, chunky)] = entrances          # Add entrances to chunk

    background = Entity(position = (offset_x + 14, offset_y + 8, 1),       # Level background
                        model = 'quad',
                        texture = load_texture('Sprites/background.png'),
                        scale = (28, 17))        
    level_parent.model.generate()       # Actually not sure what this does but removing it makes the level invisible, I think it somehow morphs the parent model to the level?

# Checks Chunks
def CheckChunk(x, y):
    global loaded_chunks
    chunkpos = (x, y)         # Checks chunk at location
    if chunkpos in loaded_chunks:       # If chunk position is loaded
        return True      # Chunk is active
    else:      # If chunk not active
        loaded_chunks[chunkpos] = set()      # Add chunk to loaded chunks
        print(chunkpos)       # Debug, leaving it here just in case
        return False          # Chunk is not active
    
UpLevels = []       # Empty list for Up levels
with open('Levels/UpLevels.txt') as f:       # Checks Uplevels file
            for line in f:         # For every line in the text file
                UpLevels.append(line.strip())          # Add that level to UpLevels
DownLevels = []     # Empty list for Down Levels
with open('Levels/DownLevels.txt') as f:     # Checks Downlevels file
            for line in f:         # For every line in the text file
                DownLevels.append(line.strip())        # Add that level to DownLevels
LeftLevels = []          # etc. etc.
with open('Levels/LeftLevels.txt') as f:
            for line in f:
                LeftLevels.append(line.strip())
RightLevels = []
with open('Levels/RightLevels.txt') as f:
            for line in f:
                RightLevels.append(line.strip())

# Generate Random Level, levels will very often make or not make entrances/exits where needs to have/not have one. It's complicated and not necessary to fix, just makes the UX more annoying, besides I have no idea why it's happening
def RandomLevel(direction, x, y, chunkx, chunky, portals = True, **kwargs):
    LeftChunk = (chunkx - 1, chunky)    # Chunk to the left
    RightChunk = (chunkx + 1, chunky)   # Chunk to the right
    UpChunk = (chunkx, chunky + 1)      # Chunk above
    DownChunk = (chunkx, chunky - 1)    # Chunk below
    extraargs = {**kwargs}

    required_direction = set()          # Set list for exits needed for level
    forbidden_directions = set()        # Set list for exits level can't have
    if 'down' in loaded_chunks.get((UpChunk), set()):       # If level above has down exit
         required_direction.add('up')        # Up exit required
    else:      # If down is not in the exits for the level above
         forbidden_directions.add('up')      # Up exit forbidden
    if 'up' in loaded_chunks.get((DownChunk), set()):       # If up exit in below level
         required_direction.add('down')      # Down exit required
    else:      # If up is not in the exits for the below level
         forbidden_directions.add('down')    # Down exit forbidden
    if 'left' in loaded_chunks.get((RightChunk), set()):         # etc. etc.
         required_direction.add('right')
    else:
         forbidden_directions.add('right')
    if 'right' in loaded_chunks.get((LeftChunk), set()):
         required_direction.add('left')
    else:
         forbidden_directions.add('left')

     # Check which direction player entered from and select from levels with an entrance in that direction
    if direction == 'up':          # If player entered from below
         AvailableLevels = UpLevels          # Select from levels with entrance on bottom
    if direction == 'down':        # If player entered from top
         AvailableLevels = DownLevels        # Select from levels with entrance on top
    if direction == 'left':        # etc. etc.
         AvailableLevels = LeftLevels
    if direction == 'right':
         AvailableLevels = RightLevels

    FilteredLevels = []       # List for filtered levels
    for Level in AvailableLevels:       # For every available level
         entrances = GetEntrances(Level)          # Find the entrances of the level
         if required_direction.issubset(entrances) and forbidden_directions.isdisjoint(entrances):       # If it has all the required directions and none of the forbidden directions
             FilteredLevels.append(Level)         # If add level to filtered levels
    
    if not FilteredLevels:         # If there are no Filtered Levels
         FilteredLevels = AvailableLevels         # Add all available levels (might be what's breaking it now that I think of it, this was intended for rooms with no adjacent rooms)

    RandomLevel = random.choice(FilteredLevels)        # Random level is chosen from the filtered levels
    texture = load_texture(RandomLevel)      # texture is the random level
    if not texture:      # If texture is gone print debug statement and don't continue (avoids crash and yells in terminal)
         print(f'Missing Texture: {RandomLevel} DEBUG STATEMENT DEBUG STATMENT READ THIS DEBUG STATMENT')
         return
    
    if portals:          # If portals are enabled for this room
         if random.randint(1, 30) == 1:      # 1/30 chance to make portal
               SummonPortal(x + 13, y + 10, chunkx, chunky)

    return make_level(texture, x, y, chunkx, chunky, **extraargs)

# Finds all the entrances for given level
def GetEntrances(Level):
     entrances = set()        # Set list for entrances
     if Level in UpLevels:         # If level is in UpLevels text file
         entrances.add('up')       # Add up as an entrance
     if Level in DownLevels:       # If level is in DownLevels text file
         entrances.add('down')     # Add down as an entrance
     if Level in LeftLevels:       # etc. etc.
         entrances.add('left')
     if Level in RightLevels:  
         entrances.add('right')
     return entrances

# Create Vertical Locked Door
def CreateLockedDoorV(x, y, randomchance, colour = 'default'):
     if random.randint(1, 20) == 1 and randomchance:
          if colour == 'default':
               doorcolour = random.randint(1, 20)
               if doorcolour == 1:
                    colour = 'red'
                    r = 255
                    g = 0
                    b = 0
               elif doorcolour == 20:
                    colour = 'blue'
                    r = 0
                    g = 0
                    b = 255
               else:
                    colour = 'regular'
                    r = 255
                    g = 255
                    b = 255
          LockedDoor = Entity(position = (x + 0.5, y + 4),
                              model = 'quad',
                              collider = 'box',
                              texture = load_texture('Sprites/LockedDoorV.png'),
                              scale = (1, 8, 1),
                              colour = colour,
                              color = color.rgb(r, g, b),
                              despawnable = True)
          LockedDoors.append(LockedDoor)
     elif not randomchance:
          if colour == 'default':
               colour = 'regular'
          LockedDoor = Entity(position = (x + 0.5, y + 4),
                              model = 'quad',
                              collider = 'box',
                              texture = load_texture('Sprites/LockedDoorV.png'),
                              scale = (1, 8, 1),
                              colour = colour,
                              despawnable = True)
          LockedDoors.append(LockedDoor)

# Create Horizontal Locked Door
def CreateLockedDoorH(x, y, randomchance, colour = 'default'):
     if random.randint(1, 20) == 1 and randomchance:        # 1/20 chance to create a Locked Door if random
          if colour == 'default':
               doorcolour = random.randint(1, 20)      # 1/10 chance for door to be either red or blue, otherwise door is "regular" / grey
               if doorcolour == 1:
                    colour = 'red'
                    r = 255
                    g = 0
                    b = 0
               elif doorcolour == 20:
                    colour = 'blue'
                    r = 0
                    g = 0
                    b = 255
               else:
                    colour = 'regular'
                    r = 255
                    g = 255
                    b = 255
          LockedDoor = Entity(position = (x + 4, y + 0.5),
                              model = 'quad',
                              collider = 'box',
                              texture = load_texture('Sprites/LockedDoorH.png'),
                              scale = (8, 1, 1),
                              colour = colour,
                              color = color.rgb(r, g, b),
                              despawnable = True)
          LockedDoors.append(LockedDoor)
     elif not randomchance:        # If not random, no door colour and door is not random chance
          if colour == 'default':
               colour = 'regular'
          LockedDoor = Entity(position = (x + 4, y + 0.5),
                              model = 'quad',
                              collider = 'box',
                              texture = load_texture('Sprites/LockedDoorH.png'),
                              scale = (8, 1, 1),
                              colour = colour,
                              despawnable = True)
          LockedDoors.append(LockedDoor)

BossSpawners = []         # Empty Boss Spawners list for updating
# Create a Boss Spawner
def BossLevel(x, y):
     BossSpawner = Entity(position = (x, y + 1),
                          model = 'quad',
                          collider = 'box',
                          scale = (1, 1.5),
                          playercollision = False,
                          spawned = False,
                          color = color.rgba(0, 0, 0, 0),
                          despawnable = True)
     spawneranimation = Animate('bossSpawner')
     spawneranimation.parent = BossSpawner
     BossSpawners.append(BossSpawner)

# Animation Controller
def Animate(animation):
     if animation == 'bossSpawner':
          spawneranimation = SpriteSheetAnimation('Sprites/BossSpawner/BossSpawnerSheet.png', tileset_size=(10,1), fps = 10, animations={'float' : ((0, 0), (9, 0))})
          spawneranimation.scale = 3
          spawneranimation.play_animation('float')
          return spawneranimation