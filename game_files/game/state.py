"""state.py, parent class for other states to inherit from

Contains:
 - parent state class
"""

class State():
    """A class representing a game state.
    
    Methods
    -------
    update(self)
        Updates the game based on player inputs. To be defined by child classes.
    render(self)
        Renders the screen based on the game state. To be defined by child classes.
    enter_state(self)
        Add the state to the state_stack in the main game loop.
    exit_state(self)
        Pop the state from the state_stack in the main game loop.
    """

    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, delta_time, actions):
        pass
    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()