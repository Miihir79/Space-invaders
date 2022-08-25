import pygame
import random
import math

pygame.init()

pygame.display.set_caption("Space Invadors")
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('backgroundimg.png')

# to set icon
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# to add player
imgplayer = pygame.image.load('player.png')
playerx = 370
playery = 480
changex = 2

# to add aliens
imgalien = []
alienx = []
alieny = []
achangex = []
achangey = []

number = 6
for i in range(number):
    imgalien.append(pygame.image.load('alien.png'))
    alienx.append(random.randint(0, 736))
    alieny.append(random.randint(50, 150))
    achangex.append(1)
    achangey.append(2)

# bullet

imgBullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bChangeX = 0
bChangeY = 4
bState = "ready"

# score

score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

fontX = 10
fontY = 10


def show_score(x, y):
    scoreVal = font.render("Score:" + str(score), True, (255, 255, 255))
    screen.blit(scoreVal, (x, y))


def player(x, y):
    screen.blit(imgplayer, (x, y))


def alien(x, y, z):
    screen.blit(imgalien[z], (x, y))


def b_fire(x, y):
    global bState
    bState = "fire"
    screen.blit(imgBullet, (x + 16, y + 10))


def collision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX - bulletX, 2) + math.pow(alienY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


over = pygame.font.Font("freesansbold.ttf", 40)


def gameOver():
    overt = over.render("GAME OVER \n score:" + str(score), True, (255, 255, 255))
    screen.blit(overt, (200, 250))


running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                changex = -2
            if event.key == pygame.K_RIGHT:
                changex = 2
            if event.key == pygame.K_SPACE:
                if bState is "ready":
                    bulletX = playerx
                    b_fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                changex = 0

    if playerx <= 0:
        playerx = 0
    if playerx >= 736:
        playerx = 736
    for i in range(number):
        if alieny[i] > 440:
            for j in range(number):
                alieny[j] = 200
            gameOver()
            break
        if score < 10:
            if alienx[i] <= 0:
                achangex[i] = 1
                alieny[i] += achangey[i]
            elif alienx[i] >= 736:
                achangex[i] = -1
                alieny[i] += achangey[i]
        else:
            if alienx[i] <= 0:
                achangex[i] = 2
                alieny[i] += achangey[i]
            elif alienx[i] >= 736:
                achangex[i] = -2
                alieny[i] += achangey[i]

        # collision
        colision = collision(alienx[i], alieny[i], bulletX, bulletY)
        if colision:
            bulletY = 480
            bState = "ready"
            score += 1
            print(score)
            alienx[i] = random.randint(0, 736)
            alieny[i] = random.randint(50, 150)

        if score > 10:
            achangex[i] = 2
            alienx[i] += achangex[i]
            alien(alienx[i], alieny[i], i)

        else:
            alienx[i] += achangex[i]
            alien(alienx[i], alieny[i], i)
    if bulletY <= 0:
        bulletY = 480
        bState = "ready"

    if bState is "fire":
        b_fire(bulletX, bulletY)
        bulletY -= bChangeY

    playerx += changex
    player(playerx, playery)

    show_score(fontX, fontY)
    pygame.display.update()
