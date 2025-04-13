import pygame

class Tile(pygame.sprite.Sprite) :
    def __init__(self, image, pos, is_solid, npc=None) :
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = pygame.Vector2(pos))
        self.npc = npc  # Store NPC instance if this tile is an NPC
        if (is_solid) :
            self.collision_rect = self.image.get_rect(topleft = pygame.Vector2(pos))
        else :
            self.collision_rect = pygame.Rect(0, 0, 0, 0)

class NPC(pygame.sprite.Sprite):
    def __init__(self, images, positions, name, dialogues):
        super().__init__()
        self.images = images
        self.positions = positions
        self.name = name
        self.dialogues = dialogues
        self.current_dialogue = 0
        self.interacting = False

        # For drawing: use the first tile
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(int(self.positions[0][0]), int(self.positions[0][1])))

        # For collision: use all tiles
        self.rects = [img.get_rect(topleft=(int(x), int(y))) for img, (x, y) in zip(images, positions)]

        # Define an overall bounding box for the NPC based on all tiles
        min_x = min(pos[0] for pos in positions)
        min_y = min(pos[1] for pos in positions)
        max_x = max(pos[0] + img.get_width() for img, pos in zip(images, positions))
        max_y = max(pos[1] + img.get_height() for img, pos in zip(images, positions))

        self.bounding_box = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def start_interaction(self):
        if self.current_dialogue < len(self.dialogues):
            self.interacting = True
            return self.dialogues[self.current_dialogue]
        else:
            self.interacting = False
            return None

    def next_dialogue(self):
        if self.interacting:
            self.current_dialogue += 1
            if self.current_dialogue < len(self.dialogues):
                return self.dialogues[self.current_dialogue]
            else:
                self.interacting = False
                self.current_dialogue = 0  # Reset dialogue
                return None
    def collides_with(self, player_rect):
        collision = any(player_rect.colliderect(rect) for rect in self.rects)
        return collision
