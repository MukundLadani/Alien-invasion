import random
import math
import pygame
from pygame import mixer

pygame.init()

# screen
screen = pygame.display.set_mode((1000, 667))
background = pygame.image.load("space-galaxy-background.png")
pygame.display.set_caption("Alien Invasion")
logo = pygame.image.load("ufo (1).png")
pygame.display.set_icon(logo)

# background music
mixer.music.load("background.mp3")
mixer.music.play(-1)

# player
playerimg = pygame.image.load("space-invaders.png")
playerX = 500
playerY = 580
playerX_change = 0

# alien
alienimg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num = 9
for i in range(num):
    if i % 3 == 0:
        alienimg.append(pygame.image.load("alien.png"))
    elif i % 2 == 0:
        alienimg.append(pygame.image.load("alien3.png"))
    else:
        alienimg.append(pygame.image.load("alien2.png"))
    alienX.append(random.randint(0, 936))
    alienY.append(random.randint(50, 150))
    alienX_change.append(1)
    alienY_change.append(50)

# bullet
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 547
bulletY_change = 2
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('High Jersey.ttf', 45)
textX = 20
textY = 10

# game over
over = pygame.font.Font("freesansbold.ttf", 64)


def showing_score(x, y):
    score = font.render("Score: " + str(score_value), True, (170, 150, 255))
    screen.blit(score, (x, y))


def game_over(x):
    if x == True:
        over_game = over.render("GAME OVER", True, (255, 240, 230))
        screen.blit(over_game, (270, 290))
    else:
        return 0


def after_game():
    after = font.render("Press Capslock to continue & Esc to end the game", True, (150, 200, 255))
    screen.blit(after, (150, 340))


def player(x, y):
    screen.blit(playerimg, (x, y))


def alien1(x, y, i):
    screen.blit(alienimg[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def collison(alienx, alieny, bulletx, bullety):
    dis = math.sqrt(math.pow((alienx - bulletx), 2) + math.pow((alieny - bullety), 2))
    if dis < 30:
        return True
    else:
        return False


# Game loop
run = True
while run:

    screen.fill((100, 40, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            elif event.key == pygame.K_RIGHT:
                playerX_change = 2
            elif event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound("bullet.mp3")
                bullet_sound.play()
                # initial x coordinate of player
                bulletX = playerX
                fire(bulletX, bulletY)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    # alien movement
    for i in range(num):
        # terminating state
        if alienY[i] > 460:
            for j in range(num):
                alienY[j] = 2000
            game_over(True)
            after_game()

            #after one game
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_CAPSLOCK:
                        game_over(False)
                        score_value = 0
                        alienY = []
                        for j in range(num):
                            if j % 3 == 0:
                                alienimg.append(pygame.image.load("alien.png"))
                            elif j % 2 == 0:
                                alienimg.append(pygame.image.load("alien3.png"))
                            else:
                                alienimg.append(pygame.image.load("alien2.png"))
                            alienX.append(random.randint(0, 936))
                            alienY.append(random.randint(50, 150))
                            alienX_change.append(1)
                            alienY_change.append(50)
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                        break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 0.5
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 936:
            alienX_change[i] = -0.5
            alienY[i] += alienY_change[i]

        # collision
        iscollision = collison(alienX[i], alienY[i], bulletX, bulletY)
        if iscollision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 936)
            alienY[i] = random.randint(50, 150)
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()

        alien1(alienX[i], alienY[i], i)

    # bullet
    if bulletY <= 0:
        bulletY = 547
        bullet_state = "ready"
    if bullet_state == "Fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # calling elements
    player(playerX, playerY)
    showing_score(textX, textY)
    pygame.display.update()
