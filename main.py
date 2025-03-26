import pygame
import classes, player, gamemode2
from pytmx.util_pygame import load_pygame
from os import path
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("hawk tuah")

tmxdata = load_pygame(path.join("data/tmx", "test.tmx"))

clock = pygame.time.Clock()

test_font = pygame.font.Font(None, 50)

player_char = pygame.sprite.GroupSingle()
player_char.add(player.Player(False, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)))

tiles_top = pygame.sprite.Group()
tiles_below = pygame.sprite.Group()

layer_draw_below = tmxdata.get_layer_by_name("draw_below")
layer_draw_ontop = tmxdata.get_layer_by_name("draw_ontop")

npc = None
dialogue_text = None

npc_tile_positions = {}

# map
npc_tile_positions = {}  # Dictionary to store multi-tile NPCs

for x, y, gid in layer_draw_below:
    tile = tmxdata.get_tile_image_by_gid(gid)
    if tile:
        tile_props = tmxdata.get_tile_properties_by_gid(gid)  # Get properties from the tile itself

        is_solid = tile_props.get("solid", False) if tile_props else False  # Read solidity correctly

        if tile_props and "npc" in tile_props:  # Check if tile has "npc" property
            npc_name = tile_props["npc"]  # NPC identifier (e.g., "Test")

            if npc_name not in npc_tile_positions:
                npc_tile_positions[npc_name] = []  # Initialize list if missing

            # Store tile along with solidity
            npc_tile_positions[npc_name].append(
                (tile, (x * tmxdata.tilewidth, y * tmxdata.tileheight), is_solid)
            )

        # Add the tile to the world as a solid or non-solid object
        tiles_below.add(classes.Tile(tile, (x * tmxdata.tilewidth, y * tmxdata.tileheight), is_solid))

# Ensure `npcs` is defined before adding NPCs
npcs = pygame.sprite.Group()

# Create NPCs from stored multi-tile data
for npc_name, tile_data in npc_tile_positions.items():
    if isinstance(tile_data, list) and all(isinstance(t, tuple) for t in tile_data):
        images, positions, solid_flags = zip(*tile_data)

        layer_index = tmxdata.layers.index(layer_draw_below)

        tile_x = positions[0][0] // tmxdata.tilewidth
        tile_y = positions[0][1] // tmxdata.tileheight

        tile_gid = tmxdata.get_tile_gid(tile_x, tile_y, layer_index)
        tile_props = tmxdata.get_tile_properties_by_gid(tile_gid) if tile_gid else {}

        # Default dialogue in case file loading fails
        dialogue_text = ["I have nothing to say."]

        # Check if "dialogue" exists in Tiled properties
        if "dialogue" in tile_props:
            file_path = path.join("data", tile_props["dialogue"])  # ✅ Correct path

            # Ensure the path is safe and properly formatted
            file_path = path.normpath(file_path)

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    dialogue_text = file.read().splitlines()  # ✅ Read file as a list of dialogue lines
            except FileNotFoundError:
                print(f"Warning: Dialogue file '{file_path}' not found!")

        # Create NPC with file-based dialogue
        npc_instance = classes.NPC(list(images), list(positions), npc_name, dialogue_text)
        npcs.add(npc_instance)

        for img, pos, is_solid in tile_data:
            if is_solid:
                tiles_below.add(classes.Tile(img, pos, True))

for x, y, gid in layer_draw_ontop :
    tile = tmxdata.get_tile_image_by_gid(gid)
    if (tile):
        tiles_top.add(classes.Tile(tile, (x * tmxdata.tilewidth, y * tmxdata.tileheight), False))

# text
text_display = test_font.render("PAUSE", False, "black")
text_rect = text_display.get_rect(topleft = (0, 0))

game_name = test_font.render("The Fart, Press Enter", False, ("Blue"))
game_name_rect = game_name.get_rect(center = ((screen.get_width() / 2), (screen.get_height() / 2)))

# test
toggle_collision_spr = False
toggle_coords = False

# states
title = True
pause = False

def show_player_coords(player) :
    coords_text = test_font.render(f"Player(x, y) = {player.pos.x, player.pos.y}", False, "white")
    coords_rect = coords_text.get_rect(bottomleft = (0, screen.get_height()))
    screen.blit(coords_text, coords_rect)


def check_collision_npcs(player, npcs):
    for npc in npcs:
        if npc.collides_with(player.sprite.rect):
            return npc  # Return NPC if player touches any part of it
    return None

def draw_dialogue_box(screen, text, font):
    box_image = pygame.image.load(path.join("data/sprites", "dialogbox.png")).convert()
    box_rect = box_image.get_rect(midbottom = ((screen.get_width() / 2), (screen.get_height() / 1.05)))

    text_surface = font.render(text, True, "white", None, 450)
    text_rect = text_surface.get_rect(topleft=(box_rect.x + 10, box_rect.y + 20))

    screen.blit(box_image, box_rect)
    screen.blit(text_surface, text_rect)

#gamemode2.gamemode_shmup()

while True:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        # TEST: show collision rectangles
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t :
                toggle_collision_spr = not toggle_collision_spr
        # TEST: show player coordinates
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c :
                toggle_coords = not toggle_coords
        # pause
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE :
                pause = not pause
        # get past the title scree, if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN :
                title = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # Press 'E' to interact
                    if npc and npc.interacting:  # Ensure npc is not None
                        dialogue_text = npc.next_dialogue()
                        if npc and not npc.interacting:  # Check again before setting dialogue_active
                            player.dialogue_active = False  # Unfreeze player when dialogue ends
                    else:
                        npc = check_collision_npcs(player_char, npcs)  # Detect NPC
                        if npc:
                            dialogue_text = npc.start_interaction()
                            player.dialogue_active = True  # Freeze player during dialogue


    if (not pause and not title) :
        screen.fill("purple")

        player_char.update()

        if (player_char.sprite.collide_solid_group(tiles_below)) :
            player_char.sprite.pos = player_char.sprite.initial_pos
            player_char.sprite.update_rect()

        # movement
        if (toggle_coords) : show_player_coords(player_char.sprite)

        tiles_below.draw(screen)

        # draw the player
        player_char.draw(screen)

        tiles_top.draw(screen)

        if npc and npc.interacting:
            draw_dialogue_box(screen, dialogue_text, test_font)  # Draw the dialogue box every frame

        # collision
        # draw collision before update
        if (toggle_collision_spr) :
            #pygame.draw.rect(screen, "blue", gurg.collision_rect, 6)
            #pygame.draw.rect(screen, "green", gurg.rect, 3)
            for tile_collision in tiles_below.sprites() :
                pygame.draw.rect(screen, "red", tile_collision.collision_rect, 5)
            pygame.draw.rect(screen, "blue", player_char.sprite.collision_rect, 6)
            pygame.draw.rect(screen, "green", player_char.sprite.rect, 3)

        # test
        #pygame.draw.circle(screen, "red", (player.sprite.rect.x + (player.sprite.rect.w / 2), player.sprite.rect.y + (player.sprite.rect.h / 2)), 4)
        #print("NPCs loaded into the game:")
        #for npc in npcs:
        #    print(f"NPC: {npc.name}, Bounding Box: {npc.bounding_box}, Dialogues: {npc.dialogues}")

    elif title :
        screen.fill("yellow")
        screen.blit(game_name, game_name_rect)

    elif pause :
        pygame.draw.rect(screen, "white", text_rect)
        screen.blit(text_display, text_rect)

    pygame.display.flip()
    player.dt = clock.tick(60) / 1000
