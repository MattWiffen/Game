import sys
from sprites import *
from map import *
from settings import *
import encounter
import os


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Title")
        self.clock = pygame.time.Clock()
        self.cooldown = 0
        self.delay = 0.2
        self.mapX = 0
        self.mapY = 0
        self.load_data()
        self.playing = True

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        sprite_folder = os.path.join(game_folder, "sprites")
        sound_folder = os.path.join(game_folder, "sounds")
        self.map_folder = os.path.join(game_folder, "maps")
        self.spritesheet = Spritesheet(os.path.join(sprite_folder, "character.png"))
        self.NPC_spritesheet = Spritesheet(os.path.join(sprite_folder, "NPC.png"))
        self.objects_spritesheet = Spritesheet(os.path.join(sprite_folder, "objects.png"))
        self.font_spritesheet = Spritesheet(os.path.join(sprite_folder, "font.png"))
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.collects = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.collect_ids = []
        self.load_collect_sprite()
        self.load_map(self.map_folder, LOCATION[self.mapX][self.mapY])
        self.load_HUD()
        self.load_font()
        encounter.load_text(20, 30)

        self.sound_walking = []
        self.sound_sword = pygame.mixer.Sound(os.path.join(sound_folder, SOUND_SWORD))
        for effect in SOUND_WALKING:
            self.sound_walking.append(pygame.mixer.Sound(os.path.join(sound_folder, effect)))

    def load_HUD(self):
        self.HUD_elements = {
            "back": self.objects_spritesheet.get_image(0, 226, 78, 53),
            "numbers": [
                self.objects_spritesheet.get_image(99, 259, 9, 11),
                self.objects_spritesheet.get_image(83, 227, 9, 11),
                self.objects_spritesheet.get_image(99, 227, 9, 11),
                self.objects_spritesheet.get_image(115, 227, 9, 11),
                self.objects_spritesheet.get_image(131, 227, 9, 11),
                self.objects_spritesheet.get_image(83, 243, 9, 11),
                self.objects_spritesheet.get_image(99, 243, 9, 11),
                self.objects_spritesheet.get_image(115, 243, 9, 11),
                self.objects_spritesheet.get_image(131, 243, 9, 11),
                self.objects_spritesheet.get_image(83, 259, 9, 11),
            ],
            "sword": self.objects_spritesheet.get_image(114, 259, 14, 14),
            "health": [
                self.objects_spritesheet.get_image(128, 2, 14, 13),
                self.objects_spritesheet.get_image(112, 2, 14, 13),
                self.objects_spritesheet.get_image(96, 2, 14, 13),
                self.objects_spritesheet.get_image(80, 2, 14, 13),
                self.objects_spritesheet.get_image(64, 2, 14, 13),
            ],
            "coins": self.objects_spritesheet.get_image(64, 291, 63, 25)
        }

    def load_font(self):
        self.font_elements = {
            "text": {
                "0": self.font_spritesheet.get_image(216, 0, 8, 8),
                "1": self.font_spritesheet.get_image(224, 0, 8, 8),
                "2": self.font_spritesheet.get_image(232, 0, 8, 8),
                "3": self.font_spritesheet.get_image(216, 8, 8, 8),
                "4": self.font_spritesheet.get_image(224, 8, 8, 8),
                "5": self.font_spritesheet.get_image(232, 8, 8, 8),
                "6": self.font_spritesheet.get_image(216, 16, 8, 8),
                "7": self.font_spritesheet.get_image(224, 16, 8, 8),
                "8": self.font_spritesheet.get_image(232, 16, 8, 8),
                "9": self.font_spritesheet.get_image(224, 24, 8, 8),
                ".": self.font_spritesheet.get_image(2, 32, 8, 16),
                ",": self.font_spritesheet.get_image(8, 32, 8, 16),
                "!": self.font_spritesheet.get_image(16, 32, 8, 16),
                "?": self.font_spritesheet.get_image(32, 32, 8, 16),
                ":": self.font_spritesheet.get_image(80, 32, 8, 16),
                ";": self.font_spritesheet.get_image(88, 32, 8, 16),
                "'": self.font_spritesheet.get_image(96, 32, 8, 16),
                '"': self.font_spritesheet.get_image(16, 32, 8, 16)
            },
            "background": self.font_spritesheet.get_image(0, 48, 240, 72)
        }

        count = 0
        for i in "AaBbCcDdEeFfGgHhIiJjKkLlMm":
            self.font_elements["text"][i] = self.font_spritesheet.get_image(count, 0, 8, 16)
            count += 8

        count = 0
        for i in "NnOoPpQqRrSsTtUuVvWwXxYyZz":
            self.font_elements["text"][i] = self.font_spritesheet.get_image(count, 16, 8, 16)
            count += 8

    def load_collect_sprite(self):
        self.collect_sprite = {
            "coin": [
                self.objects_spritesheet.get_image(2, 66, 11, 11),
                self.objects_spritesheet.get_image(18, 66, 11, 11),
                self.objects_spritesheet.get_image(34, 66, 11, 11),
                self.objects_spritesheet.get_image(50, 66, 11, 11)
            ],
            "heart": [
                self.objects_spritesheet.get_image(2, 51, 11, 11),
                self.objects_spritesheet.get_image(18, 51, 11, 11),
                self.objects_spritesheet.get_image(34, 51, 11, 11),
                self.objects_spritesheet.get_image(50, 51, 11, 11)
            ]
        }
        self.hazard_sprite = [
            self.objects_spritesheet.get_image(64, 48, 16, 16),
            self.objects_spritesheet.get_image(80, 48, 16, 16),
            self.objects_spritesheet.get_image(96, 48, 16, 16),
            self.objects_spritesheet.get_image(112, 48, 16, 16),
            self.objects_spritesheet.get_image(128, 48, 16, 16),
            self.objects_spritesheet.get_image(144, 48, 16, 16),
            self.objects_spritesheet.get_image(160, 48, 16, 16)
        ]

    def load_map(self, map_folder, map_name):
        self.map = TiledMap(os.path.join(map_folder, map_name))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.load_objects()

    def load_objects(self):
        self.npcs = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        for tile_object in self.map.tmx_data.objects:
            if tile_object.name == "obstacle":
                Obstacle(
                    self,
                    tile_object.x * 2,
                    tile_object.y * 2,
                    tile_object.width * 2,
                    tile_object.height * 2,
                    tile_object.type
                )
            if tile_object.name == "NPC":
                NPC(self, tile_object.x*2, tile_object.y*2)

            if tile_object.name == "collect":
                x = 0
                collect_id = str(self.mapX) + str(self.mapY) + str(tile_object.x) + str(tile_object.y)
                if collect_id not in self.collect_ids:
                    if tile_object.type == "coin" or tile_object.type == "heart":
                        x = 5
                    Collect(
                        self,
                        x + tile_object.x * 2,
                        x + tile_object.y * 2,
                        collect_id,
                        tile_object.type
                    )
                    self.collect_ids.append(collect_id)

            if tile_object.name == "hazard":
                hazard_id = str(self.mapX) + str(self.mapY) + str(tile_object.x) + str(tile_object.y)
                if hazard_id not in self.collect_ids:
                    Hazard(
                        self,
                        tile_object.x * 2,
                        tile_object.y * 2,
                        hazard_id
                    )
                    self.collect_ids.append(hazard_id)

        self.camera = Camera(self.map.width, self.map.height)

    def draw_HUD(self, x, y):
        self.screen.blit(self.HUD_elements["back"], (x, y))
        self.screen.blit(self.HUD_elements["coins"], (WIDTH - 126 - x, HEIGHT - 50 - y))

        if self.player.level - 10 < 0:
            self.screen.blit(self.HUD_elements["numbers"][self.player.level], (x + 24, y + 66))
        else:
            self.screen.blit(self.HUD_elements["numbers"][int(str(self.player.level)[0])], (x+8, y+66))
            self.screen.blit(self.HUD_elements["numbers"][int(str(self.player.level)[1])], (x+24, y+66))
        self.screen.blit(self.HUD_elements["sword"], (x+14, y+14))

        self.screen.blit(self.HUD_elements["numbers"]
                         [self.player.coins % 10],
                         (WIDTH - 126 - x + 96, HEIGHT - 50 - y + 16))
        self.screen.blit(self.HUD_elements["numbers"]
                         [int((self.player.coins % 100 - self.player.coins % 10) / 10)],
                         (WIDTH - 126 - x + 76, HEIGHT - 50 - y + 16))
        self.screen.blit(self.HUD_elements["numbers"]
                         [int((self.player.coins % 1000 - self.player.coins % 100 - self.player.coins % 10) / 10)],
                         (WIDTH - 126 - x + 56, HEIGHT - 50 - y + 16))

        for i in range(self.player.max_health // 4):
            self.screen.blit(self.HUD_elements["health"][0], (x + 60 + i * 32, y + 10))
        j = 0
        for j in range(self.player.health // 4):
            self.screen.blit(self.HUD_elements["health"][4], (x + 60 + j * 32, y + 10))
        if not self.player.health % 4 == 0 and self.player.health // 4 != 0:
            self.screen.blit(self.HUD_elements["health"][self.player.health % 4], (x + 92 + j * 32, y + 10))
        elif not self.player.health % 4 == 0 and self.player.health // 4 == 0:
            self.screen.blit(self.HUD_elements["health"][self.player.health % 4], (x + 60 + j * 32, y + 10))

    def draw_text(self, string, x_offset=0, y_offset=0):
        x, y = (WIDTH - 480) / 2, HEIGHT - 148
        self.screen.blit(self.font_elements["background"], (x, y))
        x += x_offset
        y += y_offset
        string = string.split()
        for word in string:
            if x + len(word)*16 > ((WIDTH + 480) / 2) - x_offset:
                x = (WIDTH - 480) / 2 + x_offset
                y += 30
            for letter in word:
                self.screen.blit(self.font_elements["text"][letter], (x, y))
                x += 16
            x += 20

    def new(self):
        for tile_object in self.map.tmx_data.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x*2, tile_object.y*2)

    def run(self):
        # game loop - set self.playing = False to end the game
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.cooldown -= self.dt
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.npcs:
            if sprite.current_map == (self.mapX, self.mapY):
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.collects:
            if sprite.current_map == (self.mapX, self.mapY):
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.hazards:
            if sprite.y <= self.player.y:
                if sprite.current_map == (self.mapX, self.mapY):
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.player_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.hazards:
            if sprite.y > self.player.y:
                if sprite.current_map == (self.mapX, self.mapY):
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.draw_HUD(10, 10)
        if self.player.npc_key:
            if not encounter.PROGRESS[self.player.npc_key]["started"]:
                try:
                    encounter.draw_text(self, self.player.npc_key, "start", 20, 30)
                except IndexError:
                    encounter.PROGRESS[self.player.npc_key]["started"] = True
                    self.player.npc_key = False
                    encounter.drawing = False
                    self.completion = False
            elif encounter.PROGRESS[self.player.npc_key]["started"] is True\
                    and encounter.PROGRESS[self.player.npc_key]["finished"] is False\
                    and not encounter.questOBJ(self.player.npc_key, self.player):
                try:
                    encounter.draw_text(self, self.player.npc_key, "remind", 20, 30)
                except IndexError:
                    self.player.npc_key = False
                    encounter.drawing = False
                    self.completion = False
            elif encounter.PROGRESS[self.player.npc_key]["started"] is True\
                    and encounter.PROGRESS[self.player.npc_key]["finished"] is False\
                    and encounter.questOBJ(self.player.npc_key, self.player):
                try:
                    encounter.draw_text(self, self.player.npc_key, "end", 20, 30)
                    self.completion = True
                except IndexError:
                    if self.completion is True:
                        encounter.questCOMPLETE(self.player.npc_key, self.player)
                        encounter.PROGRESS[self.player.npc_key]["finished"] = True
                    self.player.npc_key = False
                    encounter.drawing = False
            elif encounter.PROGRESS[self.player.npc_key]["started"] is True\
                    and encounter.PROGRESS[self.player.npc_key]["finished"] is True:
                try:
                    encounter.draw_text(self, self.player.npc_key, "misc", 20, 30)
                except IndexError:
                    self.player.npc_key = False
                    encounter.drawing = False
                    self.completion = False
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()


# create the game object
g = Game()
#while True:
g.new()
g.run()
