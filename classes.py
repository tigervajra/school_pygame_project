import pygame

class Tile(pygame.sprite.Sprite) :
    def __init__(self, image, pos, is_solid) :
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = pygame.Vector2(pos))
        if (is_solid) :
            self.collision_rect = self.image.get_rect(topleft = pygame.Vector2(pos))
        else :
            self.collision_rect = pygame.Rect(0, 0, 0, 0)
