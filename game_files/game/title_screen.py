# title_screen.py
# 
# Contains title class for the game's Title screen
# Can go to: game_world state, options state

from game.state import State
from game.elements import Button
from game.game_world import Game_World
from game.sub_states import Options

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        # initialise buttons
        self.continue_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.28, self.game.GAME_H * 0.48),
                                0.035, "CONTINUE", 10, (0,0,0), (128,128,128))
        self.newgame_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.28, self.game.GAME_H * 0.56),
                                0.035, "NEW GAME", 10, (0,0,0), (128,128,128))
        self.options_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.28, self.game.GAME_H * 0.64),
                                0.035, "OPTIONS", 10, (0,0,0), (128,128,128))
        self.quit_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.28, self.game.GAME_H * 0.72),
                                0.035, "QUIT", 10, (0,0,0), (128,128,128))
        self.yes_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.45, self.game.GAME_H * 0.68),
                                0.035, "YES", 8, (255,255,255), (128,128,128))
        self.no_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.55, self.game.GAME_H * 0.68),
                                0.035, "NO", 8, (255,255,255), (128,128,128))
        # initialise cursor for selection (the cursor is invisible, only its pos is important)
        self.index = 0 # 0 for continue, 1 for new, 2 for options, 3 for quit
        self.index2 = 0 # 0 for yes, 1 for no
        self.cursor_pos_x = self.game.GAME_W * 0.28 + self.index2 * 0.1 # should be the same as the button x pos
        self.cursor_pos_y = self.game.GAME_H * 0.5 + self.index * 0.06# should be the same as the button y pos 
        self.cursor_pos = (self.cursor_pos_x, self.cursor_pos_y)
        #for the warning message
        self.show_message = False

    def update(self, delta_time, actions): #put title screen features here
        if actions["click"]: 
            if self.continue_button.is_clicked():
                new_state = Game_World(self.game)
                new_state.enter_state()
            if self.newgame_button.is_clicked():
                self.show_message = True
                self.cursor_pos_x = self.game.GAME_W * 0.45
                self.cursor_pos_y = self.game.GAME_H * 0.68
            if self.options_button.is_clicked():
                new_state = Options(self.game)
                new_state.enter_state()
            if self.quit_button.is_clicked():
                self.game.running = False
                self.game.playing = False
            if self.show_message:
                if self.yes_button.is_clicked():
                    self.index2 = 0
                    self.show_message = False
                    #TODO implement something to reset the level progress
                    new_state = Game_World(self.game)
                    new_state.enter_state()
                if self.no_button.is_clicked():
                    self.index2 = 0
                    self.show_message = False

        self.game.reset_keys()

    def render(self, display):
        self.game.draw_image(display, "title_screen_background.png", (240,135), 0.3)
        self.game.draw_text(display, "DN1010", (0,0,0), self.game.GAME_W/3.5, self.game.GAME_H * 0.35, 30)
        # buttons
        self.continue_button.print()
        self.continue_button.change_colour()
        self.newgame_button.print()
        self.newgame_button.change_colour()
        self.options_button.print()
        self.options_button.change_colour()
        self.quit_button.print()
        self.quit_button.change_colour()
        # warning message when starting a new game
        if self.show_message:
            self.game.draw_image(display, "title_screen_message_box.png", (240,135), 0.15)
            self.game.draw_text(display, "WARNING!", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.30, 10)
            self.game.draw_text(display, "This will reset your progress.", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.44, 8)
            self.game.draw_text(display, "Continue?", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.50, 8)
            self.yes_button.print()
            self.yes_button.change_colour()
            self.no_button.print()
            self.no_button.change_colour()