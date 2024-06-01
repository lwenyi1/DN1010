"""sprites.py, handles all sprite related matters and has classes needed for game characters

Contains:
 - the All_sprites class
 - the spritesheet class
 - the character parent class
 - the player class
 - the NPC class
"""
import pygame

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
    def __init__(self, game):
        super().__init__()
        self.half_game_w = game.GAME_W / 2
        self.half_game_h = game.GAME_H / 2
        self.offset = pygame.math.Vector2()

        self.ground_surf = pygame.image.load('game_assets/sprites/test_ground.png')
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
    
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

#TODO update the player sprite to use a sprite sheet and add in animation
class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('game_assets/sprites/test_player.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = game.speed * 3
    
    def update(self, actions):
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
        self.rect.center += self.direction * self.speed

#TODO add in the NPC class
'''
class Hint_NPC(pygame.sprite.Sprite):
    def __init__(self,pos, group):
        super().__init__(group):

class Task_NPC(pygame.sprite.Sprite):
'''