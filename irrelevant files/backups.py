# Tutorial SCRAPPED, kept here in case i need it

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
Tutorial5 = False
Tutorial6 = False
Tutorial7 = False
SecretTutorial1 = False
SecretTutorial2 = False
SecretTutorial3 = False
SecretTutorial4 = False
SecretTutorial5 = False
SecretTutorial6 = False
TutorialGuyConvo1 = Conversation()        # Creates an object handled by an Ursina prefab to handle conversations
TutorialGuyConvo1.enabled = False       # Conversation template appears on game start otherwise
TutorialGuyConvo2 = Conversation()        # Theoretically I should only need 1 conversation object for all conversations, but in practice that's not how it works
TutorialGuyConvo2.enabled = False
TutorialGuyConvo3 = Conversation()
TutorialGuyConvo3.enabled = False
TutorialGuyConvo4 = Conversation()
TutorialGuyConvo4.enabled = False
TutorialGuyConvo5 = Conversation()
TutorialGuyConvo5.enabled = False
TutorialGuyConvo6 = Conversation()
TutorialGuyConvo6.enabled = False
TutorialGuyConvo7 = Conversation()
TutorialGuyConvo7.enabled = False
TutorialGuySecret1 = Conversation()
TutorialGuySecret1.enabled = False
TutorialGuySecret2 = Conversation()
TutorialGuySecret2.enabled = False
TutorialGuySecret3 = Conversation()
TutorialGuySecret3.enabled = False
TutorialGuySecret4 = Conversation()
TutorialGuySecret4.enabled = False
TutorialGuySecret5 = Conversation()
TutorialGuySecret5.enabled = False
TutorialGuySecret6 = Conversation()
TutorialGuySecret6.enabled = False
TutorialGuy = Entity(position = (15, 1.5, 0),
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
                         This means in the future you may have to move the "make" block as well,
                         otherwise the "block" block would snap to the other side of the "make" block.
                         For now you shouldn't have to move it.
                         Once you're done, press Q to start running your CodeBlocks.
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
                         Now on to the next room.
                      ''')
TutorialGuy5 = dedent('''
                         Uh oh!
                         You can't unlock some of these doors!
                         You may have to come back later if you want to unlock horizontal doors.
                         You will need some way for the key to be moved or placed downward.
                         Additionally, some doors are different colours,
                         this means they need different coloured keys to open them.
                         For now you can only move to the right.
                         Be sure to pick up that CodeBlock on your way through as well!
                      ''')
TutorialGuy6 = dedent('''
                         Another horizontal door!
                         The only path is up.
                         See those CodeBlocks on the ground?
                         Rather than moving the "block" and "key" blocks around,
                         try making a new snippet with these CodeBlocks to move on to the next screen.
                         You can use the pre-generated snippet as a template if you want.
                      ''')
TutorialGuy7 = dedent('''
                         Great job!
                         I'll leave you alone now.
                         Goodbye!
                      ''')
SecretTutorialGuy1 = dedent('''
                         hello joposephy here i died so rip josepj
                         "emit" -faraz
                             * forsake
                                 Wohaohh how codl you do that to mee>??
                                 im died again
                             * wish me how powerful positions 
                                 no i dont
                                 i ned a mask
                                 hello everyone who is playing this game this is the token logger speaking
                                 your ip address is mine and the next 10 years of your lives will be controlled by me
                                 goodbye, have fun
                                     * stupid
                                         keep it concise, buddy.
                                             * what
                           ''')
SecretTutorialGuy2 = dedent('''
                         in memoty of joseph 2007 - 200207
                         he didnt die he lived too long
                         i died 2019 time
                             * so sad
                                 no
                             * nanananeanmmaae
                                 what
                                     * nenaeenoannemaen
                                         i dont understand
                                             * nenoaneoaeanoena
                                                 ok
                           ''')
SecretTutorialGuy3 = dedent('''
                          who are you
                             * who are you
                                 who are you
                                     * who are you
                                         who are you
                                             * jospep
                             * i am you
                                 no you arent liar
                                     * yes i am
                                         no
                                             * yes
                                                 kills you
                                     * no i arent
                                         good
                             * i am not you
                                 corrrect
                                     * incorrect
                                         for truth
                           ''')
SecretTutorialGuy4 = dedent('''
                         this is just like among us
                         you can move
                           ''')
SecretTutorialGuy5 = dedent('''
                         dialoguetest
                           ''')
SecretTutorialGuy6 = dedent('''
                         secret dialogue number 6
                             * secret dialogue number 6 choice 1
                                 secret dialogue number 7 response 1
                             * secret dialogue number 6 choice 2
                                 i hate you
                           ''')


# scrapped jospep, too laggy
ExistingJospeps = []    
class  FireableJospep(Entity):
    def __init__(self, modification, **kwargs):
        super().__init__(position = (player.x + 1, player.y),
                         playercollision = False,
                         visible = True,
                         model = 'quad',
                         collider = 'box',
                         scale = (1, 1, 1),
                         gravity = 1)
        self.spawntime = time.time()
        self.ignore_list = [self,]
        self.traverse_target = scene
        self.grounded = False
        self.jumping = False
        self.speed = 6
        self.air_time = 0
        self.velocity = player.velocity
        self.JospepAnimation = CreateAnimation('jospep')
        self.JospepAnimation.parent = self
        if modification == 'shoot':
            self.shooting = True
            self.shootspeed = 10
        
    def update(self):
            print('Updating:', self)
            print('Type:', type(self))
            print('Has ignore_list:', hasattr(self, 'ignore_list'))
            if not boxcast(
                self.position,
                direction=Vec3(self.velocity,self.scale_y / 2,0),
                distance=abs(self.scale_x / 2),
                ignore=self.ignore_list,
                traverse_target=self.traverse_target,
                thickness=(self.scale_x*.99, self.scale_y*.9)).hit:
                    
                    self.x += time.dt * self.speed * self.velocity
            else:
                self.velocity * -1
            
            ray_origin = self.world_position - Vec3(0, self.scale_y / 2, 0)
            ray = raycast(ray_origin + Vec3(0,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)
            left_ray = raycast(ray_origin + Vec3(-self.scale_x*.49,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)
            right_ray = raycast(ray_origin + Vec3(self.scale_x*.49,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)

            if any((ray.hit, left_ray.hit, right_ray.hit)):
                if not self.grounded:
                    self.air_time = 0
                    self.grounded = True
                self.y = max((r.world_point.y for r in (ray, left_ray, right_ray) if r.hit)) + self.scale_y / 2
            else:
                self.grounded = False

            if not self.grounded and not self.jumping:
                self.y -= min(self.air_time * self.gravity, ray.distance - 0.1)
                self.air_time += time.dt * 4 * self.gravity

            hit_above = raycast(self.world_position+Vec3(0,(self.scale_y/2)-0.5,0), self.up, distance=0.8, traverse_target=self.traverse_target, ignore=self.ignore_list)
            hit_above_left = raycast(self.world_position+Vec3(-self.scale_x*.49,(self.scale_y/2)-0.5,0), self.up, distance=0.8, traverse_target=self.traverse_target, ignore=self.ignore_list)
            hit_above_right = raycast(self.world_position+Vec3(self.scale_x*.49,(self.scale_y/2)-0.5,0), self.up, distance=0.8, traverse_target=self.traverse_target, ignore=self.ignore_list)
            if any((hit_above.hit, hit_above_left.hit, hit_above_right.hit)):
                if self.jumping:
                    self.y = min(min((r.world_point.y for r in (hit_above, hit_above_left, hit_above_right) if r.hit)), self.y)
                    self.jumping = False
                    self.air_time = 0
                if hasattr(self, 'y_animator'):
                    self.y_animator.kill()

            hit_forward = raycast(self.world_position+Vec3(self.scale_x / 2, 0, 0), direction=(self.velocity, 0, 0), distance=3, traverse_target = self.traverse_target, ignore=self.ignore_list)
            hit_forward_top = raycast(self.world_position+Vec3(self.scale_x / 2, self.scale_y*.49, 0), direction=(self.velocity, 0, 0), distance=3, traverse_target = self.traverse_target, ignore=self.ignore_list)
            hit_forward_bottom = raycast(self.world_position+Vec3(self.scale_x / 2, -self.scale_y*.49, 0), direction=(self.velocity, 0, 0), distance=3, traverse_target = self.traverse_target, ignore=self.ignore_list)
            if any((hit_forward.hit, hit_forward_top.hit, hit_forward_bottom.hit)):
                self.jump()
        
    def jump(self):
        if not self.grounded:
            return
        
        self.jumping = True
        self.grounded = False

        self.target_y = self.y + 10
        self.animate_y(self.target_y, 0.5, resolution = 30, curve = curve.out_expo)
        self._start_fall_sequence = invoke(self.start_fall, delay = 0.5)

    def start_fall(self):
        self.jumping = False

jospepcooldown = time.time()
def CreateJospep(modification):
    global jospepcooldown
#    if time.time() - jospepcooldown < 4:
 #       return
    Jospep = FireableJospep(modification)
    ExistingJospeps.append(Jospep)
    return Jospep

def SetupGame():
    # Camera Settings
    global height, ratio, width
    camera.orthographic = True
    camera.position = (30/2,8)
    camera.fov = 16
    height = camera.fov
    ratio = window.aspect_ratio
    width = height * ratio
    # Input Func Variables
    global CodeBlocksEnabled, blocksdragging, blockoffset, titlescreen, executing
    CodeBlocksEnabled = False
    blocksdragging = False
    blockoffset = Vec3(0, 0, 0)
    titlescreen = True
    executing = False
    # Update Loop Variables
    global chunkx, chunky, incrementchunk, keynotification, keycolour, keymessage
    chunkx = 0
    chunky = 0
    incrementchunk = False
    keynotification = False
    keycolour = 'regular'
    keymessage = Text(text = f'You need a {keycolour} key to open this door', origin = (0, -3), scale = 2, visible = False, parent = camera.ui)
    # Camera Edges Reset
    global CameraEdges, cright_edge, ctop_edge, cleft_edge, cbottom_edge
    CameraEdges = GetCameraEdges()      # Finds edges of the starting screen
    cright_edge, ctop_edge, cleft_edge, cbottom_edge = CameraEdges
    # Recreate Title Screen
    TitleSplash = Text(text = 'Dugnon', origin = (0,0), scale = 3, position = (0, 0.3))
    StartButton = Button(text = 'Start', scale = (0.2, 0.1), position = (0, -0.1), color = color.red)
    StartButton.on_click = start
    ReturnButton = Button(text='Return to Title', scale = (0.2, 0.1), position = (0, -0.1), color = color.azure)
    ReturnButton.enabled = False
    ReturnButton.on_click = reset
    # Setup other files
    SetupCodeBlocks()
    SetupCodeFunctions()
    SetupLevel()
    SetupPlayer()

    def SetupLevel():
     global quad, level_parent, ItemCodeBlocks, loaded_chunks, LockedDoors, UpLevels, DownLevels, LeftLevels, RightLevels
     quad = load_model('quad', use_deepcopy=True)
     level_parent = Entity(model=Mesh(vertices=[], uvs=[]), texture='white_cube')
     ItemCodeBlocks = []
     loaded_chunks = {}
     LockedDoors = []
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


def SetupCodeBlocks():
    global code_blocks, last_block, cbpep, cbpe, CurrentCodeBlocks
    code_blocks = []
    last_block = None
    cbpep = Entity(scale = 1, position = (0, 0), parent = camera.ui)
    cbpe = Entity(scale = 1, position = (0, 0), parent = cbpep)
    CurrentCodeBlocks = []