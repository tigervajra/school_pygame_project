import pygame
from os import path
from classes2 import Bullet, HomingBullet

dialogue_active = False
dt = 0
bullets = pygame.sprite.Group()

class Player(pygame.sprite.Sprite) :
    def __init__(self, shmup=False, vectorpos=pygame.Vector2(0, 0)) :
        super().__init__()
        #if (not shmup) :
        self.image = pygame.image.load(path.join("data/sprites", "crusader01.png")).convert_alpha()
        #else :
        #    self.image = pygame.image.load(path.join("data/sprites", "urgurg.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.collision_rect = self.image.get_rect()
        self.pos = vectorpos
        self.initial_pos = self.pos.copy()
        self.speed = 320
        self.shoot_cooldown = 0
        self.isshmup = shmup
        self.shoot_homing = True
        self.frozen = False

        self.lives = 3
        self.is_dead = False
        self.respawn_timer = 0
        self.invincible = False

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

    """

        if (self.isshmup) :
            if keys[pygame.K_w] and self.shoot_cooldown == 0:
                self.shoot()

            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1  # Countdown to next shot
    """

    def collide_solid_group(self, solids) :
        return (pygame.sprite.spritecollide(self, solids, False, collided = separate_collision_rect))

    def update_rect(self) :
        self.initial_pos = pygame.Vector2(self.rect.center)
        self.rect.center = self.pos
        self.collision_rect.center = self.pos

    def update(self) :
        if getattr(self, 'frozen', False):
            return  # skip movement

        if self.is_dead:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0 and self.lives > 0:
                self.respawn()
            return

        self.update_rect()
        self.player_input()

        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False

        if self.invincible:
            if (self.invincibility_timer // 5) % 2 == 0:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)


    def shoot(self, enemy_group=None):
        if self.shoot_homing:  # Add this toggle if needed
            bullet = HomingBullet(self.rect.center, enemy_group)
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)

        self.shoot_cooldown = 10  # Adjust shooting speed

    def die(self):
        self.lives -= 1
        self.is_dead = True
        self.respawn_timer = 60  # 1 second at 60 FPS
        self.invincible = True
        self.invincibility_timer = 120  # 2 seconds of blinking

    def respawn(self):
        self.is_dead = False
        self.invincible = True
        self.invincibility_timer = 120

def separate_collision_rect(sprite_a, sprite_b) :
    return sprite_a.collision_rect.colliderect(sprite_b.collision_rect)
