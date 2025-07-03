from ursina import *

TutorialEntity = Entity(model = 'quad',
                        collider = 'box',
                        texture = load_texture('Sprites/TutorialGuy.png'),
                        position = (15, 1.5),
                        scale = (1, 1),
                        enabled = False,
                        playercollision = True)

class Tutorial(Entity):
    def __init__(self, **kwargs):
        super().__init__(model = 'quad',
                         color = color.black,
                         scale = (0.4, 0.2),
                         position = (0, -0.3),
                         parent = camera.ui,
                         visible = False,
                         **kwargs)
        self.AdvanceDialogue = 0
        self.Dialogue = Text(text='',
                             scale = (1, 1),
                             position = (-0.2, -0.3),
                             z = -0.1,
                             color = color.white,
                             parent = camera.ui)
        self.DialogueBorder = Entity(model = 'quad',
                                     color = color.white,
                                     scale = (1.05, 1.1),
                                     parent = self,
                                     z = 0.1)
        self.RedCircle1 = Entity(model = 'quad',
                                 texture = load_texture('Sprites/RedCircle.png'),
                                 z = -0.1,
                                 parent = camera.ui,
                                 visible = False)
        self.RedCircle2 = Entity(model = 'quad',
                                 texture = load_texture('Sprites/RedCircle.png'),
                                 z = -0.1,
                                 parent = camera.ui,
                                 visible = False)
        self.RedArrow1 = Entity(model = 'quad',
                                 texture = load_texture('Sprites/RedArrow.png'),
                                 z = -0.1,
                                 parent = camera.ui,
                                 visible = False)
        self.RedArrow2 = Entity(model = 'quad',
                                 texture = load_texture('Sprites/RedArrow.png'),
                                 z = -0.1,
                                 parent = camera.ui,
                                 visible = False)
        self.WaitingForCodeBlocks = False
        self.FirstTutorial = True
        self.SecondTutorial = False
        self.ThirdTutorial = False
        self.FourthTutorial = False
        self.FifthTutorial = False
        self.IsSpeaking = False
        self.SecretTutorial = False
        self.SecretObtained = False

    def update(self):
        if not self.visible:
            self.Dialogue.visible = False
            return
        else:
            self.Dialogue.visible = True
            self.IsSpeaking = True
        
        if self.FirstTutorial:
            if self.AdvanceDialogue == 0:
                self.Dialogue.text = "Hello, I am TutorialGuy. \n Press Spacebar to continue."
                self.scale = (0.4, 0.15)
                self.position = (0, -0.2)
                self.Dialogue.position = (-0.175, -0.175)
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
                self.Dialogue.text = ""
                self.visible = False
                self.IsSpeaking = False
                self.WaitingForCodeBlocks = True
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
                self.RedCircle1.visible = True
                self.RedCircle1.scale = (1.2, 0.5)
                self.RedCircle1.position = (-0.3, 0.2)
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
                self.RedCircle2.visible = True
                self.RedCircle2.position = (-0.1, 0.1)
                self.RedCircle2.scale = (0.15, 0.15)
                self.RedArrow1.visible = True
                self.RedArrow1.position = (-0.2, 0.2)
                self.RedArrow1.scale = (0.15, 0.15)
                self.RedArrow2.visible = True
                self.RedArrow2.position = (0, 0.2)
                self.RedArrow2.scale = (0.15, 0.15)
                self.RedArrow2.rotation_z = 180
            elif self.AdvanceDialogue == 20:
                self.Dialogue.text = "Always remember to place CodeBlocks over the top\nof the block to the left of it and let\nit snap."
                self.RedCircle1.visible = False
                self.RedCircle2.visible = False
                self.RedArrow1.visible = False
                self.RedArrow2.visible = False
            elif self.AdvanceDialogue == 21:
                self.Dialogue.text = "Once you're done, press Q to toggle executing\nthe snippets."
            elif self.AdvanceDialogue == 22:
                self.Dialogue.text = "You can also press K to toggle the menu if you\nwant."
            elif self.AdvanceDialogue == 23:
                self.Dialogue.text = "I will meet you at the top of this ledge when\nyou're done."
            elif self.AdvanceDialogue == 24:
                self.Dialogue.text = ""
                self.visible = False
                TutorialEntity.position = (19.5, 7.5)
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
                TutorialEntity.position = (33, 1.5)
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
                TutorialEntity.position = (58, 1.5)
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
                TutorialEntity.position = (58, 17.5)
                self.IsSpeaking = False
        elif self.FifthTutorial:
            if self.AdvanceDialogue == 0:
                self.Dialogue.text = "Great job!"
            elif self.AdvanceDialogue == 1:
                self.Dialogue.text = "You have completed the Tutorial!"
            elif self.AdvanceDialogue == 2:
                self.Dialogue.text = "I have a secret for those who pay attention.\nReturn to the first room..."
            elif self.AdvanceDialogue == 3:
                self.Dialogue.text = "Remember, you can press P while in the CodeBlocks\nmenu to open the CodeBlocks guide if you need help."
            elif self.AdvanceDialogue == 4:
                self.Dialogue.text = ""
                self.AdvanceDialogue = 0
                self.visible = False
                self.FifthTutorial = False
                self.SecretTutorial = True
                TutorialEntity.position = (5.5, 3.5)
                self.IsSpeaking = False
        elif self.SecretTutorial:
            if self.AdvanceDialogue == 0:
                self.Dialogue.text = "For those who pay attention..."
            elif self.AdvanceDialogue == 1:
                self.Dialogue.text = "...the forbidden one is yours."
            elif self.AdvanceDialogue == 2:
                self.Dialogue.text = ""
                self.AdvanceDialogue = 0
                self.visible = False
                self.SecretTutorial  = False
                TutorialEntity.enabled = False
                self.IsSpeaking = False
                self.SecretObtained = True


    def input(self, key):
        if key == 'k' and self.WaitingForCodeBlocks:
            self.visible = True
            self.AdvanceDialogue += 1
            self.WaitingForCodeBlocks = False
        
        if not self.visible:
            return
        
        if key == 'space' and not self.WaitingForCodeBlocks:
            self.AdvanceDialogue += 1
    
TutorialGuy = Tutorial()