import pygame
import sys
from ui_coordinates import MAIN_MENU_BUTTONS, OPTIONS_MENU_BUTTONS, PORTAL_EXIT

def menu() :
	pygame.init()

	# Load and play background music
	pygame.mixer.music.load("game1.mp3")
	pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
	pygame.mixer.music.play(-1)  # -1 means loop forever

	# Screen setup
	WIDTH, HEIGHT = 960, 540
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Cyber Crusade")

	# Load Backgrounds
	background_main = pygame.image.load("data/sprites/GUI/background.png")  # Main menu background
	background_options = pygame.image.load("data/sprites/GUI/titlessbackground.png")  # Options menu background

	# Load Main Menu UI States
	ui_default = pygame.image.load("data/sprites/GUI/buttonsUI.png")
	ui_start_hover = pygame.image.load("data/sprites/GUI/hovernewgame.png")
	ui_options_hover = pygame.image.load("data/sprites/GUI/hoveroptions.png")
	ui_load_hover = pygame.image.load("data/sprites/GUI/hoverloadgame.png")

	# Load Options Menu UI States
	options_ui = pygame.image.load("data/sprites/GUI/optionsmenu.png")
	options_keybinds_hover = pygame.image.load("data/sprites/GUI/keybindshover.png")
	options_audio_hover = pygame.image.load("data/sprites/GUI/AudioHover.png")
	options_graphics_hover = pygame.image.load("data/sprites/GUI/graphicshover.png")
	options_back_hover = pygame.image.load("data/sprites/GUI/backhover.png")

	# Use imported coordinates
	buttons_main = MAIN_MENU_BUTTONS
	buttons_options = OPTIONS_MENU_BUTTONS
	portal_exit = PORTAL_EXIT

	# Game states
	in_options = False
	current_ui = ui_default  # Default UI state

	# Main loop
	clock = pygame.time.Clock()
	running = True
	while running:
	    clock.tick(60)  # Limit to 60 FPS

	    # Set correct background
	    if in_options:
		    screen.blit(background_options, (0, 0))
	    else:
		    screen.blit(background_main, (0, 0))

	    mouse_pos = pygame.mouse.get_pos()

	    # UI hover logic
	    if not in_options:
		    if buttons_main["start"].collidepoint(mouse_pos):
		        current_ui = ui_start_hover
		    elif buttons_main["load"].collidepoint(mouse_pos):
		        current_ui = ui_load_hover
		    elif buttons_main["options"].collidepoint(mouse_pos):
		        current_ui = ui_options_hover
		    else:
		        current_ui = ui_default  # Reset if not hovering
	    else:
		    if buttons_options["keybinds"].collidepoint(mouse_pos):
		        current_ui = options_keybinds_hover
		    elif buttons_options["audio"].collidepoint(mouse_pos):
		        current_ui = options_audio_hover
		    elif buttons_options["graphics"].collidepoint(mouse_pos):
		        current_ui = options_graphics_hover
		    elif buttons_options["back"].collidepoint(mouse_pos):
		        current_ui = options_back_hover
		    else:
		        current_ui = options_ui  # Default options UI

	    # Draw the UI
	    screen.blit(current_ui, (0, 0))

	    # Event Handling
	    for event in pygame.event.get():
		    if event.type == pygame.QUIT:
		        running = False
		    if event.type == pygame.MOUSEBUTTONDOWN:
		        # Handle button clicks
		        if not in_options:
		            if buttons_main["start"].collidepoint(mouse_pos):
		                return
		            elif buttons_main["load"].collidepoint(mouse_pos):
		                print("Load button clicked!")
		            elif buttons_main["options"].collidepoint(mouse_pos):
		                print("Options button clicked!")
		                in_options = True  # Switch to options menu
		            elif portal_exit.collidepoint(mouse_pos):
		                running = False  # Exit game
		        else:
		            if buttons_options["keybinds"].collidepoint(mouse_pos):
		                print("Keybinds button clicked!")
		            elif buttons_options["audio"].collidepoint(mouse_pos):
		                print("Audio button clicked!")
		            elif buttons_options["graphics"].collidepoint(mouse_pos):
		                print("Graphics button clicked!")
		            elif buttons_options["back"].collidepoint(mouse_pos):
		                print("Back button clicked!")
		                in_options = False  # Go back to main menu

	    pygame.display.update()

	pygame.quit()
	sys.exit()
