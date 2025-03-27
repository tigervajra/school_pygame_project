import pygame
import player, classes2
from classes2 import Enemy
import random
from sys import exit
from os import path

def gamemode_shmup():
    screen = pygame.display.set_mode((756, 1008))
    pygame.display.set_caption("hawk tuah")

    test_font = pygame.font.Font(None, 50)
    text_display = test_font.render("PAUSE", False, "black")
    text_rect = text_display.get_rect(topleft = (0, 0))

    clock = pygame.time.Clock()

    player_shmup = pygame.sprite.GroupSingle()
    player_shmup.add(player.Player(True, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 1.2)))

    playerimage = pygame.image.load(path.join("data/sprites", "tewi.png")).convert_alpha()

    enemy_group = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    pause = False
    enemy_spawn_timer = 0

    while True:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()
            # pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE :
                    pause = not pause

        if (not pause) :
            screen.fill("orange")

            enemy_spawn_timer += 1
            if enemy_spawn_timer > 100:  # Spawn every ~100 frames
                new_enemy = Enemy(random.randint(50, 700), -40, 4, playerimage, move_pattern=random.choice(["straight", "zigzag"]), bullet_pattern=random.choice(["straight", "spread", "circle"]), bullet_group=enemy_bullets)
                enemy_group.add(new_enemy)
                enemy_spawn_timer = 0  # Reset timer

            enemy_group.update()
            enemy_bullets.update()
            player_shmup.update()
            player.bullets.update()

            # Check if player bullets hit enemies
            for bullet in player.bullets:
                enemy_hit = pygame.sprite.spritecollide(bullet, enemy_group, True)
                if enemy_hit:
                    bullet.kill()

            # Check if enemy bullets hit the player
            if pygame.sprite.spritecollide(player_shmup.sprite, enemy_bullets, True):
               print("Player hit!")  # You can replace this with a game-over screen

            enemy_group.draw(screen)
            enemy_bullets.draw(screen)

            # draw the player
            player_shmup.draw(screen)
            player.bullets.draw(screen)

        elif pause :
            pygame.draw.rect(screen, "white", text_rect)
            screen.blit(text_display, text_rect)

        pygame.display.flip()
        player.dt = clock.tick(60) / 1000
