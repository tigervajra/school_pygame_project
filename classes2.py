import pygame
import random
import math

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

class HomingBullet(pygame.sprite.Sprite):
    def __init__(self, pos, target_group, speed=5):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill("cyan")
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.target_group = target_group
        self.velocity = pygame.Vector2(0, -speed)  # Initial straight shot

    def update(self):
        if not self.target_group:
            self.rect.y -= self.speed  # fallback behavior (straight)
            return
        # Find the closest target
        closest_enemy = None
        min_distance = float('inf')

        for enemy in self.target_group:
            dist = pygame.Vector2(enemy.rect.center).distance_to(self.rect.center)
            if dist < min_distance:
                min_distance = dist
                closest_enemy = enemy

        # Update velocity to steer toward target
        if closest_enemy:
            target_pos = pygame.Vector2(closest_enemy.rect.center)
            direction = (target_pos - pygame.Vector2(self.rect.center)).normalize()
            self.velocity = self.velocity.lerp(direction * self.speed, 0.1)

        self.rect.center += self.velocity

        # Kill if offscreen
        if not (0 <= self.rect.x <= 800 and 0 <= self.rect.y <= 1008):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=2, image=None, move_pattern="straight", bullet_pattern="straight", bullet_group=None) :
        super().__init__()
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill("red")

        self.rect = self.image.get_rect(midtop=(x, y))
        self.speed = speed
        self.move_pattern = move_pattern
        self.bullet_pattern = bullet_pattern
        self.direction = random.choice([-1, 1])  # Used for zigzag movement
        self.shoot_timer = 60  # Time between shots
        self.bullet_group = bullet_group

    def update(self):
        if self.move_pattern == "straight":
            self.rect.y += self.speed  # Move downward
        elif self.move_pattern == "zigzag":
            self.rect.y += self.speed
            self.rect.x += self.direction * 2
            if self.rect.left < 0 or self.rect.right > 756:
                self.direction *= -1  # Reverse direction

        # Enemy shooting logic
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot(self.bullet_pattern)
            self.shoot_timer = random.randint(30, 90)  # Reset timer

        # Remove enemy if off screen
        if self.rect.top > 1008:
            self.kill()

    def shoot(self, pattern="straight"):
        if pattern == "straight":
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, 0, 5)
            self.bullet_group.add(enemy_bullet)

        elif pattern == "spread":
            angles = [-30, -15, 0, 15, 30]  # Spread angles
            for angle in angles:
                rad = math.radians(angle)
                dx = math.sin(rad) * 5
                dy = math.cos(rad) * 5
                enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, dx, dy)
                self.bullet_group.add(enemy_bullet)

        elif pattern == "circle":
            for i in range(12):  # 12 bullets in a circle
                angle = (i / 12) * 360
                rad = math.radians(angle)
                dx = math.sin(rad) * 3
                dy = math.cos(rad) * 3
                enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.centery, dx, dy)
                self.bullet_group.add(enemy_bullet)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill("purple")
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.top > 1008 or self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > 756:
            self.kill()

class BossEnemy(Enemy):
    def __init__(self, x, y, bullet_group):
        super().__init__(x, y, speed=2, bullet_group=bullet_group)
        self.image = pygame.Surface((100, 100))
        self.image.fill("darkred")
        self.rect = self.image.get_rect(center=(x, y))
        self.phase = 1
        self.speed = 0.5
        self.hp = 1500
        self.max_hp = 1500
        self.timer = 0
        self.angle = 0  # Used for figure-eight movement
        self.killed = False
    def update(self):
        self.timer += 1
        self.shoot_timer -= 1

        # Phase switch
        if self.hp <= 0 and self.phase == 1:
            self.phase = 2
            self.hp = 1000  # 🔁 New phase HP
            self.max_hp = 1000
            print("Boss entered Phase 2!")

        if self.phase == 1:
            # Figure-eight motion
            self.angle += 0.05 * self.speed
            self.rect.centerx = 378 + int(math.sin(self.angle * 2) * 150)
            self.rect.centery = 100 + int(math.sin(self.angle) * 30)

            if self.shoot_timer <= 0:
                self.shoot("circle")
                self.shoot_timer = 90


        elif self.phase == 2:
            self.rect.center = (378, 100)  # stay centered
            if self.shoot_timer <= 0:
                self.shoot("spread")
                self.shoot_timer = 80

    def damage(self, amount):
        self.hp -= amount
        if self.phase == 2 and self.hp <= 0:
            self.kill()
            self.killed = True
