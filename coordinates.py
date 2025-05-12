import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Display UI Design")

# Load your UI design
ui_design = pygame.image.load('optionsmenu.png')  # Replace with your actual file name
ui_design = pygame.transform.scale(ui_design, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Display the UI design image
    screen.blit(ui_design, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")  # This shows the coordinates of the click

    pygame.display.update()

pygame.quit()
sys.exit()
