import pytmx
import pygame
from settings import *


class TiledMap:
    def __init__(self, file_name):
        tile_map = pytmx.load_pygame(file_name, pixelalpha=True)
        self.width = tile_map.width * TILE_SIZE
        self.height = tile_map.height * TILE_SIZE
        self.tmx_data = tile_map

    def render(self, surface):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (32, 32))
                        surface.blit(tile, (x * TILE_SIZE,
                                            y * TILE_SIZE))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        if not target.attacking or target.walking:
            x = -target.rect.x + int(WIDTH / 2)
            y = -target.rect.y + int(HEIGHT / 2)

            x = min(0, x)
            y = min(0, y)
            x = max(-(self.width - WIDTH), x)
            y = max(-(self.height - HEIGHT), y)
            self.camera = pygame.Rect(x, y, self.width, self.height)
