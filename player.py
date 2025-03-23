import pygame
from os import path

dialogue_active = False
dt = 0

class Player(pygame.sprite.Sprite) :
    def __init__(self) :
        super().__init__()
        self.image = pygame.image.load(path.join("data/sprites", "Th10Momiji.png")).convert_alpha()
        #self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.rect = self.image.get_rect()
        self.collision_rect = self.image.get_rect()
        self.pos = pygame.Vector2(self.rect.w / 2, self.rect.h / 2)
        self.initial_pos = self.pos
        self.speed = 320

    def player_input(self) :
        if dialogue_active:  # Prevent movement when in dialogue
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.pos.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.pos.y += self.speed * dt
        if keys[pygame.K_LEFT]:
            self.pos.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.pos.x += self.speed * dt

    def collide_solid_group(self, solids) :
        return (pygame.sprite.spritecollide(self, solids, False, collided = separate_collision_rect))

    def update_rect(self) :
        self.initial_pos = pygame.Vector2(self.rect.center)
        self.rect.center = self.pos
        self.collision_rect.center = self.pos

    def update(self) :
        self.update_rect()
        self.player_input()

def separate_collision_rect(sprite_a, sprite_b) :
    return sprite_a.collision_rect.colliderect(sprite_b.collision_rect)
