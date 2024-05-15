# elements.py
#
# Contains: 
# - the button class for title screen and pause screen to use
# - the chat box class for the game_world to use

class Button():
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
#class Chatbox():
