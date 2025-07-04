from ursina import *
from CodeBlocks import *
from Player import *
from Enemy import *
     

quad = load_model('quad', use_deepcopy=True)
level_parent = Entity(model=Mesh(vertices=[], uvs=[]), texture='white_cube')
loaded_chunks = {}
LockedDoors = []

def make_level(texture, offset_x, offset_y, chunkx, chunky, randomdoors = True, bossdisable = False, bossguarentee = False):
    for y in range(texture.height):
        collider = None
        for x in range(texture.width):
            col = texture.get_pixel(x,y)
            
            world_x = x + offset_x
            world_y = y + offset_y

            if col == color.black:
                level_parent.model.vertices += [Vec3(*e) + Vec3(world_x+.5,world_y+.5,0) for e in quad.generated_vertices]
                level_parent.model.uvs += quad.uvs
                if not collider:
                    collider = Entity(parent=level_parent, 
                                      position=(world_x,world_y), 
                                      model='cube', 
                                      origin=(-.5,-.5), 
                                      collider='box',
                                      despawnable = True, 
                                      visible=False)
                else:
                    collider.scale_x += 1
            else:
                collider = None

            if col == color.green:
                player.start_position = (world_x, world_y)
                player.position = player.start_position
            
            if col == color.red:
                if random.randint(1, 5) == 5:
                     ItemCodeBlocks.append(GenerateRareCodeBlock(RandomRareCodeBlock(), (world_x) + 0.5, (world_y + 0.5)))
                else:
                     ItemCodeBlocks.append(GenerateCodeBlock(RandomCodeBlock(), (world_x + 0.5), (world_y + 0.5)))
            
            if col == color.blue:
                 if x > (texture.width / 2) + 5 or x < (texture.width / 2) - 5:
                    CreateLockedDoorV(world_x, world_y, randomdoors)
                 elif y > (texture.height / 2) + 5 or y < (texture.height / 2) - 5:
                    CreateLockedDoorH(world_x, world_y, randomdoors)

            if col == color.yellow:
                 if bossguarentee:
                      BossLevel(world_x, world_y)
                 elif bossdisable:
                      RandomEnemy((world_x, world_y + 0.5))
                 elif random.randint(1, 20) == 1:
                      BossLevel(world_x, world_y)
                 else:
                     RandomEnemy((world_x, world_y + 0.5))
            entrances = GetEntrances(texture.name)
            loaded_chunks[(chunkx, chunky)] = entrances
            

    level_parent.model.generate()

def CheckChunk(x, y):
    global loaded_chunks
    chunkpos = (x, y)
    if chunkpos in loaded_chunks:
        return True
    else:
        loaded_chunks[chunkpos] = set()
        print(chunkpos)
        return False
    
UpLevels = []
with open('Levels/UpLevels.txt') as f:
            for line in f:
                UpLevels.append(line.strip())
DownLevels = []
with open('Levels/DownLevels.txt') as f:
            for line in f:
                DownLevels.append(line.strip())
LeftLevels = []
with open('Levels/LeftLevels.txt') as f:
            for line in f:
                LeftLevels.append(line.strip())
RightLevels = []
with open('Levels/RightLevels.txt') as f:
            for line in f:
                RightLevels.append(line.strip())

def RandomLevel(direction, x, y, chunkx, chunky):
    LeftChunk = (chunkx - 1, chunky)
    RightChunk = (chunkx + 1, chunky)
    UpChunk = (chunkx, chunky + 1)
    DownChunk = (chunkx, chunky - 1)

    required_direction = set()
    forbidden_directions = set()
    if 'down' in loaded_chunks.get((UpChunk), set()):
         required_direction.add('up')
    else:
         forbidden_directions.add('up')
    if 'up' in loaded_chunks.get((DownChunk), set()):
         required_direction.add('down')
    else:
         forbidden_directions.add('down')
    if 'left' in loaded_chunks.get((RightChunk), set()):
         required_direction.add('right')
    else:
         forbidden_directions.add('right')
    if 'right' in loaded_chunks.get((LeftChunk), set()):
         required_direction.add('left')
    else:
         forbidden_directions.add('left')

    if direction == 'up':
         AvailableLevels = UpLevels
    if direction == 'down':
         AvailableLevels = DownLevels
    if direction == 'left':
         AvailableLevels = LeftLevels
    if direction == 'right':
         AvailableLevels = RightLevels

    FilteredLevels = []
    for Level in AvailableLevels:
         entrances = GetEntrances(Level)
         if required_direction.issubset(entrances) and forbidden_directions.isdisjoint(entrances):
             FilteredLevels.append(Level)
    
    if not FilteredLevels:
         FilteredLevels = AvailableLevels

    RandomLevel = random.choice(FilteredLevels)
    texture = load_texture(RandomLevel)
    if not texture:
         print(f'Missing Texture: {RandomLevel} DEBUG STATEMENT DEBUG STATMENT READ THIS DEBUG STATMENT')
         return
    return make_level(texture, x, y, chunkx, chunky)

def GetEntrances(Level):
     entrances = set()
     if Level in UpLevels:
         entrances.add('up')
     if Level in DownLevels:
         entrances.add('down')
     if Level in LeftLevels:
         entrances.add('left')
     if Level in RightLevels:  
         entrances.add('right')
     return entrances

def CreateLockedDoorV(x, y, randomchance, colour = 'regular'):
     if random.randint(1, 20) == 1 and randomchance:
          LockedDoor = Entity(position = (x + 0.5, y + 4),
                              model = 'quad',
                              collider = 'box',
                              texture = load_texture('brick'),
                              scale = (1, 8, 1),
                              colour = colour,
                              despawnable = True)
          LockedDoors.append(LockedDoor)
     elif not randomchance:
          LockedDoor = Entity(position = (x + 0.5, y + 4),
                              model = 'quad',
                              collider = 'box',
                              texture = load_texture('brick'),
                              scale = (1, 8, 1),
                              colour = colour,
                              despawnable = True)
          LockedDoors.append(LockedDoor)

def CreateLockedDoorH(x, y, randomchance, colour = 'regular'):
     if random.randint(1, 20) == 1 and randomchance:
          LockedDoor = Entity(position = (x + 4, y + 0.5),
                              model = 'quad',
                              collider = 'box',
                              texture = load_texture('brick'),
                              scale = (8, 1, 1),
                              colour = colour,
                              despawnable = True)
          LockedDoors.append(LockedDoor)
     elif not randomchance:
          LockedDoor = Entity(position = (x + 4, y + 0.5),
                              model = 'quad',
                              collider = 'box',
                              texture = load_texture('brick'),
                              scale = (8, 1, 1),
                              colour = colour,
                              despawnable = True)
          LockedDoors.append(LockedDoor)

BossSpawners = []
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

def Animate(animation):
     if animation == 'bossSpawner':
          spawneranimation = SpriteSheetAnimation('Sprites/BossSpawner/BossSpawnerSheet.png', tileset_size=(10,1), fps = 10, animations={'float' : ((0, 0), (9, 0))})
          spawneranimation.scale = 3
          spawneranimation.play_animation('float')
          return spawneranimation