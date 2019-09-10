from settings import *

TEXT = {
    "npc1": [
        "Hello there Adventurer!",
        "My name is Marcus, what a lovely day it is today. I have a task for you!",
        "Someone has hidden many precious coins nearby, why don't you go and collect them?"
    ]
}

LOADED_TEXT = {}

drawing = False
page_count = -1


def load_text(x_offset=0, y_offset=0):
    for key in TEXT:
        page = TEXT[key]
        LOADED_TEXT[key] = []
        for sentences in page:
            count = 0
            sentences = sentences.split()
            temp = []
            temp2 = []
            x, y = (WIDTH - 480) / 2, HEIGHT - 148
            x += x_offset
            y += y_offset
            for word in sentences:
                if x + len(word)*16 > ((WIDTH + 480) / 2) - x_offset:
                    x = (WIDTH - 480) / 2 + x_offset
                    y += 30
                    if not temp == []:
                        temp2.append(temp)
                    if count >= 2:
                        LOADED_TEXT[key].append(temp2)
                        temp2 = []
                        count = 0
                    temp = []
                    count += 1
                x += (len(word)*16) + 20
                temp.append(word)
            temp2.append(temp)
            LOADED_TEXT[key].append(temp2)


def draw_text(game, npc, x_offset=0, y_offset=0):
    load = LOADED_TEXT[npc][page_count]
    x, y = (WIDTH - 480) / 2, HEIGHT - 148
    game.screen.blit(game.font_elements["background"], (x, y))
    x += x_offset
    y += y_offset
    for line in load:
        for word in line:
            for letter in word:
                game.screen.blit(game.font_elements["text"][letter], (x, y))
                x += 16
            x += 20
        x = (WIDTH - 480) / 2 + x_offset
        y += 30


def talk(player):
    global drawing
    if player.last_direction == "up":
        move = (0, -TILE_SIZE)
    elif player.last_direction == "down":
        move = (0, TILE_SIZE)
    elif player.last_direction == "left":
        move = (-TILE_SIZE, 0)
    elif player.last_direction == "right":
        move = (TILE_SIZE, 0)
    else:
        return
    new_rect = player.hit_rect.move(move)

    for key in TEXT:
        if player.collide(new_rect, key):
            drawing = True
            return key

