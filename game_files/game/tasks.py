"""tasks.py, module with all task classes for the different levels' NPCs 

Contains:
 - parent task class
 - test task class
 - Level 0:
 - Level 1:
 - Level 2:
 - Level 3:
 - level 4:
 - Level 5:
 - Level 6:
 - Level 7:
 - test task class
"""
from game.state import State
from game.sub_states import *

class Task_State(State):
    """The parent class for all task game states.
    
    Each child class should define its own task_update() function based on what the task is. 

    Attributes:
    ----------
    self.play_transition: 
        Bool to keep track of whether to play the opening transition.
    self.play_end_transition: 
        Bool to check whether to play the ending transition.
    self.finish_task: 
        Bool to check whether to exit the task state. Set to true once end transition is played.

    Methods:
    -------
    
    """
    def __init__(self, game, result):
        State.__init__(self, game)
        self.game = game
        # Some flags to handle transitions showing and the ending of the task
        self.play_transition = True # Plays transition once upon opening then gets set to False
        self.play_end_transition = False # Gets set to true upon completion of task
        self.finish_task = False # Gets set to true upon end transition finishing
        self.result = result

    def task_update(self, delta_time, actions):
        pass

    def update(self, delta_time, actions): 
        if self.play_transition:
            trans_state = Transition(self.game, "Beginning task...")
            trans_state.enter_state()
            self.play_transition = False
        if self.play_end_transition:
            trans_state = Transition(self.game, "Returning to Catopia...")
            trans_state.enter_state()
            self.play_end_transition = False
            self.finish_task = True # Once the transition finishes we can exit the task
        if self.finish_task and self.game.state_stack[-1] == self: 
            # This state check makes sure we do not pop the transition state before it is played.
            self.play_transition = True # to reset.
            self.finish_task = False # to reset.
            self.exit_state()
        if actions['esc']:
            new_state = Pause_champ(self.game)
            new_state.enter_state()
        self.task_update(delta_time, actions)

        self.game.reset_keys()
    
    def task_render(self, display):
        pass

    def render(self, display):
        # TODO: Replace these once the actual design for the task state is complete
        display.fill((0,0,0))
        self.task_render(display)

"""Level 0 tasks:"""

class Freshman_Task(Task_State):
    """Choose the correct function which prints the book's words"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Luke_Task(Task_State):
    """Choose the correct function to read in something and print out a response"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Desmon_Task(Task_State):
    """Choose the correct line of code which type casts a float into a double"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

"""Level 1 tasks"""

class MacOS_Task(Task_State):
    """Choose the correct function which reads in the number of apples 
    in basket A and B and returns the total sum"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Coffee_Task(Task_State):
    """Choose the correct function which returns the amount of coffee a mug holds"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Student_Task(Task_State):
    """Choose the correct function which calculates the quadratic formula"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

"""Level 2 tasks"""

class Jamie_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Windows_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Punk_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

"""Level 3 tasks"""

class Bensen_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Fisher_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Notepad_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

"""Level 4 tasks"""

class Linux_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Tian_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Sane_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

"""Level 5 tasks"""

class Json_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Rascal_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Chad_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

"""Level 6 tasks"""

class Mike_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Vim_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Robert_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

"""Level 7 tasks"""

class Leet_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

class Dev_Task(Task_State):
    """TODO"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)

    def task_update(self, delta_time, actions):
        pass

    def task_render(self, display):
        pass

"""Test level tasks:"""

class Test_Task_State(Task_State):
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.yes_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.4, self.game.GAME_H/2),
                                0.07, "YES", 20, (255,255,255), (128,128,128))
        self.no_button = Button(self.game, "title_screen_button.png", (self.game.GAME_W * 0.6, self.game.GAME_H/2),
                                0.07, "NO", 20, (255,255,255), (128,128,128))

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.yes_button.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.no_button.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Are the developers handsome?", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.3, 30)

        self.yes_button.print()
        self.yes_button.change_colour()
        self.no_button.print()
        self.no_button.change_colour()