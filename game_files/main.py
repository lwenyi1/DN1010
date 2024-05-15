import pygame, os, time
from pygame.locals import *

# Load game states, starting from title screen
from game.title_screen import Title

class Game():
        def __init__(self):
            pygame.init()
            pygame.display.set_caption('DN1010')
            #screen
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 1600, 900
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT), pygame.RESIZABLE)

            #game
            self.GAME_W,self.GAME_H = 480, 270
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
                # window events
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == VIDEORESIZE:
                    self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.w, event.h
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
                
                # controls
                # keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.actions['esc'] = True
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
                
                # mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.actions['click'] = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.actions['click'] = False

        def get_mouse_pos(self):
            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos() 
            mouse_pos_x = (mouse_pos_x / self.SCREEN_WIDTH * self.GAME_W)
            mouse_pos_y = (mouse_pos_y / self.SCREEN_HEIGHT * self.GAME_H)
            return (mouse_pos_x, mouse_pos_y)

        # some important functions
        def update(self):
            self.state_stack[-1].update(self.dt,self.actions)

        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
            pygame.display.flip()

        def get_dt(self):
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

        def load_assets(self):
            # Create pointers to directories 
            self.assets_dir = os.path.join("game_assets")
            self.image_dir = os.path.join(self.assets_dir, "images")
            self.sprite_dir = os.path.join(self.assets_dir, "sprites")
            self.font_dir = os.path.join(self.assets_dir, "font")

        def draw_text(self, surface, text, color, x, y, font_size):
            self.font= pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), font_size) #TODO Update font file name here
            text_surface = self.font.render(text, True, color)
            #text_surface.set_colorkey((0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)
        
        def draw_image(self, surface, image_name, pos, size):
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
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)

        def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False

# Entry point
if __name__ == "__main__":
    dn1010 = Game()
    while dn1010.running:
        dn1010.game_loop()