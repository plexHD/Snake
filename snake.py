import pygame
import os
import sys
import time
import random

window_width = 600
window_height = 600
snakecolor = (53, 92, 125) 
path = os.path.dirname(__file__)

highscorepath = path + "\\highscore.txt"

class Player():
    def __init__(self):
        self.score = 0
        self.highscore = 0

        self.position = [30, 30]
        self.color = snakecolor
        self.size = (30, 30)
        self.dir = 1

        self.oldposition = [0, 0]

        self.len = 0
        self.tiles = [Tile()]

        with open(highscorepath, "r") as file:
            self.highscore = int(file.read())

    def addtile(self, player):
        self.len += 1
        tile = Tile()
        tile.position[0] = player.position[0]
        tile.position[1] = player.position[1]
        self.tiles.append(tile)

class Tile():
    def __init__(self):
        self.position = [30, 30]
        self.color = snakecolor
        self.size = (28, 28)

        self.oldposition = [0, 0]

class Apple():
    def __init__(self):
        self.position = [10, 10]
        self.color = (246, 92, 125)
        self.size = (30, 30)

def main():
    pygame.init()

    screen = pygame.display.set_mode([window_width, window_height])
    pygame.display.set_caption("Snake by Moritz Ramge")
    font = pygame.font.Font(path + "\\Symtext.ttf", 20)
    player = Player()
    apple = Apple()
    tile = Tile()
    clock = pygame.time.Clock()
    movetimer = 0

    def checkInputs(pressed_keys):
        if pressed_keys[pygame.K_UP] and player.dir != 1:
            player.dir = 0
        elif pressed_keys[pygame.K_DOWN] and player.dir != 0:
            player.dir = 1
        elif pressed_keys[pygame.K_LEFT] and player.dir != 3:
            player.dir = 2
        elif pressed_keys[pygame.K_RIGHT] and player.dir != 2:
            player.dir = 3

    def spawnApple():
        range1 = window_width / 30
        range2 = window_height / 30

        check = False
        while check == False:
            check = True
            apple.position[0] = (random.randint(1, range1 -1) * 30)
            apple.position[1] = (random.randint(1, range2 -1) * 30)

            for tile in player.tiles:
                if tile.position == apple.position:
                    check = False

        player.score += 1
        player.addtile(player)

    spawnApple()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
        screen.fill((30, 30, 31))

        if player.position[0] in range(0, window_width) and player.position[1] in range(0, window_height):
            pressed_keys = pygame.key.get_pressed()
            checkInputs(pressed_keys)

        movetimer += clock.tick()
        if movetimer > 150:
            player.oldposition[0] = player.position[0]
            player.oldposition[1] = player.position[1]

            if len(player.tiles) > 0:
                for tile in player.tiles:
                    tile.oldposition[0] = tile.position[0]
                    tile.oldposition[1] = tile.position[1]

            if player.dir == 0:
                player.position[1] -= 30
            if player.dir == 1:
                player.position[1] += 30
            if player.dir == 2:
                player.position[0] -= 30
            if player.dir == 3:
                player.position[0] += 30
            movetimer = 0    
            i = 0
            while i < len(player.tiles):
                if i == 0:
                    player.tiles[i].position[0] = player.oldposition[0]
                    player.tiles[i].position[1] = player.oldposition[1]
                    i += 1
                    continue
                player.tiles[i].position[0] = player.tiles[i -1].oldposition[0]
                player.tiles[i].position[1] = player.tiles[i -1].oldposition[1]
                i += 1  

            # death check
            for tile in player.tiles:
                if player.position == tile.position:
                    if player.score > player.highscore:
                        with open(highscorepath, "w") as file:
                            file.write(str(player.score))
                    time.sleep(2)
                    main()

            if player.position[0] > window_width:
                player.position[0] = -30
            elif player.position[0] < 0:
                player.position[0] = window_width

            if player.position[1] > window_height:
                player.position[1] = -30
            elif player.position[1] < 0:
                player.position[1] = window_height
            

        for tile in player.tiles:
            pos = (tile.position[0] + 1, tile.position[1] + 1)
            pygame.draw.rect(screen, tile.color, pygame.Rect(pos, tile.size))

        
        pos = (player.position[0], player.position[1])
        pygame.draw.rect(screen, player.color, pygame.Rect(pos, player.size))
        
        pos = (apple.position[0], apple.position[1])
        pygame.draw.rect(screen, apple.color, pygame.Rect(pos, apple.size))

        if player.position == apple.position:
            spawnApple()

        # render score
        scoretext = font.render("SCORE " + str(player.score), True, (255, 255, 255))
        scorerect = scoretext.get_rect()

        highscoretext = font.render("HIGHSCORE " + str(player.highscore), True, (255, 255, 255))
        highscorerect = scoretext.get_rect()

        screen.blit(scoretext, (10, 0))
        screen.blit(highscoretext, (10, 30))

        pygame.display.update()

main()