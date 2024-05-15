# game_world.py
#
# the main state that runs the game, generates the map and objects etc.
# can go to pause state

from game.state import State
from game.sub_states import Pause_champ, Transition
#TODO make separate file for player and NPC classes

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.play_transition = True
        self.levels = {}

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
        self.game.draw_text(display, "GAME STATE", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2, 30)

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