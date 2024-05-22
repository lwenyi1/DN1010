"""game_world.py, the main state that runs the game, generates the map and objects etc.

Contains:
 - Game_world class
Links to:
 - pause state
"""

from game.state import State
from game.sub_states import Pause_champ, Transition
from game.sprites import *
from random import randint # NOTE for testing

class Game_World(State):
    """A class used to manage the actual game world state for the game, i.e. the one
    the player plays in."""
    def __init__(self, game):
        State.__init__(self, game)
        self.play_transition = True
        self.levels = {}

        # NOTE: for testing
        self.all_sprites = All_sprites(game)
        self.player = Player((640, 360), self.all_sprites)
        for i in range(20):
            random_x = randint(1000,2000)
            random_y = randint(1000,2000)
            Tree((random_x, random_y), self.all_sprites)

    def update(self, delta_time, actions): 
        if self.play_transition:
            trans_state = Transition(self.game)
            trans_state.enter_state()
            self.play_transition = False
        if actions['esc']:
            new_state = Pause_champ(self.game)
            new_state.enter_state()
        
        self.all_sprites.update(actions) # for testing

        #self.game.reset_keys()
    
    def render(self, display):
        #display.fill((255,255,255))
        #self.game.draw_text(display, "GAME STATE", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2, 30)

        self.all_sprites.draw(self.player, display)

    def import_map():
        pass
    
    def render_map():
        pass
    
    def import_NPCs():
        pass

    def render_NPCs():
        pass
'''
class Combat(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.play_transition = True

    def update(self, delta_time, actions): 
        if self.play_transition:
            trans_state = Transition(self.game)
            trans_state.enter_state()
            self.play_transition = False
        if actions['esc']:
            new_state = Pause_champ(self.game)
            new_state.enter_state()

        self.game.reset_keys()
    
    def render(self, display):
        display.fill((255,255,255))
        self.game.draw_text(display, "COMBAT STATE", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2, 30)
'''