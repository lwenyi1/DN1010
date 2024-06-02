"""elements.py, module with the miscellaneous elements the game needs

 Contains: 
 - the button class for title screen and pause screen to use
 - the chat box class for the game_world to use
"""

class Button():
    """A class used to represent a simple button with text inside and an image background.

    Methods
    -------
    print(self)
        Draws the button to the screen.
    is_clicked(self)
        Checks if the button has been clicked. Returns True if so.
    change_colour(self)
        Checks if the mouse is hovering over the button and updates
        the colour and size of the button for visual effect if so.
    """
    def __init__(self, game, image_name, pos, size, text, font_size, normal_colour, hovering_colour):
        self.game = game
        self.image_name = image_name
        self.size = size
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.normal_colour = normal_colour
        self.hovering_colour = hovering_colour
        self.colour = self.normal_colour
        self.text = text
        self.normal_font_size = font_size
        self.use_font_size = self.normal_font_size
        self.rect = self.game.draw_image(self.game.screen, self.image_name, (self.x_pos, self.y_pos), self.size)

    def print(self):
        self.rect = self.game.draw_image(self.game.game_canvas, self.image_name, (self.x_pos, self.y_pos), self.size)
        self.game.draw_text(self.game.game_canvas, self.text, self.colour, self.x_pos, self.y_pos, self.use_font_size)

    def is_clicked(self):
        mouse_pos = self.game.get_mouse_pos()
        if self.rect.left <= mouse_pos[0] <= self.rect.right and self.rect.top <= mouse_pos[1] <= self.rect.bottom: 
            return True
        else:
            return False
    
    def change_colour(self):
        mouse_pos = self.game.get_mouse_pos()
        if self.rect.left <= mouse_pos[0] <= self.rect.right and self.rect.top <= mouse_pos[1] <= self.rect.bottom: 
            self.colour = self.hovering_colour
            self.use_font_size = self.normal_font_size + 1
        else:
            self.colour = self.normal_colour
            self.use_font_size = self.normal_font_size

#TODO add in the chat box class
class Chatbox():
    """A class used to create dialog boxes to communicate to the player
    
    Takes in a tuple with the texts to be displayed. If only one set of
    text to be displayed, remember to use ("<text here>",) so it is still a tuple.
    
    Requires an external variable show_chat to be made to control whether the chat box will be
    shown or not. show_chat should be a list with one integer element. See Hint and Task sprites
    for elaboration on usage of this variable.  
    
    Each box can fit 4 lines and each line can fit 43 characters.
    This gives a total of 172 characters in one box.
    There is no newline character so to print a new line just leave white spaces
    until the current line reaches 43 characters lmaooo

    Methods
    -------
    chat_reset(self):
        Resets the chatbox to initial state.
    update(self, actions, show_chat):
        Updates the text being displayed when the action2 key is pressed.  
         show_chat is used to update variables in parent functions to stop showing the box. Must be of type list to enable updating by reference.
    print(self):
        Draws the chatbox and text to the screen with scrolling text animation.
    """
    def __init__(self, game, name, texts):
        self.game = game
        self.name = name # The name of the character talking.
        self.texts = texts # Array of text to print.
        self.active_text = 0
        self.text = self.texts[self.active_text]
        self.text_len = len(self.text)
        self.delay = int(2 / game.speed)
        self.counter = 0
        self.done = False # Boolean to check if the message is done printing.
        
        # Position variables. Done at initiation to reduce repetitive calculations in rendering.
        self.line_x_pos = game.GAME_W * 0.05 # For lines of text.
        self.line_x_pos_2 = game.GAME_W * 0.01 # For character name.
        self.line_x_pos_3 = game.GAME_W * 0.60 # For Press F to continue.

        self.line_y_pos_1 = game.GAME_H * 0.71 # For line 1 of text.
        self.line_y_pos_2 = game.GAME_H * 0.76 # For line 2 of text.
        self.line_y_pos_3 = game.GAME_H * 0.81 # For line 3 of text.
        self.line_y_pos_4 = game.GAME_H * 0.86 # For line 4 of text.
        self.line_y_pos_5 = game.GAME_H * 0.59 # For character name.
        self.line_y_pos_6 = game.GAME_H * 0.95 # For Press F to continue.
    
    def chat_reset(self):
        self.active_text = 0 # Reset active text
        self.text = self.texts[self.active_text] # Update text to be shown.
        self.text_len = len(self.text) # Update length of text.
        self.counter = 0 # Reset counter.

    def update(self, actions, show_chat):
        if actions['action2'] and self.done:
            if self.active_text < len(self.texts) - 1:
                self.active_text += 1
                self.text = self.texts[self.active_text] # Update text to be shown.
                self.text_len = len(self.text) # Update length of text.
                self.counter = 0 # Reset counter.
                self.done = False # Change done back to False.
            else:
                self.chat_reset()
                show_chat[0] = 2 # Used to exit the chat box.

    def print(self):
        self.game.draw_image(self.game.game_canvas, "chatbox.png", (self.game.GAME_W / 2, self.game.GAME_H / 2), 1)
        self.game.draw_chat_text(self.game.game_canvas, self.name, (0,0,0), self.line_x_pos_2, self.line_y_pos_5, 22)
        self.game.draw_chat_text(self.game.game_canvas, "Press F to continue", (128,128,128), self.line_x_pos_3, self.line_y_pos_6, 15) 

        if self.counter < self.delay * self.text_len:
            self.counter += 1
        else:
            self.done = True

        if self.counter//self.delay <= 43: # Draw one line
            self.game.draw_chat_text(self.game.game_canvas, self.text[0:self.counter//self.delay],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_1, 20)
        elif self.counter//self.delay <= 86: # Draw two lines
            self.game.draw_chat_text(self.game.game_canvas, self.text[0:43],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_1, 20)
            self.game.draw_chat_text(self.game.game_canvas, self.text[43:self.counter//self.delay],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_2, 20)
        elif self.counter//self.delay <= 129: # Draw three lines
            self.game.draw_chat_text(self.game.game_canvas, self.text[0:43],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_1, 20)
            self.game.draw_chat_text(self.game.game_canvas, self.text[43:86],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_2, 20)
            self.game.draw_chat_text(self.game.game_canvas, self.text[86:self.counter//self.delay],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_3, 20)
        elif self.counter//self.delay <= 172: # Draw four lines
            self.game.draw_chat_text(self.game.game_canvas, self.text[0:43],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_1, 20)
            self.game.draw_chat_text(self.game.game_canvas, self.text[43:86],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_2, 20)
            self.game.draw_chat_text(self.game.game_canvas, self.text[86:129],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_3, 20)
            self.game.draw_chat_text(self.game.game_canvas, self.text[129:self.counter//self.delay],
                                     (0,0,0), self.line_x_pos, self.line_y_pos_4, 20)