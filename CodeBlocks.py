# Imports
from ursina import *
from CodeFunctions import *
from Player import player
from Tutorial import *

# Variables not specific to class
code_blocks = []        # Empty list to store all code blocks
ItemCodeBlocks = []
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
        self.code = code        # Code here is a string fed into execute()
        self.texture = load_texture(texture)    # This has to be loaded after the model to properly be applied
        self.dragging = False       # Determines whether codeblock is being dragged or not
        self.Active = False     # If menu is not open, stops interaction
        code_blocks.append(self)        # Adds code block to code_blocks list

    # Loop using Ursina's update function
    def update(self):
        global last_block       # Allows last_block to be used in this function
        if self.Active:
            if self.dragging:
                mouselocalpos = cbpe.get_relative_point(camera.ui, mouse.position)      # Finds mouse position relative to codeblocks ui, since mouse is based off ui and codeblocks ui is a seperate ui
                self.position = (mouselocalpos.x, mouselocalpos.y)      # Drags block with mouse
            elif last_block == self:        # Makes sure only the last dragged block gets snapped
                self.SnapToBlock()      # Snaps block if not being dragged

    # Function to drag blocks
    def input(self, key):
        if TutorialGuy.IsSpeaking:      # Stops movement while Nosed One is speaking
            return
        if not self.enabled:
            return
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
        ExecuteArgs = {**globals(),     # Makes sure it properly registers these
                'key' : key, 
                'player' : player}

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
        noexecutedgroups = 0
        for i, group in enumerate(blockgroups):     # Ensures each group is executed in order
            if len(group) > 2:      # Excludes groups with 2 or less blocks
                noexecutedgroups += 1
                print(f"Group {noexecutedgroups}:")        # Displays which group is being executed
                executedcode = ''.join([block.code for block in group])     # Joins code to be functional (if blocks are correctly ordered)
                print(executedcode)     # Displays code that will be executed
                try:        # Prevents crashing if code is incorrect
                    exec(executedcode, ExecuteArgs, **kwargs)      # Executes code, adding kwargs from function
                except Exception as e:
                    print(f"Error: {e}")        # Displays what went wrong if code is incorrect

# Make list of all codeblocks that can be generated
def CodeBlocksList():
    AvailableCodeBlocks = []        # List for codeblocks
    with open('CodeBlocks/CodeBlocksList.txt', 'r') as CBL:      # Open codeblocks list
        for line in CBL:        # Check every line in the file
            line = line.rstrip('\n')        # I forgot what this does actually I think it separates lines at the end of the line but also i think "for line in" does that anyway?
            if '|' in line:     # Makes sure to end each line at '|', ensures it counts spaces at the end of lines
                line = line.strip().split('|', 1)[0]        
            strippedline = line.split(',,', 1)      # Separates line at ',,' since each line is 2 parts
            if len(strippedline) > 1:       # I think this makes sure it doesn't count every new line
                strippedline[1] = strippedline[1].replace('\\n', '\n')      # Replaces \n with \\n since the 2 \\ are merged and treated as \n in string, but if it were just \n it would consider that a new line instead
            AvailableCodeBlocks.append(strippedline)        # Add the line to available code blocks
    return AvailableCodeBlocks

# Randomly generate codeblock
def RandomCodeBlock():
    ACB = CodeBlocksList()      # Gets list of every codeblock
    ACBCount = 0        # Count for codeblocks
    for CB in ACB:      # for Every Codeblock
        ACBCount += 1   # Count goes up 1
    return random.randint(0, ACBCount - 1)      # Returns a random number between 0 and the count - 1 (since python counts start at 0 and this one started at 1)

# Generate codeblock as item
def GenerateCodeBlock(CBid, CBx, CBy):
    ACB = CodeBlocksList()
    CBInfo = ACB[CBid]      # Info for codeblockitem, necessary when picked up
    codeblockitem = Entity(model = 'quad', 
                           unlit = True, 
                           position = (CBx, CBy, 0.1), 
                           scale = (2, 1, 1), 
                           CBid = CBid, 
                           Active = True,
                           despawnable = True, 
                           playercollision = False)
    codeblockitem.collider = BoxCollider(codeblockitem, 
                                         center = Vec3(0, 0, 0), 
                                         size = (1.2, 1.6, 1))
    codeblockitem.texture = load_texture(CBInfo[0])     # Item texture is codeblock's textuer
    return codeblockitem

CurrentCodeBlocks = []
# Create CodeBlock based on Id
def CreateCodeBlock(CBid):
    global CurrentCodeBlocks
    CBList = CodeBlocksList()
    texture, code = CBList[CBid]        # Get texture and code from Id in list
    CreatedCodeBlock = CodeBlock(texture, code, visible = False)        # Create codeblock using above
    # Attempt to move created block out of the way so it isn't overlapping other blocks
    for c in CurrentCodeBlocks:
        if CreatedCodeBlock.intersects(c):
            CreatedCodeBlock.x += 0.2
    CurrentCodeBlocks.append(CreatedCodeBlock)
    return CreatedCodeBlock

cbpe.y -= 3     # Moves codeblock parent entity down 3 to make sure codefunctions dont aim at it, since it's calculated on screen space not world space and would return a value between -1 and 1
# Toggle CodeBlocks
def ToggleCodeBlocks(Active):
    global CurrentCodeBlocks
    if Active:      # Moves codeblock parent entity back up 3 and on to the screen
        cbpe.y += 3
    else:
        cbpe.y -= 3     # Moves cbpe back off screen
    for c in CurrentCodeBlocks:
        # If active, make functional and visible, otherwise don't
        if Active:
            c.Active = True
            c.visible = True
        else:
            c.Active = False
            c.visible = False
            CodeBlocksGuide.visible = False     # Also disable the guide

RareCodeBlocks = []
# create list for rare codeblocks (same as above just not function and different file)
with open('CodeBlocks/RareCodeBlocksList.txt', 'r') as RCBL:
    for line in RCBL:
        line = line.rstrip('\n')
        if '|' in line:
            line = line.strip().split('|', 1)[0]
        strippedline = line.split(',,', 1)
        if len(strippedline) > 1:
            strippedline[1] = strippedline[1].replace('\\n', '\n')
        RareCodeBlocks.append(strippedline)

# Create random rare block (same as above just different list)            
def RandomRareCodeBlock():
    global RareCodeBlocks
    RCBCount = 0
    for CB in RareCodeBlocks:
        RCBCount += 1
    return random.randint(0, RCBCount - 1)

# Create rare codeblock item (same as above just different list)
def GenerateRareCodeBlock(CBid, CBx, CBy):
    global RareCodeBlocks
    CBinfo = RareCodeBlocks[CBid]
    codeblockitem = Entity(model = 'quad', 
                           unlit = True, 
                           position = (CBx, CBy, 0.1), 
                           scale = (2, 1, 1), 
                           CBid = CBid, 
                           Active = True,
                           despawnable = True, 
                           playercollision = False,
                           rare = True)
    codeblockitem.collider = BoxCollider(codeblockitem, 
                                         center = Vec3(0, 0, 0), 
                                         size = (1.2, 1.6, 1))
    codeblockitem.texture = load_texture(CBinfo[0])
    return codeblockitem

# Create Rare CodeBlock based on Id (same as above just different list)
def CreateRareCodeBlock(CBid):
    global RareCodeBlocks, CurrentCodeBlocks
    texture, code = RareCodeBlocks[CBid]
    CreatedCodeBlock = CodeBlock(texture, code, visible = False)
    for c in CurrentCodeBlocks:
        if CreatedCodeBlock.intersects(c):
            CreatedCodeBlock.x += 0.2
    CurrentCodeBlocks.append(CreatedCodeBlock)
    return CreatedCodeBlock

# Zoom in and out
def scrollblock(direction):
    if direction == 'up':       # If scrolldirection is up, make ui bigger / zoom in
        cbpep.scale = ((cbpep.scale.x * 1.1), (cbpep.scale.y * 1.1), 0.1)
    elif direction =='down':    # If scrolldirection is down, make ui smaller / zoom out
        cbpep.scale = ((cbpep.scale.x * 0.9), (cbpep.scale.y * 0.9), 0.1)

# CodeBlocksGuide entity
CodeBlocksGuide = Entity(model = 'quad', texture = load_texture('CodeBlocks/CodeBlocksGuide'), scale = (1, 1.3), z = -0.1, parent = cbpe, visible = False)