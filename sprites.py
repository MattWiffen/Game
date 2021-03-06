import itertools
from settings import *
import encounter


class Spritesheet:
        def __init__(self, filename):
            self.spritesheet = pygame.image.load(filename).convert_alpha()

        def get_image(self, x, y, width, height):
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.blit(self.spritesheet, (0, 0), (x, y, width, height))
            rect = image.get_rect()
            image = pygame.transform.scale(image, (rect.width*2, rect.height*2))
            return image


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.player_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.attacking = False
        self.current_frame_walk = 0
        self.last_update_walk = 0
        self.current_frame_atk = 0
        self.last_update_atk = 0
        self.last_update_hurt = 0
        self.sound_walking_loop = itertools.cycle(self.game.sound_walking)
        self.last_direction = "down"
        self.load_images()
        self.image = self.frames["down"][0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.rect.bottomleft = self.hit_rect.bottomleft
        self.vx, self.vy = 0, 0
        self.x, self.y = x, y

        self.level = 1
        self.max_health = 16  # multiple of 4
        self.health = 16  # less than max
        self.coins = 0
        self.xp = 75

        self.npc_key = False
        self.e_flag = False

    def place(self, x, y):
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
                self.game.spritesheet.get_image(0, 224, 23, 32),
                self.game.spritesheet.get_image(32, 224, 23, 32),
                self.game.spritesheet.get_image(64, 224, 23, 32),
                self.game.spritesheet.get_image(97, 224, 23, 32)
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
                self.current_frame_atk = -1
                if not self.current_frame_walk % 2 == 0:
                    sound = next(self.sound_walking_loop)
                    sound.set_volume(SFX_VOLUME)
                    sound.play()

                if self.vx > 0:
                    self.image = self.frames["right"][self.current_frame_walk]
                    self.rect = self.image.get_rect()
                elif self.vx < 0:
                    self.image = self.frames["left"][self.current_frame_walk]
                    self.rect = self.image.get_rect()
                elif self.vy > 0:
                    self.image = self.frames["down"][self.current_frame_walk]
                    self.rect = self.image.get_rect()
                elif self.vy < 0:
                    self.image = self.frames["up"][self.current_frame_walk]
                    self.rect = self.image.get_rect()

        elif self.attacking:
            if now - self.last_update_atk > 100:
                self.last_update_atk = now
                self.current_frame_atk = (self.current_frame_atk + 1) % 5
                if self.current_frame_atk == 0:
                    sound = self.game.sound_sword
                    sound.set_volume(SFX_VOLUME)
                    sound.play()
                if self.current_frame_atk == 4:
                    self.attacking = False
                if self.last_direction == "right" and self.attacking is True:
                    self.image = self.frames["attack_right"][self.current_frame_atk]
                    left = self.rect.left
                    self.rect = self.image.get_rect()
                    self.rect.left = left

                if self.last_direction == "down" and self.attacking is True:
                    self.image = self.frames["attack_down"][self.current_frame_atk]
                    left = self.rect.left
                    self.rect = self.image.get_rect()
                    self.rect.left = left

                if self.last_direction == "up" and self.attacking is True:
                    self.image = self.frames["attack_up"][self.current_frame_atk]
                    left = self.rect.left
                    self.rect = self.image.get_rect()
                    self.rect.left = left

                if self.last_direction == "left" and self.attacking is True:
                    self.right = self.rect.right
                    self.image = self.frames["attack_left"][self.current_frame_atk]
                    self.rect = self.image.get_rect()
                    self.rect.right = self.right

                else:
                    self.walking = False

        if not self.walking and not self.attacking:
            self.image = self.frames[self.last_direction][0]
            self.current_frame_walk = 0
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
                if self.collide(new_rect, "wall"):
                    return
                elif self.collide(new_rect, "left"):
                    self.game.mapX -= 1
                    self.game.load_map(self.game.map_folder, LOCATION[self.game.mapX][self.game.mapY])
                    self.place(self.game.map.width, self.y)
                    return
                self.vx = -PLAYER_SPEED
                self.game.cooldown = self.game.delay
                encounter.page_count = 0
                self.npc_key = False
                encounter.drawing = False

            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.last_direction = "right"
                self.attacking = False
                new_rect = self.hit_rect.move(TILE_SIZE, 0)
                if self.collide(new_rect, "wall"):
                    return
                elif self.collide(new_rect, "right"):
                    self.game.mapX += 1
                    self.game.load_map(self.game.map_folder, LOCATION[self.game.mapX][self.game.mapY])
                    self.place(0 - TILE_SIZE, self.y)
                    return
                self.vx = PLAYER_SPEED
                self.game.cooldown = self.game.delay
                encounter.page_count = 0
                self.npc_key = False
                encounter.drawing = False

            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.last_direction = "up"
                self.attacking = False
                new_rect = self.hit_rect.move(0, -TILE_SIZE)
                if self.collide(new_rect, "wall"):
                    return
                elif self.collide(new_rect, "up"):
                    self.game.mapY += 1
                    self.game.load_map(self.game.map_folder, LOCATION[self.game.mapX][self.game.mapY])
                    print(self.game.mapY)
                    self.place(self.x, self.game.map.height)
                    self.map_transition = True
                    return
                self.vy = -PLAYER_SPEED
                self.game.cooldown = self.game.delay
                encounter.page_count = 0
                self.npc_key = False
                encounter.drawing = False

            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.last_direction = "down"
                self.attacking = False
                new_rect = self.hit_rect.move(0, TILE_SIZE)
                if self.collide(new_rect, "wall"):
                    return
                elif self.collide(new_rect, "down"):
                    self.game.mapY -= 1
                    self.game.load_map(self.game.map_folder, LOCATION[self.game.mapX][self.game.mapY])
                    self.place(self.x, 0 - TILE_SIZE)
                    return
                self.vy = PLAYER_SPEED
                self.game.cooldown = self.game.delay
                encounter.page_count = 0
                self.npc_key = False
                encounter.drawing = False

            elif keys[pygame.K_SPACE]:
                self.attacking = True

            elif keys[pygame.K_e]:
                if not encounter.drawing:
                    self.npc_key = encounter.talk(self)

                elif encounter.drawing and not self.e_flag:
                    encounter.page_count += 1
                    self.e_flag = True

            elif not keys[pygame.K_e]:
                self.e_flag = False

    def collide(self, rect, obstacle_name):
        for obstacle in self.game.obstacles:
            if rect.colliderect(obstacle.rect):
                if obstacle.name == obstacle_name:
                    return True
        return False

    def collect(self):
        for collect in self.game.collects:
            if self.hit_rect.colliderect(collect.rect):
                collect.kill()
                if collect.type == "coin":
                    self.coins += 1
                    self.xp += 10
                elif collect.type == "heart":
                    self.health += 4

    def hazard(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_hurt > 1000:
            self.last_update_hurt = now
            for hazard in self.game.hazards:
                if self.hit_rect.colliderect(hazard.rect):
                    self.health -= 1

    def level_up(self):
        if self.xp > 100:
            self.level += 1
            self.xp -= 100
            self.max_health += 4

    def update(self):
        self.get_keys()
        self.animate()
        self.collect()
        self.hazard()
        self.level_up()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        if self.attacking and self.last_direction == "left":
            self.rect.topleft = (self.x, self.y)
            self.rect.right = self.right
            self.hit_rect.right = self.right
        else:
            self.rect.topleft = (self.x, self.y)
            self.hit_rect.bottomleft = self.rect.bottomleft
        if self.health > self.max_health:
            self.health = self.max_health
        if self.health <= 0:
            self.game.playing = False


class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_map = (game.mapX, game.mapY)
        self.image = self.game.NPC_spritesheet.get_image(0, 0, 16, 32)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.topleft = (x,y)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name):
        self.groups = game.obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.rect = pygame.Rect(x, y, w, h)
        self.x, self.y = x, y
        self.rect.x = x
        self.rect.y = y


class Collect(pygame.sprite.Sprite):
    def __init__(self, game, x, y, cid, type):
        self.groups = game.all_sprites, game.collects
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_map = (game.mapX, game.mapY)
        self.current_frame = 0
        self.type = type
        self.image = game.collect_sprite[self.type][self.current_frame]
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.topleft = (x,y)
        self.last_update = 0
        self.id = cid

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 125:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 4
            self.image = self.game.collect_sprite[self.type][self.current_frame]

    def update(self):
        self.animate()


class Hazard(pygame.sprite.Sprite):
    def __init__(self, game, x, y, hid):
        self.groups = game.all_sprites, game.hazards
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_map = (game.mapX, game.mapY)
        self.current_frame = 0
        self.image = game.hazard_sprite[self.current_frame]
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.topleft = (x,y)
        self.last_update = 0
        self.id = hid

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 7
            self.image = self.game.hazard_sprite[self.current_frame]

    def update(self):
        self.animate()


class Button(pygame.sprite.Sprite):
    def __init__(self, game, up, down, name):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = up
        self.up = up
        self.down = down
        self.name = name
        self.rect = self.image.get_rect()
        self.pos = (0, 0)

    def is_pressed(self):
        position = pygame.mouse.get_pos()
        if self.rect.collidepoint(position) and self.game.click_down:
            self.image = self.down
        elif not self.game.click_down:
            self.image = self.up

    def end_pause(self):
        position = pygame.mouse.get_pos()
        if self.rect.collidepoint(position):
            self.game.playing = True

    def update(self):
        self.rect.topleft = self.pos
        self.is_pressed()
