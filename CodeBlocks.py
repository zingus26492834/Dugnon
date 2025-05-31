from ursina import *
from CodeFunctions import *
from Player import player

# Variables not specific to class
code_blocks = []        # Empty list to store all code blocks
last_block = None       # Tracks last dragged block
cbpep = Entity(scale = 1, position = (0, 0), parent = camera.ui)    # Code Block Parent Entity Parent, for zooming codeblocks ui
cbpe = Entity(scale = 1, position = (0, 0), parent = cbpep)         # Code Block Parent Entity, for moving all codeblocks as if panning

# Class to create code blocks
class CodeBlock(Button):    
    def __init__(self, texture, code, **kwargs):
        super().__init__(model = 'quad', 
                         scale = (0.2, 0.1), 
                         color = color.white, 
                         unlit = True, 
                         parent = cbpe, 
                         **kwargs)
        self.code = code
        self.texture = load_texture(texture)    # This has to be loaded after the model to properly be applied
        self.dragging = False
        self.Active = False
        code_blocks.append(self)        # Adds code block to code_blocks list

    # Loop using Ursina's update function
    def update(self):
        global last_block       # Allows last_block to be used in this function
        if self.Active:
            if self.dragging:
                mouselocalpos = cbpe.get_relative_point(camera.ui, mouse.position)
                self.position = (mouselocalpos.x, mouselocalpos.y)      # Drags block with mouse
            elif last_block == self:        # Makes sure only the last dragged block gets snapped
                self.SnapToBlock()      # Snaps block if not being dragged

    # Function to drag blocks
    def input(self, key):
        global last_block       # Allows last_block to be used in this function
        if self.hovered and key == 'left mouse down':       # Checks if mouse if being clicked while over block
            self.dragging = True
            last_block = self       # Sets self as the last dragged block
        elif key == 'left mouse up':        # Checks if mouse is no longer being clicked
            self.dragging = False

    # Function to snap nearby blocks together
    def SnapToBlock(self):
        for block in code_blocks:       # Checks every block
            if block != self and not block.dragging:        # Makes sure it's not checking itself and isn't being dragged
                distance = (self.position - block.position)        # Checks distance between blocks
                if abs(distance.x) < self.scale.x * 0.9 and abs(distance.y) < self.scale.y * 0.9:       # Compares distance to size of block, if distance is smaller than it snaps
                    snappos = Vec2(block.scale.x, 0)      # Offsets block to snap to the right side
                    self.position = block.position + snappos         # Snaps block
                    

ExecutedEntities = []
# Function to execute code blocks
def execute(key = None, **kwargs):
        blockgroups = []
        sortedblocks = set()

        # Groups code blocks that are snapped together
        def creategroups(startblock, group):
            for other_block in code_blocks:         # Checks every block that isn't this one
                if other_block not in sortedblocks:     # Makes sure block is not already sorted
                    blockbox = startblock.scale.x * 1.2        # Creates a variable slightly larger than the length of the block
                    distance = (startblock.position.x - other_block.position.x)        # Checks distance between blocks
                    if distance <= blockbox and startblock.position.y == other_block.position.y:        # Checks if block has been snapped
                        group.append(other_block)       # Adds block to group if they have been snapped
                        sortedblocks.add(other_block)       # Indicates this block no longer needs to be sorted
                        creategroups(other_block, group)        # Repeats process to check for blocks snapped to the new block

        # Sorts blocks into groups to be executed
        for block in code_blocks:
            if block not in sortedblocks:
                group = [block]    # Starts a new group with the first block
                sortedblocks.add(block)     # Indicates that this block has been sorted
                creategroups(block, group)   # Checks for blocks that are snapped to the first block and adds them to the group

                group = sorted(group, key=lambda block: block.position.x)       # Orders group contents from top to bottom, left to right (based on block position)
                blockgroups.append(group)       # Adds group to a list to be executed

        blockgroups.sort(key=lambda group: min(block.position.y for block in group), reverse = True)        # Sorts groups to be executed in order of top to bottom

        # Executes groups
        for i, group in enumerate(blockgroups):     # Ensures each group is executed in order
            if len(group) > 1:      # Excludes groups with 1 block only
                print(f"Group {i + 1}:")        # Displays which group is being executed
                executedcode = ''.join([block.code for block in group])     # Joins code to be functional (if blocks are correctly ordered)
                print(executedcode)     # Displays code that will be executed
                try:        # Prevents crashing if code is incorrect
                    exec(executedcode, {**globals(), 'key': key,  'FireableBlock' : FireableBlock, 'player': player, **kwargs})      # Executes code, adding kwargs from function
                except Exception as e:
                    print(f"Error: {e}")        # Displays what went wrong if code is incorrect


def CodeBlocksList():
    AvailableCodeBlocks = []
    with open('CodeBlocks/CodeBlocksList.txt', 'r') as CBL:
        for line in CBL:
            line = line.rstrip('\n')
            if '|' in line:
                line = line.strip().split('|', 1)[0]
            strippedline = line.split(',', 1)
            if len(strippedline) > 1:
                strippedline[1] = strippedline[1].replace('\\n', '\n')
            AvailableCodeBlocks.append(strippedline)
    return AvailableCodeBlocks

def RandomCodeBlock():
    ACB = CodeBlocksList()
    ACBCount = 0
    for CB in ACB:
        ACBCount += 1
    return random.randint(0, ACBCount - 1)

def GenerateCodeBlock(CBid, CBx, CBy):
    ACB = CodeBlocksList()
    CBInfo = ACB[CBid]
    codeblockitem = Entity(model = 'quad', 
                           unlit = True, 
                           position = (CBx, CBy, 0.1), 
                           scale = (2, 1, 1), 
                           CBid = CBid, 
                           Active = True, 
                           playercollision = False)
    codeblockitem.collider = BoxCollider(codeblockitem, 
                                         center = Vec3(0, 0, 0), 
                                         size = (1.2, 1.6, 1))
    codeblockitem.texture = load_texture(CBInfo[0])
    return codeblockitem

CurrentCodeBlocks = []
def CreateCodeBlock(CBid):
    global CurrentCodeBlocks
    CBList = CodeBlocksList()
    texture, code = CBList[CBid]
    CreatedCodeBlock = CodeBlock(texture, code, visible = False)
    CurrentCodeBlocks.append(CreatedCodeBlock)
    return CreatedCodeBlock

def ToggleCodeBlocks(Active):
    global CurrentCodeBlocks
    for c in CurrentCodeBlocks:
        if Active:
            c.Active = True
            c.visible = True
        else:
            c.Active = False
            c.visible = False

def scrollblock(direction):
    if direction == 'up':
        cbpep.scale = ((cbpep.scale.x * 1.1), (cbpep.scale.y * 1.1), 0.1)
    elif direction =='down':
        cbpep.scale = ((cbpep.scale.x * 0.9), (cbpep.scale.y * 0.9), 0.1)