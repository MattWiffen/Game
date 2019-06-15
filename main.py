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
        self.dev = False
        self.mapX = 0
        self.mapY = 0
        self.load_data()

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        sprite_folder = os.path.join(game_folder, "sprites")
        sound_folder = os.path.join(game_folder, "sounds")
        self.map_folder = os.path.join(game_folder, "maps")
        self.spritesheet = Spritesheet(os.path.join(sprite_folder, "character.png"))
        self.all_sprites = pygame.sprite.Group()
        self.load_map(self.map_folder, LOCATION[self.mapX][self.mapY])

        self.sound_walking = []
        self.sound_sword = pygame.mixer.Sound(os.path.join(sound_folder, SOUND_SWORD))
        for effect in SOUND_WALKING:
            self.sound_walking.append(pygame.mixer.Sound(os.path.join(sound_folder, effect)))

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
        self.camera = Camera(self.map.width, self.map.height)

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
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.dev:
                pygame.draw.rect(self.screen, (255, 0, 255), self.camera.apply_rect(sprite.rect), 2)
                pygame.draw.rect(self.screen, (0, 255, 255), self.camera.apply_rect(sprite.hit_rect), 2)

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_k:
                    self.dev = not self.dev
                if event.key == pygame.K_l:
                    self.load_map(self.map_folder, "new_world2.tmx")



# create the game object
g = Game()
while True:
    g.new()
    g.run()
