import pygame

npc_talk_distance = 150

class NPC() :
    def __init(self, obj_name, npc_file)
        super().__init__(obj_name)
        self.npc_file = npc_file

    def on(self, other, distance) :
        from player import Player
        player = other.get(Player)
        if distance < npc_talk_distance :
            file = open(path.join("data/dialog", "test_npc"))
            data = file.read()
            files.close()
            lines = data.split('\n')
            print(lines)
