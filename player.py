import pygame
from os import path
from classes2 import Bullet

dialogue_active = False
dt = 0
bullets = pygame.sprite.Group()

class Player(pygame.sprite.Sprite) :
    def __init__(self, shmup=False, vectorpos=pygame.Vector2(0, 0)) :
        super().__init__()
        if (not shmup) :
            self.image = pygame.image.load(path.join("data/sprites", "crusader01.png")).convert_alpha()
        else :
            self.image = pygame.image.load(path.join("data/sprites", "urgurg.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.collision_rect = self.image.get_rect()
        self.pos = vectorpos
        self.initial_pos = self.pos.copy()
        self.speed = 320
        self.shoot_cooldown = 0
        self.isshmup = shmup

    def player_input(self) :
        if dialogue_active:  # Prevent movement when in dialogue
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.image = pygame.image.load(path.join("data/sprites", "backviewcrusader01.png")).convert_alpha()
            self.pos.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.image = pygame.image.load(path.join("data/sprites", "crusader01.png")).convert_alpha()
            self.pos.y += self.speed * dt
        if keys[pygame.K_LEFT]:
            self.image = pygame.image.load(path.join("data/sprites", "sideviewcrusader2.png")).convert_alpha()
            self.pos.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.image = pygame.image.load(path.join("data/sprites", "sideviewcrusader.png")).convert_alpha()
            self.pos.x += self.speed * dt

        if (self.isshmup) :
            if keys[pygame.K_w] and self.shoot_cooldown == 0:
                self.shoot()

            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1  # Countdown to next shot

    def collide_solid_group(self, solids) :
        return (pygame.sprite.spritecollide(self, solids, False, collided = separate_collision_rect))

    def update_rect(self) :
        self.initial_pos = pygame.Vector2(self.rect.center)
        self.rect.center = self.pos
        self.collision_rect.center = self.pos

    def update(self) :
        self.update_rect()
        self.player_input()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        self.shoot_cooldown = 10  # Adjust shooting speed

def separate_collision_rect(sprite_a, sprite_b) :
    return sprite_a.collision_rect.colliderect(sprite_b.collision_rect)
