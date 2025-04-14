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
    def __init__(self, frames, pos, name, dialogue_phases=None, *, speed=0, patrol_distance=0):
        super().__init__()
        self.frames = frames
        self.image = frames[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = self.rect
        self.name = name
        self.dialogue_phases = dialogue_phases or {0: []}
        self.phase = 0
        self.dialogue_index = 0
        self.interacting = False
        self.freeze_player = False
        self.unfreeze_player = False
        self.pending_commands = []  # queue of commands
        self.deferred_commands = []

        # Movement
        self.speed = speed
        self.direction = 1
        self.patrol_distance = patrol_distance
        self.start_x = pos[0]
        self.moving_to_target = False
        self.target_pos = pygame.Vector2(self.rect.topleft)

        # Animation timing
        self.elapsed = 0
        self.frame_index = 0

    def start_interaction(self):
        self.interacting = True
        self.dialogue_index = 0
        current = self.dialogue_phases.get(self.phase, [])
        return current[0] if current else ""


    def next_dialogue(self):
        current_dialogue = self.dialogue_phases.get(self.phase, [])

        while self.dialogue_index < len(current_dialogue):
            line = current_dialogue[self.dialogue_index]
            self.dialogue_index += 1

            if isinstance(line, str) and line.startswith("::"):
                # Only defer this specific command
                if line.startswith("::unfreeze_player"):
                    if not any(cmd == line for cmd, _ in self.deferred_commands):
                        self.deferred_commands.append((line, self.phase))
                        print(f"🕒 Deferred command: {line} (phase {self.phase})")
                    else:
                        print(f"⚠️ Skipping duplicate deferred command: {line}")
                    continue

                self.handle_command(line)
                continue

            if line.strip():
                return line

        self.interacting = False
        return ""

    def update(self, dt):
        if self.interacting:
            return  # pause animation + movement during dialogue

        # Animate only when moving
        if self.moving_to_target:
            self.elapsed += dt
            if self.elapsed > 0.1:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
                self.elapsed = 0
        else:
            self.image = self.frames[0]

        # Move toward target if needed
        if self.moving_to_target:
            direction = pygame.Vector2(self.target_pos) - pygame.Vector2(self.rect.topleft)
            if direction.length_squared() < 1:
                self.rect.topleft = self.target_pos
                self.moving_to_target = False

                while self.deferred_commands:
                    command, saved_phase = self.deferred_commands.pop(0)
                    print(f"✅ Running deferred command: {command} (from phase {saved_phase})")

                    # Temporarily switch to the saved phase
                    original_phase = self.phase
                    self.phase = saved_phase
                    self.handle_command(command)
                    self.phase = original_phase
            else:
                step = direction.normalize() * self.speed
                self.rect.x += int(step.x)
                self.rect.y += int(step.y)

    def move_to(self, x, y):
        self.target_pos = pygame.Vector2(x, y)
        self.moving_to_target = True

    def handle_command(self, line):
        parts = line.strip()[2:].split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        print(f"[{self.name}] Command received: {cmd} (phase {self.phase})")

        if cmd == "move_right_tiles" and self.phase == 0:
            try:
                tiles = int(args[0])
                pixels = tiles * 64
                self.move_to(self.rect.x + pixels, self.rect.y)
                
                 # ✅ Queue unfreeze if it's the next command
                future_lines = self.dialogue_phases.get(self.phase, [])[self.dialogue_index:]
            except ValueError:
                print(f"⚠️ Invalid tile count: {args[0]}")
        elif cmd == "set_phase" and args:
            try:
                new_phase = int(args[0])
                self.phase = new_phase
            except ValueError:
                pass
        elif cmd == "freeze_player":
            self.freeze_player = True  # we'll notify main loop
            print(f"[{self.name}] set freeze_player = True")
        elif cmd == "unfreeze_player":
            self.unfreeze_player = True
            print(f"[{self.name}] set unfreeze_player = True")

    def collides_with(self, other_rect):
        return self.rect.colliderect(other_rect)
