import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Small rectangle bullet
        self.image.fill("yellow")  # Bullet color
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = -10  # Moves upwards

    def update(self):
        self.rect.y += self.speed  # Move bullet up
        if self.rect.bottom < 0:  # Remove if it goes off-screen
            self.kill()
