"""sprites.py, handles all sprite related matters and has classes needed for game characters

Contains:
 - the All_sprites class
 - the spritesheet class
 - the character parent class
 - the player class
 - the NPC class
"""
import pygame, time
import pytmx
from game.tasks import *
from game.elements import *

# Start of NOTE: The following classes are for testing and interation purposes only,
#                they will not be in the final game

class Tree(pygame.sprite.Sprite):
    """Class used to generate trees on the map in the milestone 1 TPOC"""
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('game_assets/sprites/test_tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)      


# End of NOTE

class All_sprites(pygame.sprite.Group):
    def __init__(self, game): # TODO: take in level map when working on levels
        super().__init__()
        self.half_game_w = game.GAME_W / 2
        self.half_game_h = game.GAME_H / 2
        self.offset = pygame.math.Vector2()

        # Load the TMX map
        tmx_data = pytmx.load_pygame('game_assets/maps/logic_links.tmx')
        
        # Create a surface to render the map
        map_width = tmx_data.width * tmx_data.tilewidth
        map_height = tmx_data.height * tmx_data.tileheight
        self.ground_surf = pygame.Surface((map_width, map_height))

        # Draw the map onto the surface
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        self.ground_surf.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

        new_width = int(map_width * 2)
        new_height = int(map_height * 2)
        self.ground_surf = pygame.transform.scale(self.ground_surf, (new_width, new_height))

        # Handle collision layer
        self.collision_rects = []
        for obj in tmx_data.objects:
            if obj.name == "Collision":
                rect = pygame.Rect(obj.x * 2, obj.y * 2, obj.width * 2, obj.height * 2)
                self.collision_rects.append(rect)

        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
    
    
    def check_collision(self, rect):
        """Check if a given rectangle collides with any collision rectangles."""
        for collision_rect in self.collision_rects:
            if rect.colliderect(collision_rect):
                return True
        return False
    
    def draw(self, player, display):
        # camera logic
        self.offset.x = player.rect.centerx - self.half_game_w
        self.offset.y = player.rect.centery - self.half_game_h
        
        # Start of NOTE: The following lines are for testing purposes only
        display.fill('#71ddee')

        # ground 
        ground_offset = self.ground_rect.topleft - self.offset
        display.blit(self.ground_surf,ground_offset)

        # active elements
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display.blit(sprite.image,offset_pos)

        # End of NOTE

#TODO Maybe update the player sprite to use a sprite sheet and add in animation
class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('game_assets/sprites/player.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = game.speed * 3
        self.original_rect = self.rect.copy()  # Store the original position
    
    def update_player(self, actions):
        original_rect = self.rect.copy()  # Store the original position

        # Update direction based on actions
        if actions['up']:
            self.direction.y = -1
        elif actions['down']:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if actions['left']:
            self.direction.x = -1
        elif actions['right']:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        # Move player and check for collision
        self.rect.center += self.direction * self.speed
        
        # Check collision with map objects using the game's sprite group
        if self.game.all_sprites.check_collision(self.rect):
            self.rect = original_rect  # Revert to original position if collision detected

    

#TODO add in the NPC class

class Hint_NPC(pygame.sprite.Sprite):
    """Class for all 'Hint' NPCs

    Attributes
    ----------
    group:
        The sprite group the NPC will be added to.
    name:
        The name of the NPC. 
    file_name:
        The name of the NPC's image file.
    pos:
        The position of the NPC.
    self.image:
        The image of the sprite. Should be stored in the path game_assets/sprites and following the naming
        convention of <NPC name>.png.
    self.radius:
        The radius in which the player can stand in for them to be considered in range.
    self.show_chat:
        Keep track of whether the chat box has been shown and whether it should be shown.  
        0 for not shown, do not show. 1 for show. 2 for shown, do not show.
    
    Methods
    -------
    player_in_range(self, player_pos):
        Checks if the player is in range of the NPC, returns True if so. Called by the update method.
    update(self, actions, player_pos):
        Updates the NPC based on player actions and position. Called as part of the sprite group update call.
    chatters(self):
        Displays the chat box for the NPC.
    
    """
    def __init__(self, game, group, name, file_name, pos, texts):
        super().__init__(group)
        self.image = pygame.image.load(f'game_assets/sprites/{file_name}.png').convert_alpha() # TODO: change this line if upgrading to using spritesheets
        self.rect = self.image.get_rect(center = pos)
        self.chat_box = Chatbox(game, name, texts)
        self.show_chat = [0]
        self.radius = 20
    
    def player_in_range(self, player_pos):
        """Checks if the player is in range."""
        if (self.rect.left - self.radius <= player_pos[0] <= self.rect.right + self.radius and 
            self.rect.top - self.radius <= player_pos[1] <= self.rect.bottom + self.radius):
            return True
        else:
            return False

    def update(self, actions, player_pos):
        """Updates the NPC when the sprite group update is called."""
        if actions['action1'] and self.player_in_range(player_pos):
            self.show_chat[0] = 1
        if not self.player_in_range(player_pos):
            self.chat_box.chat_reset()
            self.show_chat[0] = 0
        if self.show_chat[0] == 1:
            self.chat_box.update(actions, self.show_chat)
    
    def chatters(self):
        """Displays the chat box for the NPC"""
        if self.show_chat[0] == 1:
            self.chat_box.print()

class Task_NPC(pygame.sprite.Sprite):
    """Class for all 'Task' NPCs

    When creating an instance of a task NPC, remember to define its task_state after initialisation, e.g.
    test_task_NPC = Test_Task_NPC(...)
    test_task_NPC.task_state = Test_Task_state(game, self.text_pointer)

    Attributes
    ----------
    group:
        The sprite group the NPC will be added to.
    name:
        The name of the NPC. Important to keep this alligned with the image name.
    pos:
        The position of the NPC.
    start_texts:
        The text to show when the player first talks to the NPC.
    correct_texts:
        The text to show when the player successfully finishes the task.
    wrong_texts:
        The text to show when the player fails the task.
    
    task_state:
        Instance of the task object for this NPC.
    self.image:
        The image of the sprite. Should be stored in the path game_assets/sprites and following the naming
        convention of <NPC name>.png.
    self.radius:
        The radius in which the player can stand in for them to be considered in range.
    self.show_chat:
        Keep track of whether the chat box has been shown and whether it should be shown.  
        0 for not shown, do not show. 1 for show. 2 for shown, do not show.
    self.update_chat:
        Bool to check when it is time to update the dialog based on task completion.
        Set to true when the task state is added to the stack.
    
    Methods
    -------
    player_in_range(self, player_pos):
        Checks if the player is in range of the NPC, returns True if so. Called by the update method.
    update(self, actions, player_pos):
        Updates the NPC based on player actions and position. Called as part of the sprite group update call.
    chatters(self):
        Displays the chat box for the NPC.
    
    """
    task_state = None
    
    def __init__(self, game, group, name, file_name, pos, start_texts, correct_texts, wrong_texts):
        super().__init__(group)
        self.image = pygame.image.load(f'game_assets/sprites/{file_name}.png').convert_alpha() # TODO: change this line if upgrading to using spritesheets
        self.rect = self.image.get_rect(center = pos)
        self.game = game
        self.name = name

        self.texts = (start_texts, correct_texts, wrong_texts)
        self.text_pointer = [0] 
        # The above can also be used to check if the task has been successfully completed (i.e. when it contains 1)

        self.chat_box = Chatbox(game, name, self.texts[self.text_pointer[0]])
        self.show_chat = [0]
        self.update_chat = False # Flag used to check when it is time to update the dialog

        self.radius = 20
    
    def player_in_range(self, player_pos):
        """Checks if the player is in range."""
        if (self.rect.left - self.radius <= player_pos[0] <= self.rect.right + self.radius and 
            self.rect.top - self.radius <= player_pos[1] <= self.rect.bottom + self.radius):
            return True
        else:
            return False

    def update(self, actions, player_pos):
        """Updates the NPC when the sprite group update is called."""
        if actions['action1'] and self.player_in_range(player_pos):
            self.show_chat[0] = 1
        if actions['action2'] and self.player_in_range(player_pos) and self.text_pointer[0] == 0 and self.show_chat[0] == 2: 
            self.task_state.enter_state() 
            self.chat_box.counter = 0
            self.update_chat = True
            #self.show_chat[0] = 1

        if not self.player_in_range(player_pos):
            if self.text_pointer[0] == 2:
                self.text_pointer[0] = 0
                self.chat_box.texts = self.texts[self.text_pointer[0]]
                self.chat_box.chat_reset()
                self.show_chat[0] = 0
            else:
                self.show_chat[0] = 0
                self.chat_box.chat_reset()
        if self.player_in_range(player_pos) and self.update_chat and (not self.text_pointer[0] == 0): # TODO fix the show yes or no at end thing
            self.chat_box.texts = self.texts[self.text_pointer[0]]
            if self.chat_box.counter == 0:
                self.chat_box.chat_reset()
            self.show_chat[0] = 1
            self.update_chat = False

        if self.show_chat[0] == 1:
            self.chat_box.update(actions, self.show_chat) # This will change show_start_chat[0] to 2 once done.

    
    def chatters(self):
        """Displays the chat box for the NPC"""
        if self.show_chat[0] == 1:
            self.chat_box.print()