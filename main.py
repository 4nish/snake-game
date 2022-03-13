"""
First make a directory named "sounds" in same folder as this python file.
Then download "hit.mp3" & "point.mp3" in that directory.
Else code will not work.
"""

import pygame
from pygame.locals import *
import sys
import random
import time

# Global Variables
pygame.init()

# Screen
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# FPS
FPS = 32
FPSCLOCK = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (48, 217, 76)

# Texts
SCORE = 0
FONT = pygame.font.SysFont(None, 40)

# Format
HEADER_TEXT = 14
HEADER_LINE = [0, SCREEN_WIDTH, 45]
GAME_BOX = [10, HEADER_LINE[2] + 15, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10]

# Snake
SNAKE_SIZE = 25
HEAD_X = 100
HEAD_Y = 100
SNAKE_HEAD = []
SNAKE_DIRECTION = -1

# Snake Velocity
VEL_X = 0
VEL_Y = 0

# Snake Tail
SNAKE_LENGTH = 0
SNAKE_POSITIONS = []

# Ball
BALL_POSITION = []
BALL_MADE = False

# Booleans
GAME_OVER = True
PLAYED = False


class Game:
    def __init__(self, title="Window", bg=WHITE):
        pygame.display.set_caption(title)
        SCREEN.fill(bg)
        self.__setInitials()

    # Setting Global Variables
    @staticmethod
    def __setInitials():
        # Snake
        global HEAD_X, HEAD_Y, SNAKE_HEAD, SNAKE_DIRECTION
        HEAD_X, HEAD_Y, SNAKE_HEAD, SNAKE_DIRECTION = 100, 100, [], -1

        # Snake Velocity
        global VEL_X, VEL_Y
        VEL_X, VEL_Y = 0, 0

        # Snake Tail
        global SNAKE_LENGTH, SNAKE_POSITIONS
        SNAKE_LENGTH, SNAKE_POSITIONS = 0, []

        # Ball
        global BALL_POSITION, BALL_MADE
        BALL_POSITION, BALL_MADE = [], False

        # Booleans
        global GAME_OVER
        GAME_OVER = True

    # Drawing Line
    @staticmethod
    def __drawLine(color=BLACK, x1=10, y1=10, x2=20, y2=20, width=5):
        pygame.draw.line(SCREEN, color, (x1, y1), (x2, y2), width)

    # Typing Text
    @staticmethod
    def __typeText(text, color=BLACK, x=0, y=0):
        SCREEN.blit(FONT.render(text, True, color), [x, y])

    # Drawing Rectangle
    @staticmethod
    def __drawRect(color=BLACK, x1=10, y1=10, x2=20, y2=20, width=0):
        pygame.draw.rect(SCREEN, color, [x1, y1, x2 - x1, y2 - y1], width)

    # Setting Snake head Position
    @staticmethod
    def __setSnakeHead():
        global SNAKE_HEAD
        SNAKE_HEAD = [HEAD_X, HEAD_Y, SNAKE_SIZE]

    # Making Header & Game-Box
    def __setFormat(self):
        self.__typeText(text=f"Score : {SCORE}", color=RED, x=HEADER_TEXT, y=HEADER_TEXT)
        self.__drawLine(color=RED, x1=HEADER_LINE[0], x2=HEADER_LINE[1], y1=HEADER_LINE[2], y2=HEADER_LINE[2])
        self.__drawRect(x1=GAME_BOX[0], y1=GAME_BOX[1], x2=GAME_BOX[2], y2=GAME_BOX[3])

    # Drawing Snake Head
    def __snakeHead(self):
        self.__setSnakeHead()
        self.__drawRect(color=GREEN, x1=SNAKE_HEAD[0], y1=SNAKE_HEAD[1], x2=SNAKE_HEAD[0] + SNAKE_HEAD[2],
                        y2=SNAKE_HEAD[1] + SNAKE_HEAD[2])

    # Changing Velocity
    @staticmethod
    def __changeVel():
        global VEL_X, VEL_Y
        if SNAKE_DIRECTION == 0:
            VEL_X = 5
            VEL_Y = 0
        elif SNAKE_DIRECTION == 270:
            VEL_X = -5
            VEL_Y = 0
        elif SNAKE_DIRECTION == 90:
            VEL_X = 0
            VEL_Y = 5
        elif SNAKE_DIRECTION == 360:
            VEL_X = 0
            VEL_Y = -5

    # Changing Direction
    def __changeDir(self, newDir):
        global SNAKE_DIRECTION
        SNAKE_DIRECTION = newDir
        self.__changeVel()

    # Moving Snake
    def __moveSnake(self):
        global HEAD_X, HEAD_Y
        HEAD_X += VEL_X
        HEAD_Y += VEL_Y
        self.__magicWalls()

    # Transferring snake threw walls
    @staticmethod
    def __magicWalls():
        global HEAD_X, HEAD_Y
        offset = SNAKE_SIZE
        if HEAD_X >= GAME_BOX[2] - offset and SNAKE_DIRECTION == 0:
            HEAD_X = GAME_BOX[0]
        elif HEAD_X <= GAME_BOX[0] and SNAKE_DIRECTION == 270:
            HEAD_X = GAME_BOX[2] - offset
        if HEAD_Y <= GAME_BOX[1] and SNAKE_DIRECTION == 360:
            HEAD_Y = GAME_BOX[3] - offset
        elif HEAD_Y >= GAME_BOX[3] - offset and SNAKE_DIRECTION == 90:
            HEAD_Y = GAME_BOX[1]

    # Adding Tail
    def __addTail(self):
        global SNAKE_POSITIONS, GAME_OVER
        SNAKE_POSITIONS.append([HEAD_X, HEAD_Y])

        if len(SNAKE_POSITIONS) > SNAKE_LENGTH:
            del SNAKE_POSITIONS[0]

        for item in SNAKE_POSITIONS:
            self.__drawRect(color=GREEN, x1=item[0], y1=item[1], x2=item[0] + SNAKE_SIZE,
                            y2=item[1] + SNAKE_SIZE)

        if [HEAD_X, HEAD_Y] in SNAKE_POSITIONS[:-1]:
            GAME_OVER = True
            self.__playSound("hit")
            time.sleep(1)

    # Inserting Ball
    def __insertBall(self):
        global BALL_POSITION, BALL_MADE
        ballX, ballY = 1, 1
        if not BALL_MADE:
            while ballX % 5 != 0 and ballY % 5 != 0:
                ballX = (random.randint(GAME_BOX[0], int(GAME_BOX[2] - SNAKE_SIZE)))
                ballY = (random.randint(GAME_BOX[1], int(GAME_BOX[3] - SNAKE_SIZE)))
            BALL_POSITION = [ballX, ballY]
        self.__drawRect(color=RED, x1=BALL_POSITION[0], y1=BALL_POSITION[1], x2=BALL_POSITION[0] + SNAKE_SIZE,
                        y2=BALL_POSITION[1] + SNAKE_SIZE)
        BALL_MADE = True

    # Checking for ball to be eaten
    def __checkEaten(self):
        global BALL_MADE, BALL_POSITION, SCORE, SNAKE_LENGTH
        if abs(HEAD_X - BALL_POSITION[0]) < 20 and abs(HEAD_Y - BALL_POSITION[1]) < 20:
            BALL_MADE = False
            BALL_POSITION = [SCREEN_WIDTH + 100, SCREEN_HEIGHT + 100]
            SCORE += 1
            SNAKE_LENGTH += 5
            self.__playSound("point")

    # Game Window
    def __gameRun(self):
        self.__setFormat()
        self.__snakeHead()
        self.__insertBall()
        self.__checkEaten()
        self.__moveSnake()
        self.__addTail()

    # Game Over Window
    def __gameOver(self):
        SCREEN.fill(GREEN)
        SCREEN.blit(pygame.image.load("Gallery/logo.png"), (100, 100))
        if PLAYED:
            self.__typeText(text=f"Score : {SCORE}", x=300, y=200)
        self.__typeText(text="1. SPACE to start", x=100, y=350)
        self.__typeText(text="2. Arrow Keys to play", x=100, y=400)
        self.__typeText(text="3. ENTER to Game Over", x=100, y=450)
        self.__typeText(text="4. Esc to exit", x=100, y=500)
        self.__setInitials()

    # Handling Events
    def __handleEvents(self):
        global GAME_OVER, PLAYED, SCORE
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP and (SNAKE_DIRECTION != 90 and SNAKE_DIRECTION != 360):
                    self.__changeDir(360)
                elif event.key == K_DOWN and (SNAKE_DIRECTION != 90 and SNAKE_DIRECTION != 360):
                    self.__changeDir(90)
                elif event.key == K_LEFT and (SNAKE_DIRECTION != 0 and SNAKE_DIRECTION != 270):
                    self.__changeDir(270)
                elif event.key == K_RIGHT and (SNAKE_DIRECTION != 0 and SNAKE_DIRECTION != 270):
                    self.__changeDir(0)
                elif GAME_OVER and event.key == K_SPACE:
                    GAME_OVER = False
                    PLAYED = True
                    SCORE = 0
                elif not GAME_OVER and event.key == K_RETURN:
                    GAME_OVER = True

    # Play Sounds
    @staticmethod
    def __playSound(sound):
        pygame.mixer.music.load(f"Sounds/{sound}.mp3")
        pygame.mixer.music.play()

    # Control Loop
    def start(self, bg=WHITE):
        while True:
            SCREEN.fill(bg)
            if GAME_OVER:
                self.__gameOver()
            else:
                self.__gameRun()
            self.__handleEvents()
            pygame.display.update()
            FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    player = Game(title="Snake Game by Saksham")
    player.start()
