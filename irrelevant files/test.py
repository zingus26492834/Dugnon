from ursina import *
from ursina.prefabs.conversation import *
app = Ursina()

variables = Empty(
    evil=0,
    chaos=0,
    bar_mission_solved=False,
)
conversation = Conversation(variables_object=variables)

convo = dedent('''
I'm looking for my sister. Can you help me find her, please? I haven't seen her in days! Who know what could've happened!?
I'm worried. Will you help me?
    * Yes, of course. This can be a dangerous city.
        Oh no! Do you think something happened to her?
        What should I do?!
            * She's probably fine. She can handle herself.
                You're right. I'm still worried though.
                    * Don't worry, I'll look for her.
            * Maybe. (stats.chaos += 1)
                Help me look for her, please! *runs off*
    * I'm sorry, but I don't have time right now. (evil += 1)
        A true friend wouldn't say that.
    * I know where she is! (if bar_mission_solved)
        Really? Where?
            * I saw her on a ship by the docks, it looked like they were ready to set off.
                Thank you! *runs off*
''')
conversation.start_conversation(convo)
amongus = dedent('''
                 * moglus
                 ''')



def input(key):
    if key == 'space':
        print(variables.evil)
    if key == 'k':
        conversation.start_conversation(amongus)

Sprite('shore', z=1)
app.run()

