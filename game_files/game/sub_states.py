
# sub_states.py
#
# Contains:
# - the option page
# - the pause menu
# - the transition screen
# NOTE I dont actually know what options to put yet. To think about it at some point.

from game.state import State
from game.elements import Button

# Options page for the game, does not lead to other states
class Options(State):
    def __init__(self, game):
        State.__init__(self, game)
        # buttons
        self.done_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W/2, self.game.GAME_H * 0.64),
                                0.035, "DONE", 8, (255,255,255), (128,128,128))

    def update(self, delta_time, actions): 
        if actions['esc']:
            self.exit_state()
        if actions['click']:
            if self.done_button.is_clicked():
                self.exit_state()

        self.game.reset_keys()
    
    def render(self, display):
        self.game.draw_image(display, "pause_screen_box.png", (240,135), 0.15)
        self.game.draw_text(display, "OPTIONS", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.32, 12)
        # draw buttons
        self.done_button.print()
        self.done_button.change_colour()

# Pause menu, can go to options state
class Pause_champ(State):
    def __init__(self, game):
        State.__init__(self, game)
        # buttons
        self.save_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W/2, self.game.GAME_H * 0.40),
                                0.035, "SAVE", 8, (255,255,255), (128,128,128))
        self.resume_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W/2, self.game.GAME_H * 0.48),
                                0.035, "RESUME", 8, (255,255,255), (128,128,128))
        self.options_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W/2, self.game.GAME_H * 0.56),
                                0.035, "OPTIONS", 8, (255,255,255), (128,128,128))
        self.home_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W/2, self.game.GAME_H * 0.64),
                                0.035, "HOME", 8, (255,255,255), (128,128,128))

    def update(self, delta_time, actions): 
        if actions['esc']:
            self.exit_state()
        if actions['click']:
            if self.save_button.is_clicked():
                #TODO implement saving mechanism
                print("saving...")
            if self.resume_button.is_clicked():
                self.exit_state()
            if self.options_button.is_clicked():
                new_state = Options(self.game)
                new_state.enter_state()
            if self.home_button.is_clicked():
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop() # pop states until we reach back to the title screen

        self.game.reset_keys()

    def render(self, display):
        self.game.draw_image(display, "pause_screen_box.png", (240,135), 0.15)
        self.game.draw_text(display, "GAME PAUSED", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.32, 12)
        # draw buttons
        self.save_button.print()
        self.save_button.change_colour()
        self.resume_button.print()
        self.resume_button.change_colour()
        self.options_button.print()
        self.options_button.change_colour()
        self.home_button.print()
        self.home_button.change_colour()

class Transition(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.time_passed = 0
    
    def update(self, delta_time, actions):
        self.time_passed += delta_time
        if self.time_passed > 1:
            self.exit_state()
    
    def render(self, display):
        display.fill((0,0,0))
        self.game.draw_text(display, "THIS IS A TRANSITION", (255,255,255), self.game.GAME_W/2, self.game.GAME_H/2, 20)