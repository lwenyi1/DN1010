"""game_world.py, the main state that runs the game, generates the map and objects etc.

Contains:
 - Game_world class
 - Level classes
Links to:
 - pause state
"""

from game.state import State
from game.sub_states import Pause_champ, Transition
from game.sprites import *
from game.elements import *
from random import randint # NOTE for testing

class Game_World(State):
    """A class used to manage the actual game world state for the game, i.e. the one
    the player plays in."""
    def __init__(self, game):
        State.__init__(self, game)

        # Level management:
        self.levels = {"test": Test_Level(game)} 
        self.current_level = self.levels['test']

    def update(self, delta_time, actions): 
        if actions['esc']:
            new_state = Pause_champ(self.game)
            new_state.enter_state()
        self.current_level.update(delta_time, actions)
    
    def render(self, display):
        self.current_level.render(display)

"""Level classes:"""

class Test_Level():
    """A class used to create an instance of the test level.

    Location: Test map
    Programming concepts: Nil
    Hint NPCs: test_hint_NPC
    Task NPC: test_task_NPC

    ### NOTE:
    Uses temporary map, player and NPC designs. Used for milestone 1 to show proof of concept.

    At the time this class was made, there the map and characters etc were all imported from image files. 
    This level may not work once the sprite logic etc is changed to handle tmx files and maybe spritesheets.
    """
    def __init__(self, game):
        self.game = game
        self.play_transition = True
        self.all_sprites = All_sprites(game)
        self.player = Player(game, (900,500), self.all_sprites)

        # TODO: When working on levels, all these lesser being instances should be shoved into its level class.
        self.test_hint_NPC_texts = ("Hi there. I am a test hint NPC.", "I give no hints, except...", "Vim is the best text editor.")
        self.test_hint_NPC = Hint_NPC(game, self.all_sprites, "test_hint_NPC", (600,350), self.test_hint_NPC_texts)
        self.test_task_NPC_texts = ("Hi there. I am a test task NPC.", "I just need one thing from you...", "Are the developers handsome?")
        self.test_hint_NPC_correct = ("Yes it's true!", "They are quite good looking!")
        self.test_hint_NPC_wrong = ("Hmm you seem to be wrong...", "Walk away and come back to try again...")
        self.test_task_NPC = Task_NPC(game, self.all_sprites, "test_task_NPC", (800,350), self.test_task_NPC_texts, self.test_hint_NPC_correct, self.test_hint_NPC_wrong)
        self.test_task_NPC.task_state = Test_Task_State(game, self.test_task_NPC.text_pointer)

        # Start of NOTE: for testing
        for i in range(20):
            random_x = randint(1000,2000)
            random_y = randint(1000,2000)
            Tree((random_x, random_y), self.all_sprites)
        self.show_chat = [1]        
        
        self.welcome_chatbox = Chatbox(game, "Developer No. 2",
                               ("Welcome to Catopia.","Use W, A, S and D to move around.","Press E while standing near NPCs to talk tothem."))
        # End of NOTE.

    def update(self, delta_time, actions):
        if self.play_transition:
            trans_state = Transition(self.game, "Entering Catopia...")
            trans_state.enter_state()
            self.play_transition = False

        self.all_sprites.update(actions, (self.player.rect.center)) # for NPCs.
        self.player.update_player(actions) # player has its own update function.
        self.welcome_chatbox.update(actions, self.show_chat)
    
    def render(self, display):
        self.all_sprites.draw(self.player, display)
        self.test_hint_NPC.chatters()
        self.test_task_NPC.chatters()
        if self.show_chat[0] == 1:
            self.welcome_chatbox.print()
