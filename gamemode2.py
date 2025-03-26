import pygame
import player, classes2
from sys import exit

def gamemode_shmup():
    screen = pygame.display.set_mode((756, 1008))
    pygame.display.set_caption("hawk tuah")

    test_font = pygame.font.Font(None, 50)
    text_display = test_font.render("PAUSE", False, "black")
    text_rect = text_display.get_rect(topleft = (0, 0))

    clock = pygame.time.Clock()

    player_shmup = pygame.sprite.GroupSingle()
    player_shmup.add(player.Player(True, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 1.2)))

    pause = False

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

            player_shmup.update()
            player.bullets.update()

            # draw the player
            player_shmup.draw(screen)
            player.bullets.draw(screen)

        elif pause :
            pygame.draw.rect(screen, "white", text_rect)
            screen.blit(text_display, text_rect)

        pygame.display.flip()
        player.dt = clock.tick(60) / 1000
