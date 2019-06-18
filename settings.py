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
        "start2.tmx", "start.tmx"
    ],
    [
        "start3.tmx"
    ],
    [
        "start4.tmx"
    ]
]

# SOUNDS
SFX_VOLUME = 0.05
SOUND_WALKING = ["footstep1.wav", "footstep2.wav"]
SOUND_SWORD = "sword1.wav"
