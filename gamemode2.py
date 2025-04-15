import pygame
import player, classes2
from classes2 import Enemy
import random
from sys import exit
from os import path

def gamemode_shmup(level):
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
    boss_spawned = False

    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()
            # pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE :
                    pause = not pause

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if player_shmup.sprite.shoot_cooldown == 0 :
                player_shmup.sprite.shoot(enemy_group)
            if player_shmup.sprite.shoot_cooldown > 0:
                player_shmup.sprite.shoot_cooldown -= 1  # Countdown to next shot

        if (not pause) :
            screen.fill("orange")

            enemy_group.update()
            enemy_bullets.update()
            player_shmup.update()
            player.bullets.update()

            if not player_shmup.sprite.invincible and not player_shmup.sprite.is_dead:
                if pygame.sprite.spritecollide(player_shmup.sprite, enemy_bullets, True):
                    if not player_shmup.sprite.is_dead:
                        player_shmup.sprite.die()

            if level == 1 and not boss_spawned :
                boss = classes2.BossEnemy(378, 100, enemy_bullets)
                enemy_group.add(boss)
                boss_spawned = True

            if level == 1 and boss_spawned :
                if boss.killed :
                    return "won"

            if player_shmup.sprite.is_dead:
                player_shmup.sprite.respawn_timer -= 1

                if player_shmup.sprite.respawn_timer <= 0:
                    if player_shmup.sprite.lives > 0:
                        # Respawn player
                        player_shmup.sprite.rect.center = (screen.get_width() // 2, screen.get_height() * 0.9)
                        player_shmup.sprite.is_dead = False
                    else:
                        return "lost"


            for enemy in enemy_group:
                if isinstance(enemy, classes2.BossEnemy):
                    pygame.draw.rect(screen, "black", (256, 20, 244, 20))  # background
                    bar_width = int(240 * (enemy.hp / enemy.max_hp))
                    pygame.draw.rect(screen, "red", (258, 22, bar_width, 16))

            lives_text = font.render(f"Lives: {player_shmup.sprite.lives}", True, "white")
            screen.blit(lives_text, (10, 10))


            """

            enemy_spawn_timer += 1
            if enemy_spawn_timer > 100:  # Spawn every ~100 frames
                new_enemy = Enemy(random.randint(50, 700), -40, 4, playerimage, move_pattern=random.choice(["straight", "zigzag"]), bullet_pattern=random.choice(["straight", "spread", "circle"]), bullet_group=enemy_bullets)
                enemy_group.add(new_enemy)
                enemy_spawn_timer = 0  # Reset timer

            """
            for bullet in player.bullets:
                enemy_hit = pygame.sprite.spritecollide(bullet, enemy_group, False)
                for enemy in enemy_hit:
                    if hasattr(enemy, 'damage'):
                        enemy.damage(10)  # deal 10 damage
                    else:
                        enemy.kill()
                    bullet.kill()

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
