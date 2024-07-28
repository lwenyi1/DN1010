"""tasks.py, module with all task classes for the different levels' NPCs 

Contains:
 - parent task class
 - Level 0: Freshman_Task, Luke_Task, Desmon_Task
 - Level 1: MacOS_Task, Coffee_Task, Student_Task
 - Level 2:
 - Level 3:
 - level 4:
 - Level 5:
 - Level 6:
 - Level 7:
 - test task class  
 
Tasks are named based on the character they are tagged to
"""
from game.state import State
from game.sub_states import *
from game.elements import *

class Task_State(State):
    """The parent class for all task game states.
    
    Each child class should define its own task_update() function based on what the task is.  
    Initialise buttons in init().  
    Update buttons in task_update().  
    Print and update button colours in task_render().  

    ### Note:
    Each line 40 characters at font size 22 looks good for the question.

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
        self.option_a = Button_2(game, "L0_freshman_a.png", (self.game.GAME_W*1/3, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L0_freshman_b.png", (self.game.GAME_W*2/3, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L0_freshman_c.png", (self.game.GAME_W*1/3, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L0_freshman_d.png", (self.game.GAME_W*2/3, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the program", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "that correctly prints the words", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Luke_Task(Task_State):
    """Choose the correct function to read in something and print out a response"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L0_luke_a.png", (self.game.GAME_W*1/3, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L0_luke_b.png", (self.game.GAME_W*2/3, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L0_luke_c.png", (self.game.GAME_W*1/3, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L0_luke_d.png", (self.game.GAME_W*2/3, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the program that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "can read in words and print a reply", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Desmon_Task(Task_State):
    """Choose the correct line of code which type casts a float into an int"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L0_desmon_a.png", (self.game.GAME_W*1/3, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L0_desmon_b.png", (self.game.GAME_W*2/3, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L0_desmon_c.png", (self.game.GAME_W*1/3, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L0_desmon_d.png", (self.game.GAME_W*2/3, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the lines that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "can correctly typecast from float to int", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

"""Level 1 tasks"""

class MacOS_Task(Task_State):
    """Choose the correct function which reads in the number of apples 
    in basket A and B and returns the total sum"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L1_macOS_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L1_macOS_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L1_macOS_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L1_macOS_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the function that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "returns the sum of apples in A and B", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Coffee_Task(Task_State):
    """Choose the correct function which returns the amount of coffee a mug holds"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L1_coffee_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L1_coffee_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L1_coffee_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L1_coffee_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the function that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "returns the amount of coffee a mug holds", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Student_Task(Task_State):
    """Choose the correct function which calculates the quadratic formula"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L1_student_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L1_student_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L1_student_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L1_student_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the function that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 20)
        self.game.draw_text(display, "returns one of the solutions to a quadratic eqn", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 20)
        self.game.draw_text(display, "Note: sqrt() is part of the math.h library", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.2, 20)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

"""Level 2 tasks"""

class Jamie_Task(Task_State):
    """Check which grade (from A to D) a score out of 100 will get"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L2_jamie_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L2_jamie_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L2_jamie_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L2_jamie_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the function that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 20)
        self.game.draw_text(display, "returns the correct grade based on score", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 20)
        self.game.draw_text(display, "A: 75-100, B: 50-74, C: 25-49, D: 0-24", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.2, 20)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Windows_Task(Task_State):
    """Choose the correct statement to use to check for glitches"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 0.15, "for loop", 22, (255,255,255), (128,128,128))
        self.option_b = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 0.2, "while loop", 22, (255,255,255), (128,128,128))
        self.option_c = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8),  0.2, "switch statement", 22, (255,255,255), (128,128,128))
        self.option_d = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 0.2, "if/else statement", 22, (255,255,255), (128,128,128))

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the statement that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "can be used to find glitches in updates", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Punk_Task(Task_State):
    """Choose the correct statement to check if two conditions to win a gang fight are fulfilled"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L2_punk_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L2_punk_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L2_punk_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L2_punk_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the function that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 20)
        self.game.draw_text(display, "checks if both conditions to win are fulfilled", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 20)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

"""Level 3 tasks"""

class Bensen_Task(Task_State):
    """Choose the function that counts to 69"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L3_bensen_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L3_bensen_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L3_bensen_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L3_bensen_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the function that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "counts to 69", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Fisher_Task(Task_State):
    """Choose the correct statement to use to check for glitches in fish"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L3_fisher_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L3_fisher_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L3_fisher_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L3_fisher_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the statement that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "can be used to check for glitches", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Notepad_Task(Task_State):
    """Choose the correct method to print something indefinitely"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 0.15, "for loop", 22, (255,255,255), (128,128,128))
        self.option_b = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 0.2, "while loop", 22, (255,255,255), (128,128,128))
        self.option_c = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8),  0.2, "recursion", 22, (255,255,255), (128,128,128))
        self.option_d = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 0.2, "if/else statement", 22, (255,255,255), (128,128,128))

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the method that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "can be used to print something indefinitely", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

"""Level 4 tasks"""

class Linux_Task(Task_State):
    """Choose the correct statement that creates a pointer to the memories and dereferences it"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L4_linux_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L4_linux_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L4_linux_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L4_linux_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the statements that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 20)
        self.game.draw_text(display, "creates a pointer to the memories then", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 20)
        self.game.draw_text(display, "dereferences it.", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.2, 20)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Tian_Task(Task_State):
    """Choose the correct output for the following code"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.7), 0.15, "Option A: 100", 22, (255,255,255), (128,128,128))
        self.option_b = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.7), 0.2, "Option B: 200", 22, (255,255,255), (128,128,128))
        self.option_c = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8),  0.2, "Option C: 400", 22, (255,255,255), (128,128,128))
        self.option_d = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 0.2, "Option D: 300", 22, (255,255,255), (128,128,128))

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the correct amount", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "of water for the given code:", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)
        self.game.draw_image(display, "L4_tian.png", (self.game.GAME_W/2, self.game.GAME_H * 0.4), 2)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Sane_Task(Task_State):
    """Choose the correct statement to print the location's address"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L4_sane_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L4_sane_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L4_sane_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L4_sane_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the code that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "prints the address of the int COM1", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

"""Level 5 tasks"""

class Json_Task(Task_State):
    """Choose the correct line to initialise an array to store deaths in 10 years"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 0.15, "int death_list[10];", 22, (255,255,255), (128,128,128))
        self.option_b = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 0.2, "int death_list(10);", 22, (255,255,255), (128,128,128))
        self.option_c = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8),  0.2, "int *death_list[10];", 22, (255,255,255), (128,128,128))
        self.option_d = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 0.2, "int death_list<10>;", 22, (255,255,255), (128,128,128))

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the statement that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "can be used to check for glitches", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Rascal_Task(Task_State):
    """Choose the correct line that accesses the first element of the list"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 0.15, "numbers[1];", 22, (255,255,255), (128,128,128))
        self.option_b = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 0.2, "numbers[0];", 22, (255,255,255), (128,128,128))
        self.option_c = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8),  0.2, "numbers(1);", 22, (255,255,255), (128,128,128))
        self.option_d = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 0.2, "*numbers[1];", 22, (255,255,255), (128,128,128))

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the line that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "accesses the first element of the list", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Chad_Task(Task_State):
    """Choose the correct function to store the number of glitches"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L5_chad_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L5_chad_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L5_chad_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L5_chad_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the program that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "can be used to store glitch counts", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

"""Level 6 tasks"""

class Mike_Task(Task_State):
    """Choose the correct statement to use to check for glitches"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L6_mike_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L6_mike_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L6_mike_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L6_mike_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the lines that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "allocate memory based on energy level", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Vim_Task(Task_State):
    """Choose the correct statement to use to check for glitches"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 0.15, "malloc", 22, (255,255,255), (128,128,128))
        self.option_b = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 0.2, "calloc", 22, (255,255,255), (128,128,128))
        self.option_c = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8),  0.2, "realloc", 22, (255,255,255), (128,128,128))
        self.option_d = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 0.2, "free", 22, (255,255,255), (128,128,128))

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the function that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "can be used to reallocate memory", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Robert_Task(Task_State):
    """Choose the correct statement to use to check for glitches"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 0.15, "dealloc", 22, (255,255,255), (128,128,128))
        self.option_b = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 0.2, "calloc", 22, (255,255,255), (128,128,128))
        self.option_c = Button(game, "title_screen_button.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8),  0.2, "realloc", 22, (255,255,255), (128,128,128))
        self.option_d = Button(game, "title_screen_button.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 0.2, "free", 22, (255,255,255), (128,128,128))

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the statement that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "can be used to deallocate memory", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

"""Level 7 tasks"""

class Leet_Task(Task_State):
    """Choose the correct statement to use to check for glitches"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L7_leet_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L7_leet_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L7_leet_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L7_leet_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the lines that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "creates a struct with leetcoder details", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

class Dev_Task(Task_State):
    """Choose the correct statement to use to check for glitches"""
    def __init__(self, game, result):
        Task_State.__init__(self, game, result)
        self.option_a = Button_2(game, "L7_dev_a.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.4), 1)
        self.option_b = Button_2(game, "L7_dev_b.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.4), 1)
        self.option_c = Button_2(game, "L7_dev_c.png", (self.game.GAME_W*1/4, self.game.GAME_H*0.8), 1)
        self.option_d = Button_2(game, "L7_dev_d.png", (self.game.GAME_W*3/4, self.game.GAME_H*0.8), 1)

    def task_update(self, delta_time, actions):
        if actions["click"]:
            if self.option_a.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_b.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True
            if self.option_c.is_clicked():
                self.result[0] = 1
                self.play_end_transition = True
            if self.option_d.is_clicked():
                self.result[0] = 2
                self.play_end_transition = True

    def task_render(self, display):
        self.game.draw_text(display, "Select the option with the lines that", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.1, 22)
        self.game.draw_text(display, "will cause the program to crash", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.15, 22)

        self.option_a.print()
        self.option_a.change_colour()
        self.option_b.print()
        self.option_b.change_colour()
        self.option_c.print()
        self.option_c.change_colour()
        self.option_d.print()
        self.option_d.change_colour()

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
        self.game.draw_text(display, "1234512345123451234512345123451234512345", (255,255,255), self.game.GAME_W/2, self.game.GAME_H * 0.3, 22)

        self.yes_button.print()
        self.yes_button.change_colour()
        self.no_button.print()
        self.no_button.change_colour()