""" main.py, the main game program that calls every other module.

Contains the game class.
"""

import pygame, os, time
from pygame.locals import *

# Load game states, starting from title screen
from game.title_screen import Title

class Game():
    """A class used to manage the overall game logic and flow of the game.
    
    Attributes
    ----------
    GAME_W: int
        The size of the game canvas' width, fixed at 960.
    GAME_H: int
        The size of the game canvas' height, fixed at 540.
    game_canvas: pygame.Surface
        The canvas of the game, used as the 'display' when blitting.
        Has an aspect ratio of 16:9.
    running: bool
        Set to true for the program to continue running.
    playing: bool
        Set to true for the game loop to continue running.
    actions: dict
        List of actions and respective booleans representing if that action's key
        is pressed or not.
    dt: float
        The delta time between game cycles.
    prev_time: float
        Used along with time.time to find dt.
    state_stack: list
        A list used as the stack containing the different game states.
    
    Methods
    -------
    game_loop(self)
        Manages the overall game loop by calling get_dt(), get_events(), update() and render()
        while self.playing is True.
    get_events(self)
        Manages the events using pygame.event.get(). Updates the booleans in actions[] accordingly
        when the user presses a key.
    get_mouse_pos(self)
        A helper function to get the coordinates of the mouse position. Returns those coordinates.
    update(self)
        Calls the update methods from the different game state classes, i.e. updates game based
        off player input.
    render(self)
        Calls the render methods from the different game state classes, i.e. renders the respective
        screens for the different states.
    get_dt(self)
        Calculates the delta time and returns it.
    draw_text(self, surface as pygame.surface, colour as RGB tuple or hex, x coords, y coords, 
            font size)
        Prints text to the screen with the desired parameters.
    draw_image(self, surface as pygame.surface, image file name as str, pos as (x,y) tuple,
            size as float (multiplied to original image size))
        Prints image to the screen with the desired parameters. Returns the image rect.
    load_states(self)
        Loads the game states.
    reset_keys(self)
        Resets all the values in actions[] to False.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('DN1010')

        # Config

        # Screen
        self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 1600, 900
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT), pygame.RESIZABLE)

        # Game
        self.GAME_W,self.GAME_H = 960, 540
        self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
        self.running, self.playing = True, True
        self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, 
                        "action2" : False, "click": False, "esc": False }
        self.dt, self.prev_time = 0, 0 # self.dt is the time between cycles
        self.state_stack = []
        self.load_assets()
        self.load_states()

    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            # Window events
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == VIDEORESIZE:
                self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.w, event.h
                self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
            
            # Controls
            # Keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    self.actions['esc'] = True
                    time.sleep(0.2) # prevents debouncing issues when using esc in the game state
                if event.key == pygame.K_a:
                    self.actions['left'] = True
                if event.key == pygame.K_d:
                    self.actions['right'] = True
                if event.key == pygame.K_w:
                    self.actions['up'] = True
                if event.key == pygame.K_s:
                    self.actions['down'] = True
                if event.key == pygame.K_e:
                    self.actions['action1'] = True
                if event.key == pygame.K_f:
                    self.actions['action2'] = True    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE: 
                    self.actions['esc'] = False
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['up'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = False
                if event.key == pygame.K_e:
                    self.actions['action1'] = False
                if event.key == pygame.K_f:
                    self.actions['action2'] = False
            
            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.actions['click'] = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.actions['click'] = False

    def get_mouse_pos(self):
        """Get position of mouse and transform it to game canvas coordinates"""
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos() 
        mouse_pos_x = (mouse_pos_x / self.SCREEN_WIDTH * self.GAME_W)
        mouse_pos_y = (mouse_pos_y / self.SCREEN_HEIGHT * self.GAME_H)
        return (mouse_pos_x, mouse_pos_y)

    # Some important functions

    def update(self):
        self.state_stack[-1].update(self.dt,self.actions)

    def render(self):
        """Render current state to the screen"""
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        pygame.display.flip()

    def get_dt(self):
        """Get delta time"""
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def load_assets(self):
        """Create paths to asset directories."""
        self.assets_dir = os.path.join("game_assets")
        self.image_dir = os.path.join(self.assets_dir, "images")
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "font")

    # Some useful functions

    def draw_text(self, surface, text, color, x, y, font_size):
        """Draws given text string to the screen."""
        # NOTE: Change font file name here:
        self.font= pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), font_size)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)
    
    def draw_image(self, surface, image_name, pos, size):
        """Draws given image file to the screen. Returns the image rect."""
        # NOTE: This function makes the developer's life easier but is not optimised. Change if the game lags. 
        image = pygame.image.load(os.path.join(self.image_dir, image_name))
        if size != 1:
            og_width, og_height = image.get_size()
            new_width = og_width * size
            new_height = og_height * size
            resized_image = pygame.transform.scale(image, (new_width, new_height))
        else:
            resized_image = image
        image_rect = resized_image.get_rect(center=(pos[0], pos[1]))
        surface.blit(resized_image, image_rect)
        return image_rect

    
    def load_states(self):
        """load game states"""
        # load the title screen first.
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        """Reset status of keys back to false (unpressed)"""
        # call at the end of game loop in each state to prevent funny input issues
        for action in self.actions:
            self.actions[action] = False

# Entry point
if __name__ == "__main__":
    dn1010 = Game()
    while dn1010.running:
        dn1010.game_loop()