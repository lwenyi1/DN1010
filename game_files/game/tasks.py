"""tasks.py, module with all task classes for the different levels' NPCs 

Contains:
 - parent task class
 - test task class
 - Level 1:
 - Level 2:
 - Level 3:
 - level 4:
 - Level 5:
 - Level 6:
 - Level 7:
 - Level 8:
"""
from game.state import State
from game.sub_states import *

class Task_State(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.play_transition = True
        self.result = 0
    
    def result_update(self): # TODO: THERE HAS TO BE A BETTER WAY
        print("at update", self.result)
        return self.result

    def task_update(self, delta_time, actions):
        pass

    def update(self, delta_time, actions): 
        if self.play_transition:
            trans_state = Transition(self.game, "Beginning task...")
            trans_state.enter_state()
            self.play_transition = False
        if actions['esc']:
            new_state = Pause_champ(self.game)
            new_state.enter_state()
        self.task_update(delta_time, actions)

        self.game.reset_keys()
    
    def task_render(self, display):
        pass

    def render(self, display):
        # TODO: Replace these once the actual design for the task state is complete
        display.fill((255,255,255))
        self.task_render(display)

class Test_Task_State(Task_State):
    def __init__(self, game):
        Task_State.__init__(self, game)
        self.yes_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.4, self.game.GAME_H/2),
                                0.07, "YES", 20, (0,0,0), (128,128,128))
        self.no_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.6, self.game.GAME_H/2),
                                0.07, "NO", 20, (0,0,0), (128,128,128))

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.yes_button.is_clicked():
                self.result = 1
                print("at click", self.result)
                #trans_state = Transition(self.game, "Entering Catopia...")
                #trans_state.enter_state()
                self.exit_state()
            if self.no_button.is_clicked():
                self.result = 2
                print(self.result)
                #trans_state = Transition(self.game, "Entering Catopia...")
                #trans_state.enter_state()
                self.exit_state()

    def task_render(self, display):
        self.game.draw_text(display, "Are the developers handsome?", (0,0,0), self.game.GAME_W/2, self.game.GAME_H * 0.3, 30)

        self.yes_button.print()
        self.yes_button.change_colour()
        self.no_button.print()
        self.no_button.change_colour()