import pygame

class Tile(pygame.sprite.Sprite) :
    def __init__(self, image, pos, is_solid=False, npc=None) :
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

class AnimatedMovingNPC(pygame.sprite.Sprite):
    def __init__(self, frames, pos, name, dialogue=None, speed=2, patrol_distance=100):
        super().__init__()
        self.frames = frames
        self.image = frames[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.name = name
        self.dialogue = dialogue or []
        self.dialogue_phase_1 = []  # You can load a second dialogue file or hardcode it
        self.phase = 0
        self.dialogue_index = 0
        self.interacting = False

        self.speed = speed
        self.direction = 1
        self.patrol_distance = patrol_distance
        self.start_x = pos[0]
        self.elapsed = 0
        self.frame_index = 0
        
        self.moving_to_target = False
        self.target_pos = self.rect.topleft
    
    def update(self, dt):
        if self.interacting:
            return  # Pause during dialogue

        if self.moving_to_target:
            self.elapsed += dt
            if self.elapsed > 0.1:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
                self.elapsed = 0
        else:
            self.image = self.frames[0]  # default standing frame

        if self.moving_to_target:
            direction = pygame.Vector2(self.target_pos) - pygame.Vector2(self.rect.topleft)
            if direction.length_squared() < 1:
                self.rect.topleft = self.target_pos
                self.moving_to_target = False
            else:
                step = direction.normalize() * self.speed
                self.rect.x += int(step.x)
                self.rect.y += int(step.y)
        else:
            # Normal patrol movement (optional)
            pass


    def collides_with(self, player_rect):
        return self.rect.colliderect(player_rect)

    def start_interaction(self):
        self.interacting = True
        self.dialogue_index = 0

        # Different dialogue if phase has changed
        if self.phase == 1 and self.dialogue_phase_1:
            self.dialogue = self.dialogue_phase_1

        return self.dialogue[0] if self.dialogue else ""

    def next_dialogue(self):
        self.dialogue_index += 1

        if self.dialogue_index < len(self.dialogue):
            line = self.dialogue[self.dialogue_index]

            # Handle command lines
            if line.startswith("::"):
                self.handle_command(line)
                return self.next_dialogue()  # skip command display

            return line
        else:
            self.interacting = False
            return ""


    def move_to(self, x, y):
        self.target_pos = pygame.Vector2(x, y)
        self.moving_to_target = True

    def handle_command(self, line):
        parts = line.strip()[2:].split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if cmd == "move_right_tiles" and args:
            try:
                tiles = int(args[0])
                pixels = tiles * 64
                self.move_to(self.rect.x + pixels, self.rect.y)
                self.phase = 1
            except ValueError:
                print(f"⚠️ Invalid tile count: {args[0]}")

        elif cmd == "move_right" and args:
            try:
                pixels = int(args[0])
                print(f"🧭 Command: moving {self.name} right by {pixels} pixels")
                self.move_to(self.rect.x + pixels, self.rect.y)
                self.phase = 1
            except ValueError:
                print(f"⚠️ Invalid pixel value: {args[0]}")
