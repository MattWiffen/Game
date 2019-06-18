import sys
from sprites import *
from map import *
from settings import *
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

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        sprite_folder = os.path.join(game_folder, "sprites")
        sound_folder = os.path.join(game_folder, "sounds")
        self.map_folder = os.path.join(game_folder, "maps")
        self.spritesheet = Spritesheet(os.path.join(sprite_folder, "character.png"))
        self.NPC_spritesheet = Spritesheet(os.path.join(sprite_folder, "NPC.png"))
        self.objects_spritesheet = Spritesheet(os.path.join(sprite_folder, "objects.png"))
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.load_map(self.map_folder, LOCATION[self.mapX][self.mapY])
        self.load_HUD()

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
            ]
        }

    def load_map(self, map_folder, map_name):
        self.map = TiledMap(os.path.join(map_folder, map_name))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.load_objects()

    def load_objects(self):
        self.obstacles = pygame.sprite.Group()
        for tile_object in self.map.tmx_data.objects:
            if tile_object.name == "obstacle":
                Obstacle(
                    self,
                    tile_object.x * 2,
                    tile_object.y * 2,
                    tile_object.width * 2,
                    tile_object.height * 2,
                    tile_object.type,
                )
            if tile_object.name == "NPC":
                NPC(self, tile_object.x*2, tile_object.y*2)

        self.camera = Camera(self.map.width, self.map.height)

    def draw_HUD(self, x, y):
        self.screen.blit(self.HUD_elements["back"], (x, y))
        if self.player.level - 10 < 0:
            self.screen.blit(self.HUD_elements["numbers"][self.player.level], (x + 24, y + 66))
        else:
            self.screen.blit(self.HUD_elements["numbers"][int(str(self.player.level)[0])], (x+8, y+66))
            self.screen.blit(self.HUD_elements["numbers"][int(str(self.player.level)[1])], (x+24, y+66))
        self.screen.blit(self.HUD_elements["sword"], (x+14, y+14))

        for i in range(self.player.max_health //4):
            self.screen.blit(self.HUD_elements["health"][0], (x + 60 + i * 32, y + 10))
        j = 0
        for j in range(self.player.health // 4):
            self.screen.blit(self.HUD_elements["health"][4], (x + 60 + j * 32, y + 10))
        if not self.player.health % 4 == 0:
            self.screen.blit(self.HUD_elements["health"][self.player.health % 4], (x + 92 + j * 32, y + 10))






    def new(self):
        for tile_object in self.map.tmx_data.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x*2, tile_object.y*2)

    def run(self):
        # game loop - set self.playing = False to end the game
        while True:
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
        for sprite in self.player_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.draw_HUD(10, 10)
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
while True:
    g.new()
    g.run()
