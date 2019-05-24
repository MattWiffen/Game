import pygame

FPS = 120
TILE_SIZE = 32

WIDTH = TILE_SIZE * 20
HEIGHT = TILE_SIZE * 20

PLAYER_SPEED = TILE_SIZE*5
PLAYER_HIT_RECT = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)

# LOCATION[X][Y]
LOCATION = [
    [
        "new_world2.tmx"
    ],
    [
        "new_world.tmx"
    ]
]

# SOUNDS
SFX_VOLUME = 0.05
SOUND_WALKING = ["footstep1.wav", "footstep2.wav"]
