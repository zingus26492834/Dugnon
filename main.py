from ursina import *
from CodeBlocks import *

app = Ursina()

ifblock = CodeBlock('CodeBlocks/if.png', 'if ')
cheese = CodeBlock('CodeBlocks/cheese.png', 'apple:\n    ')
banana = CodeBlock('CodeBlocks/banana.png', 'print("Banana")')

def input(key):
    if key == 'space':
        execute(apple=True)

app.run()