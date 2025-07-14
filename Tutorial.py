# Imports
from ursina import *

# Create Tutorial Entity / Nosed One (Sometimes referred to as TutorialGuy)
TutorialEntity = Entity(model = 'quad',
                        collider = 'box',
                        color = color.rgba(0, 0, 0, 0),     # Invisible, self.visible = False would make all children also invisible
                        position = (15, 2),
                        scale = (2, 2),
                        enabled = False,
                        playercollision = True)

# Nosed One Animation Creation
animation = SpriteSheetAnimation('Sprites/NosedOne/NosedOneSheet.png', tileset_size=(7,1), fps = 6, animations={'spin' : ((0, 0), (6, 0))}, doublesided = True)
animation.scale = 1
animation.play_animation('spin')
animation.parent = TutorialEntity       # Parent Animation to TutorialEntity

# Class to control all Tutorial Dialogue and UI
class Tutorial(Entity):
    def __init__(self, **kwargs):
        super().__init__(model = 'quad',
                         color = color.black,
                         scale = (0.4, 0.2),
                         position = (0, -0.3),
                         parent = camera.ui,
                         visible = False,
                         **kwargs)
        self.AdvanceDialogue = 0        # Checks how far dialogue has progressed
        self.Dialogue = Text(text='',       # Dialogue text
                             scale = (1, 1),
                             position = (-0.2, -0.2),
                             z = -0.1,
                             color = color.white,
                             parent = camera.ui)
        self.DialogueBorder = Entity(model = 'quad',        # Dialogue white border
                                     color = color.white,
                                     scale = (1.05, 1.1),
                                     parent = self,
                                     z = 0.1)
        self.RedCircle1 = Entity(model = 'quad',        # Red Circle
                                 texture = load_texture('Sprites/RedCircle.png'),
                                 z = -0.1,
                                 parent = camera.ui,
                                 visible = False)
        self.RedCircle2 = Entity(model = 'quad',        # Duplicate Red Circle
                                 texture = load_texture('Sprites/RedCircle.png'),
                                 z = -0.1,
                                 parent = camera.ui,
                                 visible = False)
        self.RedArrow1 = Entity(model = 'quad',         # Red Arrow
                                 texture = load_texture('Sprites/RedArrow.png'),
                                 z = -0.1,
                                 parent = camera.ui,
                                 visible = False)
        self.RedArrow2 = Entity(model = 'quad',         # Duplicate Red Arrow
                                 texture = load_texture('Sprites/RedArrow.png'),
                                 z = -0.1,
                                 parent = camera.ui,
                                 visible = False)
        self.WaitingForCodeBlocks = False       # Changes input needed to advance Tutorial to K temporarily
        self.FirstTutorial = True       # Tutorial dialogue is split into parts, every time Nosed One moves is another part
        self.SecondTutorial = False
        self.ThirdTutorial = False
        self.FourthTutorial = False
        self.FifthTutorial = False
        self.IsSpeaking = False     # True if Nosed One is currently speaking
        self.SecretTutorial = False     # The Secret after tutorial has ended
        self.SecretObtained = False     # True when no more available tutorials

    def update(self):
        # Updates Dialogue visibility with self visibility, since Dialogue is not a child of self
        if not self.visible:
            self.Dialogue.visible = False
            return
        else:
            self.Dialogue.visible = True
            self.IsSpeaking = True      # If self is visible, Nosed One is speaking
        
        # Dialogue controller
        if self.FirstTutorial:
            if self.AdvanceDialogue == 0:
                self.Dialogue.text = "Hello, I am the NosedOne. \n Press Z to continue."
                self.scale = (0.5, 0.15)        # Ressizes Dialogue Box
                self.position = (0, -0.2)       # Moves Dialogue box
                self.Dialogue.position = (-0.175, -0.175)       # Moves Dialogue text
            elif self.AdvanceDialogue == 1:
                self.Dialogue.text = "Keep in mind that you will not be able to interact with \nthe game while I am speaking."
                self.scale = (0.7, 0.15)
                self.position = (0.15, -0.2)
            elif self.AdvanceDialogue == 2:
                self.Dialogue.text = "In this game you have CodeBlocks and Code Snippets.\n You will need to use these to fight enemies and complete puzzles."
                self.scale = (0.9, 0.15)
                self.position = (0.25, -0.2)
            elif self.AdvanceDialogue == 3:
                self.Dialogue.text = "Press K to open your CodeBlocks menu. \n I will meet you in there."
                self.scale = (0.7, 0.15)
                self.position = (0.15, -0.2)
            elif self.AdvanceDialogue == 4:
                self.Dialogue.text = ""     # Blank text
                self.visible = False
                self.IsSpeaking = False     # Nosed One pauses to let player open CodeBlocks menu
                self.WaitingForCodeBlocks = True        # Nosed One is waiting for the CodeBlocks menu
            elif self.AdvanceDialogue == 5:
                self.Dialogue.text = "This is the menu where you edit your CodeBlocks."
                self.scale = (0.7, 0.08)
                self.position = (0.15, -0.2)
            elif self.AdvanceDialogue == 6:
                self.Dialogue.text = "You can move this menu with ScrollWheel and Right Click,\nand the CodeBlocks with Left Click."
                self.scale = (0.8, 0.15)
                self.position = (0.2, -0.2)
            elif self.AdvanceDialogue == 7:
                self.Dialogue.text = "This is a Code Snippet. \nCurrently it creates a key when you press E"
                self.scale = (0.7, 0.15)
                self.position = (0.4, -0.3)
                self.RedCircle1.visible = True      # Red Circle for demonstrion purposes
                self.RedCircle1.scale = (1.2, 0.5)      # Makes Red Circle huge
                self.RedCircle1.position = (-0.3, 0.2)      # Moves Red Circle
                self.Dialogue.position = (self.x - 0.3, self.y + 0.03)
            elif self.AdvanceDialogue == 8:
                self.Dialogue.text = "The If block checks if\nthe following statement\nhas been met."
                self.RedCircle1.scale = (0.3, 0.3)
                self.RedCircle1.position = (-0.7, 0.3)
                self.position = (-0.5, 0)
                self.Dialogue.position = (self.x -0.14, self.y + 0.03)
                self.scale = (0.3, 0.2)
            elif self.AdvanceDialogue == 9:
                self.Dialogue.text = "This Block checks whether\nthe shown key has been\npressed."
                self.position = (-0.4, -0.06)
                self.scale = (0.35, 0.2)
                self.Dialogue.position = (self.x -0.14, self.y + 0.03)
                self.RedCircle1.position = (-0.5, 0.3)
            elif self.AdvanceDialogue == 10:
                self.Dialogue.text = "In this case the Key is E"
            elif self.AdvanceDialogue == 11:
                self.Dialogue.text = "The Colon Block ends the if\nstatement and moves on\nto the code." 
                self.RedCircle1.position = (-0.3, 0.3)
                self.Dialogue.position = (self.x -0.16, self.y + 0.03)
            elif self.AdvanceDialogue == 12:
                self.Dialogue.text = "So this full if statement\nexecutes the following code\nwhen the E key is pressed."
            elif self.AdvanceDialogue == 13:
                self.Dialogue.text = "Yellow CodeBlocks are\nused to create things."
                self.position = (0.3, 0.1)
                self.Dialogue.position = (self.x -0.14, self.y + 0.03)
                self.RedCircle1.visible = False
            elif self.AdvanceDialogue == 14:
                self.Dialogue.text = "This one creates a Key."
                self.RedCircle1.visible = True
                self.RedCircle1.position = (-0.1, 0.3)
            elif self.AdvanceDialogue == 15:
                self.Dialogue.text = "This one creates a Block"
                self.RedCircle1.position = (-0.1, 0.1)
            elif self.AdvanceDialogue == 16:
                self.Dialogue.text = "Pink blocks modify yellow\nCodeBlocks"
                self.RedCircle1.visible = False
                self.position = (0.4, -0.15)
                self.Dialogue.position = (self.x - 0.14, self.y + 0.03)
            elif self.AdvanceDialogue == 17:
                self.Dialogue.text = "This one can be thought\nof as a default modifier."
                self.RedCircle1.position = (0.1, 0.3)
                self.RedCircle1.visible = True
            elif self.AdvanceDialogue == 18:
                self.Dialogue.text = "Every Yellow CodeBlock works differently\nbased on the modifiers."
                self.RedCircle1.visible = False
                self.position = (0, -0.2)
                self.scale = (0.6, 0.2)
                self.Dialogue.position = (self.x - 0.27, self.y + 0.03)
            elif self.AdvanceDialogue == 19:
                self.Dialogue.text = "Now Try swapping both Yellow CodeBlocks."
                self.RedCircle1.visible = True
                self.RedCircle1.position = (-0.1, 0.3)
                self.RedCircle1.scale = (0.15, 0.15)
                self.RedCircle2.visible = True      # Duplicate Red Circle
                self.RedCircle2.position = (-0.1, 0.1)
                self.RedCircle2.scale = (0.15, 0.15)
                self.RedArrow1.visible = True       # Red Arrow
                self.RedArrow1.position = (-0.2, 0.2)
                self.RedArrow1.scale = (0.15, 0.15)
                self.RedArrow2.visible = True       # Red Arrow Duplicate
                self.RedArrow2.position = (0, 0.2)
                self.RedArrow2.scale = (0.15, 0.15)
                self.RedArrow2.rotation_z = 180
            elif self.AdvanceDialogue == 20:
                self.Dialogue.text = "Always remember to place CodeBlocks over \nthe top of the block to the left \nand let it snap."
                self.RedCircle1.visible = False
                self.RedCircle2.visible = False
                self.RedArrow1.visible = False
                self.RedArrow2.visible = False
            elif self.AdvanceDialogue == 20:
                self.Dialogue.text = "And note that Snippets execute in order\nfrom top to bottom."
            elif self.AdvanceDialogue == 21:
                self.Dialogue.text = "Once you're done, press Q to toggle executing\nthe snippets."
            elif self.AdvanceDialogue == 22:
                self.Dialogue.text = "You can also press K to toggle the menu if you\nwant."
            elif self.AdvanceDialogue == 23:
                self.Dialogue.text = "I will meet you at the top of this ledge when\nyou're done."
            elif self.AdvanceDialogue == 24:
                self.Dialogue.text = ""
                self.visible = False
                TutorialEntity.position = (19.5, 8)
                self.FirstTutorial = False
                self.SecondTutorial = True
                self.AdvanceDialogue = 0
                self.IsSpeaking = False
        elif self.SecondTutorial:
            if self.AdvanceDialogue == 0:
                self.Dialogue.text = "Good job!"
            elif self.AdvanceDialogue == 1:
                self.Dialogue.text = "Now we are faced with a Locked Door."
            elif self.AdvanceDialogue == 2:
                self.Dialogue.text = "Different coloured doors need different\ncoloured keys."
            elif self.AdvanceDialogue == 3:
                self.Dialogue.text = "This door has no colour and neither does\nyour key."
            elif self.AdvanceDialogue == 4:
                self.Dialogue.text = "So they will work together."
            elif self.AdvanceDialogue == 5:
                self.Dialogue.text = "Swap the yellow blocks again and unlock\nthe door."
            elif self.AdvanceDialogue == 6:
                self.Dialogue.text = "I will meet you again on the other side\nof the door."
            elif self.AdvanceDialogue == 7:
                self.Dialogue.text = ""
                self.visible = False
                self.SecondTutorial = False
                self.IsSpeaking = False
                self.ThirdTutorial = True
                self.AdvanceDialogue = 0
                TutorialEntity.position = (33, 2)
        elif self.ThirdTutorial:
            if self.AdvanceDialogue == 0:
                self.Dialogue.text = "Oh no an enemy!"
            elif self.AdvanceDialogue == 1:
                self.Dialogue.text = "Currently you have no way of fighting back."
            elif self.AdvanceDialogue == 2:
                self.Dialogue.text = "So the enemy should be avoided."
            elif self.AdvanceDialogue == 3:
                self.Dialogue.text = "But look there!"
                self.RedCircle1.visible = True
                self.RedCircle1.scale = (0.3, 0.3)
                self.RedCircle1.position = (0, 0.15)
            elif self.AdvanceDialogue == 4:
                self.Dialogue.text = "A CodeBlock!"
            elif self.AdvanceDialogue == 5:
                self.Dialogue.text = "If you're feeling confident, try\ngrabbing that CodeBlock."
                self.RedCircle1.visible = False
            elif self.AdvanceDialogue == 6:
                self.Dialogue.text = "Also, you've probably noticed by\nnow, but there are locked doors on\nthe floor and ceiling."
            elif self.AdvanceDialogue == 7:
                self.Dialogue.text = "To open these you will need a\ndifferent modifier for your key."
            elif self.AdvanceDialogue == 8:
                self.Dialogue.text = "That leaves us only one way forward."
            elif self.AdvanceDialogue == 9:
                self.Dialogue.text = "I will meet you past the door to\nthe right."
            elif self.AdvanceDialogue == 10:
                self.Dialogue.text = ""
                self.AdvanceDialogue = 0
                self.visible = False
                self.ThirdTutorial = False
                self.FourthTutorial  = True
                TutorialEntity.position = (58, 2)
                self.IsSpeaking = False
        elif self.FourthTutorial:
            if self.AdvanceDialogue == 0:
                self.Dialogue.text = "There are some more CodeBlocks in here."
            elif self.AdvanceDialogue == 1:
                self.Dialogue.text = "Pick them up and try making a new snippet\nso you don't have to constantly\nswap Block and Key."
            elif self.AdvanceDialogue == 2:
                self.Dialogue.text = "If you have just picked up new CodeBlocks\nthey will not appear if you have\nthe menu open."
            elif self.AdvanceDialogue == 3:
                self.Dialogue.text = "In that case just close and reopen the menu."
            elif self.AdvanceDialogue == 4:
                self.Dialogue.text = "Then proceed up."
            elif self.AdvanceDialogue == 5:
                self.Dialogue.text = ""
                self.AdvanceDialogue = 0
                self.visible = False
                self.FifthTutorial = True
                self.FourthTutorial  = False
                TutorialEntity.position = (58, 18)
                self.IsSpeaking = False
        elif self.FifthTutorial:
            if self.AdvanceDialogue == 0:
                self.Dialogue.text = "Great job!"
            elif self.AdvanceDialogue == 1:
                self.Dialogue.text = "You have completed the Tutorial!"
            elif self.AdvanceDialogue == 2:
                self.Dialogue.text = "There also happens to be a Boss Summoner here!"
                self.RedCircle1.visible = True
            elif self.AdvanceDialogue == 3:
                self.Dialogue.text = "Bosses can drop Rare CodeBlocks, as well as\na portal that takes you to a different\narea!"
                self.RedCircle1.visible = False
            elif self.AdvanceDialogue == 4:
                self.Dialogue.text = "However they are harder to fight than regular\nenemies and will trap you in the room."
            elif self.AdvanceDialogue == 5:
                self.Dialogue.text = "But you don't have a way to hurt it, so it's\ncertain death if you fight it now!..\nUnless..."
            elif self.AdvanceDialogue == 6:
                self.Dialogue.text = "If you're reading this...\n...Return to the first room...\nI may have something of use to you..."
            elif self.AdvanceDialogue == 7:
                self.Dialogue.text = "Remember, you can press P while in the \nCodeBlocks menu to open the CodeBlocks \nguide if you need help."
            elif self.AdvanceDialogue == 8:
                self.Dialogue.text = ""
                self.AdvanceDialogue = 0
                self.visible = False
                self.FifthTutorial = False
                self.SecretTutorial = True
                TutorialEntity.position = (5.5, 4)
                self.IsSpeaking = False
        elif self.SecretTutorial:
            if self.AdvanceDialogue == 0:
                self.Dialogue.text = "Thank you for listening to the tutorial."
            elif self.AdvanceDialogue == 1:
                self.Dialogue.text = "..."
            elif self.AdvanceDialogue == 2:
                self.Dialogue.text = "Take him."
            elif self.AdvanceDialogue == 3:
                self.Dialogue.text = "The forbidden one is yours."
            elif self.AdvanceDialogue == 4:
                self.Dialogue.text = ""
                self.AdvanceDialogue = 0
                self.visible = False
                self.SecretTutorial  = False
                TutorialEntity.enabled = False
                self.IsSpeaking = False
                self.SecretObtained = True      # Gives player Secret CodeBlock


    def input(self, key):
        # Advances and opens dialogue if K is pressed rather than Z while WaitingForCodeBlocks
        if key == 'k' and self.WaitingForCodeBlocks:
            self.visible = True
            self.AdvanceDialogue += 1
            self.WaitingForCodeBlocks = False
        
        if not self.visible:
            return
        
        # Progress Dialogue if Nosed One is speaking
        if key == 'z' and self.IsSpeaking and not self.WaitingForCodeBlocks:
            self.AdvanceDialogue += 1
    
TutorialGuy = Tutorial()        # Creates an object to control Tutorial, TutorialGuy was a placeholder for Nosed One that I'm not bothered to go through all my code and update the name for

