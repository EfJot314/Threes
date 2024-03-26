import numpy as np
from enum import Enum
import pygame
from pygame import *


pygame.init()


#colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (220, 220, 220)
dark_gray = (180, 180, 180)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#images
images = {
    1: pygame.image.load("./images/threes1.png"),
    2: pygame.image.load("./images/threes2.png"),
    3: pygame.image.load("./images/threes3.png"),
    6: pygame.image.load("./images/threes6.png"),
    12: pygame.image.load("./images/threes12.png"),
    24: pygame.image.load("./images/threes24.png"),
    48: pygame.image.load("./images/threes48.png"),
    96: pygame.image.load("./images/threes96.png"),
    192: pygame.image.load("./images/threes192.png"),
    384: pygame.image.load("./images/threes384.png"),
    768: pygame.image.load("./images/threes768.png"),
    1536: pygame.image.load("./images/threes1536.png"),
    3072: pygame.image.load("./images/threes3072.png"),
    6144: pygame.image.load("./images/threes6144.png"),
}

#directions
class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    




#game class
class Game:
    def __init__(self, nX: int, nY: int, fps: int):
        self.nX = nX
        self.nY = nY
        self.width = 600
        self.height = 700
        self.board = np.zeros((self.nX, self.nY))
        self.tile_tab = [1, 2, 3, 3, 3, 3]
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.score = 0

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("monospace", 25)

        #first tiles
        for i in range(np.random.randint(2, 4+1)):
            self.new_tile()


    def new_tile(self, edge: Direction = None):
        if edge != None:
            edge = edge.value
        else:
            edge = np.random.randint(1, 4+1)
        while True:
            if edge % 2 == 0:
                x = int((edge-2)/2 * (self.nX-1))
                y = np.random.randint(0, self.nY)
                if self.board[x][y] == 0:
                    self.board[x][y] = 3
                    break
            else:
                x = np.random.randint(0, self.nX)
                y = int((3-edge)/2 * (self.nY-1))
                if self.board[x][y] == 0:
                    self.board[x][y] = np.random.choice(self.tile_tab)
                    break

    def draw(self):

        self.screen.fill(white)

        hx = self.width / 12
        hy = 1.555555555 * hx   #proportion for pretty scaled images c:
        # hy = self.height / 9



        dx = (self.width - self.nX*hx) / 2
        dy = (self.height - self.nY*hy) / 2

        margin = 20
        pygame.draw.rect(self.screen, gray, (dx-margin, dy-margin, self.nX*hx+2*margin, self.nY*hy+2*margin))
        for i in range(self.nX):
            for j in range(self.nY):
                xi = dx + i*hx
                yi =dy + j*hy
                pygame.draw.rect(self.screen, dark_gray, (xi, yi, 0.95*hx, 0.95*hy))
                if self.board[i][j] != 0:
                    img = pygame.transform.scale(images[self.board[i][j]], (0.95*hx, 0.95*hy))
                    self.screen.blit(img, (xi, yi))

    def check_game_over(self):
        board_copy = self.board.copy()
        for direction in Direction:
            if self.move(direction):
                self.board = board_copy
                return False
        self.board = board_copy
        return True

    def count_score(self):
        self.score = 0
        for i in range(self.nX):
            for j in range(self.nY):
                value = self.board[i][j]
                if value >= 3:
                    delta_score = 1
                    while value > 2:
                        delta_score *= 3
                        value //= 3
                    self.score += delta_score

    def move(self, direction: Direction):
        def move_indexes(x, y, dx, dy):
            #empty space
            if self.board[x+dx][y+dy] == 0:
                self.board[x+dx][y+dy] = self.board[x][y]
                self.board[x][y] = 0
                return True
            # 1 
            if self.board[x+dx][y+dy] == 1:
                if self.board[x][y] == 2:
                    self.board[x+dx][y+dy] = 3
                    self.board[x][y] = 0
                    return True
                return False
            # 2 
            if self.board[x+dx][y+dy] == 2:
                if self.board[x][y] == 1:
                    self.board[x+dx][y+dy] = 3
                    self.board[x][y] = 0
                    return True
                return False
            #same value
            if self.board[x+dx][y+dy] == self.board[x][y]:
                self.board[x+dx][y+dy] *= 2
                self.board[x][y] = 0
                return True
            return False
        
        toReturn = False
        if direction == Direction.UP:
            for x in range(self.nX):
                for y in range(1, self.nY):
                    toReturn = move_indexes(x, y, 0, -1) or toReturn
        elif direction == Direction.RIGHT:
            for x in range(self.nX-2, -1, -1):
                for y in range(self.nY):
                    toReturn = move_indexes(x, y, 1, 0) or toReturn
        elif direction == Direction.DOWN:
            for x in range(self.nX):
                for y in range(self.nY-2, -1, -1):
                    toReturn = move_indexes(x, y, 0, 1) or toReturn
        elif direction == Direction.LEFT:
            for x in range(1, self.nX):
                for y in range(self.nY):
                    toReturn = move_indexes(x, y, -1, 0) or toReturn
        return toReturn
        
    
    def run(self):
        #main loop
        self.running = True
        while self.running:

            #get screen size
            self.width, self.height = self.screen.get_size()

            #check if game is over
            if self.check_game_over():
                self.running = False
            
            #score
            self.count_score()

            #drawing
            self.draw()


            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    #moving
                    elif event.key == pygame.K_UP:
                        if self.move(Direction.UP):
                            self.new_tile(Direction.UP)
                        break
                    elif event.key == pygame.K_RIGHT:
                        if self.move(Direction.RIGHT):
                            self.new_tile(Direction.RIGHT)
                        break
                    elif event.key == pygame.K_DOWN:
                        if self.move(Direction.DOWN):
                            self.new_tile(Direction.DOWN)
                        break
                    elif event.key == pygame.K_LEFT:
                        if self.move(Direction.LEFT):
                            self.new_tile(Direction.LEFT)
                        break



            #time control and refreshing display
            self.clock.tick(self.fps)
            pygame.display.flip()

        
        #exit pygame
        pygame.quit()





#creating and running a game
game = Game(4, 4, 60)
game.run()

            











