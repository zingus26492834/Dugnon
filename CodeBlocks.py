from ursina import *

# Variables not specific to class
code_blocks = []        # Empty list to store all code blocks
last_block = None       # Tracks last dragged block

# Class to create code blocks
class CodeBlock(Button):    
    def __init__(self, texture, code, **kwargs):
        super().__init__(texture = load_texture(texture), model = 'quad', scale = (0.2, 0.1), color = color.white, unlit = True, **kwargs)
        self.code = code
        self.dragging = False
        self.Active = False
        code_blocks.append(self)        # Adds code block to code_blocks list

    # Loop using Ursina's update function
    def update(self):
        global last_block       # Allows last_block to be used in this function
        if self.Active:
            if self.dragging:
                self.position = mouse.position      # Drags block with mouse
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
        snapthresh = max(self.scale.x, self.scale.y) * 0.9        # Creates a variable smaller than the size of the block
        for block in code_blocks:       # Checks every block
            if block != self and not block.dragging:        # Makes sure it's not checking itself and isn't being dragged
                distance = (self.position - block.position).length()        # Checks distance between blocks
                if distance < snapthresh:       # Checks if block is close enough to snap

                    offset = Vec2(block.scale.x, 0)      # Offsets block to snap to the right side
                    self.position = block.position + offset         # Snaps block
                    


# Function to execute code blocks
def execute(**kwargs):
        blockgroups = []
        sortedblocks = set()

        # Groups code blocks that are snapped together
        def creategroups(startblock, group):
            for other_block in code_blocks:         # Checks every other block
                if other_block not in sortedblocks:     # Makes sure block is not already sorted
                    blockbox = max(startblock.scale.x, startblock.scale.y) * 1.2        # Creates a variable slightly larger than the size of the block
                    distance = (startblock.position - other_block.position).length()        # Checks distance between blocks
                    if distance <= blockbox:        # Checks if blocks have been snapped
                        group.append(other_block)       # Adds block to group if they have been snapped
                        sortedblocks.add(other_block)       # Indicates this block no longer needs to be sorted
                        creategroups(other_block, group)        # Repeats process to check for blocks snapped to the new block

        # Sorts blocks into groups to be executed
        for block in code_blocks:
            if block not in sortedblocks:
                group = [block]    # Starts a new group with the first block
                sortedblocks.add(block)     # Indicates that this block has been sorted
                creategroups(block, group)   # Checks for blocks that are snapped to the first block and adds them to the group

                group = sorted(group, key=lambda block: block.position.x)       # Orders group contents from left to right (based on block position)
                blockgroups.append(group)       # Adds group to a list to be executed

        # Executes groups
        for i, group in enumerate(blockgroups):     # Ensures each group is executed in order
            if len(group) > 1:      # Excludes groups with 1 block only
                print(f"Group {i + 1}:")        # Displays which group is being executed
                executedcode = ''.join([block.code for block in group])     # Joins code to be functional (if blocks are correctly ordered)
                print(executedcode)     # Displays code that will be executed
                try:        # Prevents crashing if code is incorrect
                    exec(executedcode, {}, kwargs)      # Executes code, adding kwargs from function
                except Exception as e:
                    print(f"Error: {e}")        # Displays what went wrong if code is incorrect