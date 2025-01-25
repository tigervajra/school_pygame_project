import pygame
from pytmx.util_pygame import load_pygame
from os import path
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("hawk tuah")

tmxdata = load_pygame(path.join("data/tmx", "test.tmx"))

clock = pygame.time.Clock()
dt = 0

test_font = pygame.font.Font(None, 50)

class Tile(pygame.sprite.Sprite) :
    def __init__(self, image, pos, is_solid) :
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = pygame.Vector2(pos))
        if (is_solid) :
            self.collision_rect = self.image.get_rect(topleft = pygame.Vector2(pos))
        else :
            self.collision_rect = pygame.Rect(0, 0, 0, 0)

# player
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
        if (self.collide_solid_group(tiles_below)) :
            self.pos = self.initial_pos
            self.update_rect()


player = pygame.sprite.GroupSingle()
player.add(Player())
player.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

tiles_top = pygame.sprite.Group()
tiles_below = pygame.sprite.Group()

layer_draw_below = tmxdata.get_layer_by_name("draw_below")
layer_draw_ontop = tmxdata.get_layer_by_name("draw_ontop")
data_layer = tmxdata.get_layer_by_name("Data")

for x, y, gid in layer_draw_below :
    tile = tmxdata.get_tile_image_by_gid(gid)
    if (tile) :
        is_solid = tmxdata.get_tile_properties(x, y, tmxdata.layers.index(data_layer))
        print(is_solid)
        if (is_solid["solid"]) :
            tiles_below.add(Tile(tile, (x * tmxdata.tilewidth, y * tmxdata.tileheight), True))
        else :
            tiles_below.add(Tile(tile, (x * tmxdata.tilewidth, y * tmxdata.tileheight), False))

for x, y, gid in layer_draw_ontop :
    tile = tmxdata.get_tile_image_by_gid(gid)
    if (tile):
        tiles_top.add(Tile(tile, (x * tmxdata.tilewidth, y * tmxdata.tileheight), False))
# text
text_display = test_font.render("PAUSE", False, "black")
text_rect = text_display.get_rect(topleft = (0, 0))

game_name = test_font.render("The Fart, Press Enter", False, ("Blue"))
game_name_rect = game_name.get_rect(center = ((screen.get_width() / 2), (screen.get_height() / 4)))

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

def separate_collision_rect(sprite_a, sprite_b) :
    return sprite_a.collision_rect.colliderect(sprite_b.collision_rect)

def check_collision_npcs(player, npcs) :
    return pygame.sprite.spritecollide(player.sprite, npcs, False, collided = separate_collision_rect)

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

    if (not pause and not title) :
        screen.fill("purple")

        player.update()

        # movement
        if (toggle_coords) : show_player_coords(player.sprite)

        tiles_below.draw(screen)

        # draw the player
        player.draw(screen)

        tiles_top.draw(screen)

        # collision
        # draw collision before update
        if (toggle_collision_spr) :
            #pygame.draw.rect(screen, "blue", gurg.collision_rect, 6)
            #pygame.draw.rect(screen, "green", gurg.rect, 3)
            for tile_collision in tiles_below.sprites() :
                pygame.draw.rect(screen, "red", tile_collision.collision_rect, 5)
            pygame.draw.rect(screen, "blue", player.sprite.collision_rect, 6)
            pygame.draw.rect(screen, "green", player.sprite.rect, 3)

        # test
        #pygame.draw.circle(screen, "red", (player.sprite.rect.x + (player.sprite.rect.w / 2), player.sprite.rect.y + (player.sprite.rect.h / 2)), 4)

    elif title :
        screen.fill("yellow")
        screen.blit(game_name, game_name_rect)

    elif pause :
        pygame.draw.rect(screen, "white", text_rect)
        screen.blit(text_display, text_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000
