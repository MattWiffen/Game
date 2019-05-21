import pygame
from settings import *


class Spritesheet:
        def __init__(self, filename):
            self.spritesheet = pygame.image.load(filename).convert()

        def get_image(self, x, y, width, height):
            image = pygame.Surface((width, height))
            image.blit(self.spritesheet, (0, 0), (x, y, width, height))
            rect = image.get_rect()
            image = pygame.transform.scale(image, (rect.width*2, rect.height*2))
            image.set_colorkey((0, 0, 0))
            return image


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.attacking = False
        self.current_frame_walk = 0
        self.last_update_walk = 0
        self.current_frame_atk = 0
        self.last_update_atk = 0
        self.last_direction = "down"
        self.load_images()
        self.image = self.frames["down"][0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.rect.bottomleft = self.hit_rect.bottomleft
        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y

    def load_images(self):
        self.frames = {
            "down": [
                self.game.spritesheet.get_image(0, 0, 16, 32),
                self.game.spritesheet.get_image(16, 0, 16, 32),
                self.game.spritesheet.get_image(32, 0, 16, 32),
                self.game.spritesheet.get_image(48, 0, 16, 32)
            ],
            "right": [
                self.game.spritesheet.get_image(0, 32, 16, 32),
                self.game.spritesheet.get_image(16, 32, 16, 32),
                self.game.spritesheet.get_image(32, 32, 16, 32),
                self.game.spritesheet.get_image(48, 32, 16, 32),
                self.game.spritesheet.get_image(64, 32, 16, 32)
            ],
            "up": [
                self.game.spritesheet.get_image(0, 64, 16, 32),
                self.game.spritesheet.get_image(16, 64, 16, 32),
                self.game.spritesheet.get_image(32, 64, 16, 32),
                self.game.spritesheet.get_image(48, 64, 16, 32),
                self.game.spritesheet.get_image(64, 64, 16, 32)
            ],
            "left": [
                self.game.spritesheet.get_image(0, 96, 16, 32),
                self.game.spritesheet.get_image(16, 96, 16, 32),
                self.game.spritesheet.get_image(32, 96, 16, 32),
                self.game.spritesheet.get_image(48, 96, 16, 32),
                self.game.spritesheet.get_image(64, 96, 16, 32)
            ],
            "attack_down": [
                self.game.spritesheet.get_image(9, 128, 16, 32),
                self.game.spritesheet.get_image(41, 128, 16, 32),
                self.game.spritesheet.get_image(73, 128, 16, 32),
                self.game.spritesheet.get_image(105, 128, 16, 32)
            ],
            "attack_up": [
                self.game.spritesheet.get_image(8, 160, 24, 32),
                self.game.spritesheet.get_image(40, 160, 24, 32),
                self.game.spritesheet.get_image(72, 160, 24, 32),
                self.game.spritesheet.get_image(104, 160, 24, 32)
            ],
            "attack_right": [
                self.game.spritesheet.get_image(6, 192, 24, 32),
                self.game.spritesheet.get_image(39, 192, 24, 32),
                self.game.spritesheet.get_image(71, 192, 24, 32),
                self.game.spritesheet.get_image(104, 192, 24, 32)
            ],
            "attack_left": [
                self.game.spritesheet.get_image(0, 224, 22, 32),
                self.game.spritesheet.get_image(32, 224, 22, 32),
                self.game.spritesheet.get_image(64, 224, 22, 32),
                self.game.spritesheet.get_image(97, 224, 22, 32)
            ]
        }

    def animate(self):
        now = pygame.time.get_ticks()

        if self.vx != 0 or self.vy != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update_walk > 200:
                self.last_update_walk = now
                self.current_frame_walk = (self.current_frame_walk + 1) % 4
                self.current_frame_atk = 0

                if self.vx > 0:
                    self.image = self.frames["right"][self.current_frame_walk]
                elif self.vx < 0:
                    self.image = self.frames["left"][self.current_frame_walk]
                elif self.vy > 0:
                    self.image = self.frames["down"][self.current_frame_walk]
                elif self.vy < 0:
                    self.image = self.frames["up"][self.current_frame_walk]

        elif self.attacking:
            if now - self.last_update_atk > 100:
                self.last_update_atk = now
                self.current_frame_atk = (self.current_frame_atk + 1) % 5
                if self.current_frame_atk == 4:
                    self.attacking = False
                if self.last_direction == "right" and self.attacking is True:
                    self.image = self.frames["attack_right"][self.current_frame_atk]
                    left = self.rect.left
                    self.rect = self.image.get_rect()
                    self.rect.left = left

                elif self.last_direction == "down" and self.attacking is True:
                    self.image = self.frames["attack_down"][self.current_frame_atk]
                    left = self.rect.left
                    self.rect = self.image.get_rect()
                    self.rect.left = left

                elif self.last_direction == "up" and self.attacking is True:
                    self.image = self.frames["attack_up"][self.current_frame_atk]
                    left = self.rect.left
                    self.rect = self.image.get_rect()
                    self.rect.left = left

                elif self.last_direction == "left" and self.attacking is True:
                    self.right = self.rect.right
                    self.image = self.frames["attack_left"][self.current_frame_atk]
                    self.rect = self.image.get_rect()
                    self.rect.right = self.right

        if not self.walking and not self.attacking:
            self.image = self.frames[self.last_direction][0]
            self.rect = self.image.get_rect()

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if self.game.cooldown <= 0:
            self.x = round(self.x / TILE_SIZE)*TILE_SIZE
            self.y = round(self.y / TILE_SIZE)*TILE_SIZE
            self.vx, self.vy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.last_direction = "left"
                self.attacking = False
                new_rect = self.hit_rect.move(-TILE_SIZE, 0)
                if self.collide(new_rect):
                    return
                self.vx = -PLAYER_SPEED
                self.game.cooldown = self.game.delay
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.last_direction = "right"
                self.attacking = False
                new_rect = self.hit_rect.move(TILE_SIZE, 0)
                if self.collide(new_rect):
                    return
                self.vx = PLAYER_SPEED
                self.game.cooldown = self.game.delay
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.last_direction = "up"
                self.attacking = False
                new_rect = self.hit_rect.move(0, -TILE_SIZE)
                if self.collide(new_rect):
                    return
                self.vy = -PLAYER_SPEED
                self.game.cooldown = self.game.delay
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.last_direction = "down"
                self.attacking = False
                new_rect = self.hit_rect.move(0, TILE_SIZE)
                if self.collide(new_rect):
                    return
                self.vy = PLAYER_SPEED
                self.game.cooldown = self.game.delay
            elif keys[pygame.K_SPACE]:
                self.attacking = True

    def collide(self, rect):
        for wall in self.game.obstacles:
            if rect.colliderect(wall.rect):
                return True
        return False

    def update(self):
        self.get_keys()
        self.animate()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        if self.attacking and self.last_direction == "left":
            self.rect.topleft = (self.x, self.y)
            self.rect.right = self.right
            self.hit_rect.right = self.right
        else:
            self.rect.topleft = (self.x, self.y)
            self.hit_rect.bottomleft = self.rect.bottomleft


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

