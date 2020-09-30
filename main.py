import pygame
import random
import math
import sys
from pygame import mixer

# Global Variables for the game
FPS = 32
SCREENWIDTH = 800
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  # create the SCREEN
BACKGROUND = pygame.image.load('back123.jpg')  # create BACKGROUND

# create PLAYER
PLAYERImg = pygame.image.load('player.png')
PLAYERX = 370
PLAYERY = 480
PLAYERX_change = 0

# create ENEMY
ENEMYImg = []
ENEMYX = []
ENEMYY = []
ENEMYX_change = []
ENEMYY_change = []
no_enemies = 6

# create BULLET
BULLETImg = pygame.image.load('BULLET.png')
BULLETX = 0
BULLETY = 480
BULLETX_change = 0
BULLETY_change = 30
BULLET_state = 'ready'

# score_value
score_value = 0

# this file is used to store high score value
with open("highscore.txt", 'r') as f:
    hiscore = f.read()

# to show welcome Screen to user
running = True


def welcomeScreen():
    """
    Shows welcome image on the screen
    """

    # to show message on welcome page
    message = pygame.font.Font('freesansbold.ttf', 25)
    startmsg = message.render("Press Space Bar To Play", True, (255, 0, 0))

    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return

            else:
                SCREEN.blit(BACKGROUND, (0, 0))
                dropShadowText(SCREEN, "SPACE INVADERS", 100, 100, 250)
                SCREEN.blit(startmsg, (250, 330))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    global PLAYERX, PLAYERX_change, ENEMYX, ENEMYY, ENEMYX_change
    global BULLETY, BULLET_state, score_value, running, hiscore
    running = False

    # player movement
    PLAYERX += PLAYERX_change
    # set boundries for player
    if PLAYERX < 0:
        PLAYERX = 0
    elif PLAYERX > 736:
        PLAYERX = 736

    for i in range(no_enemies):
        # Game over
        if ENEMYY[i] > 470:
            # write high score value in highscore.txt file
            with open("highscore.txt", 'w') as f:
                f.write(str(hiscore))
            for j in range(no_enemies):
                ENEMYY[j] = 1000
            dropShadowText(SCREEN, "GAME OVER", 100, 200, 250)
            SCREEN.blit(overgame, (270, 330))

        else:
            # enemy movement
            ENEMYX[i] += ENEMYX_change[i]
            # set boundries for enemy
            if ENEMYX[i] < 0:
                ENEMYX_change[i] = 8
                ENEMYY[i] += ENEMYY_change[i]
            elif ENEMYX[i] > 746:
                ENEMYX_change[i] = -8
                ENEMYY[i] += ENEMYY_change[i]

            # collision of bullet and enemy
            collision = isCollision(i)
            if collision:
                explosionSound = mixer.Sound('explosion.wav')
                explosionSound.play()
                BULLETY = 480
                BULLET_state = "ready"
                ENEMYX[i] = random.randint(0, 746)
                ENEMYY[i] = random.randint(50, 150)
                score_value += 5
                if score_value > int(hiscore):
                    hiscore = score_value
            SCREEN.blit(ENEMYImg[i], (ENEMYX[i], ENEMYY[i]))

    SCREEN.blit(PLAYERImg, (PLAYERX, PLAYERY))

    # bullet movement
    if BULLETY < 0:
        BULLET_state = "ready"
        BULLETY = 480

    if BULLET_state == "fire":
        BULLETY -= BULLETY_change
        bullet(BULLETX, BULLETY)

    # Score and Highscore
    font = pygame.font.Font('freesansbold.ttf', 32)
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    SCREEN.blit(score, (10, 10))
    highscore = font.render("Record :" + str(hiscore), True, (255, 255, 255))
    SCREEN.blit(highscore, (600, 10))

    pygame.display.update()


def bullet(x, y):
    global BULLET_state
    BULLET_state = "fire"
    SCREEN.blit(BULLETImg, (x + 16, y + 10))


def isCollision(i):
    distance = math.sqrt((math.pow(ENEMYX[i] - BULLETX, 2)) + (math.pow(ENEMYY[i] - BULLETY, 2)))
    if distance < 27:
        return True
    else:
        return False


def dropShadowText(SCREEN, text, size, x, y, colour=(255, 0, 0), drop_colour=(11, 4, 82), font=None):
    # how much 'shadow distance' is best?
    dropshadow_offset = 1 + (size // 15)
    text_font = pygame.font.Font(font, size)
    # make the drop-shadow
    text_bitmap = text_font.render(text, True, drop_colour)
    SCREEN.blit(text_bitmap, (x + dropshadow_offset, y + dropshadow_offset))
    # make the overlay text
    text_bitmap = text_font.render(text, True, colour)
    SCREEN.blit(text_bitmap, (x, y))


if __name__ == "__main__":
    # Initialize all pygame's modules
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # Game Sound
    mixer.music.load('background.wav')
    mixer.music.play(-1)

    # create title and icon
    pygame.display.set_caption('Space Invaders')
    ICON = pygame.image.load('ufo.png')
    pygame.display.set_icon(ICON)

    # to create multiple enemies
    for i in range(no_enemies):
        ENEMYImg.append(pygame.image.load('ENEMY.png'))
        ENEMYX.append(random.randint(0, 746))
        ENEMYY.append(random.randint(50, 150))
        ENEMYX_change.append(5)
        ENEMYY_change.append(40)

    # to show message on gameover page
    message = pygame.font.Font('freesansbold.ttf', 25)
    overgame = message.render("Press Enter To Continue", True, (255, 0, 0))

    # Game loop
    while True:
        # BACKGROUND
        SCREEN.blit(BACKGROUND, (0, 0))

        # for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    PLAYERX_change = -7
                if event.key == pygame.K_RIGHT:
                    PLAYERX_change = 7
                if event.key == pygame.K_SPACE:
                    BULLETX = PLAYERX
                    bullet(BULLETX, BULLETY)
                    BULLETsound = mixer.Sound('shoot.wav')
                    BULLETsound.play()
                if event.key == pygame.K_RETURN:
                    running = True
                    score_value = 0
                    ENEMYY.clear()
                    for i in range(no_enemies):
                        ENEMYY.append(random.randint(50, 150))

            if event.type == pygame.KEYUP:
                PLAYERX_change = 0

        if running == True:
            welcomeScreen()  # show welcome screen to the end user until he pressed the button
        mainGame()  # this is the main game function
